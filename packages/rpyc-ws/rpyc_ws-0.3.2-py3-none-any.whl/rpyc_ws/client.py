from functools import wraps

from rpyc.utils.classic import connect_stream
from websockets import ConnectionClosed
from websockets.sync.client import connect

from rpyc_ws.stream import CallbackStream


@wraps(connect)
def connect_ws(*args, **kwargs):
    websocket = connect(*args, **kwargs)

    def receive_bytes(timeout: float | None) -> bytes:
        try:
            return websocket.recv(timeout) or b""  # returns bytes, None impossible
        except TimeoutError:
            return b""
        except ConnectionClosed as exc:
            raise EOFError("WS closed") from exc

    def send_bytes(data: bytes):
        try:
            websocket.send(data)
        except ConnectionClosed as exc:
            raise EOFError("WS closed") from exc

    def close():
        websocket.close()
        stream.close()

    stream = CallbackStream(receive_bytes, send_bytes, close)
    return connect_stream(stream)
