import os
import copy
import json

from inspect import signature
from typing import Any, List, Callable, Optional, Type

from graphql import GraphQLError
from graphql_api.context import GraphQLContext
from werkzeug.wrappers import Request, Response
from werkzeug.test import Client
from json import JSONDecodeError

from graphql.type.schema import GraphQLSchema
from graphql.execution.execute import ExecutionContext

from graphql_http_server.helpers import (
    HttpQueryError,
    encode_execution_results,
    json_encode,
    load_json_body,
    run_http_query,
)
import jwt
from jwt import (
    PyJWKClient,
    InvalidTokenError,
    InvalidAudienceError,
    InvalidIssuerError,
    DecodeError,
)


def run_simple(
    schema,
    root_value: Any = None,
    middleware: List[Callable[[Callable, Any], Any]] = None,
    hostname: str = None,
    port: int = None,
    **kwargs,
):
    return GraphQLHTTPServer.from_api(
        schema=schema, root_value=root_value, middleware=middleware, **kwargs
    ).run(hostname=hostname, port=port, **kwargs)


graphiql_dir = os.path.join(os.path.dirname(__file__), "graphiql")


class GraphQLHTTPServer:
    @classmethod
    def from_api(cls, api, root_value: Any = None, **kwargs) -> "GraphQLHTTPServer":
        try:
            from graphql_api import GraphQLAPI
            from graphql_api.context import GraphQLContext

        except ImportError:
            raise ImportError("GraphQLAPI is not installed.")

        api: GraphQLAPI = api

        executor = api.executor(root_value=root_value)

        schema: GraphQLSchema = executor.schema
        meta = executor.meta
        root_value = executor.root_value

        middleware = executor.middleware
        context = GraphQLContext(schema=schema, meta=meta, executor=executor)

        return GraphQLHTTPServer(
            schema=schema,
            root_value=root_value,
            middleware=middleware,
            context_value=context,
            execution_context_class=executor.execution_context_class,
            **kwargs,
        )

    def __init__(
        self,
        schema: GraphQLSchema,
        root_value: Any = None,
        middleware: List[Callable[[Callable, Any], Any]] = None,
        context_value: Any = None,
        serve_graphiql: bool = True,
        graphiql_default_query: str = None,
        graphiql_default_variables: str = None,
        allow_cors: bool = False,
        health_path: str = None,
        execution_context_class: Optional[Type[ExecutionContext]] = None,
        auth_domain: str = None,
        auth_audience: str = None,
        auth_enabled: bool = False,
    ):
        if middleware is None:
            middleware = []

        self.schema = schema
        self.root_value = root_value
        self.middleware = middleware
        self.context_value = context_value
        self.serve_graphiql = serve_graphiql
        self.graphiql_default_query = graphiql_default_query
        self.graphiql_default_variables = graphiql_default_variables
        self.allow_cors = allow_cors
        self.health_path = health_path
        self.execution_context_class = execution_context_class
        self.auth_domain = auth_domain
        self.jwks_client = PyJWKClient(f"https://{auth_domain}/.well-known/jwks.json")
        self.auth_audience = auth_audience
        self.auth_enabled = auth_enabled

    @staticmethod
    def format_error(error: GraphQLError) -> {}:
        return error.formatted

    encode = staticmethod(json_encode)

    def dispatch(self, request: Request) -> Response:
        headers = {}

        try:
            request_method = request.method.lower()
            data = self.parse_body(request=request)

            if self.health_path and request.path == self.health_path:
                return Response("OK")

            if self.auth_enabled and request_method != "options":
                try:
                    token = request.headers["Authorization"]
                    token = token[len("Bearer ") :]

                    header = jwt.get_unverified_header(token)
                    signing_key = self.jwks_client.get_signing_key(header["kid"])

                    jwt.decode(
                        token,
                        audience=self.auth_audience,
                        issuer=f"https://{self.auth_domain}/",
                        key=signing_key.key,
                        algorithms=["RS256"],
                    )
                except (
                    InvalidTokenError,
                    InvalidAudienceError,
                    InvalidIssuerError,
                    JSONDecodeError,
                    DecodeError,
                    KeyError,
                ) as e:
                    return self.error_response(e, status=401)

            # GraphiQL
            if request_method == "get" and self.should_serve_graphiql(request=request):
                graphiql_path = os.path.join(graphiql_dir, "index.html")
                if self.graphiql_default_query:
                    default_query = json.dumps(self.graphiql_default_query)
                else:
                    default_query = '""'

                if self.graphiql_default_variables:
                    default_variables = json.dumps(self.graphiql_default_variables)
                else:
                    default_variables = '""'

                html = open(graphiql_path, "r").read()
                html = html.replace("DEFAULT_QUERY", default_query)
                html = html.replace("DEFAULT_VARIABLES", default_variables)

                return Response(html, content_type="text/html")

            if self.allow_cors:
                allow_headers = ["Content-Type"]
                if self.auth_enabled:
                    allow_headers.append("Authorization")

                headers = {
                    "Access-Control-Allow-Credentials": "true",
                    "Access-Control-Allow-Headers": ", ".join(allow_headers),
                    "Access-Control-Allow-Methods": "GET, POST",
                }
                origin = request.headers.get("ORIGIN")
                if origin:
                    headers["Access-Control-Allow-Origin"] = origin

                if request_method == "options":
                    return Response(response="OK", headers=headers)

            context_value = copy.copy(self.context_value)

            if isinstance(context_value, GraphQLContext):
                context_value.meta["http_request"] = request

            execution_results, all_params = run_http_query(
                self.schema,
                request_method,
                data,
                query_data=request.args,
                root_value=self.root_value,
                middleware=self.middleware,
                context_value=context_value,
                execution_context_class=self.execution_context_class,
            )
            result, status_code = encode_execution_results(
                execution_results, is_batch=isinstance(data, list), encode=json_encode
            )

            return Response(
                result,
                status=status_code,
                content_type="application/json",
                headers=headers,
            )

        except HttpQueryError as e:
            return self.error_response(e, headers)

    @staticmethod
    def error_response(e, headers=None, status=None):
        if headers is None:
            headers = {}
        return Response(
            json_encode({"errors": [str(e)]}),
            status=status if status is not None else getattr(e, "status_code", 200),
            headers={**(getattr(e, "headers", {}) or {}), **headers},
            content_type="application/json",
        )

    # noinspection PyMethodMayBeStatic
    def parse_body(self, request):
        content_type = request.mimetype
        if content_type == "application/graphql":
            return {"query": request.data.decode("utf8")}

        elif content_type == "application/json":
            return load_json_body(request.data.decode("utf8"))

        elif content_type in (
            "application/x-www-form-urlencoded",
            "multipart/form-data",
        ):
            return request.form

        if request.data:
            try:
                body = request.data.decode("utf8")
                return load_json_body(body)
            except Exception:
                return {"query": request.data.decode("utf8")}

        return {}

    def should_serve_graphiql(self, request):
        if not self.serve_graphiql or "raw" in request.args:
            return False

        return self.request_wants_html(request=request)

    # noinspection PyMethodMayBeStatic
    def request_wants_html(self, request):
        best = request.accept_mimetypes.best_match(["application/json", "text/html"])

        if best == "text/html":
            accept_best = request.accept_mimetypes[best]
            accept_json = request.accept_mimetypes["application/json"]
            return accept_best > accept_json

        return False

    def app(self, main: Callable[[Request], Response] = None):
        @Request.application
        def app(request):
            if main is not None:
                return main(request)
            return self.dispatch(request=request)

        return app

    def client(self, main=None):
        return Client(self.app(main=main), Response)

    def run(
        self,
        main: Callable[[Request], Response] = None,
        hostname: str = None,
        port: int = None,
        **kwargs,
    ):
        if hostname is None:
            hostname = "localhost"

        if port is None:
            port = 5000

        from werkzeug.serving import run_simple

        valid_arg_names = list(signature(run_simple).parameters)

        kwargs = {k: v for k, v in kwargs.items() if k in valid_arg_names}

        run_simple(
            hostname=hostname, port=port, application=self.app(main=main), **kwargs
        )
