import dataclasses
import http
import typing as tp

from slowapi.request import Request
from slowapi.response import Response


@dataclasses.dataclass
class Route:
    path: str
    method: str
    func: tp.Callable

    def validate_data(self, request):
        if request.method != self.method:
            return False
        path_data = self.path.split("/")
        request_path_data = request.path.split("/")
        if len(path_data) == len(request_path_data):
            for i in range(len(request_path_data)):
                if not path_data[i].startswith("{") and path_data[i].endswith("}"):
                    if path_data[i] != request_path_data[i]:
                        return False
            return True
        return False

    def parse_args(self, request) -> tp.List[str]:
        path_spl = self.path.split("/")
        req_path_spl = request.path.split("/")
        args = []
        if len(path_spl) == len(req_path_spl):
            for i in range(len(req_path_spl)):
                if path_spl[i].startswith("{") and path_spl[i].endswith("}"):
                    args.append(req_path_spl[i])
        return args

    def handle_route(self, request):
        args = self.parse_args(request)
        return self.func(request, *args)


@dataclasses.dataclass
class Router:
    def __init__(self):
        self.routes: tp.List[Route] = []

    def resolve(self, request: Request) -> Response:
        for route in self.routes:
            if route.validate_data(request):
                return route.handle_route(request)
        status = http.HTTPStatus(404)
        response_body = "\n".join([str(status.value), status.phrase, status.description])
        return Response(status.value, {}, response_body)

    def add_route(self, route: Route):
        self.routes.append(route)
