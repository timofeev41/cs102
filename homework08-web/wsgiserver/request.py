import dataclasses
import typing as tp
import io

from httpserver import HTTPRequest

@dataclasses.dataclass
class WSGIRequest(HTTPRequest):
    def to_environ(self) -> tp.Dict[str, tp.Any]:
        environ = {}
        environ["REQUEST_METHOD"] = self.method
        environ["SCRIPT_NAME"] = None
        environ["PATH_INFO"] = self.url.split(b"?")[0] if b"?" in self.url else self.url
        environ["CONTENT_TYPE"] = self.headers[b"Content-Type"]
        environ["CONTENT_LENGTH"] = self.headers[b"Content-Length"]
        environ["SERVER_NAME"], environ["SERVER_PORT"] = ()
        environ["SERVER_PROTOCOL"] = "HTTP/1.1"
        environ["HTTP_Variables"] = None
        environ["wsgi.version"] = (1, 0)
        environ["wsgi.url_scheme"] = "http"
        environ["wsgi.input"] = io.BytesIO(self.body)
        environ["wsgi.errors"] = io.BytesIO(None)
        environ["wsgi.multithread"] = True
        environ["wsgi.multiprocess"] = False
        environ["wsgi.run_once"] = True
        return environ
