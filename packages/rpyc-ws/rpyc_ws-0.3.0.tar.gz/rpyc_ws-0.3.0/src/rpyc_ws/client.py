from functools import wraps

from rpyc.utils.classic import connect_stream
from websockets import ConnectionClosed
from websockets.sync.client import connect

from rpyc_ws.stream import CallbackStream


@wraps(connect)
def connect_ws(*args, **kwargs):
    websocket = connect(*args, **kwargs)

    def receive_bytes(timeout: float):
        try:
            result = websocket.recv(timeout, False)
            return result
        except TimeoutError:
            return None
        except ConnectionClosed as exc:
            raise EOFError("WS closed") from exc

    def send_bytes(data: bytes):
        try:
            websocket.send(data)
        except ConnectionClosed as exc:
            raise EOFError("WS closed") from exc

    def close():
        websocket.close()

    stream = CallbackStream(receive_bytes, send_bytes, close)
    return connect_stream(stream)
