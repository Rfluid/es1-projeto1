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

O sistema permite ainda a exportação da biblioteca de dados do usuário como URL compartilhável em Base64, possibilitando backup e compartilhamento de configurações entre dispositivos. Não há cadastro de usuários, autenticação ou banco de dados — toda persistência é feita via `localStorage` do navegador, e o compartilhamento ocorre por codificação de dados na própria URL.

O sistema será desenvolvido em **Python com PyScript** (execução de Python no navegador via WebAssembly) e HTML, sem necessidade de servidor de aplicação em produção.

## Definições, Acrônimos e Abreviações

| Termo                | Definição                                                                         |
| -------------------- | --------------------------------------------------------------------------------- |
| RF                   | Requisito Funcional                                                               |
| RN                   | Regra de Negócio                                                                  |
| RNF                  | Requisito Não Funcional                                                           |
| Round                | Período de trabalho contínuo em treinos de combate                                |
| Combo                | Sequência nomeada de técnicas de ataque ou defesa                                 |
| Footwork             | Movimentação de pés e deslocamento corporal                                       |
| Timing Drill         | Modalidade de treino baseada em reação a estímulo sonoro em intervalo aleatório   |
| Combo Drill          | Modalidade de treino baseada em execução de combos anunciados pelo sistema        |
| Footwork Drill       | Modalidade de treino baseada em execução de movimentações anunciadas pelo sistema |
| Round Timer          | Modalidade de treino baseada em controle de rounds com trabalho e descanso        |
| localStorage         | Mecanismo de armazenamento de dados no navegador do usuário, sem servidor         |
| PyScript             | Framework que permite executar código Python no navegador via WebAssembly         |
| Web Audio API        | API do navegador para síntese e reprodução de áudio sem arquivos externos         |
| Speech Synthesis API | API do navegador para síntese de voz a partir de texto (text-to-speech)           |

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

- **Modalidades de treino:** Round Timer, Timing Drill, Combo Drill e Footwork Drill, cada uma com configurações específicas e execução com estímulos sonoros e anúncios de voz sintetizada.
- **Controle de execução:** pausa e retomada de qualquer modalidade de treino em andamento; contagem regressiva de preparação antes do início.
- **Treino personalizado:** cadastro de treinos sugeridos pelo técnico, com nome, duração e descrição livre.
- **Gerenciamento de combos:** listagem, criação, edição e exclusão de combos nomeados com sequências de técnicas descritas em texto livre.
- **Gerenciamento de movimentações:** definição da lista de opções de footwork disponíveis para uso no Footwork Drill.
- **Controle de áudio:** ajuste de volume dos sinais sonoros e anúncios de voz, persistido entre sessões.
- **Exportação e importação via URL:** a biblioteca de dados do usuário (combos, movimentações e treinos personalizados) pode ser codificada em Base64 numa URL compartilhável; ao colar a URL, o sistema restaura os dados exportados.
- **Persistência local:** todas as configurações são salvas automaticamente no `localStorage` do navegador.
- **Internacionalização:** interface disponível em português (pt-BR) e inglês (en), com detecção automática pelo navegador.

## Características dos Usuários

O sistema é destinado a um único perfil de usuário:

**Praticante de artes marciais ou esportes de combate** — pessoa que realiza treinos de forma autônoma ou semiorientada por um técnico. Não é necessário conhecimento técnico de informática além do uso básico de navegador web. O usuário pode ser iniciante ou avançado na modalidade esportiva; o sistema não distingue níveis.

## Restrições

- O sistema deve funcionar inteiramente no navegador, sem backend ou banco de dados.
- A implementação deve ser feita inteiramente em Python (via PyScript e WebAssembly) e HTML; não é permitido uso de frameworks JavaScript para lógica de aplicação.
- Não haverá sistema de autenticação ou cadastro de usuários.
- A reprodução de áudio depende do suporte do navegador à Web Audio API e à Speech Synthesis API — navegadores modernos (Chrome, Firefox, Edge) são suportados.
- Não é permitido upload de arquivos de áudio próprios pelo usuário; todos os sons são gerados sinteticamente.
- O armazenamento de dados depende do `localStorage` do navegador; dados são perdidos caso o usuário limpe o armazenamento do navegador.
- O sistema deve ser responsivo o suficiente para uso em telas de desktop e tablet.

## Suposições e Dependências

- O usuário dispõe de um navegador moderno com suporte a WebAssembly, Web Audio API e Speech Synthesis API.
- O PyScript é carregado via CDN no momento do acesso à aplicação; portanto, é necessária conexão com a internet no primeiro carregamento.
- Assume-se que o usuário realizará os exercícios físicos em paralelo ao uso da aplicação (o sistema fornece estímulos, não valida execução física).

# Requisitos

## Requisitos Funcionais

**RF01 — Configurar e executar Round Timer**

O sistema deve permitir que o usuário configure e execute um treino do tipo Round Timer. As configurações incluem: número de rounds, duração do período de trabalho por round, duração do período de descanso entre rounds e tempo de aviso sonoro antes do fim de cada round. Durante a execução, o sistema deve emitir beeps sinteticamente distintos para: início de round, aviso de fim de round e fim de round / início de descanso.

**RF02 — Configurar e executar Timing Drill**

O sistema deve permitir que o usuário configure e execute um treino do tipo Timing Drill. As configurações incluem: duração total do treino, intervalo mínimo entre estímulos, intervalo máximo entre estímulos e técnica-alvo (texto livre, ex.: "jab", "teep"). Durante a execução, o sistema deve emitir um sinal sonoro e anunciar a técnica-alvo por voz sintetizada em um momento aleatório dentro do intervalo configurado.

**RF03 — Configurar e executar Combo Drill**

O sistema deve permitir que o usuário configure e execute um treino do tipo Combo Drill. As configurações incluem: seleção de até 4 combos da biblioteca (conforme RN01), intervalo entre chamadas e duração total do treino. O modo de chamada (sequencial ou aleatório) é configurado conforme RF09. Durante a execução, o sistema deve anunciar por voz sintetizada (Speech Synthesis API) o nome do combo a ser executado.

**RF04 — Configurar e executar Footwork Drill**

O sistema deve permitir que o usuário configure e execute um treino do tipo Footwork Drill. As configurações incluem: seleção das opções de movimentação a serem utilizadas (mínimo de uma, conforme RN05), intervalo mínimo e máximo entre estímulos e duração total do treino. Durante a execução, o sistema deve anunciar por voz sintetizada (Speech Synthesis API) a movimentação a ser executada, escolhida aleatoriamente entre as opções selecionadas.

**RF05 — Cadastrar treino personalizado**

O sistema deve permitir que o usuário cadastre treinos personalizados, tipicamente sugeridos por um técnico. Cada treino personalizado deve conter: nome, duração estimada e descrição livre (texto com instruções, observações ou sequências de exercícios). Treinos personalizados devem ser listados e acessíveis na interface.

**RF06 — Gerenciar biblioteca de combos**

O sistema deve permitir que o usuário liste, crie, edite e exclua combos na biblioteca de combos. A interface deve exibir a lista completa de combos cadastrados e permitir pesquisa por nome. Cada combo deve conter: nome (ex.: "Combo 1") e descrição em texto livre da sequência de técnicas (ex.: "jab, jab, cross, gancho"). Os combos cadastrados ficam disponíveis para seleção no Combo Drill.

**RF07 — Configurar intervalo de descanso entre sessões**

O sistema deve permitir que o usuário configure um intervalo de descanso a ser respeitado entre sessões consecutivas de treino. Durante esse intervalo, o sistema deve exibir contagem regressiva e impedir o início de nova sessão até sua conclusão.

**RF08 — Gerenciar lista de movimentações**

O sistema deve permitir que o usuário gerencie a lista de opções de movimentação disponíveis para o Footwork Drill. O usuário pode adicionar, editar e excluir opções de movimentação (ex.: "passo lateral direito", "recuo", "pivô esquerdo"). As opções cadastradas ficam disponíveis para seleção na configuração do Footwork Drill.

**RF09 — Configurar modo de execução do Combo Drill**

O sistema deve permitir ao usuário selecionar o modo de chamada dos combos no Combo Drill: **sequencial** (combos chamados em ordem cíclica, conforme RN02) ou **aleatório** (sem repetição consecutiva, conforme RN03). O modo selecionado deve ser aplicado durante toda a execução da sessão.

**RF10 — Pausar e retomar treino em execução**

O sistema deve permitir que o usuário pause e retome qualquer modalidade de treino em execução (Round Timer, Timing Drill, Combo Drill e Footwork Drill). Durante a pausa, os temporizadores devem ser suspensos e os estímulos sonoros interrompidos. Ao retomar, a sessão deve continuar a partir do estado em que foi pausada.

**RF11 — Reproduzir sinais sonoros durante treinos**

O sistema deve reproduzir sinais sonoros durante a execução de qualquer modalidade de treino ativa, sem necessidade de arquivos de áudio externos. Para eventos de temporização (Round Timer), os sinais devem ser beeps gerados via Web Audio API, distintos entre si pela frequência ou padrão de emissão. Para anúncios de movimentos e combos (Combo Drill, Footwork Drill e Timing Drill), o sistema deve usar a Speech Synthesis API para sintetizar o nome do movimento em voz.

**RF12 — Ajustar volume dos sinais sonoros**

O sistema deve permitir que o usuário ajuste o volume dos sinais sonoros e dos anúncios de voz emitidos durante os treinos. A configuração de volume deve ser persistida entre sessões (conforme RNF08).

**RF13 — Exportar biblioteca de dados como URL compartilhável**

O sistema deve permitir que o usuário exporte sua biblioteca de dados (combos cadastrados, movimentações cadastradas e treinos personalizados) como uma URL compartilhável. Os dados devem ser codificados em JSON e embutidos na URL em Base64. A URL gerada deve ser exibida ao usuário para cópia e compartilhamento.

**RF14 — Importar biblioteca de dados a partir de URL**

O sistema deve permitir que o usuário importe uma biblioteca de dados a partir de uma URL exportada. Ao colar a URL em campo específico, o sistema deve decodificar os dados e substituir a biblioteca atual no `localStorage`, após confirmação do usuário (conforme RN07).

## Requisitos Não Funcionais

**RNF01 — Internacionalização**

O sistema deve estar disponível em português (pt-BR) e inglês (en), com detecção automática do idioma pelo navegador. O usuário deve poder alternar manualmente entre os idiomas disponíveis pela interface.

**RNF02 — Implementação em Python**

Todo o sistema deve ser desenvolvido inteiramente em Python via PyScript (WebAssembly), com HTML para estrutura de página. Não é permitido o uso de frameworks JavaScript para lógica de aplicação.

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

**RNF08 — Persistência local de configurações**

O sistema deve salvar automaticamente no `localStorage` do navegador todas as configurações do usuário, incluindo: combos cadastrados, movimentações cadastradas, treinos personalizados e preferência de volume. As configurações devem ser restauradas automaticamente ao reabrir a aplicação.

## Regras de Negócio

**RN01 — Limite de combos selecionados no Combo Drill**

O Combo Drill aceita no máximo 4 combos selecionados por sessão de treino. O sistema deve impedir a seleção de mais de 4 combos e exibir mensagem informativa caso o usuário tente ultrapassar esse limite.

_Aplica-se a:_ RF03

**RN02 — Modo sequencial no Combo Drill**

No modo **sequencial**, os combos selecionados devem ser chamados em ordem cíclica, retornando ao primeiro combo após o último ser chamado.

_Aplica-se a:_ RF03, RF09

**RN03 — Modo aleatório no Combo Drill**

No modo **aleatório**, o sistema não pode chamar o mesmo combo em duas chamadas consecutivas, desde que haja mais de um combo selecionado.

_Aplica-se a:_ RF03, RF09

**RN04 — Requisitos mínimos para salvar treino personalizado**

Um treino personalizado só pode ser salvo se possuir, no mínimo, um nome não vazio e uma duração estimada maior que zero. O campo de descrição é opcional.

_Aplica-se a:_ RF05

**RN05 — Requisito mínimo para iniciar Footwork Drill**

O Footwork Drill não pode ser iniciado sem que ao menos uma opção de movimentação esteja selecionada na configuração do treino. O sistema deve impedir o início e exibir mensagem orientativa caso nenhuma opção esteja selecionada.

_Aplica-se a:_ RF04

**RN06 — Identificação de movimentos por voz sintetizada e beeps distintos**

Durante a execução de treinos com estímulos de movimento (Combo Drill, Footwork Drill e Timing Drill), cada estímulo deve ser acompanhado de anúncio em voz sintetizada pela Speech Synthesis API com o nome do movimento ou combo correspondente, permitindo que o usuário identifique o que executar sem consultar a tela. Para eventos de temporização do Round Timer (início de round, aviso de fim de round, fim de round / início de descanso), devem ser emitidos beeps sinteticamente distintos via Web Audio API, diferenciáveis entre si pela frequência ou padrão de emissão.

_Aplica-se a:_ RF01, RF02, RF03, RF04, RF11

**RN07 — Codificação e substituição na exportação/importação de dados via URL**

A exportação da biblioteca de dados deve codificar toda a estrutura (combos, movimentações e treinos personalizados) em formato JSON codificado em Base64, embutido como parâmetro de URL. A importação deve decodificar este parâmetro e **substituir integralmente** a biblioteca atual no `localStorage`, após confirmação do usuário.

_Aplica-se a:_ RF13, RF14

# Matriz de Rastreabilidade RN x RF

|          | RF01 | RF02 | RF03 | RF04 | RF05 | RF06 | RF07 | RF08 | RF09 | RF10 | RF11 | RF12 | RF13 | RF14 |
| -------- | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| **RN01** |      |      |  X   |      |      |      |      |      |      |      |      |      |      |      |
| **RN02** |      |      |  X   |      |      |      |      |      |  X   |      |      |      |      |      |
| **RN03** |      |      |  X   |      |      |      |      |      |  X   |      |      |      |      |      |
| **RN04** |      |      |      |      |  X   |      |      |      |      |      |      |      |      |      |
| **RN05** |      |      |      |  X   |      |      |      |      |      |      |      |      |      |      |
| **RN06** |  X   |  X   |  X   |  X   |      |      |      |      |      |      |  X   |      |      |      |
| **RN07** |      |      |      |      |      |      |      |      |      |      |      |      |  X   |  X   |
