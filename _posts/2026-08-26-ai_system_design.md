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

### 4.5 Generation

* **Model provenance [C core, I details]:**

Baseten confirms "**billions of custom, fine-tuned LLM calls per week**" and use of Baseten Training. In-house fine-tuned open-weight base model + LoRA/PEFT adapters — almost certainly separate adapters (or separate small models) for rerank, synthesis, and grounding behavior. Raw lab-API wrapping is ruled out by unit economics (300 calls/consult × frontier-API pricing > revenue), latency control requirements, and the behavioral-consistency requirement below.

* **Citation enforcement at the architecture level [C behavior, I mechanism]:**

The product guarantee is "no uncited claims." Prompting can't reliably deliver that at billions of calls. The plausible mechanisms, roughly in order of likelihood:

1. *Constrained generation*: output grammar requires citation spans referencing retrieved document IDs; uncited continuations are structurally disallowed
2. *Post-hoc verification pass*: generated claims checked against retrieved evidence before emission; unverifiable sentences dropped
3. *Fine-tuned refusal behavior*: model trained to abstain when retrieved context is insufficient ("evidence is inconclusive")

Observable behavior supports all three coexisting: inline citations resolve to specific papers, low-evidence topics produce explicit abstentions, and hard-coded refusals exist for policy domains (the vaccines/autism case Polevikov dissects).

* **Serving [C]:**

Baseten Multi-Cloud Capacity Management — GPU capacity pooled across clouds and regions; traffic spikes or hardware failures fail over instead of queueing; no multi-year GPU commitments. This is how a 30-person company absorbs 1000x demand spikes without owning capacity planning as a discipline.

* **Failure semantics [C philosophy, I implementation]:**

Degrade capability, don't degrade trust. Slow retrieval → "still searching," never an uncited guess. Backup model endpoints sit on the critical path. Contrast with consumer chatbots whose guardrails come *off* under failure — inverted design.

### 4.6 Caching

Clinical questions are ferociously repetitive: hundreds of thousands of clinicians ask overlapping questions daily. **[I]** Plausible cache layers:

| Layer | Key | TTL logic |
|---|---|---|
| Exact-match | normalized question hash | invalidate on corpus update affecting sources |
| Semantic | embedding similarity above threshold | same, with conservative threshold |
| Section-level | sub-query → evidence bundle | reusable across different full questions |
| Citation metadata | DOI → resolved link/metadata | effectively permanent |

If half of consultations hit any cache layer, effective real-time load halves — which is exactly how "billions of requests/week" reconciles with a ~27-node GPU fleet. Cache invalidation ties to ingestion: new guideline published → affected-topic entries flushed.

### 4.7 Ingestion & Freshness Pipeline

**[C corpus, I mechanics]** Medical knowledge doubles every [~73 days](https://pmc.ncbi.nlm.nih.gov/articles/PMC3116346/). The pipeline:

```
licensed feed (API/bulk) → parse PDF/XML → chunk (structure-aware:
sections, tables, figures kept atomic) → batch embed offline
→ upsert ES index → attach recency/journal-tier metadata
→ trigger targeted cache invalidation
```

Recency flags matter clinically: recommendations based on superseded literature must say so.

### 4.8 Async Sidecars

Everything non-latency-critical rides Kafka off the synchronous path [C components confirmed via engineer profile: event-driven microservices]:

- Analytics & usage dashboards
- Ad serving (the business model — ads rendered alongside answers, never inside the evidence chain)
- Email digest / "deep consultation" follow-ups (hours-scale SLA, zero latency budget)
- Physician feedback signals → fine-tuning data flywheel

---

## <span style="color: #FF6B6B;">5. Reliability Engineering</span>

| Failure mode | Behavior | Why |
|---|---|---|
| Model endpoint down/slow | Failover to backup provider/region (MCM pool) | [C] Redundancy was an explicit Baseten requirement |
| Retrieval degraded | "Still searching" state; cached results bridge | Never generate without evidence |
| Traffic spike (viral/conference) | Absorb via multi-cloud burst + autoscale | [C] TikTok surge: logs stayed green, nobody provisioned anything |
| Audit log write failure | Must buffer-and-retry, never drop | HIPAA/compliance trail is legally required |
| Corpus update bad batch | Canary index swap; rollback path | A poisoned index poisons every answer downstream |

Uptime claim: 99.99% [C] ≈ 4.4 minutes/month downtime budget. Achievable precisely because every hard part is someone else's managed service.

---

## <span style="color: #FF6B6B;">6. Design Philosophy — What Makes This Buildable by 30 People</span>

1. **Asymmetry of read/write.** ~95% of request work is read-only retrieval over precomputed structures. Reads scale linearly and cheaply; only generation touches GPUs.
2. **Precompute everything that can be precomputed.** Corpus embeddings, citation resolution, journal metadata — all offline. The hot path does the minimum possible novel work per query.
3. **Buy every non-differentiating layer.** Vercel, GCP, Elastic, Kafka, K8s, Baseten. Vendor case studies read like an org chart for a 200-person infra team that doesn't exist.
4. **Concentrate engineers only on compounding assets:** the licensed corpus, the embedding/rerank quality, the citation-grounded generation behavior, and the clinician distribution network.
5. **Make trust architectural, not aspirational.** Refusal paths, citation constraints, and degradation modes are structure, not policy documents.

## <span style="color: #FF6B6B;">7. Honest Limits of This Analysis</span>

- The multi-agent "conductor + specialist" topology comes from secondary analysis, unconfirmed by the company
- Polevikov's counter-reading — "a retrieval-summarizer with a marketing department," where "no hallucinations" is architecturally impossible and refusals are hard-coded policy dressed as humility — deserves weight; both readings agree on the mechanical stack and disagree on framing
- All GPU/cost figures assume ~70B-class fine-tunes at standard batching efficiency; frontier-class serving would shift numbers 2–4x without changing conclusions
- Cache hit rates, adapter counts, and orchestration internals are reconstruction, not observation

## <span style="color: #FF6B6B;">8. If You Were Building This From Scratch</span>

The transferable playbook, stripped of healthcare:

1. Make your correctness constraint *structural*, not prompt-level
2. Precompute embeddings offline; make corpus growth free for query latency
3. Put a semantic cache in front of everything; measure its hit rate obsessively
4. Isolate latency-critical GPU workloads (embed, rerank, generate) into separate pools so they never queue behind each other
5. Rent elasticity across clouds rather than owning peak capacity
6. Push every async concern behind a queue, no exceptions
7. Spend your headcount only where it compounds; outsource the rest

---

## <span style="color: #FF6B6B;">9. Transferable Lessons from the Competitive Landscape</span>

What each player in the clinical-AI market (2026) teaches for system design, independent of healthcare:

### From OpenEvidence
1. **Precompute everything offline** — corpus embeddings built once, updated async via queue; query path does minimum novel work. Query latency stays flat as corpus grows 100x.
2. **Make the correctness constraint structural** — citations/refusals enforced by output grammar or verification pass, never by prompt. Any high-stakes domain bakes guarantees into architecture.
3. **Semantic caching as a first-class layer** — repetitive-question domains get 50–70% hit rates; biggest combined cost + latency lever in RAG.
4. **Isolate GPU workloads into separate pools** — embed / rerank / generation never queue behind each other; no cross-stage backpressure.

### From ChatGPT for Clinicians (OpenAI)
5. **Model moat vs corpus moat is a strategic fork** — capability-first vs data-first demand different stacks. Decide early whether your advantage is *what you know* or *how well you reason*.
6. **Verification as onboarding** — one cheap identity check (NPI) = abuse protection + audience quality + query-routing prior simultaneously.

### From UpToDate
7. **Curated beats comprehensive for trust** — human-in-the-loop curation pipeline feeding the index outranks raw retrieval quality in high-stakes domains.

### From DynaMed
8. **Evidence grading as ingestion-time metadata** — quality scores attached to documents at index time let ranking weigh sources mechanically, not at query time.

### From Doximity
9. **Distribution you own beats distribution you build** — embed where users already are (their EHR play) rather than building destination apps.

> [!important] Meta-lesson
> Every winner's architecture mirrors its moat: OpenEvidence precomputed indexes because its asset is a static corpus; OpenAI optimizes serving because its asset is the model; UpToDate invests in editorial tooling because its asset is authorship. Start with "what compounds here?" and infrastructure decisions mostly make themselves.

---
Thank you,

Ashish
