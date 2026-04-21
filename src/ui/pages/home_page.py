from src.ui.page import Page


class HomePage(Page):
    def render(self) -> str:
        t = self.ctx.i18n.t
        audio_vol = int(self.ctx.app_state.audio_volume * 100)
        voice_vol = int(self.ctx.app_state.voice_volume * 100)
        voice_rate = int(self.ctx.app_state.voice_rate * 100)
        return f"""
        <h1>FightDrill</h1>
        <p class="subtitle">{t("home.subtitle")}</p>

        <h2>{t("home.drills_heading")}</h2>
        <div class="card-grid">
            <button class="nav-card" id="nav-round-timer">
                <span class="card-icon">&#9201;</span>
                <span class="card-title">Round Timer</span>
                <span class="card-desc">{t("home.round_timer_desc")}</span>
            </button>
            <button class="nav-card" id="nav-timing-drill">
                <span class="card-icon">&#9889;</span>
                <span class="card-title">Timing Drill</span>
                <span class="card-desc">{t("home.timing_drill_desc")}</span>
            </button>
            <button class="nav-card" id="nav-combo-drill">
                <span class="card-icon">&#9994;</span>
                <span class="card-title">Combo Drill</span>
                <span class="card-desc">{t("home.combo_drill_desc")}</span>
            </button>
            <button class="nav-card" id="nav-footwork-drill">
                <span class="card-icon">&#128095;</span>
                <span class="card-title">Footwork Drill</span>
                <span class="card-desc">{t("home.footwork_drill_desc")}</span>
            </button>
        </div>

        <h2>{t("home.manage_heading")}</h2>
        <div class="card-grid">
            <button class="nav-card nav-card--manage" id="nav-combo-library">
                <span class="card-title">{t("home.combo_library")}</span>
            </button>
            <button class="nav-card nav-card--manage" id="nav-footwork-moves">
                <span class="card-title">{t("home.footwork_moves")}</span>
            </button>
            <button class="nav-card nav-card--manage" id="nav-custom-workouts">
                <span class="card-title">{t("home.custom_workouts")}</span>
            </button>
        </div>

        <h2>{t("home.settings_heading")}</h2>
        <div class="settings-section">
            <label for="slider-audio-volume">{t("home.audio_volume")}: <span id="lbl-audio-volume">{audio_vol}%</span></label>
            <input type="range" id="slider-audio-volume" min="0" max="100" value="{audio_vol}">
            <label for="slider-voice-volume">{t("home.voice_volume")}: <span id="lbl-voice-volume">{voice_vol}%</span></label>
            <input type="range" id="slider-voice-volume" min="0" max="100" value="{voice_vol}">
            <label for="slider-voice-rate">{t("home.voice_rate")}: <span id="lbl-voice-rate">{voice_rate}%</span></label>
            <input type="range" id="slider-voice-rate" min="50" max="200" step="10" value="{voice_rate}">
        </div>
        """

    def mount(self) -> None:
        from js import document  # type: ignore[import-not-found]
        from pyodide.ffi import create_proxy  # type: ignore[import-not-found]

        routes = {
            "nav-round-timer": "#/round-timer",
            "nav-timing-drill": "#/timing-drill",
            "nav-combo-drill": "#/combo-drill",
            "nav-footwork-drill": "#/footwork-drill",
            "nav-combo-library": "#/combo-library",
            "nav-footwork-moves": "#/footwork-moves",
            "nav-custom-workouts": "#/custom-workouts",
        }
        self._proxies = []
        for elem_id, path in routes.items():
            proxy = create_proxy(lambda e, p=path: self.ctx.router.navigate(p))
            document.getElementById(elem_id).addEventListener("click", proxy)
            self._proxies.append(proxy)

        def on_audio_volume(e):
            vol = int(e.target.value) / 100
            self.ctx.audio_engine.volume = vol
            self.ctx.app_state.audio_volume = vol
            self.ctx.app_state.save()
            document.getElementById("lbl-audio-volume").textContent = f"{int(e.target.value)}%"

        def on_voice_volume(e):
            vol = int(e.target.value) / 100
            self.ctx.announcer.volume = vol
            self.ctx.app_state.voice_volume = vol
            self.ctx.app_state.save()
            document.getElementById("lbl-voice-volume").textContent = f"{int(e.target.value)}%"

        def on_voice_rate(e):
            rate = int(e.target.value) / 100
            self.ctx.announcer.rate = rate
            self.ctx.app_state.voice_rate = rate
            self.ctx.app_state.save()
            document.getElementById("lbl-voice-rate").textContent = f"{int(e.target.value)}%"

        p_audio = create_proxy(on_audio_volume)
        p_voice = create_proxy(on_voice_volume)
        p_rate = create_proxy(on_voice_rate)
        document.getElementById("slider-audio-volume").addEventListener("input", p_audio)
        document.getElementById("slider-voice-volume").addEventListener("input", p_voice)
        document.getElementById("slider-voice-rate").addEventListener("input", p_rate)
        self._proxies.extend([p_audio, p_voice, p_rate])

    def destroy(self) -> None:
        if hasattr(self, "_proxies"):
            for p in self._proxies:
                p.destroy()
