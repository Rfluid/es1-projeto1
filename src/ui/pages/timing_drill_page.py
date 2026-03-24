from src.domain.drill_config import TimingDrillConfig
from src.session.timing_drill_session import TimingDrillSession
from src.session.events import DrillEvent, EventType
from src.ui.page import Page
from src.ui.drill_timer import DrillTimer


def _fmt_time(seconds: int) -> str:
    m, s = divmod(max(0, seconds), 60)
    return f"{m:02d}:{s:02d}"


class TimingDrillPage(Page):
    def __init__(self, ctx):
        super().__init__(ctx)
        self._timer: DrillTimer | None = None
        self._session: TimingDrillSession | None = None
        self._proxies = []

    def render(self) -> str:
        return """
        <div class="page-header">
            <button class="btn-back" id="btn-back">&#8592; Voltar</button>
            <h1>Timing Drill</h1>
        </div>

        <div id="config-section" class="config-form">
            <label>Duração total (s)
                <input type="number" id="in-duration" value="180" min="1">
            </label>
            <label>Intervalo mínimo (s)
                <input type="number" id="in-min" value="2" min="1">
            </label>
            <label>Intervalo máximo (s)
                <input type="number" id="in-max" value="8" min="1">
            </label>
            <label>Técnica-alvo
                <input type="text" id="in-technique" value="jab" placeholder="ex: jab, teep">
            </label>
            <button class="btn-primary" id="btn-start">Iniciar</button>
            <p id="config-error" class="error-msg"></p>
        </div>

        <div id="running-section" class="running-display" style="display:none;">
            <div class="timer-display" id="timer-display">00:00</div>
            <div class="stimulus-zone" id="stimulus-zone"></div>
            <div class="timer-controls">
                <button class="btn-secondary" id="btn-pause">Pausar</button>
                <button class="btn-danger" id="btn-stop">Parar</button>
            </div>
        </div>
        """

    def mount(self) -> None:
        from pyodide.ffi import create_proxy  # type: ignore[import-not-found]
        from js import document  # type: ignore[import-not-found]

        p = create_proxy(lambda e: self.ctx.router.navigate("#/"))
        document.getElementById("btn-back").addEventListener("click", p)
        self._proxies.append(p)

        p = create_proxy(lambda e: self._on_start())
        document.getElementById("btn-start").addEventListener("click", p)
        self._proxies.append(p)

        p = create_proxy(lambda e: self._on_pause())
        document.getElementById("btn-pause").addEventListener("click", p)
        self._proxies.append(p)

        p = create_proxy(lambda e: self._on_stop())
        document.getElementById("btn-stop").addEventListener("click", p)
        self._proxies.append(p)

    def destroy(self) -> None:
        if self._timer:
            self._timer.stop()
        for p in self._proxies:
            p.destroy()

    def _on_start(self) -> None:
        from js import document  # type: ignore[import-not-found]

        try:
            config = TimingDrillConfig(
                total_duration=int(document.getElementById("in-duration").value),
                min_interval=int(document.getElementById("in-min").value),
                max_interval=int(document.getElementById("in-max").value),
                target_technique=document.getElementById("in-technique").value,
            )
            config.validate()
        except (ValueError, TypeError) as e:
            document.getElementById("config-error").textContent = str(e)
            return

        document.getElementById("config-section").style.display = "none"
        document.getElementById("running-section").style.display = ""

        self._total = config.total_duration
        self._session = TimingDrillSession(config)
        self._session.on_event(self._handle_event)
        self._timer = DrillTimer(self._session, self._update_display)
        self._timer.start()

    def _on_pause(self) -> None:
        from js import document  # type: ignore[import-not-found]

        if not self._timer or not self._session:
            return
        if self._session.is_paused:
            self._timer.resume()
            document.getElementById("btn-pause").textContent = "Pausar"
        else:
            self._timer.pause()
            document.getElementById("btn-pause").textContent = "Continuar"

    def _on_stop(self) -> None:
        if self._timer:
            self._timer.stop()
        self._show_config()

    def _handle_event(self, event: DrillEvent) -> None:
        from js import document  # type: ignore[import-not-found]

        if event.event_type == EventType.STIMULUS:
            self.ctx.audio_engine.play_start_signal()
            self.ctx.announcer.announce(event.data["technique"])
            zone = document.getElementById("stimulus-zone")
            zone.textContent = event.data["technique"].upper()
            zone.classList.add("stimulus-flash")
            # Remove animation class after a short time to allow re-trigger
            from js import window  # type: ignore[import-not-found]
            from pyodide.ffi import create_proxy  # type: ignore[import-not-found]

            def _clear(e=None):
                zone.classList.remove("stimulus-flash")

            p = create_proxy(_clear)
            window.setTimeout(p, 500)
        elif event.event_type == EventType.SESSION_END:
            self.ctx.audio_engine.play_end_signal()
            self.ctx.announcer.announce("Fim do treino")
            self._show_config()

    def _update_display(self) -> None:
        from js import document  # type: ignore[import-not-found]

        if not self._session:
            return
        remaining = max(0, self._total - self._session.elapsed)
        document.getElementById("timer-display").textContent = _fmt_time(remaining)

    def _show_config(self) -> None:
        from js import document  # type: ignore[import-not-found]

        document.getElementById("config-section").style.display = ""
        document.getElementById("running-section").style.display = "none"
