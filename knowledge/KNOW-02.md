---
id: KNOW-02
derived_from:
  - KNOW-02.AUD-01
  - KNOW-02.AUD-02
  - KNOW-02.AUD-03
  - KNOW-02.AUD-04
  - KNOW-02.AUD-05
---

# Feedback loops in AI-agent user workflows

## Navigation map

- [A quick orientation](#a-quick-orientation): what a user-facing loop is, and what it is not.
- [How the cycle works](#how-the-cycle-works): the parts and the role of feedback.
- [What people do in practice](#what-people-do-in-practice): observed patterns and their costs.
- [Cases by user need](#cases-by-user-need): where a loop may fit, what has been measured, and where evidence stops.
- [What the evidence supports](#what-the-evidence-supports): positive, mixed, null, and adverse results.
- [Configure and evaluate a loop](#configure-and-evaluate-a-loop): practical choices labeled by evidence type.
- [Quick reference](#quick-reference), [glossary](#glossary), [open questions](#open-questions), and [provenance](#provenance).

## A quick orientation

A feedback loop is a repeated work cycle in which a person and an AI system use what happened in one pass to decide what to do next. The person states an intent or constraint; the system returns an answer, proposed action, or changed artifact; someone inspects the result against a goal or evidence; and the next move may be to accept, edit, ask, redirect, verify, undo, or stop. The loop may be informal prompt-and-response, agent execution with checkpoints, or revision of a shared artifact. The terms and exact stages vary by task and study. ([S1 E1–E6](audit/KNOW-02.AUD-01.md); [S2 E1–E6](audit/KNOW-02.AUD-02.md))

“Feedback loop” can also mean something different: an agent may use environment observations to update its own plan, or researchers may train a model from feedback. Those system-side loops do not, by themselves, show how a user should steer or verify a workflow. This guide focuses on user-facing work; model-internal and training loops appear only as bounded evidence about possible mechanisms and failure modes. ([S1 E8](audit/KNOW-02.AUD-01.md); [S3 E5–E6, E8](audit/KNOW-02.AUD-03.md))

The evidence is varied and mostly task- and system-specific. Some studies directly observe people using agents; others compare a feedback feature or checkpoint policy; still others study ordinary assistants, controlled judgment tasks, or model-only repair. Access-to-AI studies do not isolate the effects of a feedback loop. A favorable result in one setting is not proof of better user workflow quality in general. ([S2 E1–E12](audit/KNOW-02.AUD-02.md); [S3 E1–E8](audit/KNOW-02.AUD-03.md))

## How the cycle works

The cycle is easiest to understand as four connected questions:

1. **What is the goal and current state?** The person supplies a task, constraints, context, and sometimes a starting artifact or plan.
2. **What changed?** The system responds, takes actions, proposes a revision, or reports a result. In tool-using work, useful feedback can include progress, action history, changed files, test output, or side effects—not just fluent text.
3. **What signal tells us whether it is better?** A person may compare the result with the request, source evidence, requirements, tests, or an independent reviewer. A system's own assertion that it succeeded is not automatically a reliable check.
4. **What should happen next?** Keep the result, make a targeted correction, gather missing information, undo or redo dependent work, hand the task back to the person, or stop.

This is a practical description synthesized from observed interaction patterns; it is not a tested universal taxonomy. Direct studies show the signal differs by work: relevance and evidence tracing in information seeking; diffs, execution and tests in coding; state and action history in multi-step tasks; and clarity or informativeness in review writing. ([S1 E2–E7](audit/KNOW-02.AUD-01.md); [S2 E2–E6](audit/KNOW-02.AUD-02.md); [S3 E4, E8](audit/KNOW-02.AUD-03.md))

Vendor documentation supplies concrete examples of how a configured loop can connect these parts: Anthropic describes a goal-based loop with a completion condition and turn limit; the OpenAI Codex repair example feeds validation results into a bounded next pass; and Microsoft Agent Framework documents evaluator feedback with a completion condition and iteration limit. These are product-specific capabilities or examples, not tested evidence that the patterns improve user outcomes. Microsoft's loop feature is marked experimental and has a stated language-availability limit. ([AUD-04 S1/E19, S3/E5–E6, S9/E101, E107](audit/KNOW-02.AUD-04.md); [AUD-05 C1](audit/KNOW-02.AUD-05.md))

The important distinction is between **a new turn** and **useful information**. Another prompt can merely invite the same system to reconsider its own output. A stronger loop has a reason to change course: a missed requirement, a source that contradicts a claim, a failing test, an observed wrong state, or a specific human correction. Benchmarks found that ungrounded model self-correction sometimes reduced accuracy, while a bounded repair setup improved some test-defined code outcomes and failed or regressed in others. These are adjacent benchmark results, not proof of user-workflow effects. ([S3 E5, E6, E8](audit/KNOW-02.AUD-03.md))

## What people do in practice

Observed practice is not “check every step.” In interviews with 17 experienced software-agent users, people commonly set boundaries and decompose work before execution, monitored agent progress only occasionally, then inspected diffs, tests, code, or artifacts afterward. Some relied on rough cues such as a long run or unusual number of turns; the interviews did not test whether these habits improve results. Each regeneration could make users feel they had to review the whole code change again. This is qualitative evidence from an expert-heavy, company-skewed sample, not a prevalence estimate. ([S2 E3](audit/KNOW-02.AUD-02.md))

Web-task traces show a wider range of interaction styles: hands-off supervision, active oversight, collaborative problem solving, and full takeover. Users intervened to correct wrong or premature actions, resolve stuck or redundant actions, or clarify preferences. In the analyzed trajectories, human actions made up 21.63% of steps on standardized tasks and 16.06% on free-form tasks; these descriptive shares do not tell us which level of intervention is best. ([S2 E4](audit/KNOW-02.AUD-02.md))

In a one-company study of 19 developers resolving open software issues, researchers observed both one-shot delegation and incremental issue resolution, where developers split work across prompts and reviewed intermediate results. Incremental resolution and requested refinements were associated with higher task success, but strategy was not randomized: issue difficulty, user skill, number of turns, and human edits could explain some or all of the difference. One participant abandoned a task after a long command sequence damaged the environment. The study also describes cases where an agent agreed with the latest correction rather than contributing a substantive diagnosis. ([S1 E1, E7](audit/KNOW-02.AUD-01.md); [S2 E5](audit/KNOW-02.AUD-02.md))

These reports suggest that a loop has a human attention cost: formulating context, noticing a meaningful change, checking the result, and repeating review after repairs. The research does not provide a common accounting of attention, latency, money, compute, rework, and quality, so costs from one case cannot be compared directly with another. ([S2 E1–E6](audit/KNOW-02.AUD-02.md); [S3 E4, E7–E8](audit/KNOW-02.AUD-03.md))

## Cases by user need

### When you need to shape a shared artifact as work unfolds

**Fit:** a task where the person can see and change the same artifact as the agent, and where preferences or quality criteria may become clearer during work—such as drafting an ad or developing a code patch.

In a randomized ad-creation experiment, 2,234 participants worked in human–AI or human–human pairs in a shared chat-and-editing workspace for up to 40 minutes. The AI could edit text, select or generate images, message, or wait; people could respond, edit, select, and submit. Human–AI pairs produced 50% more ads per worker, received higher text ratings but lower image ratings, and produced less diverse outputs than human–human pairs. In a separate live ad test, the overall performance difference between team types was not clear. This measured the effect of being paired with an AI in that workspace; it did not isolate iteration, feedback frequency, or delegation as the cause. ([S2 E1](audit/KNOW-02.AUD-02.md))

**Configure from the case:** expose the evolving artifact and meaningful actions; let the user state preferences and make direct edits; make the task endpoint visible. The study's session ended after 40 minutes or submission, which is an experimental boundary, not a recommended stopping rule. The system called the model every ten seconds, but that implementation detail does not establish an optimal cadence. User time was bounded by the session; model cost and the value of extra review were not reported in a comparable way. ([S2 E1](audit/KNOW-02.AUD-02.md))

**Limit:** throughput and one quality dimension improved while other dimensions worsened. More output is not the same as better work, and this experiment cannot establish that the same design will help research, coding, or other creative tasks. ([S2 E1](audit/KNOW-02.AUD-02.md))

### When you need to supervise a multi-step agent before errors spread

**Fit:** tasks with a sequence of dependent actions where the user can inspect state or history and recover from an earlier mistake. A useful checkpoint is one where the user can still prevent or limit downstream rework.

In a formative study, participants used a pattern the authors called **Confirmation–Diagnosis–Correction–Redo**: the user confirms the current state; if it is wrong, diagnoses the first incorrect step, corrects the instruction or state, and initiates redo of dependent work. In the controlled comparison, the task stopped when the task was complete. That is the study endpoint, not a general user stopping rule. A comparison with 48 participants tested model-scheduled intermediate confirmations against confirmation only at the end in simulated shopping, image-editing, and Overcooked tasks. Intermediate confirmation lowered completion time by 13.54% on average (35.84 seconds) and was preferred by 81%. The benefit varied with the simulated error location: about 29% time savings for early errors, around 2% for mid-task errors, and a 4.5% time increase for late errors. Checkpoints added inspection time but reduced diagnosis and redo time. ([S1 E5](audit/KNOW-02.AUD-01.md); [S2 E2](audit/KNOW-02.AUD-02.md))

This is the clearest direct test of a loop policy in the reviewed set, but it is a simulation with fixed agent accuracy and time, bounded tasks, and a comparison against end-only confirmation. It measured completion time and preference, not improved work quality or safety in live research or office work. Some formative users missed the first error or found a step hard to confirm; some skipped steps using domain knowledge, and some manually fixed a minor error rather than request a redo. ([S2 E2](audit/KNOW-02.AUD-02.md))

**Configure from the case:** place a checkpoint before consequential dependent steps, show enough action history or state to identify what changed, and provide a correction/redo path. This is a practice-based design recommendation informed by the simulation, not a proven universal schedule. No universal optimal checkpoint cadence or stopping rule has been established. ([S2 E2](audit/KNOW-02.AUD-02.md); [S3 C6](audit/KNOW-02.AUD-03.md))

Vendor frameworks document related controls in their own settings: Microsoft Agent Framework describes evaluator-driven repetition with a default iteration limit, while Azure's maker-checker pattern sends specific checker feedback back to the maker and describes a cap and fallback. Treat these as implementation examples for multi-step work; they do not corroborate the simulation's timing result or establish an effective checkpoint schedule in other products. ([AUD-04 S9/E101, S11/E103, E107–E108](audit/KNOW-02.AUD-04.md); [AUD-05 C1, C3](audit/KNOW-02.AUD-05.md))

### When the system can anticipate useful moments for intervention

**Fit:** browser workflows where a user may want to pause, correct a preference, or take over when an action is wrong, redundant, premature, or stuck.

CowPilot trajectories document these intervention patterns across 400 web-navigation tasks and over 4,200 interleaved human and agent actions. A follow-up with 16 users compared CowPilot with PlowPilot, which added an intervention-aware module while keeping the execution agent unchanged. PlowPilot scored 36.8% higher on average across six subjective usefulness, control, and alignment dimensions. The outcome was user ratings, not objective task success, accuracy, or time; the small follow-up and user mix limit causal and broader conclusions. The trace corpus and follow-up support a design possibility, not proof that more interventions improve work. ([S2 E4](audit/KNOW-02.AUD-02.md))

**Configure from the case:** make pause, correction, takeover, and return-to-agent available; use intervention signals to decide when to offer control, not to force the user into a fixed number of checks. The observed workflow stopped when the task was complete or the user continued taking over; the study did not test a universal stopping rule. Treat this as a hypothesis to evaluate locally. A resource-cost comparison was not reported. ([S2 E4](audit/KNOW-02.AUD-02.md))

### When you need to revise writing with specific, optional feedback

**Fit:** writing where a reviewer can decide whether an identified issue is valid and revise the text themselves.

In an ICLR 2025 randomized deployment involving more than 44,000 reviews selected for feedback or control, a review-feedback agent offered optional suggestions in three categories: vague critique, possible misreading, and professionalism. The system used reliability checks and retried at most once; if it failed again, it withheld the comment. Of those who received feedback, 26.6% updated their review, compared with 9.4% in control. In a selected subset of 100 revised review pairs, two blinded human researchers preferred the updated review 89 times, describing it as clearer or more informative. Yet the full randomized comparison found no significant difference in average score changes. Suggestion incorporation was classified by another LLM, and the blind quality comparison selected reviews with substantial uptake; neither establishes factual correctness or improved paper decisions. The feedback was optional and reviewers retained control. ([S3 E4](audit/KNOW-02.AUD-03.md))

**Configure from the case:** make feedback specific to an observable issue, keep it optional, preserve the author's ability to edit or decline, and fail closed when the feedback system's reliability checks fail. These are practice-based recommendations from one writing system's design and outcome; the study did not compare retry limits or prove that two attempts is an optimal stopping rule. Human reading and editing effort and total service cost were not measured. ([S3 E4, C6](audit/KNOW-02.AUD-03.md))

### When you need to steer research or analysis as understanding changes

**Fit:** open-ended information work where the question may change as sources, data, or hypotheses emerge. Useful loop signals include the evidence behind a claim, the actions a research agent took, relevance to the current question, and whether a hypothesis survives a check.

In a formative interactive deep-research study, 15 frequent users received training, completed tasks, and rated features. Users wanted visibility into research dependencies and timely steering; a research-action dependency graph received a 4.7/5 rating. The study documents a way to inspect and trace research actions, not an improvement in report accuracy or task completion. Its in-product, user-specific stopping or research-adequacy criterion was not reported. ([S1 E2](audit/KNOW-02.AUD-01.md); [S2 E6](audit/KNOW-02.AUD-02.md))

In a participatory prompting study with 15 people doing data analysis using Bing Chat, participants alternated between information foraging and hypothesis development/testing, reflecting on answers and sometimes pivoting to a new question. They reported help with gathering information and ideating hypotheses or tests, alongside difficulty formulating queries, supplying context, assessing relevance, and verifying claims. A researcher mediated prompting, and there was no randomized comparator or objective causal outcome. One example ended when the participant was satisfied, but a general user-specific stopping or adequacy criterion was not reported. ([S1 E3](audit/KNOW-02.AUD-01.md); [S2 E10](audit/KNOW-02.AUD-02.md))

**Configure from the cases:** preserve links from conclusions to sources and from actions to intermediate state; let the user revise the question or inject constraints; verify key claims against sources or data. These suggestions match documented user needs and study procedures, but evidence for their effect on final quality, time, or effort remains unestablished. One real questionnaire-analysis case reports progressive refinement of requests with a conversational assistant, but it involved a single analyst and retrospective assessment, not an autonomous agent efficacy test; its stop conditions were not standardized, and a user-specific adequacy criterion was not reported. ([S1 E2–E3](audit/KNOW-02.AUD-01.md); [S2 E6, E10–E11](audit/KNOW-02.AUD-02.md))

### When you are tempted to ask the model to “check itself”

Treat this as a distinct, adjacent case rather than established user workflow advice. On reasoning benchmarks with 2023 models, up to two rounds of intrinsic self-correction without an oracle signal reduced accuracy in the reported settings; correct answers were sometimes changed to wrong ones. In paired code-conformance benchmarks, requiring explanation or repair increased false rejection of correct code in some model/task conditions. By contrast, a bounded LLM code-repair benchmark that reran functional and exploit tests improved some narrow-scope cases, while other projects did not converge or regressed. Crucially, S3 E8 reuses the same functional and exploit test signal to guide repair rounds and define the final pass score; the test is external to the model's self-report, but the final score is not independent of the loop feedback signal. All three are model or artifact benchmarks, not studies of a user steering an agent. ([S3 E5, E6, E8](audit/KNOW-02.AUD-03.md))

The transferable caution is modest: another generation is not evidence of improvement. If there is no new, discriminating evidence, a retry can reinforce an error, undo a correct result, or consume resources. The claim that new, checkable evidence makes continuation more defensible is a cross-case inference, not a protocol tested across user workflows. ([S3 E3, E5–E8](audit/KNOW-02.AUD-03.md))

## What the evidence supports

| Evidence status | What was found | What it does not show |
|---|---|---|
| **Positive, bounded direct evidence** | Intermediate confirmation reduced simulated task completion time overall versus confirm-at-end, with gains concentrated in early errors and a late-error penalty. Optional review feedback improved blind human ratings in a selected writing subset, while overall score change was not significant. ([S2 E2](audit/KNOW-02.AUD-02.md); [S3 E4](audit/KNOW-02.AUD-03.md)) | A universal advantage from adding checkpoints, feedback, or extra turns; improved safety or factual accuracy across workflows. |
| **Mixed direct outcomes** | AI-human ad teams produced more ads per worker and higher-rated text, but lower-rated images and less diverse output; overall live-ad performance did not clearly differ. ([S2 E1](audit/KNOW-02.AUD-02.md)) | That iterative collaboration itself caused any of these differences. |
| **Descriptive practices and perceptions** | Developers described pre-planning, sparse monitoring, post-hoc review, and repeated review effort; web users used several intervention styles; deep-research users rated visibility features; researchers observed iterative analysis and verification barriers. ([S2 E3–E6, E10](audit/KNOW-02.AUD-02.md); [S1 E2–E3](audit/KNOW-02.AUD-01.md)) | A causal improvement in quality, speed, or user effort from these practices. |
| **Adverse or cautionary adjacent evidence** | Biased AI feedback shifted later judgments in a controlled perceptual task; offering an edit option increased confidence and algorithm uptake but worsened accuracy in a stylized forecast task; model-only self-correction harmed benchmark accuracy in tested settings. ([S3 E1, E3, E5](audit/KNOW-02.AUD-03.md)) | That human feedback or revision always harms; these are task-bound results and not general agent-workflow tests. |
| **Access-to-AI, not loop evidence** | METR's early-2025 coding-assistant RCT found tasks took 19% longer despite participants estimating time savings; a later estimate was weak because selection and time-accounting problems limited its interpretation. ([S3 E7](audit/KNOW-02.AUD-03.md)) | Any effect attributable to a feedback-loop policy; the studies compared access to tools, not loop designs. |
| **Nulls and unknowns** | The ICLR trial found no significant average score-change difference. S2 did not locate a direct user-agent trial that isolates an overall null feedback effect. No located direct study randomized adaptive versus fixed/user-controlled stopping while measuring independent work quality and user/resource cost. ([S3 E4, C6](audit/KNOW-02.AUD-03.md); [S2 C5–C6](audit/KNOW-02.AUD-02.md)) | Absence of evidence is not evidence that no such effects or studies exist. The search was bounded, not exhaustive. |

Taken together, the evidence supports conditional claims, not a universal formula. Reliable, task-relevant feedback can help in a bounded setting; biased, weak, or absent feedback can mislead; human involvement alone does not ensure an accurate result; and benefits can be offset by review, interruption, or rework. Most evidence is task/system specific, and many direct agent studies compare access or a feature bundle rather than isolate the loop itself. ([S2 C2–C6](audit/KNOW-02.AUD-02.md); [S3 C1–C6](audit/KNOW-02.AUD-03.md))

## Configure and evaluate a loop

The following are recommendations for local design and use. The labels describe their basis; they do not imply that a full protocol has been validated.

### Choose a signal before choosing a cadence

- **Evidence-backed, bounded:** In simulation, the value of an intermediate checkpoint depended on when an error occurred; early errors left more work to recover, while late checkpoints could cost more time. Use this as a reason to consider consequence and recoverability when placing checks, not as a universal schedule. ([S2 E2](audit/KNOW-02.AUD-02.md))
- **Practice-based:** Match the check to the artifact: source trace for a research claim, requirement or test for code, current state/action history for a multi-step task, and a specific clarity or interpretation issue for writing. These signals appear in the reviewed cases, but the combination has not been tested as one general policy. ([S1 E2–E7](audit/KNOW-02.AUD-01.md); [S2 E2–E6](audit/KNOW-02.AUD-02.md))
- **Inference:** A feedback signal is more useful when it can distinguish plausible success from a specific failure and can change the next action. This follows across evidence on signal quality, checkpoints, model self-correction, and test-grounded repair; it has not been tested as a single user-workflow rule. ([S3 E1, E3, E5–E8](audit/KNOW-02.AUD-03.md))

### Make the next action explicit

At each check, decide which of these outcomes is warranted: accept and proceed; edit the artifact directly; ask for a targeted correction; gather or trace more evidence; undo and redo dependent steps; take over; or stop. In observed coding, web, and checkpoint cases, people used several of these options rather than always continuing with another prompt. ([S2 E2–E5](audit/KNOW-02.AUD-02.md))

**Practice-based recommendation:** tell the agent what changed and what criterion failed, then ask for a bounded correction. Do not make the next cycle merely “try again” unless the system has new information to use. This is a design inference from reported repair patterns and adjacent findings about ungrounded correction; a direct comparative trial of this wording was not located. ([S1 E1, E5](audit/KNOW-02.AUD-01.md); [S3 E5–E8](audit/KNOW-02.AUD-03.md))

Vendor-authored guidance adds implementation options, not proof of effectiveness: Anthropic recommends applying loop patterns selectively and describes turning repeated checks into custom Claude Code verification loops; OpenAI's Codex example bounds repair attempts and stops on a pass, no remaining delta, or a need for human review. Microsoft advises bounding autonomous loops because completion can fail and judges may be probabilistic, and its Azure architecture guidance recommends criteria, an iteration cap, and fallback. These product-specific recommendations do not establish that any particular cap or arrangement is optimal. ([AUD-04 S1/E2, S2/E4, S3/E6, S9/E107, S11/E108](audit/KNOW-02.AUD-04.md); [AUD-05 C2](audit/KNOW-02.AUD-05.md))

### Set checkpoints and stopping around consequence and evidence

There is no established universal optimal cadence or stopping rule. The closest direct timing result is simulated and shows benefits vary with error location. The ICLR service's two-attempt, fail-closed behavior is a documented engineering choice, not a comparison proving two attempts is best. The bounded repair benchmark uses a fixed cap and stops on its own tests, but those same tests drive the loop and can miss defects. ([S2 E2](audit/KNOW-02.AUD-02.md); [S3 E4, E8](audit/KNOW-02.AUD-03.md))

The vendor examples likewise show design choices rather than validated thresholds: Codex's repair example uses a configurable maximum number of attempts; Microsoft Agent Framework documents a default maximum of 10 iterations and marks looping experimental; Azure guidance calls for an iteration cap and fallback without establishing an optimal value. The cap should therefore be treated as a product-specific bound, not a general recipe. ([AUD-04 S3/E6, S9/E101, E107, S11/E108](audit/KNOW-02.AUD-04.md); [AUD-05 C1–C2](audit/KNOW-02.AUD-05.md))

**Inference for local use:** stop or hand back when the check does not provide a new actionable signal, when repeated attempts do not reduce a named failure, when the remaining work is not worth the likely recovery, or when an independent check cannot support acceptance. These are sensible evaluation conditions, not empirically optimized thresholds. Record whether termination came from success, a retry cap, a user decision, or unresolved failure. ([S3 C6, E8](audit/KNOW-02.AUD-03.md))

### Verify with an outcome that is not just the loop's own signal

Where possible, keep separate: (a) the feedback that guides the next cycle, and (b) the outcome used to judge whether the workflow succeeded. A failing test can guide a repair; a broader held-out test suite or human review can assess the result separately. However, S3 E8's functional and exploit tests are reused as both feedback and final secure-and-correct criterion, so that benchmark's final score is not independent of the loop signal. The authors also report test-coverage limits. In the ICLR writing case, automated checks gated comments, while blind human review provided a distinct, subjective revision-quality judgment on a selected subset. ([S3 E8](audit/KNOW-02.AUD-03.md); [S3 E4](audit/KNOW-02.AUD-03.md))

When evaluating a local loop, record the task and system; comparator; signal and its reliability; next-cycle action; stop condition; human review time; latency/compute or money where available; rework and failures; and outcome quality. Keep objective task measures separate from satisfaction, uptake, confidence, output length, or the system's own pass signal. Existing studies often report only part of this picture, and no shared cross-study cost measure exists. ([S2 E1–E6](audit/KNOW-02.AUD-02.md); [S3 C5, E7–E8](audit/KNOW-02.AUD-03.md))

## Quick reference

| User need | Useful loop element to consider | Evidence boundary |
|---|---|---|
| Shape a shared draft or artifact | Visible shared state, direct edits, preference correction | Ad creation showed mixed outcome dimensions; feedback policy was not isolated. ([S2 E1](audit/KNOW-02.AUD-02.md)) |
| Prevent errors spreading through dependent steps | Check state/action history before costly downstream work; support correction and redo | Positive overall timing result only in a bounded simulation; effect varied by error timing. ([S2 E2](audit/KNOW-02.AUD-02.md)) |
| Let users intervene in browser tasks | Pause, clarify, take over, and return control | Trace patterns plus small subjective feature comparison; objective task gains unknown. ([S2 E4](audit/KNOW-02.AUD-02.md)) |
| Improve a written review | Specific optional feedback, author choice, reliability gate | Selected blind quality subset positive; overall score changes null. ([S3 E4](audit/KNOW-02.AUD-03.md)) |
| Explore research or data | Trace actions and sources; revise question/hypothesis; verify claims | User needs and mediated practice documented; causal work-quality gains unknown. ([S1 E2–E3](audit/KNOW-02.AUD-01.md)) |
| Ask the model to reconsider | Require new evidence or an external check before accepting a revision | Model-only benchmarks include degradation; test-grounded repair is bounded and not user-workflow evidence. ([S3 E5–E8](audit/KNOW-02.AUD-03.md)) |

## Glossary

- **Feedback signal:** Information used to judge the current result or state and choose a next action; examples include a source, test, user correction, action history, or human review.
- **Checkpoint:** A planned opportunity to inspect progress before dependent work continues.
- **Confirmation–Diagnosis–Correction–Redo (CDCR):** The checkpoint and repair sequence identified in the multi-step task study: confirm state, diagnose the first error, correct, and redo affected steps. ([S1 E5](audit/KNOW-02.AUD-01.md))
- **Post hoc review:** Inspection after an agent has completed a set of actions or produced an artifact, such as checking a code diff or final research report. ([S2 E3](audit/KNOW-02.AUD-02.md))
- **Independent outcome check:** An assessment separate from the signal that drives another cycle. “Independent” does not necessarily mean objective or infallible; blind human review, ground-truth labels, or separate tests have different strengths and limits. ([S3 E4, E8](audit/KNOW-02.AUD-03.md))
- **Agent-internal loop:** A system-side action/observation or self-correction process. It is not the same evidence as a person steering a user workflow. ([S1 E8](audit/KNOW-02.AUD-01.md))
- **Access effect:** The effect of being offered an AI tool compared with a control condition. It cannot by itself identify which loop behavior caused a change. ([S2 C3](audit/KNOW-02.AUD-02.md); [S3 E7](audit/KNOW-02.AUD-03.md))

## Open questions

The reviewed evidence does not establish an optimal number or spacing of checkpoints, an adaptive stopping policy for real user workflows, or a general quality gain from more cycles. No located direct user-agent trial jointly varied signal reliability, checkpoint/stopping policy, and external verification while measuring independent work quality and human/resource cost. ([S2 C3, C6](audit/KNOW-02.AUD-02.md); [S3 C6](audit/KNOW-02.AUD-03.md))

Direct research and analysis cases mainly document affordances, user preferences, and verification burdens rather than causal effects on final accuracy, quality, or time. The available findings also leave long-term adaptation, representative production failures, and comparable accounting of attention, latency, money, compute, and rework unresolved. These are gaps in this bounded evidence set, not proof that no relevant studies exist. ([S2 C6](audit/KNOW-02.AUD-02.md); [S2 Conflicts and limitations](audit/KNOW-02.AUD-02.md))

## Provenance

This is a bounded synthesis of five reviewed audits, not an exhaustive survey or systematic review. The evidence cited at each claim retains the S1/S2/S3 research audit and E# so a reader can inspect study methods, source details, limitations, and confidence judgments. Vendor-derived additions are cited to the vendor-source audit and evidence entries; the S2 integration audit records their placement and exclusions:

- [S1 — KNOW-02.AUD-01 audit: terminology, mechanisms, and direct user–AI workflows](audit/KNOW-02.AUD-01.md)
- [S2 — KNOW-02.AUD-02 audit: agent workflow cases and measured outcomes](audit/KNOW-02.AUD-02.md)
- [S3 — KNOW-02.AUD-03 audit: signal quality, verification, revision, and stopping](audit/KNOW-02.AUD-03.md)
- [LR-07 S1 — KNOW-02.AUD-04 audit: first-party vendor loop guidance and examples](audit/KNOW-02.AUD-04.md)
- [LR-07 S2 — KNOW-02.AUD-05 audit: integration sufficiency and trace](audit/KNOW-02.AUD-05.md)

Claims about what studies measured are empirical findings; descriptions of what users did are observed or reported practices; explanations that connect results across different studies are identified as inference; and configuration advice is labeled as a recommendation. Vendor documentation is used only for the capabilities, examples, and recommendations it documents; vendor-reported outcomes remain distinct from independently tested effects. The two new audit records document the source trail and exact integration decisions, not additional empirical evidence. Study outcomes remain specific to their tasks, systems, comparators, and measures.
