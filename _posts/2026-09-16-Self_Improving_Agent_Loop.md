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

**TODO (Ashish: paste your real top 3 buckets here with % + 1 redacted trace each)**

- Bucket 1: [e.g. tool-arg hallucinations — 40%] — example trace snippet
- Bucket 2: [e.g. planner loops — 25%] — example trace snippet
- Bucket 3: [e.g. retriever misses — 20%] — example trace snippet

## Bucket -> fix: closing the loop

This is the part most posts skip. Don't.

- tool-arg fails -> added JSON-schema verifier eval, reject before execute
- planner loops -> added step-count guard + "try different approach" nudge
- retriever misses -> turned 50 prod misses into golden eval set, test every embedding change against it

**TODO: add your one number that moved** — pass rate, cost per task, p95 latency. One number beats ten adjectives.

## What I learned

1. Batch beats realtime for learning. Nightly Claude job > streaming classifier.
2. Binary buckets beat scores. Yes/no "was this a tool-arg fail?" calibrates, 1-10 doesn't.
3. Humans moved up-stack: we stopped writing envs, now we just review Claude's buckets and bless fixes.
4. Your eval set should be stolen from prod. Ours is.

## The real question

> When your agent fails at 2am, does it leave a lesson or just a log?

Ours leaves both now.

---
*Next: full code for the Postgres hook + Claude categorizer script? Say the word and I'll publish it.*
