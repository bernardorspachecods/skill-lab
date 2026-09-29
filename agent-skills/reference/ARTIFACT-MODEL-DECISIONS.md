# Modelo de artefactos — decisões

Registo conceptual; não altera as skills nem constitui um plano de execução.
Objetivo: automatizar identidade, localização, relações e manutenção dos
artefactos de planos, research e reviews.

## Princípios aprovados

- Reduzir custo do LLM preservando qualidade; o conteúdo continua a exigir julgamento.
- Automatizar criação, navegação e manutenção, com validação.
- Mesmo tipo segue o mesmo contrato no repositório; tipos diferentes podem ter campos e estruturas diferentes.
- Decidir uma questão de cada vez e registar apenas a regra vigente, sem transcrever a conversa.

## Decisões aprovadas

### D01 — Unidade e artefactos

**Regra:** cada entidade recebe um ID próprio, formado hierarquicamente com
segmentos separados por pontos. Os artefactos principais/intermédios usam o ID
da entidade seguido do papel em texto; quando há várias instâncias do mesmo
papel, o segmento inclui um ordinal. Podem ter responsável, estado e referências
próprios. Códigos de tipo e papéis canónicos de artefacto usam maiúsculas;
papéis descritivos de artefacto usam minúsculas. Os papéis deste modelo são
`PLAN`; `working` e `audit` para research; `assessment` e perspetivas numeradas
opcionais para review; e `RESULT` apenas para um deliverable autónomo requerido
pelo consumer. `KNOW` identifica a própria entrada de knowledge; `Outcome` é
uma secção do `PLAN`, não um artefacto. Cada review tem um `assessment` final; a
síntese é a operação de integrar perspetivas, não um artefacto obrigatório.

**Fundamento:** identificar cada ficheiro sem criar uma sequência independente
de IDs que esconda a sua pertença à unidade.

**Exemplo ilustrativo:**

```text
LR-01.REV-02                  review
LR-01.REV-02.perspective-01   perspetiva dessa review
LR-01.REV-02.assessment       avaliação final dessa review
```

### D02 — Continuidade de review

**Regra:** ajustar, completar ou verificar correções no âmbito da review mantém
o ID. Nova atribuição de review cria outro. Novos artefactos, perspetivas,
rondas ou alterações do alvo não obrigam, por si só, a outro ID. O coordenador
declara continuar um ID existente ou criar uma review; a ferramenta aplica.

**Fundamento:** a identidade acompanha a continuidade do trabalho, não a
quantidade de ficheiros ou a semelhança do tema. A declaração explícita evita
que o executor tenha de inferir qual das operações foi pedida.

**Exemplo:** «Confirma se os três problemas encontrados ficaram resolvidos»
continua `REV-02` quando assim atribuído pelo coordenador. «Faz uma nova
avaliação global desta implementação» abre outra review, por exemplo `REV-03`.

### D03 — Continuidade de research

**Regra:** aprofundar a pergunta, procurar evidência em falta ou verificar
fontes mantém o ID. Nova atribuição de pesquisa cria outro, mesmo sobre tema
semelhante. Mais queries, fontes ou artefactos não determinam nova identidade.
O coordenador declara continuar ou criar. Outra pesquisa pode enriquecer a
mesma entrada de knowledge.

**Fundamento:** a pesquisa pode exigir várias iterações para responder à sua
pergunta; essas iterações não devem fragmentar automaticamente a unidade.
A identidade da pesquisa é distinta da identidade da knowledge que alimenta.

**Exemplo:** verificar uma fonte em falta na comparação em curso continua
`RES-07`. Uma nova atribuição para estudar outro requisito abre `RES-08`,
podendo ambas contribuir para `KNOW-04`.

### D04 — Identidade e continuidade de knowledge

**Regra:** cada entrada de knowledge tem identidade própria. Corrigir,
aprofundar ou acrescentar evidência ao mesmo assunto e propósito de utilização
atualiza a entrada existente. Um propósito distinto, consultável separadamente,
justifica outra entrada. Antes de criar, procurar uma entrada que já sirva esse
propósito; uma nova atribuição de trabalho não implica nova knowledge. Quando
existe um `INDEX.md`, este orienta a descoberta e não é uma lista fechada das
entradas que podem ser consultadas. Uma descoberta útil pode ser reutilizada por
tarefas futuras.

**Fundamento:** knowledge é reutilizável entre pesquisas e tarefas. A sua
identidade acompanha o propósito de consulta, não a execução que a produziu.

**Exemplo:** acrescentar evidência a uma comparação de opções de autenticação
atualiza `KNOW-04`. Um guia para implementar a opção escolhida tem outro
propósito e recebe outra identidade, ligada à comparação.

### D05 — Delegação não cria identidade própria

**Regra:** não criar IDs de delegação neste modelo. Delegar ou mudar o agente
executor mantém a identidade da unidade e dos seus artefactos. A review avalia
o trabalho e os outputs dessa unidade, não o desempenho individual dos agentes.
Quando necessário, a responsabilidade atual de escrita é registada no contrato
de execução da tarefa, sem criar uma entidade `DEL-*` nem um histórico de
agentes no modelo partilhado. Numa transferência, o novo agente assume a mesma
unidade e os mesmos artefactos, com o estado do trabalho, os pontos por resolver
e a próxima ação; detalhes operacionais pertencem à skill proprietária.

**Fundamento:** distinguir execuções por agente não acrescenta valor ao objetivo
deste sistema. Uma interrupção não transforma trabalho parcial em concluído nem
exige outra identidade para continuar o trabalho existente.

**Exemplo:** se o agente B continuar o trabalho do agente A em `SP-03`, ambos
trabalham na mesma unidade; a review avalia o resultado de `SP-03`. Não se criam
`DEL-01` e `DEL-02` para distinguir os agentes.

### D06 — Proveniência obrigatória de knowledge

**Regra:** cada entrada de knowledge referencia explicitamente os artefactos
que lhe deram origem. Ao enriquecer a entrada, atualizar essas referências
para conservar a proveniência do conteúdo mantido. A ligação identifica os
artefactos concretos, não apenas a unidade de pesquisa ou o subplano. Quando
uma entrada local é promovida a knowledge global, promove-se também o material
de origem necessário para manter essa proveniência rastreável, sem dependência
do ciclo de vida do plano de origem. Os detalhes de IDs, localização e
duplicados pertencem ao [plano de promoção](PLAN_knowledge-promotion.md).

**Fundamento:** permitir ao agente chegar ao apoio da knowledge sem reconstruir
a sua origem por nomes, localização ou inferência. Pode haver vários artefactos
de origem; a regra não limita a proveniência a pesquisas.

**Exemplo:** `KNOW-04` referencia `RES-07.audit`; se outra pesquisa enriquecer a
entrada, referencia também `RES-08.audit` para o conteúdo proveniente desta.
Ao promover `KNOW-04`, os artefactos de origem necessários para sustentar essas
referências acompanham a promoção; o plano de origem pode ser apagado sem
quebrar o tracking da knowledge global.

### D07 — Alvos e critérios explícitos de review

**Regra:** o frontmatter da atribuição de cada review declara um ou vários
alvos concretos e os critérios pelos quais serão avaliados; ambos são
referências obrigatórias. Materiais de apoio podem ser referências opcionais e
não se tornam automaticamente alvos da avaliação.

**Fundamento:** associar uma review a um subplano não esclarece se avalia o
plano, a knowledge, a implementação ou o resultado. Alvos e critérios delimitam
a conclusão que o agente deve produzir.

**Exemplo:** `REV-02` avalia `SP-03.RESULT` segundo os requisitos e condições de
conclusão de `SP-03.PLAN`. Uma review de integração pode avaliar os resultados
de `SP-03` e `SP-04` segundo critérios de compatibilidade entre ambos.

### D08 — Frontmatter, corpo e fonte canónica

**Regra:** todos os ficheiros do modelo declaram no frontmatter as relações
relevantes que os ligam às respetivas unidades e aos artefactos relacionados.
Relações e campos necessários às ferramentas ficam no frontmatter do documento
que os possui. O corpo contém o conteúdo substantivo e apenas
instruções ou critérios adicionais que não estejam já nos metadados ou nas
fontes referenciadas. Não repetir alvos, relações ou critérios em prosa nem
criar secções sem informação própria. Dados comuns da unidade ficam no seu
documento de entrada; os artefactos associados não os duplicam.

**Fundamento:** permitir resolução automática e leitura focada, evitando
redundância e fontes concorrentes. Referenciar critérios existentes dispensa
reescrevê-los no corpo.

**Exemplo:** se o frontmatter de `REV-02` declara `targets` e `criteria_refs`,
não acrescentar «avaliar estes alvos segundo estes critérios» no corpo. Uma
exigência adicional de compatibilidade só aparece no corpo se não estiver já
nas referências; assessment, evidência e conclusões constituem o output da
review. Os nomes e contratos das secções próprias de cada workflow são
definidos pelas skills proprietárias, conforme D16; os campos de relação
partilhados seguem as decisões aplicáveis do modelo.

### D09 — Execução e review alternam sobre o mesmo alvo

**Regra:** a review só começa depois de o executor declarar a tarefa concluída.
Não fazer alterações ao alvo durante a avaliação. Se a review exigir correções,
retomar a execução; a nova verificação só começa depois de o executor concluir
essas correções. A continuação ou criação de review segue D02.

**Fundamento:** avaliar um trabalho entregue e estável, com uma fronteira clara
entre produção, avaliação e correção. Esta restrição aplica-se ao alvo avaliado,
não impede trabalho paralelo em unidades independentes.

**Exemplo:** concluir `SP-03.RESULT` → avaliar → corrigir → concluir correções
→ verificar novamente. Nunca corrigir o resultado enquanto está a ser avaliado.
O avaliador pode escrever os artefactos da própria review durante a avaliação.

### D10 — Atribuição e não reutilização de IDs

**Regra:** a ferramenta atribui e reserva o próximo número disponível; o agente
não escolhe números. IDs de planos principais e de knowledge global têm
sequências próprias, únicas no repositório. Os restantes tipos têm sequências
únicas dentro do plano principal, partilhadas pelos seus subplanos. Knowledge
local inclui o ID do plano principal (`LR-01.KNOW-04`); knowledge global não
inclui esse prefixo (`KNOW-12`). Os ordinais usam dois dígitos, com zero à
esquerda quando necessário. IDs removidos nunca são reutilizados. A reserva
impede atribuições concorrentes do mesmo ID.

**Fundamento:** evitar colisões entre agentes, tornar explícito o âmbito da
knowledge global e impedir que referências antigas passem a identificar trabalho
novo após uma remoção.

**Exemplo:** apagar `LR-01.REV-02` não liberta o número 02. A próxima review
recebe `LR-01.REV-03`, mesmo que pertença a outro subplano. O âmbito dos IDs de
planos principais (`LR-01`) e de knowledge global (`KNOW-12`) é o repositório;
as duas categorias usam sequências próprias e os IDs não precisam de ser únicos
entre repositórios.

### D11 — Referências usam IDs, não paths

**Regra:** relações entre artefactos usam IDs estáveis; o mapa resolve cada ID
para o caminho atual. Para uma secção específica, usar `ID#anchor`. A ferramenta
valida que o ID e a âncora existem.

**Fundamento:** mover um ficheiro não deve obrigar a reescrever todas as
referências. A resolução centralizada mantém links funcionais e permite detetar
referências inválidas automaticamente.

**Exemplo:** `derived_from: [LR-01.RES-07.audit]` e
`criteria_refs: [LR-01.SP-03.PLAN#completion-criteria]`. Paths não são a
identidade nem a referência canónica.

### D12 — Inventário de entidades com identidade própria

**Regra:** têm identidade própria: plano principal, subplano, research, review,
knowledge local e knowledge global. Delegação não é entidade deste modelo.
Os códigos são `LR` para plano principal, `SP` para subplano, `RES` para
research, `REV` para review e `KNOW` para knowledge local ou global. Ficheiros
como `PLAN`, `RESULT`, `working`, `audit`, `assessment` e `perspective` são
artefactos dessas entidades.

**Fundamento:** atribuir IDs apenas ao que tem objetivo, relações e ciclo de
vida próprios; o papel do ficheiro deriva da entidade a que pertence.

**Exemplo:** o plano principal é `LR-01` e o seu artefacto de plano pode ser
`LR-01.PLAN`; o subplano é `LR-01.SP-03` e o seu artefacto correspondente é
`LR-01.SP-03.PLAN`. Ambos têm o papel `PLAN`, mas não são o mesmo artefacto.

### D13 — Artefactos de research seguem as três camadas da skill

**Regra:** `working` e `audit` são artefactos da entidade research (`RES`). O
output consumer-facing é normalmente uma entidade knowledge (`KNOW`) criada ou
atualizada pela research, sobretudo quando a pesquisa prepara o plano e os
findings podem servir fases ou subplanos futuros. Não é um artefacto interno de
`RES`. Pesquisa pontual durante a execução pode entregar à secção `Outcome` do
`PLAN` do subplano uma síntese curta que justifique uma decisão local, sem criar
`KNOW`, se não houver valor esperado de reutilização. Não criar um `RESEARCH.md`
apenas para representar a unidade. A `$research` define o propósito, o conteúdo
e o ciclo de vida dos artefactos `working` e `audit`, incluindo a adaptação por
nível de rigor. O contrato interno desses artefactos pertence à skill
proprietária, conforme D16.

**Fundamento:** respeitar a separação da `$research` sem adicionar um ficheiro
redundante. `working` e `audit` conservam o processo e o apoio verificável da
research; `KNOW` conserva findings com valor para fases ou subplanos futuros.
Uma conclusão pontual pode integrar o `Outcome` do `PLAN`, enquanto o detalhe e
a evidência permanecem no `audit`.

**Exemplo:** `RES-07.working` + `RES-07.audit` produzem ou enriquecem
`LR-01.KNOW-04` quando os findings podem ajudar fases ou subplanos futuros. Se,
durante a execução, a pesquisa apenas justificar uma decisão local e pontual,
uma síntese curta pode entrar no `Outcome` do `PLAN`; não se cria `KNOW` só para
guardar essa justificação.

### D14 — Dependência e proveniência sem relações redundantes

**Regra:** `depends_on` regista exclusivamente uma condição de avanço; se uma
unidade tiver de esperar por um output, referencia esse output nessa relação.
`derived_from` regista a proveniência concreta do conteúdo. O modelo partilhado
não exige campos separados `consumes` ou `produces`: a pertença de um artefacto
à sua entidade é registada por `belongs_to`, e a proveniência por
`derived_from`.

**Fundamento:** evitar campos que repetem a associação do artefacto à entidade,
a proveniência ou uma dependência que já controla o avanço.

**Exemplo:**

```text
SP-04 depends_on SP-03.RESULT
RES-07.working belongs_to RES-07
KNOW-04 derived_from RES-07.audit
```

`depends_on` condiciona o avanço; `belongs_to` associa um artefacto à entidade
que integra; `derived_from` explica a origem do conteúdo.

### D15 — Resultado do subplano

**Regra:** o agente regista uma nota breve na secção `Outcome` do `PLAN` do
subplano, cobrindo conclusão, verificação e diferenças materiais face ao plano,
sem repetir o objetivo ou os critérios. Só se cria um artefacto `RESULT`
separado quando o output definido para a tarefa é um deliverable autónomo,
consumer-facing e consultável como artefacto próprio. A implementação de uma
tarefa, por si só, não exige um `RESULT` adicional.

**Fundamento:** o agente executa a tarefa acordada; não precisa de produzir uma
composição genérica para provar que a concluiu. Separar `RESULT` só tem valor
quando esse artefacto é, ele próprio, um output requerido pelo consumer.

**Exemplo:** numa tarefa de implementação, o código é o output e a secção
`Outcome` do `PLAN` regista conclusão, verificação e diferenças relevantes face
ao planeado. Se a tarefa pedir um relatório ou dataset como deliverable próprio,
esse conteúdo pode ser produzido num artefacto `RESULT` separado.

### D16 — Ownership dos contratos de artefactos por skill

**Regra:** o modelo partilhado e `$plan-management` definem o núcleo do plano:
entidades, IDs, relações e organização/localização comum dos ficheiros. Cada
skill proprietária define o propósito, conteúdo e ciclo de vida detalhado dos
artefactos do seu workflow, incluindo requisitos específicos do nível de rigor.
O modelo partilhado fixa os papéis e relações necessários à coordenação sem
duplicar esses contratos internos.

**Fundamento:** manter uma arquitetura de plano comum sem deslocar para
`$plan-management` as regras específicas dos workflows que o plano coordena.

**Exemplo:** o mapa resolve `LR-01.RES-07.audit` ou
`LR-01.REV-02.assessment` e liga esses artefactos ao plano; `$research` define
o conteúdo e a persistência de `audit`, e `$agent-delegation` define a execução e
o conteúdo da review.

### D17 — Research e review ligadas à unidade que as pediu

**Regra:** como aplicação da regra geral de ligação por frontmatter (D08), cada
research e review referencia explicitamente, por ID, o plano principal ou
subplano que a solicitou. A referência ao solicitante identifica onde a unidade
se enquadra no ciclo de execução; não substitui as relações de alvo da review
(D07) ou dependência (D14). Para `RES`, o plano ou subplano solicitante
é também um input obrigatório, e a research segue as guidelines fornecidas
pela `$research`; estas são contexto da skill, não um artefacto adicional no
  grafo. O campo chama-se `requested_by`.

**Fundamento:** o coordenador atribui research e review como parte do ciclo de
uma unidade e recebe os seus resultados. A ligação explícita mantém cada
atividade integrada nesse ciclo e permite ao mapa navegar entre solicitação e
output.

**Exemplo:** uma research pedida por `LR-01.SP-03` referencia esse subplano;
uma review pedida pelo plano principal `LR-01` referencia esse plano, além de
declarar os alvos e critérios próprios.

### D18 — Disponibilidade de outputs segue o ciclo do plano

**Regra:** um output fica disponível ao consumidor quando a unidade produtora
está concluída, o coordenador recebeu e reconciliou o resultado, e as
dependências e gates de review/integração aplicáveis estão satisfeitos. Outputs
provisórios não desbloqueiam unidades downstream. O ciclo do plano determina
esta transição; o modelo de artefactos não cria um fluxo de estados paralelo.

**Fundamento:** disponibilidade depende da conclusão e dos gates da unidade,
não da existência ou localização de um ficheiro. O ciclo distingue trabalho
sequencial, resultados recebidos e integração de trabalho paralelo.

**Exemplo:** numa cadeia sequencial, o coordenador recebe o resultado do
subplano concluído antes de avançar. Em trabalho paralelo, integra os resultados
antes da review de qualidade, se esta estiver prevista para o plano.

### D19 — Estados mínimos das unidades e bloqueio como pausa

**Regra:** o estado de uma unidade usa apenas `not_started`, `in_progress`,
`blocked` ou `complete`. Os requisitos acordados e registados no plano são
obrigatórios. O agente executa o objetivo completo e pode resolver
autonomamente problemas menores dentro do scope aprovado. `blocked` é uma pausa
intermédia enquanto se aguarda uma decisão do utilizador; não é um estado final
nem permite declarar o trabalho concluído. Se o agente não conseguir cumprir
um requisito dentro do scope
autorizado, ou se para avançar precisar de alterar esse scope, deve parar,
explicar o requisito afetado e a razão do bloqueio, e consultar o utilizador.
Não pode contornar o impedimento, omitir o requisito ou apresentar o trabalho
incompleto como concluído sob a forma de limitações. Depois da decisão do
utilizador, a unidade só retoma após atualizar o plano quando necessário e
regressa a `in_progress`. `complete` significa que o trabalho da unidade
terminou; a disponibilidade dos seus outputs continua sujeita a D18.

**Fundamento:** manter a execução dentro do scope aprovado e tornar visível
qualquer impedimento que exija intervenção do utilizador. Um estado de bloqueio
não substitui a conclusão dos requisitos nem transforma uma entrega parcial em
resultado aceite.

**Exemplo:** se um requisito depender de acesso que o agente não tem, ou a
única solução exigir uma alteração de scope, o agente marca a unidade como
`blocked`, indica o requisito e o impedimento, e aguarda a decisão do
utilizador. Não marca a unidade como `complete` nem regista o requisito em falta
como uma limitação aceite.

### D20 — Campos de frontmatter variam conforme o tipo de artefacto

**Regra:** os campos obrigatórios dependem do tipo de documento; não se replica
o frontmatter de `PLAN` em todos os ficheiros. Um `PLAN` de plano principal ou
subplano mantém `plan_id`, `kind`, `parent`, `phase`, `status`, `depends_on` e
`consumers` (este último apenas para destinos externos ao grafo de planos).
Artefactos associados declaram `belongs_to` com o ID da entidade a que
pertencem. A metadata de research e review declara `requested_by` com o ID do
plano ou subplano que as solicitou (D17). A atribuição de review declara também
`targets` e `criteria_refs` (D07); knowledge declara `derived_from` (D06).
Dados comuns da unidade não se repetem em cada artefacto; a skill proprietária
define em qual dos seus artefactos fica essa metadata. `consumes` e `produces`
não fazem parte do frontmatter do modelo partilhado (D14).

**Fundamento:** exigir só os metadados relevantes para cada tipo preserva as
relações necessárias à navegação sem criar campos vazios ou duplicados.

**Exemplo:** um subplano usa os campos do contrato de `PLAN`; o artefacto de
auditoria de uma research referencia a entidade `RES` em `belongs_to`; a
atribuição de uma review guarda o seu solicitante, alvos e critérios; uma
entrada `KNOW` lista as fontes concretas em `derived_from`.

### D21 — Operações do mapa gerado

**Regra:** o mapa é uma projeção gerada a partir dos IDs e metadados dos
artefactos. Deve resolver um ID ou `ID#anchor` para a localização atual,
permitir navegar pelas relações declaradas e descobrir entidades e artefactos
por ID, tipo e relações. Deve validar IDs duplicados, referências inexistentes
e âncoras inválidas. Ficheiros ou metadados alterados atualizam o mapa
automaticamente; atribuição e reserva de IDs seguem D10. A localização física e
a implementação do mapa não fazem parte desta decisão.

**Fundamento:** manter um ponto de navegação consistente sem transformar o
mapa numa fonte manual concorrente dos IDs e relações canónicos.

**Exemplo:** ao mover `LR-01.SP-03.PLAN`, a resolução do seu ID passa a devolver
o novo caminho sem alterar as referências que lhe apontam. Se uma referência
apontar para um ID ou âncora inexistente, a validação assinala o erro.

### D22 — Organização física por unidade de trabalho

**Regra:** os artefactos locais ficam junto da unidade que os coordena. Os
artefactos do plano principal ficam na sua pasta; os artefactos específicos de
um subplano ficam na pasta desse subplano. Um `RESULT` separado só aparece
quando exigido por D15. Consumidores referenciam artefactos partilhados pelos
seus IDs, sem criar cópias nem alterar a sua pertença. A opção B é a estrutura
selecionada; esta escolha não é apresentada como conclusão do piloto A/B, que
não demonstrou um vencedor geral.

**Fundamento:** manter juntos os artefactos locais de cada unidade e usar o
mapa para navegar entre unidades e relações.

**Exemplo:**

```text
<plan>/
├── PLAN.md
├── research/       # artefactos pertencentes ao plano principal, se existirem
├── reviews/        # reviews do plano principal, se existirem
├── knowledge/      # knowledge local do plano principal, se existir
└── subplans/
    └── <subplan>/
        ├── PLAN.md
        ├── RESULT.md        # apenas se for um deliverable autónomo (D15)
        ├── research/        # artefactos locais, se existirem
        ├── reviews/         # reviews locais, se existirem
        └── knowledge/       # knowledge local, se existir
```

### D23 — Schema de frontmatter de `PLAN`

**Regra:** todo `PLAN` de plano principal ou subplano usa frontmatter YAML com
os campos-base obrigatórios `plan_id`, `kind`, `parent`, `phase`, `status`,
`depends_on` e `consumers`. `plan_id` é uma string segundo D10; `kind` é
`root` ou `subplan`; `parent` é `null` no root e o ID do plano pai no
subplano; `phase` é `root` no root e o identificador da fase do pai no
subplano; `status` usa os valores de D19; `depends_on` é uma lista de
referências por ID aos outputs condicionantes, conforme D14; `consumers` é
uma lista de destinos externos ao grafo, vazia quando não existirem, conforme
D20. O root inclui também `execution`, e um subplano pode incluir
`execution_exception`, conforme D24–D26. Referências usam IDs estáveis, não
paths (D11).

**Fundamento:** dar à skill e ao validador um contrato estrutural único para
planos principais e subplanos, mantendo as dimensões de execução ligadas às
skills proprietárias.

**Exemplo:**

```yaml
---
plan_id: LR-01.SP-03
kind: subplan
parent: LR-01
phase: S2
status: in_progress
depends_on: [LR-01.SP-02.RESULT]
consumers: []
---
```

### D24 — Dimensões independentes de execução

**Regra:** o plano principal declara em `execution` três dimensões
independentes: `research`, `review` e `delegation`. Cada dimensão pode ser
ativada ou não sem ativar ou desativar as outras; review e delegação podem ser
usadas separadamente ou em conjunto. Os valores permitidos e a herança para
subplanos são definidos separadamente.

**Fundamento:** permitir configurar cada workflow conforme a necessidade do
plano sem confundir avaliação com execução paralela.

**Exemplo:** um plano pode declarar research e review, sem delegação; outro
pode declarar delegação sem research nem review.

### D25 — Valores de execução pertencem às skills proprietárias

**Regra:** cada skill proprietária define os valores e configurações válidos
da sua dimensão de execução. `$plan-management` regista a configuração
escolhida e aponta para a skill proprietária, sem duplicar nem manter uma
enumeração concorrente desses valores. `research` remete para `$research`; `review` e
`delegation` remetem para `$agent-delegation`.

**Fundamento:** alterações às configurações de um workflow devem ser mantidas
na sua skill proprietária e não exigir sincronização de uma segunda enumeração em
`$plan-management`.

**Exemplo:** se `$research` mudar os nomes dos seus níveis de rigor,
`$plan-management` continua a referenciar os valores atuais dessa skill, sem
preservar uma lista antiga. `$agent-delegation` define `true` e `false` para
as dimensões de review e delegação.

### D26 — Herança e exceções locais de execução

**Regra:** a configuração `execution` do plano principal é o valor por
omissão herdado por todos os subplanos. Quando necessário, um subplano pode
declarar em `execution_exception` apenas as dimensões que diferem desse
default. A exceção pode desativar uma dimensão ou ativá-la com um valor
definido pela skill proprietária, mesmo que a dimensão esteja desativada no
plano principal.

**Fundamento:** manter uma configuração comum e concisa no plano principal,
permitindo diferenças locais sem alterar a configuração dos restantes
subplanos.

**Exemplo:** o plano principal deixa `review` desativada; um subplano que
precise dessa etapa declara em `execution_exception` `review: true`, conforme
a configuração definida por `$agent-delegation`.

### D27 — Ownership de review e delegação

**Regra:** `$plan-management` declara em que unidades se aplicam review e
delegação, mantém os defaults e exceções locais, e coordena os gates do plano.
`$agent-delegation` executa os workflows de review e delegação e define os seus
procedimentos e pacotes temporários. Se ambos forem usados, o executor conclui
e reconcilia o resultado antes do início da review; o alvo permanece estável
durante a avaliação, conforme D09. A delegação não é uma entidade do grafo
partilhado, conforme D05.

**Fundamento:** separar a configuração e coordenação do plano da execução dos
workflows proprietários, mantendo uma fronteira clara entre produção e
avaliação.

**Exemplo:** um subplano pode ativar delegação e review por exceção local; os
agentes executam e entregam o resultado, o coordenador reconcilia-o e só então
`$agent-delegation` inicia a review desse resultado.

### D28 — Corpo do `PLAN` de subplano

**Regra:** o corpo do `PLAN` de um subplano funciona como brief executável da
tarefa, definindo o objetivo, o scope, os inputs relevantes, o output esperado
e a condição de conclusão. Não redefine o objetivo global nem repete o conteúdo
do plano-pai. As relações e dependências seguem o frontmatter e as regras
aplicáveis do modelo.

**Fundamento:** dar ao agente contexto suficiente para executar e verificar a
unidade sem duplicar o plano que a coordena.

**Exemplo:** o `PLAN` de `LR-01.SP-03` declara o objetivo e o output da sua
tarefa, liga os inputs e dependências pelos IDs aplicáveis e define a condição
que permite concluir o subplano; não copia o objetivo geral de `LR-01`.

### D29 — Enriquecimento de knowledge na coordenação simples

**Regra:** a coordenação simples, sem plano durável, e a coordenação durável,
com plano, são níveis distintos; o enriquecimento por knowledge pode acompanhar
ambos. Numa coordenação simples, consultar `knowledge/` quando for útil à tarefa
não cria um plano durável nem exige registar as entradas consultadas. Se surgir
uma lacuna relevante, o agente pode propor a utilização de `$research`, mas só
executa a skill quando o utilizador a invoca explicitamente, conforme o seu
contrato. A localização, o routing e a discoverability da knowledge global são
definidos separadamente no [plano de promoção de knowledge](PLAN_knowledge-promotion.md).

**Fundamento:** permitir que tarefas simples aproveitem knowledge disponível
sem lhes impor o custo de um plano durável, mantendo explícita a fronteira para
research e deixando a descoberta global para o plano proprietário.

**Exemplo:** numa tarefa simples, o agente consulta uma entrada útil de
`knowledge/` sem criar um plano nem registar a consulta. Se encontrar uma lacuna
relevante, propõe `$research`; só inicia a pesquisa após invocação explícita do
utilizador.

### D30 — Corpo do `PLAN` principal

**Regra:** o corpo do `PLAN` principal apresenta o objetivo geral, a filosofia
e os limites do plano, a fase atual, uma sequência breve das fases com ligações
para os subplanos e o gate global de conclusão. Os critérios detalhados de cada
fase pertencem aos subplanos.

**Fundamento:** manter o plano principal como mapa global do trabalho e evitar
que repita o detalhe executável das suas unidades.

**Exemplo:** o plano principal indica que a fase atual é S2, liga ao subplano
que define essa fase e declara o gate global; os critérios de S2 ficam no
`PLAN` do subplano correspondente.

### D31 — Índice de navegação da knowledge

**Regra:** se existir um `knowledge/INDEX.md`, este mantém um catálogo curto
com o ID, o título e a utilidade de cada entrada. O ID funciona como ligação
para a entrada através da resolução definida em D11 e D21; não se mantém uma
coluna separada de paths. O índice não contém colunas de estado, relações ou
versões; o conteúdo, a proveniência e as limitações ficam na entrada de
knowledge, conforme D06 e D29.

**Fundamento:** permitir localizar knowledge pelo que é e pelo uso que serve,
sem duplicar no índice os metadados e o conteúdo da entrada.

**Exemplo:**

```markdown
| ID | Título | Serve para |
|---|---|---|
| LR-01.KNOW-01 | App framework benchmark | Escolher a stack técnica |
| LR-01.KNOW-02 | Authentication patterns | Definir autenticação e autorização |
```

### Trabalho específico das skills, a tratar depois

- Na `$research`, definir por nível de rigor quando `working`, `audit` e o
  output consumer-facing são obrigatórios, temporários ou persistentes, e como
  esse output é entregue sem duplicação. `$plan-management` precisa apenas do
  contrato de interface e handoff.
- No plano de promoção de knowledge, fechar a transição de ID local para
  global, proveniência, duplicados e reparação de referências. A
  `$plan-management` precisa apenas do contrato de integração para criar,
  consultar e entregar knowledge.

## Manutenção do registo

Cada decisão contém uma regra, uma fundamentação curta e um exemplo útil.
Evitar repetir o mesmo ponto nas três partes ou transcrever o debate.
Substituir propostas ultrapassadas, conservar IDs das decisões e distinguir
aprovação de hipótese. Não promover perguntas ou silêncio a aprovação.
Reconciliar a lista de questões após cada decisão: remover o que fechou e
manter apenas os pontos residuais concretos; não conservar categorias genéricas
indefinidamente nem acrescentar novas questões sem necessidade identificada.
