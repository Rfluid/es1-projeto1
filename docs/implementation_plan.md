# FightDrill — Plano de Implementação

Plano faseado para implementação do FightDrill conforme a especificação de requisitos (`entrega1.md`).
Código-fonte em `./src`. Stack: Python (PyScript) + HTML. Arquitetura fortemente orientada a objetos.

---

## Fase 1 — Modelo de Domínio (classes de negócio)

Objetivo: definir todas as classes do domínio, sem UI nem persistência. Cada classe deve ser testável isoladamente.

- [x] **Classe `Combo`** — nome (`str`) e descrição/sequência de técnicas (`str`). `src/domain/combo.py`
    - [x] Validação: nome não vazio.
- [x] **Classe `FootworkMove`** — nome da movimentação (`str`). `src/domain/footwork_move.py`
    - [x] Validação: nome não vazio.
- [x] **Classe `CustomWorkout`** — nome (`str`), duração estimada (`int`, segundos) e descrição opcional (`str`). `src/domain/custom_workout.py`
    - [x] Validação conforme **RN04**: nome não vazio e duração > 0.
- [x] **Classe abstrata `DrillConfig`** — configuração base de qualquer modalidade (duração total, etc.). `src/domain/drill_config.py`
- [x] **Classe `RoundTimerConfig(DrillConfig)`** — número de rounds, duração trabalho, duração descanso, tempo aviso. `src/domain/drill_config.py`
- [x] **Classe `TimingDrillConfig(DrillConfig)`** — duração total, intervalo mín, intervalo máx, técnica-alvo. `src/domain/drill_config.py`
    - [x] Validação conforme **RN01**: intervalo mín < intervalo máx.
- [x] **Classe `ComboDrillConfig(DrillConfig)`** — lista de `Combo` selecionados, modo de chamada (enum `SEQUENTIAL`/`RANDOM`), intervalo entre chamadas, duração total. `src/domain/drill_config.py`
    - [x] Validação: pelo menos um combo selecionado.
- [x] **Classe `FootworkDrillConfig(DrillConfig)`** — lista de `FootworkMove` selecionados, intervalo mín, intervalo máx, duração total. `src/domain/drill_config.py`
    - [x] Validação conforme **RN01** e **RN05**: intervalo mín < intervalo máx; pelo menos uma movimentação selecionada.
- [x] **Enum `CallMode`** — `SEQUENTIAL`, `RANDOM`. `src/domain/call_mode.py`
- [x] **Classe `ComboLibrary`** — coleção de `Combo` com métodos CRUD (add, update, remove, list, get_by_name). `src/domain/libraries.py`
- [x] **Classe `FootworkMoveLibrary`** — coleção de `FootworkMove` com métodos CRUD. `src/domain/libraries.py`
- [x] **Classe `CustomWorkoutLibrary`** — coleção de `CustomWorkout` com métodos CRUD. `src/domain/libraries.py`
- [x] Testes unitários para todas as classes e validações desta fase. (84 testes — `tests/test_combo.py`, `tests/test_footwork_move.py`, `tests/test_custom_workout.py`, `tests/test_drill_config.py`, `tests/test_libraries.py`)

---

## Fase 2 — Motor de Áudio

Objetivo: abstrair a Web Audio API para emissão de sinais sonoros e anúncios por voz sintética (Speech Synthesis API).

- [x] **Classe `AudioEngine`** — encapsula `AudioContext` (Web Audio API). `src/audio/audio_engine.py`
    - [x] Método `play_tone(frequency, duration)` — gera tom senoidal (beep).
    - [x] Método `play_start_signal()` — sinal de início de round/drill.
    - [x] Método `play_warning_signal()` — sinal de aviso de fim de round.
    - [x] Método `play_end_signal()` — sinal de fim de round/drill.
- [x] **Classe `Announcer`** — encapsula Speech Synthesis API do navegador. `src/audio/announcer.py`
    - [x] Método `announce(text)` — reproduz nome do combo/movimentação/fase via voz sintética (**RN06**).
    - [x] Usado em todas as modalidades: nomes de combos, movimentações, técnica-alvo, fases do round timer (trabalho/descanso/atenção), e fim de treino.
- [x] **Backends do navegador** — `WebAudioPlayer` (TonePlayer) e `WebSpeechBackend` (SpeechBackend). `src/audio/web_backends.py`
- [x] Testes unitários via fake backends (16 testes — `tests/test_audio_engine.py`, `tests/test_announcer.py`).
- [ ] Testes manuais de reprodução de áudio no navegador.

---

## Fase 3 — Camada de Persistência (localStorage)

Objetivo: serialização/desserialização dos dados do domínio, com validação de integridade (**RNF07**).

- [x] **Classe `StorageManager`** — interface de leitura/escrita no `localStorage`. `src/persistence/storage_manager.py`
    - [x] Método `save(key, data)` — serializa para JSON e salva.
    - [x] Método `load(key) -> dict | None` — lê e desserializa JSON. Raises `ValueError` se JSON corrompido.
    - [x] Método `clear(key)` — remove chave.
- [x] **Classe `AppState`** — centraliza o estado da aplicação (bibliotecas de combos, movimentações, treinos personalizados, calendário). `src/persistence/app_state.py`
    - [x] Método `save()` — persiste estado completo via `StorageManager`.
    - [x] Método `load()` — restaura estado do `localStorage`; se dados corrompidos, inicializa estado padrão e notifica usuário (**RNF07**).
    - [x] Método `to_dict()` / `_load_from_dict(data)` — conversão de/para dicionário.
- [x] **Backend do navegador** — `LocalStorageBackend`. `src/persistence/web_backend.py`
- [x] Testes unitários para serialização/desserialização e tratamento de dados inválidos (21 testes — `tests/test_storage_manager.py`, `tests/test_app_state.py`).

---

## Fase 4 — Lógica de Execução dos Treinos

Objetivo: implementar a máquina de estados de cada modalidade de treino (sem UI).

- [x] **Classe abstrata `DrillSession`** — base para execução de qualquer treino. `src/session/drill_session.py`
    - [x] Atributos: `config`, `elapsed`, `is_running`, `is_paused`, `is_finished`.
    - [x] Métodos: `start()`, `pause()`, `resume()`, `stop()`.
    - [x] Método abstrato `_on_tick()` — chamado a cada ciclo do timer.
    - [x] Callback `on_event(callback)` — para a UI reagir a eventos.
- [x] **Classe `RoundTimerSession(DrillSession)`** — implementa lógica de rounds. `src/session/round_timer_session.py`
    - [x] Controle de round atual, tempo restante de trabalho/descanso.
    - [x] Emite eventos: `ROUND_START`, `ROUND_WARNING`, `ROUND_END`, `REST_END`, `SESSION_END`.
- [x] **Classe `TimingDrillSession(DrillSession)`** — implementa estímulo aleatório. `src/session/timing_drill_session.py`
    - [x] Gera próximo instante de estímulo aleatório dentro do intervalo configurado.
    - [x] Emite eventos: `STIMULUS`, `SESSION_END`.
- [x] **Classe `ComboDrillSession(DrillSession)`** — implementa chamadas de combo. `src/session/combo_drill_session.py`
    - [x] Modo sequencial: iteração cíclica (**RN02**).
    - [x] Modo aleatório: sem repetição consecutiva (**RN02**).
    - [x] Emite eventos: `COMBO_CALL(combo)`, `SESSION_END`.
- [x] **Classe `FootworkDrillSession(DrillSession)`** — implementa chamadas de movimentação. `src/session/footwork_drill_session.py`
    - [x] Escolha aleatória entre movimentações selecionadas.
    - [x] Emite eventos: `MOVE_CALL(move)`, `SESSION_END`.
- [x] **Tipos de evento** — `EventType` enum + `DrillEvent` dataclass. `src/session/events.py`
- [ ] **Classe `DrillTimer`** — wrapper de `setInterval`/`requestAnimationFrame` para chamar `tick()` com precisão (**RNF01**). _(será implementada na Fase 5 junto com a UI)_
- [x] Testes unitários para lógica de cada sessão via simulação de ticks (37 testes — `tests/test_round_timer_session.py`, `tests/test_timing_drill_session.py`, `tests/test_combo_drill_session.py`, `tests/test_footwork_drill_session.py`).

---

## Fase 5 — Interface do Usuário (HTML + PyScript)

Objetivo: construir as telas da aplicação, conectando UI às classes de domínio e sessão.

- [x] **Estrutura base HTML** — `index.html` com PyScript 2024.1.1, CSS dark theme responsivo (**RNF05**), container `#app`. `index.html`
- [x] **Configuração PyScript** — `pyscript.toml` mapeando `./src/` para imports.
- [x] **Classe `Router`** — navegação SPA hash-based com `resolve()`, `navigate()`, `start()`. `src/ui/router.py`
- [x] **Classe abstrata `Page`** — `render()` → HTML string, `mount()` → bind events, `destroy()` → cleanup. `src/ui/page.py`
- [x] **Classe `AppContext`** — container para app_state, audio_engine, announcer, router. `src/ui/app_context.py`
- [x] **Classe `DrillTimer`** — wrapper de `setInterval` chamando `session.tick()` a cada segundo. `src/ui/drill_timer.py`
    - [x] Contagem regressiva de 3 segundos antes de iniciar a sessão (**RF13**). Callback `on_countdown` notifica a UI a cada segundo da contagem.
- [x] **`HomePage(Page)`** — grid de navegação para modalidades e gerenciamento. `src/ui/pages/home_page.py`
- [x] **`RoundTimerPage(Page)`** — config + execução do Round Timer (**RF01**). `src/ui/pages/round_timer_page.py`
    - [x] Timer com contagem regressiva, round atual, fase trabalho/descanso.
    - [x] Botões: iniciar, pausar/continuar, parar.
    - [x] Integração com `RoundTimerSession` e `AudioEngine`.
    - [x] Contagem regressiva 3…2…1 com badge "PREPARE-SE" antes de iniciar (**RF13**).
- [x] **`TimingDrillPage(Page)`** — config + execução do Timing Drill (**RF02**). `src/ui/pages/timing_drill_page.py`
    - [x] Timer, estímulo visual animado (flash) + anúncio sonoro.
    - [x] Integração com `TimingDrillSession`, `AudioEngine` e `Announcer`.
    - [x] Contagem regressiva 3…2…1 antes de iniciar (**RF13**).
- [x] **`ComboDrillPage(Page)`** — config + execução do Combo Drill (**RF03**). `src/ui/pages/combo_drill_page.py`
    - [x] Seleção de combos via checkboxes, modo sequencial/aleatório.
    - [x] Exibe nome + sequência do combo atual; anúncio por voz.
    - [x] Mensagem e link para biblioteca se não houver combos.
    - [x] Contagem regressiva 3…2…1 antes de iniciar (**RF13**).
- [x] **`FootworkDrillPage(Page)`** — config + execução do Footwork Drill (**RF04**). `src/ui/pages/footwork_drill_page.py`
    - [x] Seleção de movimentações via checkboxes.
    - [x] Exibe movimentação atual; anúncio por voz.
    - [x] Contagem regressiva 3…2…1 antes de iniciar (**RF13**).
- [x] **`ComboLibraryPage(Page)`** — CRUD de combos (**RF06**). `src/ui/pages/combo_library_page.py`
    - [x] Listagem, adição, exclusão com re-render.
- [x] **`FootworkMovePage(Page)`** — CRUD de movimentações (**RF07**). `src/ui/pages/footwork_move_page.py`
    - [x] Listagem, adição, exclusão com re-render.
- [x] **`CustomWorkoutPage(Page)`** — CRUD de treinos personalizados (**RF05**). `src/ui/pages/custom_workout_page.py`
    - [x] Listagem, adição, exclusão com re-render.
- [x] Persistência automática via `AppState.save()` após cada operação CRUD (**RF11**).
- [x] **Entry point** — `src/main.py` bootstraps backends, state, router, routes.
- [x] Testes unitários para Router.resolve() e Page.render() (21 testes — `tests/test_router.py`, `tests/test_pages_render.py`).
- [ ] Testes manuais de usabilidade (**RNF04**) e responsividade (**RNF05**).

---

## Fase 6 — Calendário Semanal e Compartilhamento via URL

Objetivo: implementar calendário semanal, exportação/importação por URL (**RF08, RF09, RF10**).

- [ ] **Classe `WeeklyCalendar`** — estrutura de dados para o calendário (dict de dia da semana → lista de treinos).
    - [ ] Métodos: `add_workout(day, workout)`, `remove_workout(day, index)`, `get_day(day)`, `clear()`.
    - [ ] Método `to_dict()` / `from_dict(data)`.
- [ ] **Classe `CalendarExporter`** — codifica calendário em JSON → Base64 → parâmetro de URL (**RN03**).
    - [ ] Método `export_url(calendar) -> str`.
- [ ] **Classe `CalendarImporter`** — decodifica URL → Base64 → JSON → `WeeklyCalendar` (**RN03**).
    - [ ] Método `import_from_url(url) -> WeeklyCalendar`.
    - [ ] Validação de integridade dos dados decodificados.
- [ ] **`CalendarPage(Page)`** — tela do calendário semanal (**RF08**).
    - [ ] Visualização semanal (segunda a domingo) com treinos atribuídos.
    - [ ] Adição/remoção de treinos em cada dia.
    - [ ] Botão exportar URL (**RF09**) — exibe URL copiável.
    - [ ] Botão/campo importar URL (**RF10**) — com confirmação antes de substituir (**RN03**).
- [ ] Detecção automática de parâmetro de calendário na URL ao carregar a aplicação.
- [ ] Persistência do calendário via `AppState` (**RF11**).
- [ ] Testes unitários para codificação/decodificação Base64 e integridade.
- [ ] Testes end-to-end: exportar → copiar URL → abrir em novo navegador → verificar calendário.

---

## Fase 7 — Internacionalização (i18n): Português e Inglês

Objetivo: suportar português (pt-BR) e inglês (en), detectando o idioma padrão do navegador. Todas as strings visíveis ao usuário e anúncios por voz devem ser traduzidas.

### Infraestrutura i18n

- [x] **Classe `I18n`** — gerenciador de traduções. `src/i18n.py`
    - [x] Dicionário de traduções por locale (`pt` e `en`), mapeando chaves a strings.
    - [x] Método `t(key: str, **kwargs) -> str` — retorna a string traduzida, com suporte a interpolação (ex.: `t("round_start", round=3)` → `"Round 3, trabalho"`).
    - [x] Método `detect_locale() -> str` — lê `navigator.language` do navegador; retorna `"pt"` se começar com `"pt"`, senão `"en"`.
    - [x] Propriedade `locale` — idioma ativo, inicializado via `detect_locale()`.
- [x] **Registrar `I18n` no `AppContext`** — disponibilizar a instância para todas as páginas.
- [x] Testes unitários para `I18n.t()` com ambos os locales, interpolação, chave inexistente (fallback para inglês).

### Dicionário de traduções

- [x] **Strings da UI (labels, botões, títulos)** — todas as strings hardcoded nas páginas. Inclui:
    - [x] Títulos das páginas (ex.: "Round Timer", "Biblioteca de Combos").
    - [x] Botões: "Voltar", "Iniciar", "Pausar", "Continuar", "Parar", "Adicionar", "Excluir".
    - [x] Labels de formulário: "Rounds", "Trabalho (s)", "Descanso (s)", etc.
    - [x] Mensagens de estado vazio: "Nenhum combo cadastrado", etc.
    - [x] Textos da Home Page: título, subtítulo, descrições dos cards.
- [x] **Strings de anúncio por voz (Announcer)** — frases faladas durante treinos:
    - [x] "Round N, trabalho" / "Round N, work"
    - [x] "Atenção" / "Warning"
    - [x] "Descanso" / "Rest"
    - [x] "Fim do treino" / "Workout complete"
- [x] **Strings de contagem regressiva (RF13):**
    - [x] "PREPARE-SE" / "GET READY"
- [x] **Mensagens de erro e validação:**
    - [x] "Dados corrompidos no localStorage..." (alert no main.py).
    - [x] Mensagens de `ValueError` exibidas ao usuário (considerar traduzir apenas no nível da UI, não no domínio).

### Migração das páginas

- [x] **Substituir strings hardcoded por chamadas `ctx.i18n.t(...)`** em todas as 8 páginas:
    - [x] `home_page.py`
    - [x] `round_timer_page.py`
    - [x] `timing_drill_page.py`
    - [x] `combo_drill_page.py`
    - [x] `footwork_drill_page.py`
    - [x] `combo_library_page.py`
    - [x] `footwork_move_page.py`
    - [x] `custom_workout_page.py`
- [x] **Substituir strings hardcoded nos `_handle_event`** (anúncios por voz) por `ctx.i18n.t(...)`.
- [x] **Atualizar `index.html`** — traduzir o texto de carregamento ("Carregando FightDrill...").
- [x] **Configurar `lang` do `<html>`** dinamicamente conforme o locale detectado.
- [x] **Configurar `WebSpeechBackend.lang`** conforme o locale detectado (para pronúncia correta do TTS).

### Testes

- [x] Testes unitários: `I18n` com locale `pt` e `en`, interpolação, fallback (18 testes — `tests/test_i18n.py`).
- [x] Testes de render das páginas: verificar que `render()` usa chaves i18n (testar com ambos os locales) (8 testes EN — `tests/test_pages_render.py`).
- [ ] Testes manuais: alternar idioma do navegador e verificar UI + voz.

---

## Referência: Rastreabilidade Fase × Requisito

| Requisito | Fase    |
| --------- | ------- |
| RF01      | 4, 5    |
| RF02      | 4, 5    |
| RF03      | 4, 5    |
| RF04      | 4, 5    |
| RF05      | 1, 5    |
| RF06      | 1, 5    |
| RF07      | 1, 5    |
| RF08      | 6       |
| RF09      | 6       |
| RF10      | 6       |
| RF11      | 3, 5, 6 |
| RF12      | 2       |
| RF13      | 5       |
| RN01      | 1       |
| RN02      | 4       |
| RN03      | 6       |
| RN04      | 1       |
| RN05      | 1       |
| RN06      | 2, 4    |
| RNF01     | 4       |
| RNF02     | 2       |
| RNF03     | 5       |
| RNF04     | 5       |
| RNF05     | 5       |
| RNF06     | 5       |
| RNF07     | 3       |
