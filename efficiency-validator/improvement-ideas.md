# Próximas prioridades

## Mapa de navegação

| Se precisares de... | Consulta |
| --- | --- |
| Prioridades imediatas | [Secções 1–3](#1-automatizar-a-quality-review-tanto-quanto-possível) |
| Ideias futuras | [Ideias futuras](#ideias-futuras) |
| Rever uma prioridade concreta | A secção numerada correspondente |

Estas são as prioridades que fazem mais sentido para a próxima fase do
`efficiency-validator`. O objectivo é fechar a base de evidência, tornar os
resultados mais fáceis de interpretar e permitir que a ferramenta seja útil
mesmo quando não existe tracing de filesystem.

## 1. Automatizar a quality review tanto quanto possível

### O que é

Reduzir o trabalho manual necessário para produzir uma quality review válida,
sem permitir que a automação transforme uma avaliação incerta numa aprovação.

O sistema deve evoluir para:

- rubricas versionadas por tipo de tarefa;
- avaliação claim-by-claim;
- verificação de claims obrigatórios e proibidos;
- análise de completude;
- verificação de autoridade das fontes;
- verificação de suporte para cada afirmação;
- identificação automática de casos ambíguos;
- revisão humana apenas quando a confiança for insuficiente;
- registo da versão do avaliador e da política usada.

### Problema que resolve

O quality gate é correctamente separado do custo, mas uma review totalmente
manual pode tornar-se o maior gargalo quando forem avaliadas muitas skills,
modelos ou tarefas.

Também existe o risco de avaliações inconsistentes se diferentes revisores
interpretarem a mesma rubrica de maneira diferente.

### Resultado esperado

Para cada claim, o relatório deve conseguir mostrar algo semelhante a:

```text
claim: workspace-membership-required
estado: pass
evidência: resposta final + fonte autorizada
avaliador: quality-policy-3
confiança: alta
```

Quando a evidência for insuficiente, o resultado deve ser `indeterminate`,
com encaminhamento opcional para revisão humana. A redução de custo ou de
tokens nunca pode compensar uma falha de qualidade.

### Pontos para rever

- Que partes da review podem ser determinísticas?
- Que partes precisam de um avaliador LLM?
- Quando é obrigatória uma revisão humana?
- Como medir a concordância entre avaliação automática e humana?
- Como impedir que o próprio agente influencie indevidamente a avaliação?

## 2. Criar um modo Basic que não dependa de filesystem tracing

### O que é

Definir um modo de captura mínimo, útil e operacional, que funcione sem
privilégios especiais e sem depender de tracing de baixo nível do sistema
operativo.

O modo Basic deve capturar pelo menos:

- prompt e proveniência disponível;
- modelo e runtime;
- tokens;
- turnos;
- comandos e chamadas de ferramentas observáveis;
- resposta final;
- quality gate;
- relatório comparativo.

O filesystem tracing deve continuar a existir como uma capacidade adicional,
mas não como requisito para usar o produto.

### Problema que resolve

O tracing de filesystem pode exigir privilégios, depender do sistema operativo
e ser difícil de instalar ou executar em CI. Se for obrigatório, impede a
adopção do validador em ambientes normais.

### Resultado esperado

O produto deve ter uma hierarquia clara de captura:

- **Basic**: execução e custos principais;
- **Standard**: contexto efectivo, ferramentas e qualidade detalhada;
- **Forensic**: filesystem tracing, processos e diagnóstico de baixo nível.

Cada modo deve declarar exactamente que perguntas consegue responder e quais
ficam fora da sua autoridade.

### Pontos para rever

- Qual é o conjunto mínimo de dados que torna o Basic útil?
- Que comparações devem ser bloqueadas sem tracing?
- O modo Basic deve ser o modo predefinido?
- Como evitar que “indisponível” seja confundido com “zero”?

## 3. Integrar CI/regression testing para skills e contexto

### O que é

Executar avaliações controladas automaticamente quando houver alterações a
skills, prompts, `CONTEXT.md`, documentação, oráculos, modelos ou políticas de
ferramentas.

A integração deve conseguir produzir estados simples para uma pipeline:

```text
PASS   qualidade preservada e custo reduzido
WARN   qualidade preservada mas existe uma regressão secundária
FAIL   claim obrigatório ausente ou qualidade inferior
BLOCK  comparação inválida por proveniência incompleta
```

### Problema que resolve

Sem CI, a avaliação acontece apenas quando alguém se lembra de executar a
ferramenta. Uma alteração pequena numa skill ou num documento pode introduzir
regressões sem ser detectada.

### Resultado esperado

Cada alteração relevante deve poder ser avaliada contra uma colecção fixa de
tarefas e replicações. A pipeline deve guardar os artefactos e comparar o
resultado com a versão anterior, sem transformar uma única execução num facto
definitivo.

O CI deve bloquear apenas quando a política assim o justificar. Resultados
exploratórios ou com observabilidade insuficiente devem aparecer como aviso ou
bloqueio explícito, não como aprovação silenciosa.

### Pontos para rever

- Que alterações devem disparar uma avaliação?
- Quantas tarefas e replicações são necessárias para cada tipo de mudança?
- Que regressões bloqueiam o merge?
- Como controlar o custo e o tempo das avaliações em CI?
- Que artefactos devem ser preservados para auditoria?

# Ideias futuras

Estas ideias ficam fora das próximas prioridades. Podem tornar o produto mais
completo depois de a captura, a qualidade, os relatórios e a integração básica
estarem suficientemente estáveis.

## 1. Agregação estatística e incerteza

Substituir gradualmente decisões agregadas baseadas apenas em contagens de
veredictos por análise de variância e tamanho do efeito.

O agregador poderia mostrar média, mediana, intervalo interquartil, percentis,
intervalos de confiança, taxa de vitórias e custo esperado por tarefa bem
sucedida. O objectivo não seria tornar o sistema menos conservador, mas
explicar melhor a diferença entre uma melhoria consistente, uma melhoria
pequena e um resultado instável.

## 2. Dashboard histórico por skill, tarefa, modelo e runtime

Criar uma visão histórica para acompanhar como uma skill ou configuração muda
ao longo do tempo.

O dashboard poderia mostrar regressões, tendências de custo, tarefas mais
instáveis, qualidade por modelo e diferenças entre versões do runtime. Deveria
ligar cada conclusão aos artefactos originais, para que os gráficos não se
transformassem numa camada impossível de auditar.

## 3. Exportação e API de integração

Disponibilizar os dados através de formatos e interfaces adequados a outros
sistemas, por exemplo JSON Schema, SQLite, Parquet ou uma API.

Isto permitiria integrar resultados com pipelines, dashboards, relatórios de
projecto e sistemas de análise sem obrigar cada consumidor a ler directamente
os ficheiros internos do observador.


## 4. Detecção de efficiency debt

Identificar skills, regras ou documentos que aumentam o contexto sem melhorar
qualidade, taxa de sucesso, tempo ou número de erros.

Uma alteração que adiciona contexto significativo e não produz benefício
mensurável acumula uma espécie de dívida de eficiência. O relatório deveria
mostrar esta dívida como uma hipótese sustentada por comparações, não como uma
penalização arbitrária.

## 5. Impressão digital do percurso do agente

Criar perfis dos caminhos utilizados durante uma execução:

- pesquisa ampla;
- leitura directa;
- caminhos sem resultado;
- repetição de comandos;
- retorno aos mesmos ficheiros;
- exploração excessiva antes da primeira leitura relevante.

Isto permitiria optimizar o processo de navegação e não apenas o resultado
final. A análise só deve usar eventos com autoridade suficiente; texto do
agente ou comandos declarados não devem ser promovidos automaticamente a prova
de acesso físico.

## 6. Paragem adaptativa das avaliações

Permitir que o sistema decida quando já existe evidência suficiente para parar
ou quando deve recolher mais replicações.

Uma diferença muito clara poderia terminar mais cedo; resultados próximos ou
instáveis exigiriam mais execuções. A política de paragem teria de ser
determinística e auditável, para não criar uma forma de escolher apenas os
resultados favoráveis.
