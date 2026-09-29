---
plan_id: P1
kind: root
parent: null
phase: root
status: not_started
depends_on: [P0]
consumers: []
---

# Repository knowledge — architecture, promotion and integration

> Este plano define a arquitetura da knowledge durável ao nível da repository,
> a skill que pode promover knowledge produzida em planos e a integração com
> `$context-architecture` e `$plan-management`. Não implementa ainda a skill,
> não migra repositories existentes e não cria uma biblioteca inicial.
>
> Este plano permanece em standby até o plano `P0` estar concluído, porque
> reutiliza decisões e contratos definidos no plano principal.

## Objective

Definir a arquitetura e o modelo de integração de uma camada de knowledge
durável e específica de cada repository, concebida como uma mini biblioteca de
benchmarks e informação reutilizável para agentes. O plano tem duas linhas
principais: definir a skill transversal que decide quando knowledge produzida
em planos deve ser promovida e definir como esta camada se integra com
`$context-architecture` e `$plan-management`.

## Scope

Este plano cobre três vertentes relacionadas:

1. **Knowledge durável da repository** — definir uma mini biblioteca de
   informação específica da repository que os agentes possam consultar em
   tarefas futuras. Pode conter benchmarks, decisões, padrões, referências e
   outras informações úteis, independentemente de terem sido ou não criadas
   por um plano. Esta camada funciona como apoio contextual às skills, mas não
   substitui skills generalistas nem deve ser confundida com `CONTEXT.md`,
   planos ou artefactos de research.
2. **Skill de promoção** — definir a skill transversal que avalia knowledge
   produzida em planos e decide se deve permanecer local, ser atualizada ou ser
   promovida para a knowledge global da repository. A promoção é uma forma de
   alimentar a biblioteca, não o seu único propósito nem a condição para uma
   entrada existir.
3. **Integração das skills de organização** — definir como
   `$context-architecture` representa, localiza e encaminha a knowledge e como
   `$plan-management` cria, usa e entrega knowledge local e outputs de planos.

Ficam fora do scope a implementação imediata da skill de promoção, a migração
de repositories existentes, a criação de uma biblioteca inicial de knowledge,
e a definição do conteúdo substantivo de cada entrada.

## Output

Uma especificação conceptual aprovada para a knowledge durável da repository,
para a skill de promoção e para a sua integração com as skills de organização,
contendo:

- o propósito e o contrato da pasta global `knowledge/`, do seu índice e das
  suas entradas;
- a distinção entre knowledge global, knowledge local, skills, contexto,
  planos e artefactos de research;
- o papel, trigger, inputs, avaliação e output esperado da skill transversal de
  promoção;
- os critérios e o ciclo de vida da promoção, incluindo proveniência, IDs,
  ownership, atualização e tratamento de duplicados;
- as alterações necessárias ao routing e ownership definidos por
  `$context-architecture`;
- as alterações necessárias aos contratos e outputs definidos por
  `$plan-management`;
- a forma como este sistema é consumido por coordenações simples e duráveis.

O plano principal, [PLAN.md](PLAN.md), é uma dependência deste plano e define a
forma leve de declarar uma coordenação simples enriquecida por knowledge. Este
plano reutiliza esse contrato e não o redefine.

## Plan tree

Este plano é atualmente um plano raiz de definição e não possui subplanos. A
divisão em subplanos só deve ser criada depois de a arquitetura e os seus
limites estarem suficientemente definidos.

## Sequence

1. **S1 — Definir a finalidade e as fontes da knowledge da repository**
   - **Action:** Definir a knowledge como uma mini biblioteca específica da
     repository e distinguir as suas possíveis fontes, incluindo curadoria
     direta, benchmarks, informação de referência e knowledge produzida em
     planos.
   - **Output:** Modelo de finalidade, fontes e limites da knowledge global.
   - **Exit check:** A knowledge global não fica limitada à promoção nem se
     confunde com skills, `CONTEXT.md`, planos ou research.

2. **S2 — Integrar a knowledge com `$context-architecture`**
   - **Action:** Definir localização, índice, IDs, formato das entradas,
     proveniência, ownership e routing da pasta global `knowledge/`, incluindo
     a forma como os mapas de contexto a tornam descobrível.
   - **Output:** Contrato estrutural e de discoverability da knowledge da
     repository.
   - **Exit check:** Um agente consegue localizar uma entrada relevante sem
     carregar a biblioteca inteira, e os mapas não se tornam depósitos de
     conteúdo.

3. **S3 — Integrar a knowledge com `$plan-management`**
   - **Action:** Definir a relação entre knowledge global, knowledge local,
     research, `RESULT.md`, planos simples e planos duráveis, incluindo os
     owners e handoffs de cada output.
   - **Output:** Contrato de integração entre knowledge e gestão de planos.
   - **Exit check:** Cada output de um plano tem um destino claro e a
     knowledge não duplica `working.md`, `audit.md`, `RESULT.md` ou o plano.

4. **S4 — Definir a skill transversal de promoção**
   - **Action:** Definir o propósito, trigger, inputs, avaliação e output da
     skill que pode ser aplicada a qualquer repository para identificar
     knowledge produzida em planos que seja candidata a promoção.
   - **Output:** Brief funcional da skill de promoção.
   - **Exit check:** A skill tem uma responsabilidade delimitada e não duplica
     `$plan-management`, `$research` ou `$context-architecture`.

5. **S5 — Definir o ciclo de promoção**
   - **Action:** Definir como a skill avalia knowledge local produzida por
     planos e decide entre manter local, atualizar uma entrada existente,
     criar uma entrada global ou rejeitar a promoção, incluindo IDs,
     proveniência, duplicados e ownership.
   - **Output:** Política de promoção com decisões e estados explícitos.
   - **Exit check:** É possível decidir de forma consistente se uma entrada
     local deve permanecer local, ser atualizada ou ser disponibilizada à
     repository.

6. **S6 — Definir o consumo por coordenação simples e durável**
   - **Action:** Registar como agentes em coordenação simples ou durável podem
     consultar knowledge global, mantendo a coordenação simples leve e sem
     tracking próprio.
   - **Output:** Regra de consumo compatível com o contrato de
     `plan-management`.
   - **Exit check:** O primeiro plano consegue declarar o enriquecimento simples
     sem introduzir um plano durável, enquanto planos complexos mantêm o seu
     detalhe e proveniência locais.

7. **S7 — Consolidar a arquitetura**
   - **Action:** Rever as decisões, ligações, owners, outputs e limites antes
     de qualquer implementação.
   - **Output:** Especificação conceptual final deste plano.
   - **Exit check:** A arquitetura, o ciclo de vida, o papel das skills e a
     integração com `$context-architecture` estão definidos sem decisões
     estruturais pendentes.

## Completion criteria

- O conceito de knowledge durável e específico da repository está definido.
- A relação entre knowledge local e global está definida.
- A estrutura, discoverability, ownership, IDs e proveniência da knowledge
  global estão definidas.
- Os critérios e o ciclo de vida de promoção estão definidos.
- O papel e os limites da skill transversal de promoção estão definidos.
- A integração com `$context-architecture` está definida.
- O consumo por coordenações simples e duráveis está definido.
- O output pode ser aplicado pelo primeiro plano sem exigir implementação ou
  migração durante este brainstorm.
