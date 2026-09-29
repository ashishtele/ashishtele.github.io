---
layout: post
title: "Postgres Remembers, Claude Diagnoses: Our LangGraph Self-Heal Loop"
date: 2026-09-16
categories: [agents, evals, langgraph]
tags: [self-improving-loop, traces, postgres, azure-monitor, claude]
excerpt: "LangGraph traces died in Azure Monitor. We piped them to Postgres, let Claude perform the autopsy, and turned failures into evals."
---

## The problem: demo worked, prod rotted

Our LangGraph agent passed manual QA. Then real users touched it.

No single bug. Death by a thousand weird traces — wrong tool args here, planner loop there, retriever miss somewhere else. Azure Monitor had logs. Nobody was learning from them.

> Traces without a loop are just expensive receipts.

## The loop in one diagram

```
LangGraph run
  -> Postgres (structured traces: runs, steps, tool_calls, latency, tokens)
  -> Azure Monitor (logs / metrics / alerts)
  -> Claude pathologist (nightly job: read traces, categorize failures)
  -> Failure buckets -> new evals / prompt guards / router fixes
  -> redeploy -> repeat
```

Postgres is memory. Azure is eyes. Claude is brain.

## How we store it

Postgres, dead simple. No fancy vector store needed for this part.

```sql
-- runs: one row per LangGraph invocation
-- steps: one row per node/tool call with input, output, latency, error
CREATE TABLE agent_runs (
  run_id UUID PRIMARY KEY,
  started_at TIMESTAMPTZ,
  user_query TEXT,
  final_output TEXT,
  status TEXT
);

CREATE TABLE agent_steps (
  id BIGSERIAL PRIMARY KEY,
  run_id UUID REFERENCES agent_runs(run_id),
  node_name TEXT,
  tool_name TEXT,
  input JSONB,
  output JSONB,
  error TEXT,
  latency_ms INT
);
```

Azure Monitor keeps the raw logs + KQL for spikes. Postgres keeps the queryable truth.

### The eval design principles that make measurement meaningful

Anthropic's evaluation framework identifies four principles that distinguish a useful eval from a misleading one. First, **eval tasks must mirror production** — you sample tasks from the actual distribution your application sees in production, not from cases that are easy to generate or easy to grade. Second, **performance should improve with stronger models and more thinking**; if a more capable model at higher effort does not score better, the tasks are ambiguous or the grader is miscalibrated. Third, there must be **passable headroom at the frontier** — the best model at maximum effort should sit well below 100%, and that gap should come from genuinely hard cases, not impossible or underspecified ones. A telltale sign of a broken task is that it fails every evaluation run regardless of replication. Fourth, **run-to-run variance must be low** — high variance usually signals poorly designed tasks, a grader that produces different verdicts on identical output, or environmental leakage (leftover state from a previous trial handing the agent the answer). Our deterministic aggregates — terminal-state coverage, tool-count parity, citation coverage, latency percentiles, failure grouping by bounded error code — exist precisely to enforce these principles in code rather than hope.

A related trap: **adversarial sampling**. If you pick evaluation cases because today's model fails them, you are sampling the valleys of that model's capability surface rather than what is intrinsically hard or valuable for your application. The test is whether you can say *why* a task is hard before you include it. Include specific failures from production traffic, bug reports, or tickets — but do not blindly trust user traffic either, since users often try what they expect to work, skewing the distribution easy. Our eval set is stolen from prod, and that choice is validated by this principle: we measure on the actual distribution, not a model's failure fingerprint.

## Claude the pathologist

Nightly job. Not realtime — batch is cheaper and smarter.

Prompt skeleton:

```
You are a failure pathologist. Given LangGraph traces (steps + errors),
categorize each failed run into ONE bucket:
1. tool-arg hallucination
2. retriever miss
3. planner loop / retry storm
4. policy / guardrail violation
5. OTHER with proposed new bucket

Return JSON: {run_id, bucket, evidence_step_ids, one-line cause, suggested fix}
```

### Validating the grader before you trust it

Before the nightly job's judgments carry weight, the grader itself must be validated. We run the grader twice on the same model output and require the verdict to be stable — flapping graders are a silent source of noise. We hand-validate a sample of scored transcripts, because scoring failures are among the most common ways an evaluation is misconfigured. When a baseline exists, the judge reads both the candidate and baseline outputs in random order, blind to which is which, and picks the better one — this pairwise comparison is more reliable than absolute scoring. The judge model is never the model under test. Our `learnings` table enforces this rigor: a fix is stored only after a corrected execution succeeds, giving us ground-truth labels for any future judge validation.

## The reflection step: closing the loop when the score stalls

When the hillclimb score stalls for two or three rounds, the analyzer stops proposing edits and instead reads every remaining train failure and sorts them by root cause. This reflection step makes no edit — it only classifies. It is useful in three ways. First, reflecting across a collection of failures reveals patterns that single-case analysis misses. In Anthropic's case, the skill content was present but the model kept writing older API shapes from its training priors (for example, extended thinking with a fixed token budget, which the API now rejects on recent Opus models, instead of adaptive thinking; or older versions of the web search and web fetch tools instead of the current ones). The fix was a migration table at the top of the skill mapping remembered forms to current ones, which lifted performance from 77% to 80%. Second, tasks that never improve despite addressing obvious content gaps are tells that the example or the grader is flawed. One task asked for code that catches one error type while its grader expected a chain of at least three — the task was reworded. Another grader's instructions contradicted the documentation, and testing the real API proved the docs right. Fixing these grader bugs, along with more skill edits, brought performance to ~88%. Third, the reflection step catches ambiguous evaluation cases, harness errors, or run-to-run variance that would otherwise waste rounds on changes too small to measure.

Our own loop applies the same logic in the "Bucket → fix" stage: tool-arg failures led to a JSON-schema verifier eval that rejects bad arguments before execution (failure rate dropped 73% → 12%); planner loops triggered a step-count guard plus a "try different approach" nudge; retriever misses became a golden eval set of 50 production cases that every embedding change is tested against. One number that moved beats ten adjectives. The reflection step makes this systematic: stall → bucket by cause → fix top bucket → verify on train and test → repeat.

### The hillclimb guard: train/test split with revert-on-overfit

Every hillclimbing round splits the evaluation set randomly into a train set (which the analyzer may read) and a held-out test set (which it never sees). A proposed patch is kept **only if both train and test scores improve**. If the train score rises while the test score stays flat, that is an overfitting signal and the patch is reverted. If either score regresses, the patch is reverted. The final deployed version is the one that achieved the best score on the test set. Before the first round even runs, we verify that the evaluation's inherent noise — how far the score can move by chance alone — is smaller than the smallest improvement we would act on. If the noise floor is too high, we add more cases or more repetitions rather than chasing ghosts.

## What I learned

1. Batch beats realtime for learning. Nightly Claude job > streaming classifier.
2. Binary buckets beat scores. Yes/no "was this a tool-arg fail?" calibrates, 1-10 doesn't.
3. Humans moved up-stack: we stopped writing envs, now we just review Claude's buckets and bless fixes.
4. Your eval set should be stolen from prod. Ours is.

### Cost hillclimbing: a second objective when quality saturates

Hillclimbing is not only for quality. Anthropic ran a cost hillclimb on an internal customer-support benchmark starting from Opus 4.8 at high effort (74.4% accuracy, 4.6¢ per ticket). The hillclimber first audited the prompt, removing mandatory tool-call rituals, a scratchpad step, and contradictory rules. It then tried Opus 5.5 at low effort, clearing the accuracy bar at 87.8% and cutting cost to 1.9¢ per ticket. Because Opus 5.5 cleared the bar, it stepped down to Sonnet 5 at low effort — about the same accuracy (88.9%) at half the cost (1¢ per ticket). Finally, prompt improvements with routing rules and a refund-cap cross-reference brought Sonnet 5 to 98.9% at roughly the same cost. On 14 held-out tickets the search never saw, the final configuration scored 90.5% against the original 78.6%, at about one-fifth the cost. Our loop currently optimizes quality; adding cost or latency as a second objective — especially when quality headroom vanishes — is a direct extension of the same governed loop with a different scalar.

### Traps we avoided

Several anti-patterns are worth naming explicitly. **Never paste failure transcripts into the prompt** — that leaks test data into the training signal. **Keep the answers structurally out of the model's reach** — models can reward-hack by directly finding evaluation answers. **Don't hillclimb open-ended harness changes** — the surface must be cheap to iterate (prompts, skills, routing taxonomy) and the score change must be attributable to that surface. **Don't trust an evaluation near saturation** — if the baseline is already at 95%+, the hillclimb objective should shift to cost or latency, not quality. These guardrails are not theoretical; they are the difference between a loop that produces reproducible improvements and one that produces convincing-looking overfit.

### Related work: Anthropic's build-eval and hillclimb

Anthropic's `claude-api` skill implements `build-eval` (guided eval construction from production transcripts, bug reports, hand-written cases, and codebase synthesis, with grader validation and diagnostic checks) and `hillclimb` (train/test split, per-round patches, revert-on-overfit, reflection step on stall, cost/quality objectives). Our Postgres + nightly Claude job implements the same loop in a different stack: durable evidence in Postgres, operational telemetry in Azure Monitor, governed improvement via human review of proposed changes. The principles — production-mirroring tasks, binary graders, train/test guards, reflection on stall, governed deploy — transfer directly. The difference is architectural: Python ecosystem treats evals as separate SaaS (LangSmith, Langfuse, Weights & Biases); our loop treats eval as a transformation pipeline over data frames — traces → sample → grade → hillclimb → new artifact — all composable, all auditable.

## The real question

> When your agent fails at 2am, does it leave a lesson or just a log?

Ours leaves both now.

---

*Next: full code for the Postgres hook + Claude categorizer script? Say the word and I'll publish it.*