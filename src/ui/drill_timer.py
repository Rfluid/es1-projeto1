from typing import Callable

from src.session.drill_session import DrillSession


class DrillTimer:
    """Wraps browser setInterval to tick a DrillSession every second."""

    def __init__(self, session: DrillSession, on_tick: Callable[[], None]) -> None:
        self._session = session
        self._on_tick = on_tick
        self._interval_id: int | None = None
        self._proxy = None

    def start(self) -> None:
        from js import window  # type: ignore[import-not-found]
        from pyodide.ffi import create_proxy  # type: ignore[import-not-found]

        self._session.start()

        def _tick():
            self._session.tick()
            self._on_tick()

        self._proxy = create_proxy(_tick)
        self._interval_id = window.setInterval(self._proxy, 1000)

    def pause(self) -> None:
        self._session.pause()

    def resume(self) -> None:
        self._session.resume()

    def stop(self) -> None:
        if self._interval_id is not None:
            from js import window  # type: ignore[import-not-found]

            window.clearInterval(self._interval_id)
            self._interval_id = None
        self._session.stop()
        if self._proxy is not None:
            self._proxy.destroy()
            self._proxy = None
