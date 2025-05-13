import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from rpyc.utils.classic import connect_stream

from rpyc_ws.stream import CallbackStream


def create_rpyc_fastapi_app(path: str = "/rpyc-ws/"):
    app = FastAPI()

    @app.websocket(path)
    async def _rpyc_ws(websocket: WebSocket):
        await websocket.accept()
        loop = asyncio.get_running_loop()

        def ws_close():
            asyncio.run_coroutine_threadsafe(websocket.close(), loop).result()

        def ws_receive_bytes(timeout: float):
            future = asyncio.run_coroutine_threadsafe(websocket.receive_bytes(), loop)
            try:
                return future.result(timeout)
            except TimeoutError:
                return None
            except WebSocketDisconnect as exc:
                raise EOFError("WS closed") from exc

        def ws_send_bytes(data: bytes):
            try:
                asyncio.run_coroutine_threadsafe(
                    websocket.send_bytes(data), loop
                ).result()
            except WebSocketDisconnect as exc:
                raise EOFError("WS closed") from exc

        stream = CallbackStream(
            ws_receive_bytes,
            ws_send_bytes,
            ws_close,
        )
        conn = await loop.run_in_executor(None, connect_stream, stream)
        try:
            await loop.run_in_executor(None, conn.serve_all)
        finally:
            await loop.run_in_executor(None, conn.close)

    return app
