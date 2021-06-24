import socket
import threading
import typing as tp

import concurrent
from concurrent.futures import ThreadPoolExecutor
from .handlers import Address, BaseRequestHandler


class TCPServer:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5000,
        backlog_size: int = 1,
        max_workers: int = 1,
        timeout: tp.Optional[float] = 3,
        request_handler_cls: tp.Type[BaseRequestHandler] = BaseRequestHandler,
    ) -> None:
        self.host = host
        self.port = port
        self.server_address = (host, port)
        self.backlog_size = backlog_size
        self.request_handler_cls = request_handler_cls
        self.max_workers = max_workers
        self.timeout = timeout
        self._threads: tp.List[threading.Thread] = []

    def serve_forever(self) -> None:
        address = (self.host, self.port)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        server_socket.bind(address)
        server_socket.listen(self.backlog_size)

        print(f"Server working on {self.host}:{self.port}")

        with ThreadPoolExecutor(max_workers=self.max_workers) as exec:
            futures = []

            try:
                while True:
                    client_socket, address = server_socket.accept()
                    client_socket.settimeout(self.timeout)
                    futures.append(exec.submit(self.handle_accept, client_socket))
            except KeyboardInterrupt:
                for future in futures:
                    future.cancel()
                concurrent.futures.wait(futures, timeout=self.timeout)
                print("\nGot SIGTERM, terminated...")

        server_socket.close()

    def handle_accept(self, server_socket: socket.socket) -> None:
        self.request_handler_cls(server_socket, self.server_address, self).handle()


class HTTPServer(TCPServer):
    pass
