import dataclasses
import typing as tp
import io
import sys

from httpserver import HTTPRequest


@dataclasses.dataclass
class WSGIRequest(HTTPRequest):
    def to_environ(self) -> tp.Dict[str, tp.Any]:
        environ = {}

        environ["REQUEST_METHOD"] = self.method
        environ["SCRIPT_NAME"] = ""
        environ["PATH_INFO"] = self.url.split(b"?")[0] if b"?" in self.url else self.url
        environ["QUERY_STRING"] = self.url.split(b"?")[1] if b"?" in self.url else b""
        environ["CONTENT_TYPE"] = self.headers.get(b"Content-Type", b"")
        environ["CONTENT_LENGTH"] = self.headers[b"Content-Length"]
        environ["SERVER_NAME"], environ["SERVER_PORT"] = ("127.0.0.1", "8000")
        environ["SERVER_PROTOCOL"] = "HTTP/1.1"
        environ["HTTP_Variables"] = ""
        environ["wsgi.version"] = (1, 0)
        environ["wsgi.url_scheme"] = "http"
        environ["wsgi.input"] = io.BytesIO(self.body)
        environ["wsgi.errors"] = sys.stderr
        environ["wsgi.multithread"] = True
        environ["wsgi.multiprocess"] = False
        environ["wsgi.run_once"] = False
        return environ
