---
layout: single
sidebar: true
author_profile: true
title: "Postgres Remembers, Claude Diagnoses: My LangGraph Self-Heal Loop"
excerpt: "LangGraph traces died in Azure Monitor. I piped them to Postgres, let Claude perform the autopsy, and turned failures into evals."
description: "Self improving loop can benefit a long way"
tags: ["LLM", "AGI", "Python", "systemdesign"]
published: true
comments: true
header:
  teaserlogo:
  teaser: /images_1/llm_eval.jpg
  image: /images_1/llm_eval.jpg
  caption: "courtesy: OpenAI"
gallery:

  - image_path: ''
    url: ''
    title: ''
---

Hi All,

My LangGraph agent passed manual QA and cleared dev deployment. Then real users hit it in a higher environment. There was no single bug — instead, thousands of odd traces: the orchestrator routing to the wrong corpus in one case, the retriever missing entirely in another. Azure Monitor was capturing all of it. Nobody was learning from it.

> Traces without a loop are just expensive receipts.

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

Azure Monitor keeps the raw logs. Postgres keeps the queryable truth.

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

## Bucket -> fix: closing the loop

This is the part most posts skip. Don't.

- tool-arg fails -> added JSON-schema verifier eval, reject before execute
- planner loops -> added step-count guard + "try different approach" nudge
- retriever misses -> turned 50 prod misses into golden eval set, test every embedding change against it

## What I learned

1. Batch beats realtime for learning. Nightly Claude job > streaming classifier.
2. Binary buckets beat scores. Yes/no "was this a tool-arg fail?" calibrates, 1-10 doesn't.
3. Humans moved up-stack: we stopped writing envs, now we just review Claude's buckets and bless fixes.
4. Your eval set should be stolen from prod. Ours is.

Thanks,
Ashish
