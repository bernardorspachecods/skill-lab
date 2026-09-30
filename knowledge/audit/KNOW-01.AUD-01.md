---
belongs_to: KNOW-01
source_artifact_id: LR-04.RES-01
source_artifact_role: audit
source_requested_by: LR-04.SP-01
---

# Audit

## Navigation map

| If you need... | See |
| --- | --- |
| Research question and cue boundary | [Question and scope](#question-and-scope) |
| Claim-by-claim findings and study evidence | [Claims and evidence](#claims-and-evidence) |
| Themes across studies | [Thematic synthesis](#thematic-synthesis) |
| Source provenance and limitations | [Sources](#sources) · [Conflicts and limitations](#conflicts-limitations-and-uncertainty) |
| Search coverage and validation | [Validation](#validation) |

## Question and scope

**Question:** Does existing empirical evidence indicate that explicitly labeling
a task as important or high priority changes LLM performance, and under what
conditions?

**Operational boundary.** The target is generic verbal priority/importance
framing (e.g. “this is important,” “high priority,” or urgency language) added
without changing the task itself. Wording that says the task matters *to the
user’s career* carries an implied personal consequence. It is therefore
important overlap evidence, but not a clean test of generic priority alone.
Described real-world benefits, harms, and consequences as a separate factor
belong primarily to LR-04.SP-02. No fixed publication cutoff was imposed. The
search was conducted 2026-09-30. This is a focused evidence audit, not a
systematic or exhaustive review.

**Brief conclusion.** The evidence supports a cautious “sometimes, in some
settings” answer for emotional/importance-adjacent prompt additions, not a
reliable general performance boost from simply marking a task important.
The headline positive results come mainly from one research group’s
EmotionPrompt program, whose stimuli bundle importance with social pressure,
self-efficacy, reassurance, review requests, and other emotional wording.
The exact phrase “This is very important to my career” is tested, but it also
implies personal stakes. An independent conceptual replication finds an
approximately zero pooled accuracy change for randomized EmotionPrompt cues,
with benchmark-specific gains and losses and no robust overall advantage.
An independent PNAS study finds little change in its specific behavioral
outcome for advanced models, but that outcome is similarity to human choice
distributions rather than answer correctness. Direct experiments that isolate
plain “this task is important/high priority” wording from stakes, encouragement,
and extra instruction remain scarce in the located evidence.

## Claims and evidence

| Claim ID | Claim / subquestion | Importance | Evidence IDs | Status |
| --- | --- | --- | --- | --- |
| C1 | Effect of generic importance or priority wording on task quality or correctness | High | E1, E2, E3 | Partial; cue-specific isolation limited |
| C2 | Variation by task, model, cue wording, or study design | High | E1, E2, E3, E4 | Supported within studied settings |
| C3 | Effects on instruction following, calibration, response characteristics, or resource use when measured | Medium | E1, E2, E3, E4 | Partial; few measured these outcomes |
| C4 | Transfer limits and null/conflicting findings | High | E1-E4 | Supported; uncertainty remains material |

### Evidence entries

**E1: C1, C2, C3 -> S1.** Li et al., *Large Language Models Understand and Can
be Enhanced by Emotional Stimuli* (arXiv technical report, v7, 2023; short
version accepted at LLM@IJCAI'23). In the introduction and §2.1 the authors
define 11 appended emotional stimuli. EP02 is “This is very important to my
career”; nearby alternatives include “You’d better be sure,” “Are you sure
that’s your final answer? It might be worth taking another look,” and
encouragement/self-efficacy phrases. §2.2, Table 1 compares prompt variants on
24 Instruction Induction tasks and 21 selected BIG-Bench tasks using six models
(Flan-T5-Large, Vicuna, Llama 2, BLOOM, gpt-3.5-turbo (0613), GPT-4); accuracy
is used on Instruction Induction, and BIG-Bench uses its normalized preferred
metric. The paper reports mean relative gains for the bundle of 11 stimuli of
8.00% on Instruction Induction and 115% on BIG-Bench; those relative figures
are strongly affected by the near-zero original BIG-Bench average (Table 1),
and do not mean a 115 percentage-point correctness increase. Results are
reported as averages across tasks/models and include an “avg” across all
stimuli as well as a post-hoc best-stimulus statistic. The latter is
selection-optimistic and should not be treated as an unbiased expected effect.
In §2.3, 106 participants rate GPT-4 outputs to 30 questions on performance,
truthfulness, and responsibility; these are subjective quality ratings, not
objective correctness. The authors report 10.9% average improvement in the
abstract and note rating variance/subjectivity in §2.3.3. §3.3 says cue efficacy
varies by task: EP02 is strongest among cues on Instruction Induction but
performs poorly on BIG-Bench. This is positive bundle-level evidence plus
task-dependent evidence for the exact career-importance cue, but it does not
isolate generic priority from stakes, reassurance, social evaluation, or
instruction to re-check. The paper’s proposed attention/reward explanations
are author interpretations, not directly established causal mechanisms.
**Support:** partial for “some importance-adjacent cues can alter measured
quality”; insufficient for a general effect of generic importance wording.
**Confidence:** moderate that this specific prompt family affected the studied
outputs as reported; low for attribution to importance wording alone or transfer
to current models/tasks.

**E2: C1, C2, C4 -> S2.** Li et al., *The Good, The Bad, and Why: Unveiling
Emotions in Generative AI* (ICML 2024; arXiv v3, 2024), an expanded study by
the same author group as S1 (not independent corroboration). §3.1 expands the
cue set to 21 text EmotionPrompts; EP02 remains “This is very important to my
career.” Across 50 tasks from Instruction Induction and BIG-Bench-Hard, with
language and multimodal models (including gpt-3.5-turbo (0613), GPT-4, Llama 2,
and multimodal models), the authors report positive average results for the
*EmotionPrompt bundle*: textual prompts improve semantic-understanding and
reasoning performance by 13.88% and 11.76%, respectively (§4.1, Fig. 2).
However, they also explicitly report that the exact EP02 performs poorly on
BIG-Bench-Hard while leading on Instruction Induction (§4.3, Fig. 4), a
material within-study mixed/negative result for this cue. In a GPT-4V
multimodal combination experiment, adding EP02 to a visual prompt lowers the
average score from 0.56 to 0.46, below the original 0.48 (§4.5, Table 2); this
is a combined multimodal condition, not a text-only test of EP02. The authors
also report that too much happiness can reduce performance (§4.7), but this is
not the target cue. The paper states that findings may not generalize to tasks
not evaluated and that GPT-4 reproducibility cannot be guaranteed (§5). This
is affirmative evidence that emotional cues can affect performance and direct
evidence of task-dependent reversal, but because it shares authors, method
family, and conceptual framing with S1, it is not an independent replication.
**Support:** mixed for exact importance-adjacent wording; positive for the
broader cue bundle. **Confidence:** low-to-moderate for cue-specific effects;
low for generalization.

**E3: C1, C2, C4 -> S3.** Vaugrante, Niepert & Hagendorff, *Prompt Engineering
Techniques for Language Model Reasoning Lack Replicability* (Transactions on
Machine Learning Research, Dec. 2025; initially circulated as *A Looming
Replication Crisis in Evaluating Behavior in Language Models? Evidence and
Solutions*, arXiv:2409.20303, 2024). This is an independent conceptual
replication. §2 defines EmotionPrompting as appending emotional language such
as “This is very important to my career.” The study uses five manually checked
reasoning benchmark subsets (150 questions each; n=750 total) and tests
GPT-3.5, GPT-4o (2024-05-13), Gemini 1.5 Pro, Claude 3 Opus, and Llama 3 8B/70B
(additional attempts with Vicuna 13B and BLOOM 176B); temperature is 0 or
0.00001. The researchers randomly select one of the original study’s 11
stimuli per task, rather than selecting the best-performing cue after the
fact. §3 reports a replication rather than a strict reproduction: benchmarks
and models differ, and the authors state that some original studies do not
document all evaluation choices. The published paper’s Appendix C, Fig. 4
shows the mean EmotionPrompting accuracy change pooled across models and
benchmarks as -0.25 percentage points. Its per-benchmark aggregate changes are
positive on CommonsenseQA (+2.25 pp) and negative on CRT (-2.25 pp), NumGLUE
(-0.17 pp), ScienceQA (-0.25 pp), and StrategyQA (-0.83 pp). The paper’s
abstract/conclusion reports no statistically significant difference for
nearly all tested prompt techniques; it does not establish equivalence or rule
out small effects. Its design is a particularly relevant counterweight to S1
because it randomizes among cues and evaluates correctness on hand-checked
reasoning questions across several model families. **Support:** null/mixed
evidence against a robust average boost; individual cue-by-task effects may
remain. **Confidence:** moderate for the narrow tested setup; low for a true
zero effect across all models/tasks.

**E4: C1, C2, C3, C4 -> S4.** Gao, Lee, Burtch & Fazelpour, *Take caution in
using LLMs as human surrogates* (PNAS 122(24), e2501660122, published 2025-06-13).
The article cites the career-importance EmotionPrompt and includes it among
three zero-shot prompt strategies in its 11–20 money request game (§“Zero-Shot
Prompts,” especially lines/paragraphs associated with SI Appendix Figs. S2–S4).
Eight models are evaluated with 1,000 independent sessions each in the core
game; models include GPT-3.5, GPT-4, Claude 3 Opus/Sonnet, Llama 2 7B/13B, and
Llama 3 8B/70B. The authors state that, in most cases, the tested strategies
do not make output distributions more human-like and have little effect for
the largest models; smaller models sometimes shift but not in a more
human-like direction. **Outcome caveat:** this is not correctness on an
objective task; its comparison is the distribution of requested amounts
against human participants in a strategic-choice game. The main text groups
EmotionPrompt with chain-of-thought and “take a deep breath” and points to SI
Figs. S2–S4; it does not report an isolated, cue-specific effect estimate in
the accessible main-text results. The stimulus may be personally consequential
wording and therefore overlaps SP-02. **Support:** weak/indirect null evidence
for cue-specific quality; useful evidence against assuming emotional prompting
reliably changes strategic behavior in advanced models. **Confidence:** low for
the importance cue itself; higher for the article’s reported broader null
pattern within this game.

## Thematic synthesis

1. **Positive evidence exists, but is bundled and concentrated.** S1 and its
same-team extension S2 report average benefits for sets of EmotionPrompts.
Those interventions combine multiple mechanisms. EP02 is “very important to
my career”: it labels importance but also asserts personal stakes. Nearby
phrases ask the model to review or be certain, which directly alter the
requested response process. Thus these experiments do not cleanly estimate
the effect of a bare priority label.

2. **Task-dependence is visible even in the original research program.** The
same EP02 cue performs well on Instruction Induction and poorly on
BIG-Bench-Hard (S2 §4.3). S3 finds small aggregate gains on one benchmark and
losses on four others when the cue family is randomized, with an overall
average near zero. This is inconsistent with a dependable across-task boost.

3. **The most directly relevant independent correctness replication is null
on average, not proof of no effect.** S3 reports -0.25 percentage points
pooled, with no statistically significant effect reported for nearly all
techniques; its benchmark-level changes swing both directions. Because it is
a conceptual replication with different tasks/models and random cue choice,
the contrast with S1 could reflect original stimulus selection, task/model
differences, evaluation procedures, stochasticity, or some combination. It
does not determine which explanation is correct.

4. **Negative effects are plausible but not conclusively isolated.** S2
documents a poor EP02 result on BIG-Bench-Hard and an adverse EP02 addition in
one combined GPT-4V condition. S3’s aggregate is slightly negative, but the
authors do not establish statistical significance for that isolated average.
These results support “can fail or reduce scores in some contexts,” not a
claim that importance cues generally harm performance.

5. **No calibration, time, token, or compute effect is established for the
target cue.** S1’s human ratings cover subjective quality/truthfulness/
responsibility, while S3 focuses on benchmark accuracy. S4 measures choice
distributions. The located studies do not provide an isolated, replicated
estimate of resource use or calibration effects from generic priority wording.

## Sources

| Source ID | Bibliographic identity and source | Role, provenance, independence | Quality, relevant claims, and use decision |
| --- | --- | --- | --- |
| S1 | Cheng Li et al. (2023), [*Large Language Models Understand and Can be Enhanced by Emotional Stimuli*](https://arxiv.org/abs/2307.11760), v7 revised 2023-11-12; technical report, short version accepted at LLM@IJCAI'23. | Primary report of 45 benchmark tasks and a human rating study. Microsoft Research, Chinese Academy of Sciences, William & Mary, HKUST, and Beijing Normal University authors; same team extends work in S2. | Direct source for cue wording, methods, task outcomes, and limits. Retained, with care around mixed cue constructs, post-hoc best cue, large relative BIG-Bench figure, and author-proposed mechanism. |
| S2 | Cheng Li et al. (2024), [*The Good, The Bad, and Why: Unveiling Emotions in Generative AI*](https://arxiv.org/abs/2312.11111), arXiv v3 revised 2024-06-07; published at ICML 2024. | Primary expanded empirical study; same principal authors/team and research program as S1, so not independent corroboration. | Retained for additional models/tasks and especially task-specific EP02 result; exact cue set remains emotionally and motivationally bundled. |
| S3 | Laurène Vaugrante, Mathias Niepert & Thilo Hagendorff (2025), [*Prompt Engineering Techniques for Language Model Reasoning Lack Replicability*](https://openreview.net/forum?id=bgjR5bM44u), TMLR, December 2025; initial arXiv version [2409.20303](https://arxiv.org/abs/2409.20303). | Primary independent conceptual replication by a separate author group; replication code is linked from the [authors’ public repository](https://github.com/Laurene-v/replicatingPET). | Retained as the strongest independent correctness test found. Its task/model changes and randomized cue assignment make it a conceptual replication, not a same-protocol reproduction; findings remain bounded to its benchmarks and model snapshot. |
| S4 | Yuan Gao, Dokyun Lee, Gordon Burtch & Sina Fazelpour (2025), [*Take caution in using LLMs as human surrogates*](https://www.pnas.org/doi/10.1073/pnas.2501660122), PNAS 122(24), e2501660122, 2025-06-13. | Peer-reviewed primary empirical study by an independent team; cites S1 as the importance-stimulus source. | Retained as adjacent null evidence for behavior response distributions. Not treated as a direct task-correctness result; importance cue’s isolated results require SI figures and are not quantified in main text. |
| S5 | Minda Zhao et al. (2026), [*Do Emotions in Prompts Matter? Effects of Emotional Framing on Large Language Models*](https://arxiv.org/abs/2604.02236), preprint, 2026-04-02. | Primary, later independent emotional-framing study; tests first-person affective prefixes rather than task-priority or career-importance wording. | Screened but not counted as direct evidence: abstract reports mostly small accuracy changes across six benchmark areas, but its emotion conditions do not operationalize the target generic priority cue. Useful as context only; excluded from C1 effect estimate. |

## Conflicts, limitations, and uncertainty

- **Construct validity is the central limitation.** The main tested “importance”
  phrase invokes career stakes; other EmotionPrompt sentences invoke
  self-efficacy, social approval, uncertainty checking, or task elaboration.
  These studies show the impact of particular composite verbal cues, not a
  clean dose-response relationship between stated task importance and
  performance.
- **Original positive estimates are not directly comparable to the replication.**
  S1 uses a suite of 11 prompts and reports an average as well as the best
  selected prompt. S3 randomly chooses a stimulus per task, changes benchmark
  items and models, and uses careful item vetting. Thus the null/mixed result
  challenges generality but does not adjudicate every exact prompt from S1.
- **Small samples/items and model snapshots limit inference.** S1’s 45 task
  averages and S2’s 50 benchmark tasks differ from high-repetition per-task
  inference; model naming/version detail is uneven in the older work. S3
  documents model versions and improves benchmark validation, but uses only
  150 questions per benchmark and near-deterministic decoding. S4 runs many
  repeated sessions but studies a single strategic game, and not answer
  accuracy.
- **Human rating outcomes are not interchangeable with correctness.** S1/S2
  use human quality ratings for open-ended output, which may capture
  readability and perceived responsibility as well as information quality.
- **Mechanisms remain uncertain.** Explanations involving attention, reward,
  effort, or “motivation” are interpretations; the studies do not establish
  that the model allocates more compute or effort because it believes a task
  matters.
- **Evidence gap:** in the sources located, there is no strong, independent,
  preregistered factorial test separating bare “this task is important/high
  priority” wording from personal stakes, emotional valence, additional
  instructions, and task content across multiple current model families.

## Validation

- **Claim-to-evidence:** C1 links to E1 (positive bundled evidence), E2
  (cue-specific task variation), and E3 (independent near-null pooled
  correctness result). C2 links to cross-task and cross-model results in E1–E4.
  C3 is explicitly bounded to the outcomes actually measured; no resource-use
  or calibrated-confidence estimate for the target cue was found. C4 is
  supported by the replication and task-dependent/conflicting findings.
- **Citation and provenance check:** primary article pages/PDF or publisher
  records were inspected rather than search snippets. S1 and S2 are grouped as
  one research-program provenance cluster; their two publications are not
  counted as independent corroboration. S3 and S4 are separate author teams.
  Specific evidence locations are given by article section, table, figure,
  or SI figure where available. Search-result summaries and non-primary
  explainers were used only as discovery leads and are not cited as evidence.
- **Coverage/stop rationale:** baseline and expanded queries covered explicit
  “important,” “priority,” “urgent,” “career” and EmotionPrompt terminology;
  citation paths from the original EmotionPrompt led to its ICML extension,
  the TMLR conceptual replication, and the PNAS study using the cue. Searches
  for standalone priority/urgency wording did not locate a stronger empirical
  primary study that isolates generic priority phrasing. The marginal returns
  of these focused paths were mainly adjacent affect/framing work rather than
  a clean test of the target cue, so the bounded search stopped here. This
  does not imply complete coverage of all literature.
- **Unmet requirement:** none for the assigned scope. Cue-specific data from
  S4’s SI figures were not available as an isolated numerical estimate in the
  main text; accordingly S4 is used only as qualified adjacent null evidence.
