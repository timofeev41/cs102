import http
import typing as tp
from collections import defaultdict
from urllib.parse import parse_qsl

from slowapi.middlewares import Middleware
from slowapi.request import Request
from slowapi.router import Route, Router


class SlowAPI:
    def __init__(self):
        self.router = Router()
        self.middlewares: tp.List[Middleware] = []

    def __call__(self, environ: tp.Dict[str, tp.Any], start_response: tp.Callable[[tp.Any], None]):
        headers: tp.DefaultDict[str, tp.Any] = defaultdict(lambda: str)
        query: tp.DefaultDict[str, tp.Any] = defaultdict(lambda: str)

        for variable in environ:
            if variable.startswith("HTTP_"):
                headers[variable[5:].lower()] = environ[variable]

        for key, value in parse_qsl(environ["QUERY_STRING"] or ""):
            query[key] = value

        request = Request(
            path=environ["PATH_INFO"].rstrip("/") or "/",
            method=environ["REQUEST_METHOD"],
            query=query,
            headers=headers,
            body=environ["wsgi.input"],
        )

        answer = self.router.resolve(request)
        status = http.HTTPStatus(answer.status)
        start_response(" ".join([str(status.value), status.phrase]), answer.headers)

        return [answer.body.encode() if answer.body is not None else b""]

    def route(self, path=None, method=None, **options):
        def decorator(func: tp.Callable):
            route = Route(path.rstrip("/"), method, func)
            self.router.add_route(route)
            return func

        return decorator

    def get(self, path=None, **options):
        return self.route(path, method="GET", **options)

    def post(self, path=None, **options):
        return self.route(path, method="POST", **options)

    def patch(self, path=None, **options):
        return self.route(path, method="PATCH", **options)

    def put(self, path=None, **options):
        return self.route(path, method="PUT", **options)

    def delete(self, path=None, **options):
        return self.route(path, method="DELETE", **options)

    def add_middleware(self, middleware) -> None:
        self.middlewares.append(middleware)
