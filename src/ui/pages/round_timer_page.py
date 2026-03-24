from src.domain.drill_config import RoundTimerConfig
from src.session.round_timer_session import RoundTimerSession
from src.session.events import DrillEvent, EventType
from src.ui.page import Page
from src.ui.drill_timer import DrillTimer


def _fmt_time(seconds: int) -> str:
    m, s = divmod(max(0, seconds), 60)
    return f"{m:02d}:{s:02d}"


class RoundTimerPage(Page):
    def __init__(self, ctx):
        super().__init__(ctx)
        self._timer: DrillTimer | None = None
        self._session: RoundTimerSession | None = None
        self._proxies = []

    def render(self) -> str:
        return """
        <div class="page-header">
            <button class="btn-back" id="btn-back">&#8592; Voltar</button>
            <h1>Round Timer</h1>
        </div>

        <div id="config-section" class="config-form">
            <label>Rounds
                <input type="number" id="in-rounds" value="3" min="1">
            </label>
            <label>Trabalho (s)
                <input type="number" id="in-work" value="180" min="1">
            </label>
            <label>Descanso (s)
                <input type="number" id="in-rest" value="60" min="0">
            </label>
            <label>Aviso antes do fim (s)
                <input type="number" id="in-warning" value="10" min="0">
            </label>
            <button class="btn-primary" id="btn-start">Iniciar</button>
            <p id="config-error" class="error-msg"></p>
        </div>

        <div id="running-section" class="running-display" style="display:none;">
            <div class="timer-display" id="timer-display">00:00</div>
            <div class="timer-info">
                <span>Round <span id="round-num">-</span> / <span id="round-total">-</span></span>
                <span class="phase-badge" id="phase-badge">-</span>
            </div>
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
            config = RoundTimerConfig(
                num_rounds=int(document.getElementById("in-rounds").value),
                work_duration=int(document.getElementById("in-work").value),
                rest_duration=int(document.getElementById("in-rest").value),
                warning_time=int(document.getElementById("in-warning").value),
            )
            config.validate()
        except (ValueError, TypeError) as e:
            document.getElementById("config-error").textContent = str(e)
            return

        document.getElementById("config-section").style.display = "none"
        document.getElementById("running-section").style.display = ""
        document.getElementById("round-total").textContent = str(config.num_rounds)

        self._session = RoundTimerSession(config)
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
        audio = self.ctx.audio_engine
        announce = self.ctx.announcer.announce
        if event.event_type == EventType.ROUND_START:
            audio.play_start_signal()
            round_num = event.data.get("round", "")
            announce(f"Round {round_num}, trabalho")
        elif event.event_type == EventType.ROUND_WARNING:
            audio.play_warning_signal()
            announce("Atenção")
        elif event.event_type == EventType.ROUND_END:
            audio.play_end_signal()
            announce("Descanso")
        elif event.event_type == EventType.REST_END:
            audio.play_end_signal()
        elif event.event_type == EventType.SESSION_END:
            audio.play_end_signal()
            announce("Fim do treino")
            self._show_config()

    def _update_display(self) -> None:
        from js import document  # type: ignore[import-not-found]

        if not self._session:
            return
        document.getElementById("timer-display").textContent = _fmt_time(
            self._session.phase_remaining
        )
        document.getElementById("round-num").textContent = str(
            self._session.current_round
        )
        phase = self._session.phase
        badge = document.getElementById("phase-badge")
        badge.textContent = "TRABALHO" if phase == "work" else "DESCANSO"
        badge.className = f"phase-badge phase-{phase}"

    def _show_config(self) -> None:
        from js import document  # type: ignore[import-not-found]

        document.getElementById("config-section").style.display = ""
        document.getElementById("running-section").style.display = "none"
