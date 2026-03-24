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
    - [x] Método `announce(text)` — reproduz nome do combo/movimentação via voz sintética (**RN06**).
- [x] **Backends do navegador** — `WebAudioPlayer` (TonePlayer) e `WebSpeechBackend` (SpeechBackend). `src/audio/web_backends.py`
- [x] Testes unitários via fake backends (16 testes — `tests/test_audio_engine.py`, `tests/test_announcer.py`).
- [ ] Testes manuais de reprodução de áudio no navegador.

---

## Fase 3 — Camada de Persistência (localStorage)

Objetivo: serialização/desserialização dos dados do domínio, com validação de integridade (**RNF07**).

- [ ] **Classe `StorageManager`** — interface de leitura/escrita no `localStorage`.
    - [ ] Método `save(key, data)` — serializa para JSON e salva.
    - [ ] Método `load(key) -> dict | None` — lê e desserializa JSON.
    - [ ] Método `clear(key)` — remove chave.
- [ ] **Classe `AppState`** — centraliza o estado da aplicação (bibliotecas de combos, movimentações, treinos personalizados, calendário).
    - [ ] Método `save()` — persiste estado completo via `StorageManager`.
    - [ ] Método `load()` — restaura estado do `localStorage`; se dados corrompidos, inicializa estado padrão e notifica usuário (**RNF07**).
    - [ ] Método `to_dict()` / `from_dict(data)` — conversão de/para dicionário.
- [ ] Testes unitários para serialização/desserialização e tratamento de dados inválidos.

---

## Fase 4 — Lógica de Execução dos Treinos

Objetivo: implementar a máquina de estados de cada modalidade de treino (sem UI).

- [ ] **Classe abstrata `DrillSession`** — base para execução de qualquer treino.
    - [ ] Atributos: `config`, `elapsed_time`, `is_running`, `is_paused`.
    - [ ] Métodos: `start()`, `pause()`, `resume()`, `stop()`.
    - [ ] Método abstrato `tick()` — chamado a cada ciclo do timer.
    - [ ] Callback `on_event(event_type, data)` — para a UI reagir a eventos.
- [ ] **Classe `RoundTimerSession(DrillSession)`** — implementa lógica de rounds.
    - [ ] Controle de round atual, tempo restante de trabalho/descanso.
    - [ ] Emite eventos: `ROUND_START`, `ROUND_WARNING`, `ROUND_END`, `SESSION_END`.
- [ ] **Classe `TimingDrillSession(DrillSession)`** — implementa estímulo aleatório.
    - [ ] Gera próximo instante de estímulo aleatório dentro do intervalo configurado.
    - [ ] Emite eventos: `STIMULUS`, `SESSION_END`.
- [ ] **Classe `ComboDrillSession(DrillSession)`** — implementa chamadas de combo.
    - [ ] Modo sequencial: iteração cíclica (**RN02**).
    - [ ] Modo aleatório: sem repetição consecutiva (**RN02**).
    - [ ] Emite eventos: `COMBO_CALL(combo)`, `SESSION_END`.
- [ ] **Classe `FootworkDrillSession(DrillSession)`** — implementa chamadas de movimentação.
    - [ ] Escolha aleatória entre movimentações selecionadas.
    - [ ] Emite eventos: `MOVE_CALL(move)`, `SESSION_END`.
- [ ] **Classe `DrillTimer`** — wrapper de `setInterval`/`requestAnimationFrame` para chamar `tick()` com precisão (**RNF01**).
- [ ] Testes unitários para lógica de cada sessão (simulação de ticks).

---

## Fase 5 — Interface do Usuário (HTML + PyScript)

Objetivo: construir as telas da aplicação, conectando UI às classes de domínio e sessão.

- [ ] **Estrutura base HTML** — `index.html` com carregamento do PyScript, layout responsivo (**RNF05**), navegação entre telas.
- [ ] **Classe `Router`** — gerencia navegação SPA (single-page) entre telas via hash ou estado interno.
- [ ] **Classe abstrata `Page`** — base para cada tela da aplicação.
    - [ ] Métodos: `render()`, `bind_events()`, `destroy()`.
- [ ] **`HomePage(Page)`** — tela inicial com acesso às modalidades e ao calendário.
- [ ] **`RoundTimerPage(Page)`** — formulário de configuração + tela de execução do Round Timer (**RF01**).
    - [ ] Exibe timer com contagem regressiva, round atual, status (trabalho/descanso).
    - [ ] Botões: iniciar, pausar, parar.
    - [ ] Integração com `RoundTimerSession` e `AudioEngine`.
- [ ] **`TimingDrillPage(Page)`** — formulário de configuração + tela de execução do Timing Drill (**RF02**).
    - [ ] Exibe timer, estímulo visual acompanhando o sonoro.
    - [ ] Integração com `TimingDrillSession`, `AudioEngine` e `Announcer`.
- [ ] **`ComboDrillPage(Page)`** — formulário de configuração + tela de execução do Combo Drill (**RF03**).
    - [ ] Exibe combo atual sendo chamado.
    - [ ] Integração com `ComboDrillSession`, `AudioEngine` e `Announcer`.
- [ ] **`FootworkDrillPage(Page)`** — formulário de configuração + tela de execução do Footwork Drill (**RF04**).
    - [ ] Exibe movimentação atual sendo chamada.
    - [ ] Integração com `FootworkDrillSession`, `AudioEngine` e `Announcer`.
- [ ] **`ComboLibraryPage(Page)`** — CRUD de combos (**RF06**).
    - [ ] Listagem, formulário de criação/edição, exclusão com confirmação.
- [ ] **`FootworkMovePage(Page)`** — CRUD de movimentações (**RF07**).
    - [ ] Listagem, formulário de criação/edição, exclusão com confirmação.
- [ ] **`CustomWorkoutPage(Page)`** — CRUD de treinos personalizados (**RF05**).
    - [ ] Listagem, formulário de criação/edição, exclusão com confirmação.
- [ ] Persistência automática via `AppState.save()` após cada operação CRUD (**RF11**).
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
