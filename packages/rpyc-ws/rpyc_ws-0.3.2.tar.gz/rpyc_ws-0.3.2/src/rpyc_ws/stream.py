from typing import Callable, Optional

from rpyc.core.consts import STREAM_CHUNK
from rpyc.core.stream import Stream
from rpyc.lib import Timeout


class CallbackStream(Stream):
    """Duplex byte stream backed by three user-supplied callbacks.

    The callbacks MUST be thread-safe if you plan to access the
    stream concurrently.
    """

    __slots__ = ("_recv", "_send", "_close", "_buf", "_closed")
    MAX_IO_CHUNK = STREAM_CHUNK

    def __init__(
        self,
        recv: Callable[[Optional[float]], bytes | None],
        send: Callable[[bytes], None],
        close: Callable[[], None],
    ):
        self._recv = recv
        self._send = send
        self._close = close
        self._buf = bytearray()
        self._closed: bool = False

    # --------------------------------------------------------------------- #
    # bookkeeping
    # --------------------------------------------------------------------- #

    @property
    def closed(self) -> bool:
        return self._closed

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        try:
            self._close()
        finally:
            self._buf.clear()
            # break reference cycles
            self._recv = self._send = self._close = lambda *a, **k: None

    def fileno(self) -> int:  # not supported, but must exist
        raise EOFError("CallbackStream has no OS file descriptor")

    # --------------------------------------------------------------------- #
    # I/O
    # --------------------------------------------------------------------- #

    def read(self, count: int) -> bytes:  # must return *exactly* count bytes
        if self._closed:
            raise EOFError("stream has been closed")

        out = bytearray()

        # 1) use spill-over first
        if self._buf:
            take = self._buf[:count]
            out += take
            del self._buf[: len(take)]

        # 2) keep fetching until satisfied
        while len(out) < count:
            msg = self._recv(None)  # block until something or EOF
            if not msg:  # None or b''
                self.close()
                raise EOFError("connection closed by peer")

            need = count - len(out)
            out += msg[:need]

            # spill-over if frame was larger
            if len(msg) > need:
                self._buf += msg[need:]

        return bytes(out)

    def write(self, data: bytes | bytearray | memoryview) -> None:
        if self._closed:
            raise EOFError("stream has been closed")

        mv = memoryview(data)
        idx = 0
        try:
            while idx < len(mv):
                chunk = mv[idx : idx + self.MAX_IO_CHUNK]
                self._send(chunk.tobytes())
                idx += len(chunk)
        except Exception as exc:
            self.close()
            raise EOFError("connection closed while writing") from exc

    # --------------------------------------------------------------------- #
    # readiness
    # --------------------------------------------------------------------- #

    def poll(self, timeout: float | Timeout | None) -> bool:
        """Return *True* if at least one byte can be read within *timeout*."""
        if self._buf:  # already have buffered data
            return True

        timeout = Timeout(timeout)
        while True:
            slice_len = timeout.timeleft()
            if slice_len is not None and slice_len <= 0:
                return False

            try:
                msg = self._recv(slice_len)
            except Exception:
                # websocket client may raise its own timeout exception
                if timeout.expired():
                    return False
                raise

            if msg:
                self._buf += msg
                return True

            if timeout.expired():
                return False
