---
layout: single
sidebar: true
author_profile: true
title: "OpenEvidence — A System Design Deep Dive"
excerpt: "how ~30 engineers serve 65% of US physicians at 13 seconds per answer."
description: "how ~30 engineers serve 65% of US physicians at 13 seconds per answer."
tags: ["LLM", "AGI", "Python", "systemdesign"]
published: true
comments: true
header:
  teaserlogo:
  teaser: /images_1/openevidence.png
  image: /images_1/openevidence.png
  caption: "courtesy: OpenAI"
gallery:

  - image_path: ''
    url: ''
    title: ''
---
Hi All,

As I am building more and more AI products, I feel understanding some well crafted products help learn a lot. [OpenEvidence](https://www.openevidence.com/) is one THE products.

## <span style="color: #FF6B6B;">1. The Product, Stated as a System Contract</span>

OpenEvidence is a natural-language question-answering engine over peer-reviewed medical literature, used at the point of care. Strip away the medicine and the system contract reads like this:

| Requirement | Target | Basis |
|---|---|---|
| Latency (p50) | ≤ 15s for a complete cited answer | [C] Measured mean 13s (medRxiv study); vs 259s manual lookup |
| Latency (perceived) | First token visible in ~1s | [I] Streaming UI behavior |
| Availability | 99.99% | [C] Engineer-attributed uptime figure |
| Correctness constraint | **No claim without a citation.** Refusal is acceptable; fabrication is not | [C] Stated product guarantee; enforced architecturally |
| Traffic shape | Extreme diurnal spikes (7–9am rounds, conference surges, viral events) | [C] Documented 1000x surge survival |
| Scale | 27M consults/month, ~650K US clinicians + 1.2M intl | [C] Company claims |
| Compliance | HIPAA, SOC 2 Type II, encryption in transit/at rest, BAAs | [C] |

The correctness constraint is the load-bearing wall of the entire design. It dictates retrieval-first architecture, citation enforcement at generation time, and fail-degraded failure semantics.

## <span style="color: #FF6B6B;">2. Capacity Estimation (Back of Envelope)</span>

All numbers derivable from public claims:

```
Consults            27M/month          → 6.3M/week       → ~104/sec average
Peak multiplier     ~5x (clinical diurnal pattern)        → ~520 consults/sec peak

Model calls         "billions/week" (Baseten)
Implied fan-out     2B / 6.3M ≈ 300+ internal calls per consultation
                    (embedding, multi-pass retrieval, rerank batches,
                     generation chunks, citation verification)

Sustained call rate 3,300/sec avg → ~16,500/sec peak
```

**Embedding layer sizing [I]:**
Batched embedding inference on H100-class hardware: ~3K inf/s/node.
At peak, if ~40% of calls are query embeddings: `16,500 × 0.4 / 3,000` ≈ **7 nodes**, ×3 redundancy ≈ 20 GPUs. Trivial.

**Generation layer sizing [I]:**
Little's Law: concurrent requests = arrival rate × duration = `(27M/30/86,400) × 5 peaks × 13s` ≈ **680 concurrent streams**.
At ~75 streamed generations per GPU node (continuous batching, ~800-token outputs): **~9 nodes**, ×3 multi-cloud redundancy ≈ **27 H100 nodes total fleet**.

**Cost [I]:**
27 nodes × 24h × 30d × $2.50/hr ≈ $50K/mo generation + embeddings/rerank overhead → **<$1M/month total inference** against $8.3M/month revenue. Cost per consult: **$0.02–0.05 against $3.70 revenue**.

> [!important] The headline finding
> There is no hidden supercomputer. The entire serving fleet fits in a single rack's power budget. If they run frontier-class models instead of ~70B fine-tunes, multiply by 2–4x — still under 10% of revenue.

---

## <span style="color: #FF6B6B;">3. High-Level Architecture</span>

![Hybrid Architecture](/images_1/openevidence.png)

---
## <span style="color: #FF6B6B;">4. Component Deep Dives</span>

### 4.1 Edge & Frontend

* **Stack:** Next.js on Vercel (frontend) + Python on GCP (backend). The split mirrors
team composition — mostly Python/ML engineers, one small frontend team — and keeps
each team's deploy surface separate: the frontend team never touches GCP, the
backend team never touches Vercel config.

* **Fluid compute as a scaling lever:**
Vercel's [Fluid compute](https://vercel.com/fluid) keeps functions warm between requests instead of spinning up
a fresh container per call. After enabling it, OpenEvidence saw serverless spend drop
90%, with fewer cold starts and no reliability tradeoff [1]. The mechanism: billing
shifts from wall-clock time to active-CPU time, which matters a lot for a workload
that's mostly waiting on an LLM stream rather than computing.

* **Deploy velocity as a reliability property, not just a DX nicety:**
Every commit gets a preview URL; prod deploys take minutes, not hours.
For a small team absorbing viral growth, this matters structurally: fixes ship
before problems compound, rather than queuing behind a slow release cycle. Velocity
*is* the mitigation for a team too small to run extensive pre-release QA.

* **Perceived latency ≈ time-to-first-token:**
The frontend shell renders instantly and streams tokens as they arrive. Because the
UI never blocks on the full response, perceived latency tracks time-to-first-token,
not total generation time — which is the right metric to optimize for in a
streaming-LLM product, and different from what you'd optimize for in a traditional
request/response API.

* **EHR embed and its downstream effect on 4.2:**
OpenEvidence is embedded inside Epic via FHIR-based integrations, live at Sutter
Health and Mount Sinai [2][3]. This isn't just a distribution channel — it reshapes
the query distribution the backend sees: queries arrive mid-chart, short, urgent,
and clustered by clinical specialty. That skew is what motivates [the caching /
model-routing strategy in 4.2] — worth a forward pointer here so the reader knows
why this detail is in an infra section at all.

---
[1] Vercel customer case study, "How OpenEvidence built a healthcare AI that
    physicians actually trust" (2026)
    
[2] Beckers Hospital Review / Sutter Health press release, Feb 2026

[3] Healthcare IT News, Mount Sinai enterprise Epic integration, Mar 2026

### 4.2 Identity & Trust Layer

Unique among consumer AI products: every user is a **verified clinician** via NPI number [C]. This is simultaneously:

1. **An abuse firewall** — no anonymous scraping of a corpus that cost millions to license
2. **A regulatory posture** — the product gives information to professionals, not medical advice to consumers
3. **A business asset** — pharma advertisers pay $70–150 CPMs precisely because the audience is verified prescribers
4. **A query-distribution prior** — knowing the specialty and role of every queryer improves routing [I]

### 4.3 Query Understanding & Orchestration

A clinical question rarely decomposes to one retrieval pass. *"Should this 68yo with CKD get metformin?"* implies sub-queries across dosing, renal contraindications, guideline position, and recent trial evidence. Observable product behavior (multi-section answers, mixed source types per section) implies:

- **Sub-question decomposition** — the orchestrator splits complex questions into evidence-seeking sub-queries
- **Parallel retrieval fan-out** — each sub-query runs its own retrieve→rerank cycle concurrently; total retrieval latency = slowest branch, not sum of branches
- **Specialty routing** — queries route toward specialty-weighted indexes/adapters. The "hub-and-spoke conductor + specialist models" topology described in secondary analyses lives somewhere around here; treat specifics as unverified, but *some* routing layer must exist to hit quality bars across 160+ subspecialties
- **Cache check happens early** — see §4.6, it's the biggest lever in the whole system

### 4.4 The Retrieval Stack (where latency is won or lost)

RAG latency compounds: every millisecond added upstream delays first token downstream. OpenEvidence's known investments concentrate exactly here.

* **Corpus [C]:** ~35M papers plus licensed full-text (NEJM, JAMA Network ×11 journals, Nature portfolio, NCCN Guidelines, FDA labels, CDC, ACC, AAFP, ADA). The licensing point cannot be overstated: abstract-level indexing (what everyone else has legally) vs full-text-with-figures-and-tables (what JAMA/Nature deals grant) is a retrieval-quality chasm competitors can't close with money alone — the content isn't for sale to them.

* **Index [I built on C fragments]:** Elasticsearch (confirmed via engineer profile), horizontally sharded, hybrid BM25 + dense vector search. Hybrid because clinical vocabulary is adversarial to pure-vector search: drug names, dosing shorthand, and abbreviation-heavy queries need lexical precision; paraphrase ("heart attack" ↔ "myocardial infarction") needs semantic match.

* **Embeddings — the 700ms→160ms story [C]:**

| Before | After |
|---|---|
| Self-managed GPU inference | Baseten Embeddings Inference (BEI) |
| >700ms end-to-end | 160ms end-to-end (78% cut) |
| Python client | Rust performance client, 10x client throughput |
| Weeks-long deploy cycles | <1 hour, one engineer |

Three compounding optimizations: a runtime tuned specifically for embedding-shaped workloads (small models, huge batches), a Rust client eliminating Python serialization overhead, and continuous batching that keeps GPU utilization near saturation.

* **The precomputation trick — the most important design decision in the stack [I]:**
35M documents were embedded *once*, offline, and incrementally maintained via the ingestion pipeline. At query time only the *query* gets embedded live. Consequences:

1. Corpus can grow 100x with zero effect on query-side embedding latency
2. Embedding compute scales with *new content* (GBs/day), not *traffic* (billions of queries)
3. Index updates are async through Kafka — freshness lags slightly, latency never pays for freshness

* **Reranking [I]:** A fine-tuned cross-encoder reranker re-scores top-K candidates for clinical relevance. Cross-encoders are accurate but expensive — O(query×doc) forward passes — so they run on dedicated GPU pods, isolated from generation traffic so neither queues behind the other. Reranking quality is where generic RAG feels generic and domain RAG feels expert; this is likely one of their most valuable fine-tunes.
