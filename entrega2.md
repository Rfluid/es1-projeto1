---
title: "Especificação de Projeto — Entrega Intermediária"
subtitle: "FightDrill — Plataforma Web de Treinamento para Artes Marciais"
author:
    - "Pedro Artur de Aguiar Cabral"
    - "Ruy Agostinho Otoni Vieira Neto"
    - "Vitor Pedrosa Brito dos Santos"
date: "Abril de 2025"
lang: "pt-BR"

titlepage: true

geometry:
    - a4paper
    - margin=2.5cm

toc: true
toc-depth: 3

numbersections: true

fontsize: 12pt
mainfont: "Latin Modern Roman"

papersize: a4
indent: true

documentclass: report
header-includes:
    - \usepackage{setspace}
    - \onehalfspacing
---

# Diagrama de Casos de Uso

## Ator

O sistema possui um único ator: **Praticante**, pessoa que acessa a aplicação pelo navegador para configurar e executar sessões de treino.

## Casos de Uso

A tabela abaixo lista todos os casos de uso identificados, com breve descrição e o ator envolvido.

| Identificador | Nome                           | Descrição resumida                                                                                      | Ator       |
| ------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------- | ---------- |
| UC01          | Executar Round Timer           | Configurar e executar treino com rounds de trabalho e descanso com beeps sonoros distintos              | Praticante |
| UC02          | Executar Timing Drill          | Configurar e executar treino de reação a estímulo sonoro e anúncio de voz em intervalo aleatório        | Praticante |
| UC03          | Executar Combo Drill           | Configurar e executar treino com anúncio por voz sintetizada de combos em modo sequencial ou aleatório  | Praticante |
| UC04          | Executar Footwork Drill        | Configurar e executar treino com anúncio por voz sintetizada de movimentações escolhidas aleatoriamente | Praticante |
| UC05          | Gerenciar Combos               | Listar, criar, editar e excluir combos na biblioteca de combos                                          | Praticante |
| UC06          | Gerenciar Movimentações        | Criar, editar e excluir opções de movimentação disponíveis para o Footwork Drill                        | Praticante |
| UC07          | Cadastrar Treino Personalizado | Criar, visualizar e excluir treinos personalizados com nome, duração e descrição livre                  | Praticante |
| UC08          | Exportar Biblioteca como URL   | Codificar biblioteca de dados (combos, movimentações, treinos) em Base64 e gerar URL compartilhável     | Praticante |
| UC09          | Importar Biblioteca de URL     | Decodificar biblioteca de dados a partir de URL e substituir os dados atuais após confirmação           | Praticante |

## Relações entre Casos de Uso

Os casos de uso UC01, UC02, UC03 e UC04 incluem (\<\<include\>\>) o comportamento de **reprodução de sinais sonoros** (correspondente a RF11) e de **pausa e retomada** (RF10). Esses comportamentos são transversais a todas as modalidades de treino e dependem de funcionalidade comum do sistema.

Os casos de uso UC03 e UC04 estendem (\<\<extend\>\>) o comportamento de gerenciamento de biblioteca: UC03 pressupõe combos cadastrados via UC05, e UC04 pressupõe movimentações cadastradas via UC06.

UC09 opera sobre dados previamente exportados por UC08.

## Rastreabilidade UC × RF × RN

| UC   | Requisitos Funcionais  | Regras de Negócio      |
| ---- | ---------------------- | ---------------------- |
| UC01 | RF01, RF10, RF11       | RN06                   |
| UC02 | RF02, RF10, RF11       | RN06                   |
| UC03 | RF03, RF09, RF10, RF11 | RN01, RN02, RN03, RN06 |
| UC04 | RF04, RF10, RF11       | RN05, RN06             |
| UC05 | RF06                   |                        |
| UC06 | RF08                   |                        |
| UC07 | RF05                   | RN04                   |
| UC08 | RF13                   | RN07                   |
| UC09 | RF14                   | RN07                   |

# Diagrama de Classes

## Classes de Domínio

Esta seção descreve as classes de domínio do sistema, seus atributos e relacionamentos. As classes representam os conceitos centrais da aplicação, independentemente de camadas de interface ou persistência.

### `Combo`

Representa uma sequência nomeada de técnicas de ataque ou defesa.

| Atributo   | Tipo  | Descrição                                                       |
| ---------- | ----- | --------------------------------------------------------------- |
| `name`     | `str` | Nome identificador do combo (não pode ser vazio)                |
| `sequence` | `str` | Descrição em texto livre das técnicas (ex.: "jab, cross, hook") |

### `FootworkMove`

Representa uma opção de movimentação disponível para o Footwork Drill.

| Atributo | Tipo  | Descrição                                           |
| -------- | ----- | --------------------------------------------------- |
| `name`   | `str` | Nome da movimentação (ex.: "passo lateral direito") |

### `CustomWorkout`

Representa um treino personalizado sugerido pelo técnico.

| Atributo      | Tipo  | Descrição                                             |
| ------------- | ----- | ----------------------------------------------------- |
| `name`        | `str` | Nome do treino (não pode ser vazio)                   |
| `duration`    | `int` | Duração estimada em minutos (deve ser maior que zero) |
| `description` | `str` | Descrição livre com instruções ou observações         |

### `CallMode` (enumeração)

Modo de chamada utilizado no Combo Drill.

| Valor        | Descrição                                                 |
| ------------ | --------------------------------------------------------- |
| `SEQUENTIAL` | Combos chamados em ordem cíclica                          |
| `RANDOM`     | Combos chamados aleatoriamente, sem repetição consecutiva |

### `DrillConfig` (abstrata)

Classe base abstrata para configurações de modalidades de treino.

Sem atributos próprios; define a interface comum para todas as configurações.

#### `RoundTimerConfig`

Configuração do treino do tipo Round Timer.

| Atributo        | Tipo  | Descrição                                              |
| --------------- | ----- | ------------------------------------------------------ |
| `num_rounds`    | `int` | Número de rounds                                       |
| `work_duration` | `int` | Duração do período de trabalho por round (segundos)    |
| `rest_duration` | `int` | Duração do período de descanso entre rounds (segundos) |
| `warning_time`  | `int` | Antecedência do aviso sonoro antes do fim do round (s) |

#### `TimingDrillConfig`

Configuração do treino do tipo Timing Drill.

| Atributo           | Tipo  | Descrição                                    |
| ------------------ | ----- | -------------------------------------------- |
| `total_duration`   | `int` | Duração total do treino (segundos)           |
| `min_interval`     | `int` | Intervalo mínimo entre estímulos (segundos)  |
| `max_interval`     | `int` | Intervalo máximo entre estímulos (segundos)  |
| `target_technique` | `str` | Técnica-alvo a ser executada pelo praticante |

#### `ComboDrillConfig`

Configuração do treino do tipo Combo Drill.

| Atributo    | Tipo          | Descrição                                     |
| ----------- | ------------- | --------------------------------------------- |
| `combos`    | `list[Combo]` | Combos selecionados para uso no treino        |
| `call_mode` | `CallMode`    | Modo de chamada: sequencial ou aleatório      |
| `interval`  | `int`         | Intervalo entre chamadas de combos (segundos) |
| `duration`  | `int`         | Duração total do treino (segundos)            |

#### `FootworkDrillConfig`

Configuração do treino do tipo Footwork Drill.

| Atributo       | Tipo                 | Descrição                                     |
| -------------- | -------------------- | --------------------------------------------- |
| `moves`        | `list[FootworkMove]` | Movimentações selecionadas para uso no treino |
| `min_interval` | `int`                | Intervalo mínimo entre estímulos (segundos)   |
| `max_interval` | `int`                | Intervalo máximo entre estímulos (segundos)   |
| `duration`     | `int`                | Duração total do treino (segundos)            |

### `ComboLibrary`

Coleção gerenciável de combos cadastrados pelo usuário.

| Atributo | Tipo          | Descrição                   |
| -------- | ------------- | --------------------------- |
| `combos` | `list[Combo]` | Lista de combos cadastrados |

### `FootworkMoveLibrary`

Coleção gerenciável de movimentações cadastradas pelo usuário.

| Atributo | Tipo                 | Descrição                          |
| -------- | -------------------- | ---------------------------------- |
| `moves`  | `list[FootworkMove]` | Lista de movimentações cadastradas |

### `CustomWorkoutLibrary`

Coleção gerenciável de treinos personalizados cadastrados pelo usuário.

| Atributo   | Tipo                  | Descrição                                   |
| ---------- | --------------------- | ------------------------------------------- |
| `workouts` | `list[CustomWorkout]` | Lista de treinos personalizados cadastrados |

## Relacionamentos

- `DrillConfig` é especializada por `RoundTimerConfig`, `TimingDrillConfig`, `ComboDrillConfig` e `FootworkDrillConfig` (herança).
- `ComboDrillConfig` agrega `Combo` (0..\*).
- `FootworkDrillConfig` agrega `FootworkMove` (0..\*).
- `ComboLibrary` compõe `Combo` (0..\*).
- `FootworkMoveLibrary` compõe `FootworkMove` (0..\*).
- `CustomWorkoutLibrary` compõe `CustomWorkout` (0..\*).
- `CallMode` é referenciada por `ComboDrillConfig`.

# Implementação de Casos de Uso por Membro

Cada membro do grupo é responsável pela especificação detalhada de um caso de uso no Enterprise Architect, incluindo diagrama de atividades e diagrama de sequência.

| Membro                          | Caso de Uso                           |
| ------------------------------- | ------------------------------------- |
| Pedro Artur de Aguiar Cabral    | UC01 — Executar Round Timer           |
| Vitor Pedrosa Brito dos Santos  | UC03 — Executar Combo Drill           |
| Ruy Agostinho Otoni Vieira Neto | UC07 — Cadastrar Treino Personalizado |

## UC01 — Executar Round Timer (Pedro)

### Descrição

Permite ao praticante configurar e executar um treino do tipo Round Timer, com controle automático de rounds, períodos de trabalho e descanso, e beeps sonoros distintos para cada evento.

### Fluxo Principal — Executar Round Timer

1. O praticante acessa a tela do Round Timer.
2. O sistema exibe o formulário de configuração com os campos: número de rounds, duração do trabalho, duração do descanso e tempo de aviso antes do fim do round.
3. O praticante preenche os valores e aciona o início.
4. O sistema exibe a contagem regressiva de 3 segundos (3… 2… 1…) antes do início efetivo.
5. O sistema inicia o primeiro round: exibe o contador decrescente e emite beep de início de round (frequência alta, curto).
6. Quando o tempo de aviso é atingido, o sistema emite beep de alerta (frequência média, dois pulsos).
7. Ao fim do round, o sistema emite beep de fim de round (frequência baixa, longo) e inicia o período de descanso com contador próprio.
8. Ao fim do descanso, o sistema inicia o próximo round (retorna ao passo 5).
9. Após o último round, o sistema emite sinal de encerramento e exibe mensagem de conclusão.

### Fluxo Alternativo — Pausar e retomar (passo 5–8)

A. O praticante aciona pausa durante qualquer fase (trabalho ou descanso).
B. O sistema suspende o contador e os beeps (RF10).
C. O praticante aciona retomada.
D. O sistema reinicia o contador do ponto em que foi pausado e continua a execução.

### Fluxo Alternativo — Encerramento antecipado

A. O praticante aciona o botão de encerrar a qualquer momento.
B. O sistema interrompe a execução, emite sinal de encerramento e retorna à tela de configuração.

### Pré-condições

Nenhuma.

### Pós-condições

A sessão de Round Timer é concluída (ou encerrada antecipadamente) e o sistema retorna ao estado de configuração.

### Requisitos Relacionados

RF01, RF10, RF11, RN06.

---

## UC03 — Executar Combo Drill (Vitor)

### Descrição

Permite ao praticante configurar e executar um treino do tipo Combo Drill, com anúncio por voz sintetizada dos combos selecionados em modo sequencial ou aleatório.

### Fluxo Principal — Executar Combo Drill

1. O praticante acessa a tela do Combo Drill.
2. O sistema exibe o formulário de configuração com os campos: seleção de combos da biblioteca (máximo 4, conforme RN01), modo de chamada (sequencial ou aleatório, conforme RF09), intervalo entre chamadas e duração total do treino.
3. O praticante seleciona os combos, define o modo e os demais parâmetros, e aciona o início.
4. O sistema exibe a contagem regressiva de 3 segundos (3… 2… 1…) antes do início efetivo.
5. O sistema inicia a sessão e aguarda o intervalo configurado.
6. Ao término do intervalo, o sistema anuncia por voz sintetizada (Speech Synthesis API) o nome do próximo combo (conforme RN06).
7. Se o modo for sequencial: o sistema chama os combos em ordem cíclica (RN02).
8. Se o modo for aleatório: o sistema escolhe o próximo combo sem repetir o anterior (RN03).
9. O sistema repete os passos 5–8 até esgotar a duração total configurada.
10. O sistema emite sinal sonoro de encerramento e exibe mensagem de conclusão.

### Fluxo Alternativo — Pausar e retomar (passos 5–9)

A. O praticante aciona pausa.
B. O sistema suspende o temporizador e os anúncios (RF10).
C. O praticante aciona retomada.
D. O sistema reinicia o temporizador do ponto pausado e continua a execução.

### Fluxo Alternativo — Nenhum combo selecionado

3a. O praticante não seleciona nenhum combo e tenta iniciar.
3b. O sistema exibe mensagem de erro indicando que é necessário selecionar ao menos um combo (decorrente de RN01).
3c. Retorna ao passo 2.

### Fluxo Alternativo — Encerramento antecipado

A. O praticante aciona o botão de encerrar a qualquer momento.
B. O sistema interrompe a execução e retorna à tela de configuração.

### Pré-condições

A biblioteca de combos deve conter ao menos um combo cadastrado (UC05).

### Pós-condições

A sessão de Combo Drill é concluída (ou encerrada antecipadamente) e o sistema retorna ao estado de configuração.

### Requisitos Relacionados

RF03, RF09, RF10, RF11, RN01, RN02, RN03, RN06.

---

## UC07 — Cadastrar Treino Personalizado (Ruy)

### Descrição

Permite ao praticante criar, visualizar e excluir treinos personalizados. Cada treino possui nome, duração estimada e descrição livre.

### Fluxo Principal — Criar Treino

1. O praticante acessa a tela de treinos personalizados.
2. O sistema exibe a lista de treinos cadastrados e um formulário de cadastro.
3. O praticante preenche o nome, a duração estimada e (opcionalmente) a descrição.
4. O praticante confirma o cadastro.
5. O sistema valida que o nome não está vazio e que a duração é maior que zero (RN04).
6. O sistema adiciona o treino à biblioteca e persiste no `localStorage` (RNF08).
7. O sistema atualiza a lista exibida com o novo treino.

### Fluxo Alternativo — Dados inválidos (passo 5)

5a. O nome está vazio ou a duração é zero ou negativa.
5b. O sistema exibe mensagem de erro indicando o campo inválido.
5c. O formulário permanece preenchido para correção.
5d. Retorna ao passo 3.

### Fluxo Alternativo — Excluir Treino

1. O praticante seleciona um treino da lista e aciona a exclusão.
2. O sistema remove o treino da biblioteca e persiste a alteração no `localStorage`.
3. O sistema atualiza a lista exibida.

### Pré-condições

Nenhuma.

### Pós-condições

O treino personalizado é adicionado (ou removido) da biblioteca e a alteração é persistida no `localStorage` (RNF08).

### Requisitos Relacionados

RF05, RNF08, RN04.
