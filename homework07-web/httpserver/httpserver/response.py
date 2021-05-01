import dataclasses
import http.client
import typing as tp


@dataclasses.dataclass
class HTTPResponse:
    status: int
    headers: tp.Dict[str, str] = dataclasses.field(default_factory=dict)
    body: bytes = b""

    def to_http1(self) -> bytes:
        method = "HTTP/1.1"
        text_status = http.client.responses[self.status]
        http1 = "" + (
            str(method)
            + " "
            + str(self.status)
            + " "
            + text_status
            + "\n\n"
            + "".join(
                [
                    f"{key.decode()}: {value.decode()}\n"
                    for key, value in zip(self.headers.keys(), self.headers.values())
                ]
            )
            + "\n\n"
            + self.body.decode()
        )
        return http1.encode()
