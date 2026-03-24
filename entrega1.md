---
title: "Especificação de Requisitos de Software"
subtitle: "FightDrill — Plataforma Web de Treinamento para Artes Marciais"
author:
    - "Pedro Artur de Aguiar Cabral"
    - "Ruy Agostinho Otoni Vieira Neto"
    - "Vitor Pedrosa Brito dos Santos"
date: "Março de 2025"
lang: "pt-BR"

# Bib
# bibliography: references.bib
link-citations: true
citeproc: true

# Para criar capa exclusiva
titlepage: true

geometry:
    - a4paper
    - margin=2.5cm

toc: true
toc-depth: 3

numbersections: true

fontsize: 12pt
mainfont: "Latin Modern Roman"

# Para PDF via xelatex ou lualatex
papersize: a4
indent: true

# Metadados adicionais
documentclass: report
header-includes:
    - \usepackage{setspace}
    - \onehalfspacing
---

# Introdução

## Propósito

Este documento descreve os requisitos de software do sistema **FightDrill**, uma plataforma web voltada ao apoio de treinos de artes marciais e esportes de combate. O objetivo é especificar de forma clara e rastreável as funcionalidades, restrições e regras de negócio que guiarão o desenvolvimento do sistema ao longo do semestre.

## Escopo

O **FightDrill** é uma aplicação web que oferece diferentes modalidades de treino assistido por computador para praticantes de artes marciais e esportes de combate. O sistema fornece estímulos sonoros, controla tempos de trabalho e descanso, e gerencia combinações de técnicas e movimentações, permitindo que o usuário conduza sessões de treino de forma autônoma, sem a necessidade de um parceiro de treinamento.

O sistema permite ainda a criação de um calendário semanal de treinos, exportável como URL compartilhável. Não há cadastro de usuários, autenticação ou banco de dados — toda persistência é feita via `localStorage` do navegador, e o compartilhamento ocorre por codificação de dados na própria URL.

O sistema será desenvolvido em **Python com PyScript** (execução de Python no navegador via WebAssembly) e HTML, sem necessidade de servidor de aplicação em produção.

## Definições, Acrônimos e Abreviações

| Termo          | Definição                                                                         |
| -------------- | --------------------------------------------------------------------------------- |
| RF             | Requisito Funcional                                                               |
| RN             | Regra de Negócio                                                                  |
| Round          | Período de trabalho contínuo em treinos de combate                                |
| Combo          | Sequência nomeada de técnicas de ataque ou defesa                                 |
| Footwork       | Movimentação de pés e deslocamento corporal                                       |
| Timing Drill   | Modalidade de treino baseada em reação a estímulo sonoro em intervalo aleatório   |
| Combo Drill    | Modalidade de treino baseada em execução de combos anunciados pelo sistema        |
| Footwork Drill | Modalidade de treino baseada em execução de movimentações anunciadas pelo sistema |
| Round Timer    | Modalidade de treino baseada em controle de rounds com trabalho e descanso        |
| localStorage   | Mecanismo de armazenamento de dados no navegador do usuário, sem servidor         |
| PyScript       | Framework que permite executar código Python no navegador via WebAssembly         |

## Visão Geral do Documento

O restante deste documento está organizado da seguinte forma:

- O capítulo **Descrição Geral do Produto** apresenta o contexto, funções principais, perfil de usuário e restrições.
- O capítulo **Requisitos** detalha os requisitos funcionais e as regras de negócio.
- O capítulo **Matriz de Rastreabilidade RN x RF** apresenta o cruzamento entre regras de negócio e requisitos funcionais.

# Descrição Geral do Produto

## Perspectiva do Produto

O FightDrill é um produto independente, sem dependência de sistemas externos. Ele é acessado inteiramente pelo navegador web e não requer instalação, cadastro ou conexão com servidor de backend. Toda a lógica de execução reside no cliente (navegador), viabilizada pelo PyScript.

O sistema se posiciona como uma ferramenta de apoio ao treino individual, complementando a orientação de um técnico ou professor. Não substitui a supervisão humana, mas oferece estímulos, controle de tempo e organização de sessões de forma autônoma.

## Funções do Produto

O sistema oferece as seguintes funções principais:

- **Modalidades de treino:** Round Timer, Timing Drill, Combo Drill e Footwork Drill, cada uma com configurações específicas e execução com estímulos sonoros.
- **Treino personalizado:** cadastro de treinos sugeridos pelo técnico, com nome, duração e descrição livre.
- **Gerenciamento de combos:** criação, edição e exclusão de combos nomeados com sequências de técnicas descritas em texto livre.
- **Gerenciamento de movimentações:** definição da lista de opções de footwork disponíveis para uso no Footwork Drill.
- **Calendário semanal:** montagem de um calendário com treinos atribuídos a dias da semana.
- **Exportação e importação via URL:** o calendário configurado pode ser codificado em uma URL compartilhável; ao acessar a URL, o sistema carrega e exibe o calendário exportado.
- **Persistência local:** todas as configurações são salvas automaticamente no `localStorage` do navegador.

## Características dos Usuários

O sistema é destinado a um único perfil de usuário:

**Praticante de artes marciais ou esportes de combate** — pessoa que realiza treinos de forma autônoma ou semiorientada por um técnico. Não é necessário conhecimento técnico de informática além do uso básico de navegador web. O usuário pode ser iniciante ou avançado na modalidade esportiva; o sistema não distingue níveis.

## Restrições

- O sistema deve funcionar inteiramente no navegador, sem backend ou banco de dados.
- A implementação deve ser feita em Python (via PyScript) e HTML.
- Não haverá sistema de autenticação ou cadastro de usuários.
- A reprodução de áudio depende do suporte do navegador à Web Audio API — navegadores modernos (Chrome, Firefox, Edge) são suportados.
- O armazenamento de dados depende do `localStorage` do navegador; dados são perdidos caso o usuário limpe o armazenamento do navegador.
- O sistema deve ser responsivo o suficiente para uso em telas de desktop e tablet.

## Suposições e Dependências

- O usuário dispõe de um navegador moderno com suporte a WebAssembly e Web Audio API.
- O PyScript é carregado via CDN no momento do acesso à aplicação; portanto, é necessária conexão com a internet no primeiro carregamento.
- Assume-se que o usuário realizará os exercícios físicos em paralelo ao uso da aplicação (o sistema fornece estímulos, não valida execução física).

# Requisitos

## Requisitos Funcionais

**RF01 — Configurar e executar Round Timer**

O sistema deve permitir que o usuário configure e execute um treino do tipo Round Timer. As configurações incluem: número de rounds, duração do período de trabalho por round, duração do período de descanso entre rounds e tempo de aviso sonoro antes do fim de cada round. Durante a execução, o sistema deve emitir sinais sonoros distintos para: início de round, aviso de fim de round e fim de round / início de descanso.

**RF02 — Configurar e executar Timing Drill**

O sistema deve permitir que o usuário configure e execute um treino do tipo Timing Drill. As configurações incluem: duração total do treino, intervalo mínimo entre estímulos, intervalo máximo entre estímulos e técnica-alvo (texto livre, ex.: "jab", "teep"). Durante a execução, o sistema deve emitir um sinal sonoro em um momento aleatório dentro do intervalo configurado, indicando que o usuário deve executar a técnica-alvo.

**RF03 — Configurar e executar Combo Drill**

O sistema deve permitir que o usuário configure e execute um treino do tipo Combo Drill. As configurações incluem: seleção dos combos da biblioteca a serem utilizados, modo de chamada (sequencial ou aleatório), intervalo entre chamadas e duração total do treino. Durante a execução, o sistema deve anunciar sonoramente o nome do combo a ser executado.

**RF04 — Configurar e executar Footwork Drill**

O sistema deve permitir que o usuário configure e execute um treino do tipo Footwork Drill. As configurações incluem: seleção das opções de movimentação a serem utilizadas no drill, intervalo mínimo e máximo entre estímulos e duração total do treino. Durante a execução, o sistema deve anunciar sonoramente a movimentação a ser executada, escolhida aleatoriamente entre as opções selecionadas.

**RF05 — Cadastrar treino personalizado**

O sistema deve permitir que o usuário cadastre treinos personalizados, tipicamente sugeridos por um técnico. Cada treino personalizado deve conter: nome, duração estimada e descrição livre (texto com instruções, observações ou sequências de exercícios). Treinos personalizados devem ser listados e acessíveis na interface.

**RF06 — Gerenciar biblioteca de combos**

O sistema deve permitir que o usuário crie, edite e exclua combos na biblioteca de combos. Cada combo deve conter: nome (ex.: "Combo 1") e descrição em texto livre da sequência de técnicas (ex.: "jab, jab, cross, gancho"). Os combos cadastrados ficam disponíveis para seleção no Combo Drill.

**RF07 — Gerenciar lista de movimentações (footwork)**

O sistema deve permitir que o usuário gerencie a lista de opções de movimentação disponíveis para o Footwork Drill. O usuário pode adicionar, editar e excluir opções de movimentação (ex.: "passo lateral direito", "recuo", "pivô esquerdo"). As opções cadastradas ficam disponíveis para seleção na configuração do Footwork Drill.

**RF08 — Construir calendário semanal de treinos**

O sistema deve permitir que o usuário monte um calendário semanal, atribuindo um ou mais treinos (de qualquer modalidade cadastrada) a cada dia da semana (segunda a domingo). O calendário deve ser visualizado de forma clara, com os treinos de cada dia listados.

**RF09 — Exportar calendário como URL compartilhável**

O sistema deve permitir que o usuário exporte o calendário semanal atual como uma URL. A URL deve conter, de forma codificada, todas as informações do calendário e dos treinos nele contidos. A URL gerada deve ser exibida ao usuário para cópia e compartilhamento.

**RF10 — Importar calendário a partir de URL**

O sistema deve permitir que o usuário importe um calendário a partir de uma URL exportada. Ao acessar a URL ou colá-la em campo específico, o sistema deve decodificar os dados e substituir o calendário atual armazenado no `localStorage` pelo calendário importado.

**RF11 — Persistir configurações no localStorage**

O sistema deve salvar automaticamente no `localStorage` do navegador todas as configurações do usuário, incluindo: combos cadastrados, movimentações cadastradas, treinos personalizados e o calendário semanal. As configurações devem ser restauradas automaticamente ao reabrir a aplicação.

**RF12 — Reproduzir sinais sonoros durante treinos**

O sistema deve reproduzir sinais sonoros via Web Audio API durante a execução de qualquer modalidade de treino ativa. Os sinais sonoros devem ser distintos para diferentes eventos (ex.: início, alerta, fim), e a reprodução deve ocorrer sem necessidade de arquivos de áudio externos.

**RF13 — Contagem regressiva antes do início de treino**

O sistema deve exibir uma contagem regressiva de 3 segundos (3… 2… 1…) antes de iniciar a execução efetiva de qualquer modalidade de treino (Round Timer, Timing Drill, Combo Drill e Footwork Drill). Durante a contagem, o display do timer deve mostrar o número restante e uma indicação visual de preparação. A sessão de treino só deve começar após a conclusão da contagem regressiva, permitindo que o usuário se posicione antes do início dos estímulos.

## Requisitos Não Funcionais

**RNF01 — Precisão dos temporizadores**

Os temporizadores utilizados nas modalidades de treino devem apresentar desvio máximo de 500 milissegundos em relação ao tempo configurado. A precisão é crítica para modalidades como Timing Drill, onde a imprevisibilidade do estímulo é parte essencial do exercício.

**RNF02 — Latência do sinal sonoro**

O intervalo entre o disparo interno do estímulo e a reprodução efetiva do sinal sonoro pelo navegador não deve exceder 100 milissegundos, garantindo que o áudio seja percebido como imediato pelo usuário durante a execução do treino.

**RNF03 — Compatibilidade com navegadores modernos**

O sistema deve funcionar corretamente nas versões estáveis mais recentes dos navegadores Google Chrome, Mozilla Firefox e Microsoft Edge. Não há requisito de suporte a versões legadas ou ao Internet Explorer.

**RNF04 — Usabilidade sem treinamento prévio**

Um usuário com familiaridade básica com navegadores web deve ser capaz de configurar e iniciar qualquer modalidade de treino sem consultar documentação externa. A interface deve apresentar rótulos, descrições e feedback visual suficientes para guiar o uso intuitivo do sistema.

**RNF05 — Responsividade de layout**

A interface deve ser utilizável em telas com largura mínima de 768 pixels (tablet em modo paisagem) e em monitores de desktop padrão (1280 pixels ou mais). O layout deve se adaptar sem quebra de conteúdo ou perda de funcionalidade.

**RNF06 — Tempo de carregamento inicial**

O sistema deve estar pronto para uso em até 15 segundos após o carregamento da página em uma conexão de banda larga padrão (10 Mbps ou superior), considerando o tempo de inicialização do PyScript via CDN.

**RNF07 — Integridade dos dados persistidos**

Ao restaurar configurações do `localStorage`, o sistema deve validar a estrutura dos dados antes de utilizá-los. Caso os dados estejam corrompidos ou em formato inválido, o sistema deve inicializar com estado padrão e notificar o usuário, sem lançar erros não tratados.

## Regras de Negócio

**RN01 — Validação de intervalo no Timing Drill e Footwork Drill**

O intervalo mínimo entre estímulos deve ser estritamente menor que o intervalo máximo. O sistema deve impedir a execução do treino e exibir mensagem de erro caso esta condição não seja satisfeita.

_Aplica-se a:_ RF02, RF04

**RN02 — Comportamento do modo de chamada no Combo Drill**

No modo **sequencial**, os combos selecionados devem ser chamados em ordem cíclica, retornando ao primeiro combo após o último ser chamado. No modo **aleatório**, o sistema não pode chamar o mesmo combo em duas chamadas consecutivas, desde que haja mais de um combo selecionado.

_Aplica-se a:_ RF03

**RN03 — Codificação e substituição na exportação/importação de calendário**

A exportação do calendário deve codificar toda a estrutura de dados (dias, treinos e suas configurações) em formato JSON codificado em Base64, embutido como parâmetro de URL. A importação deve decodificar este parâmetro e **substituir integralmente** o calendário atual no `localStorage`, após confirmação do usuário.

_Aplica-se a:_ RF09, RF10

**RN04 — Requisitos mínimos para salvar treino personalizado**

Um treino personalizado só pode ser salvo se possuir, no mínimo, um nome não vazio e uma duração estimada maior que zero. O campo de descrição é opcional.

_Aplica-se a:_ RF05

**RN05 — Requisito mínimo para iniciar Footwork Drill**

O Footwork Drill não pode ser iniciado sem que ao menos uma opção de movimentação esteja selecionada na configuração do treino. O sistema deve impedir o início e exibir mensagem orientativa caso nenhuma opção esteja selecionada.

_Aplica-se a:_ RF04

**RN06 — Identificação do movimento pelos sinais sonoros**

Os sinais sonoros emitidos durante a execução de um treino devem permitir que o usuário identifique inequivocamente qual movimento deve ser executado. Em modalidades com múltiplos movimentos ou combos configurados, cada estímulo deve ser acompanhado de anúncio sonoro do nome do movimento ou combo correspondente, de forma que o usuário não precise consultar a tela para saber o que executar.

_Aplica-se a:_ RF01, RF02, RF03, RF04

# Matriz de Rastreabilidade RN x RF

|          | RF01 | RF02 | RF03 | RF04 | RF05 | RF06 | RF07 | RF08 | RF09 | RF10 | RF11 | RF12 | RF13 |
| -------- | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| **RN01** |      |  X   |      |  X   |      |      |      |      |      |      |      |      |      |
| **RN02** |      |      |  X   |      |      |      |      |      |      |      |      |      |      |
| **RN03** |      |      |      |      |      |      |      |      |  X   |  X   |      |      |      |
| **RN04** |      |      |      |      |  X   |      |      |      |      |      |      |      |      |
| **RN05** |      |      |      |  X   |      |      |      |      |      |      |      |      |      |
| **RN06** |  X   |  X   |  X   |  X   |      |      |      |      |      |      |      |      |      |
