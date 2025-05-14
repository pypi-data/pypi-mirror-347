import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState
from rpyc.utils.classic import connect_stream

from rpyc_ws.stream import CallbackStream


def create_rpyc_fastapi_app(path: str = "/rpyc-ws/"):
    app = FastAPI()

    @app.websocket(path)
    async def _rpyc_ws(websocket: WebSocket):
        await websocket.accept()
        loop = asyncio.get_running_loop()

        # ---------------------------------------------------------------- #
        #  three thin, thread-safe wrappers
        # ---------------------------------------------------------------- #
        def ws_close() -> None:
            try:
                if websocket.application_state == WebSocketState.CONNECTED:
                    asyncio.run_coroutine_threadsafe(websocket.close(), loop).result()
            except (RuntimeError, WebSocketDisconnect):
                pass

        def ws_receive_bytes(timeout: float | None) -> bytes:
            fut = asyncio.run_coroutine_threadsafe(websocket.receive_bytes(), loop)
            try:
                return fut.result(timeout)  # may raise TimeoutError
            except TimeoutError:
                return b""  # *idle* poll – no data
            except WebSocketDisconnect as exc:
                raise EOFError("WS closed") from exc

        def ws_send_bytes(data: bytes) -> None:
            try:
                asyncio.run_coroutine_threadsafe(
                    websocket.send_bytes(data), loop
                ).result()
            except WebSocketDisconnect as exc:
                raise EOFError("WS closed") from exc

        stream = CallbackStream(ws_receive_bytes, ws_send_bytes, ws_close)

        # create connection in worker thread
        conn = await loop.run_in_executor(None, connect_stream, stream)

        # -> serve until CallbackStream.read() raises EOFError
        try:
            await loop.run_in_executor(None, conn.serve_all)
        finally:
            await loop.run_in_executor(None, conn.close)

    return app
