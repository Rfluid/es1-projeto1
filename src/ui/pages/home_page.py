from src.ui.page import Page


class HomePage(Page):
    def render(self) -> str:
        return """
        <h1>FightDrill</h1>
        <p class="subtitle">Plataforma de Treinamento para Artes Marciais</p>

        <h2>Modalidades de Treino</h2>
        <div class="card-grid">
            <button class="nav-card" id="nav-round-timer">
                <span class="card-icon">&#9201;</span>
                <span class="card-title">Round Timer</span>
                <span class="card-desc">Rounds de trabalho e descanso</span>
            </button>
            <button class="nav-card" id="nav-timing-drill">
                <span class="card-icon">&#9889;</span>
                <span class="card-title">Timing Drill</span>
                <span class="card-desc">Reação a estímulo aleatório</span>
            </button>
            <button class="nav-card" id="nav-combo-drill">
                <span class="card-icon">&#9994;</span>
                <span class="card-title">Combo Drill</span>
                <span class="card-desc">Chamadas de combos</span>
            </button>
            <button class="nav-card" id="nav-footwork-drill">
                <span class="card-icon">&#128095;</span>
                <span class="card-title">Footwork Drill</span>
                <span class="card-desc">Movimentação e deslocamento</span>
            </button>
        </div>

        <h2>Gerenciamento</h2>
        <div class="card-grid">
            <button class="nav-card nav-card--manage" id="nav-combo-library">
                <span class="card-title">Biblioteca de Combos</span>
            </button>
            <button class="nav-card nav-card--manage" id="nav-footwork-moves">
                <span class="card-title">Movimentações</span>
            </button>
            <button class="nav-card nav-card--manage" id="nav-custom-workouts">
                <span class="card-title">Treinos Personalizados</span>
            </button>
        </div>
        """

    def mount(self) -> None:
        from pyodide.ffi import create_proxy  # type: ignore[import-not-found]
        from js import document  # type: ignore[import-not-found]

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

    def destroy(self) -> None:
        if hasattr(self, "_proxies"):
            for p in self._proxies:
                p.destroy()
