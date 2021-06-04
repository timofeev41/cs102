import dataclasses
import typing as tp

from httpserver import HTTPResponse
import datetime as dt


@dataclasses.dataclass
class WSGIResponse(HTTPResponse):
    status: int = 200

    def start_response(
        self, status: str, response_headers: tp.List[tp.Tuple[str, str]], exc_info=None
    ) -> None:
        self.headers_set = [status, response_headers + [('Date', str(dt.datetime.now()))]]
