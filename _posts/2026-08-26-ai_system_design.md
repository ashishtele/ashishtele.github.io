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

30 people, 27M consults a month, no supercomputer. OpenEvidence is a natural-language question-answering engine over peer-reviewed medical literature, used at the point of care. Here is the contract that makes it possible:

Legend: [C] = confirmed public claim, [I] = inferred from behavior.

| Requirement | Target | Basis | Drives |
|---|---|---|---|
| Latency (complete answer) | ≤ 15s | [C] ~13s mean observed (medRxiv study); vs 259s manual lookup | §4.4, §4.5 |
| Latency (perceived) | First token in ~1s | [I] Streaming UI behavior | §4.1 |
| Availability | 99.99% / month | [C] Engineer-attributed figure | §5 |
| Correctness constraint | **No claim without a citation.** Refusal is fine; fabrication is not | [C] Stated product guarantee | §4.5 |
| Traffic shape | 5x diurnal peak (7–9am rounds); 1000x viral headroom | [C] Documented 1000x surge survival | §5, §4.6 |
| Scale (Aug 2026) | 27M consults/mo, ~650K US + 1.2M intl clinicians | [C] Company claims | §2 |
| Compliance | HIPAA, SOC 2 Type II, encryption in transit/at rest, BAAs | [C] Company trust center | §5 |

The correctness constraint is the load-bearing wall. It forces retrieval-first architecture, citation enforcement at generation time, and degrade-capability-never-trust failure semantics.

## <span style="color: #FF6B6B;">2. Capacity Estimation (Back of Envelope)</span>

All numbers derivable from public claims (company-reported, unaudited — April 2026 figures):

```
Consults            27M in April 2026 (~900k/day)         → ~10/sec average
Peak day            1M consults (Mar 10, 2026) → ~12/sec  → ~55/sec at 5x diurnal peak

Model calls         "billions/week" (Baseten; CTO: "billions of custom,
                    fine-tuned LLM calls per week")
Implied fan-out     2B / 6.3M ≈ 300+ internal calls per consultation (lower bound)
                    (embedding, multi-pass retrieval, rerank batches,
                     generation chunks, citation verification)

Sustained call rate 3,300/sec avg → ~16,500/sec peak
```

**Embedding layer sizing [I]:**
Batched embedding inference on H100-class hardware: ~3K inf/s/node.
At peak, if ~40% of calls are query embeddings (assumption): `16,500 × 0.4 / 3,000` ≈ **2–3 nodes**, ×3 redundancy ≈ **7 nodes**. Trivial.

**Generation layer sizing [I]:**
Little's Law: concurrent requests = arrival rate × duration = `(27M/30/86,400) × 5 peaks × 13s` ≈ **680 concurrent streams**.
At ~75 streamed generations per GPU node (continuous batching, ~800-token outputs): **~9 nodes**, ×3 multi-cloud redundancy ≈ **27 H100 nodes total fleet**.
Note: assumes the ~13s quick-consult path. Since Sep 2026 the lineup is bimodal — Osler ~5s, Sackett ~30s, Snow ~5min — deeper models ride a separate slower pool.

**Cost [I]:**
27 nodes × 24h × 30d × $2.50/hr (typical H100 rental) ≈ $50K/mo generation + embeddings/rerank overhead → **<$1M/month total inference** against ~$8.3M/month revenue (CEO: topped $100M annualized in 2025, CNBC Jan 2026; Sacra estimates $150M end-'25 → $300M Jul-'26). Cost per consult: **$0.02–0.05 against ~$3.70 revenue**.

> [!important] The headline finding
> There is no hidden supercomputer. The entire serving fleet fits in a few racks' power budget (~150kW at 27 H100 nodes). If they run frontier-class models instead of ~70B fine-tunes, multiply by 2–4x — still under 10% of revenue.

---

## <span style="color: #FF6B6B;">3. High-Level Architecture</span>

![Hybrid Architecture](/images_1/openevidence.png)

---
## <span style="color: #FF6B6B;">4. Component Deep Dives</span>

### 4.1 Edge & Frontend

The frontend is Next.js on Vercel and the backend is Python on GCP [C]. This looks like team Conway's law — a small frontend team and a mostly Python/ML backend — but the real reason is trust isolation. The edge handles the app shell, authentication, and token streaming, while everything that touches PHI stays inside GCP. Neither team touches the other's deploy surface, which means a bad frontend push can't take down retrieval and a backend experiment can't break the shell. For a 30-person team, that blast-radius separation matters more than code aesthetics.

What the edge actually sells is perception, not truth. The shell renders instantly and streams tokens as they arrive, so perceived latency tracks time-to-first-token rather than the ~13s full answer [I]. But the citation guarantee complicates streaming: you cannot emit claims before they are verified against retrieved evidence. The plausible design is that time-to-first-token pays for first retrieval plus the first verified span, and everything after that feels instant because the expensive work already happened upstream.

Vercel's [Fluid compute](https://vercel.com/fluid) is the one infrastructure detail here that earns its place. It keeps functions warm between requests and shifts billing from wall-clock time to active-CPU time [C vendor claim, unaudited [1]]. That matters specifically because OpenEvidence's edge workload is mostly idle-waiting on an LLM stream, not computing. The claimed 90% serverless spend drop follows directly from that shape — do not read it as a general serverless win.

Authentication and rate-limiting happen at the edge for cost reasons, not just hygiene. Every user is NPI-verified (§4.2), and that check gates the ~300x internal fan-out before any embedding, retrieval, or generation fires. Rejecting a scraper at Vercel costs fractions of a cent; rejecting it after the backend has already fanned out costs dollars.

Deploy velocity functions as the reliability plan. Every commit gets a preview URL and production ships in minutes [C]. A team this small cannot staff extensive pre-release QA, so it compensates by fixing forward fast — which is structurally what allowed it to survive the documented 1000x surge without a formal capacity-planning discipline. The Epic/FHIR embeds at Sutter Health and Mount Sinai [2][3] then reshape what that backend must absorb: queries arrive mid-chart, short and urgent and clustered by specialty, which is exactly the skew that motivates the routing in §4.3 and the caching in §4.6. The honest caveat is that Vercel is a single point of failure — if the edge is down, a healthy backend is unreachable, and there is no public failover story [I from absence].

---
[1] Vercel customer case study, "How OpenEvidence built a healthcare AI that
    physicians actually trust" (2026)
[2] Beckers Hospital Review / Sutter Health press release, Feb 2026
[3] Healthcare IT News, Mount Sinai enterprise Epic integration, Mar 2026

### 4.2 Identity & Trust Layer

Most AI products treat identity as a login form. OpenEvidence treats it as load-bearing infrastructure. Every user is a verified clinician via NPI number [C] — checked against the federal registry at signup, then cached for sessions after [I mechanics].

One cheap check buys four expensive things at once:

1. **An abuse firewall.** The corpus cost millions to license. Anonymous access would mean anonymous scraping. NPI gating kills that at the edge, before the ~300x internal fan-out fires (§4.1). This is the cheapest request in the system protecting the most expensive one.
2. **A regulatory posture.** The product gives information to professionals, not medical advice to consumers. That single distinction shapes liability and every paragraph of the terms of service.
3. **A business asset.** Pharma advertisers pay $70–150 CPMs precisely because the audience is verified prescribers, not traffic. Identity *is* the ad inventory.
4. **Free context about who's asking.** Knowing specialty and role before retrieval is context no prompt can recover. A cardiologist asking about "AFib management" and a nephrologist asking the same words need different evidence weighted differently. That feeds the routing in §4.3 and partitions the cache in §4.6 [I].

The tradeoff is deliberate friction. Signup takes minutes, not seconds, and students, patients, and ex-US clinicians without NPI-equivalents hit a wall. OpenEvidence accepts slower growth for a corpus that can't be scraped, an audience advertisers overpay for, and queries that arrive pre-labeled.

Limitation: NPI proves credential, not intent. A verified account can still scrape slowly, and there is no public story on re-verification cadence or stolen-credential detection [I from absence].

### 4.3 Query Understanding & Orchestration

A doctor never asks one question. *"Should this 68yo with CKD get metformin?"* is really four: what's the dose, what does kidney disease change, what do guidelines say, what's new in trials?

OpenEvidence splits it up before it searches [I from answer shape — multi-section answers with mixed source types per section]. Think triage nurse, not search box.

1. **Split.** One messy question becomes 3-4 sharp evidence questions. Bad split = generic answer. Generic = doctors leave.
2. **Route.** A cardiologist and a nephrologist typing the same words don't get the same weighting. The NPI check in §4.2 already told the system who's asking — free context no prompt can recover.
3. **Run at once, not in sequence.** All four searches run in parallel. The slowest one sets the pace, not the sum. That's a big chunk of how a deep answer still lands in ~13s.
4. **Check memory first.** Before any search fires, check if we've answered this — or a piece of it — before (see §4.6). With 27M overlapping consults a month, this is the margin lever. It's why 300 internal calls still cost $0.02-0.05 per consult (§2).

Two things this layer *refuses* to do, and both are business decisions:

- **No ads in the chain.** The orchestrator merges evidence, never ad copy. Ads ride the Kafka sidecar in §4.8, rendered alongside — never inside. That separation is what lets OpenEvidence charge $70-150 CPMs without torching trust. Break it once, lose the audience that *is* the inventory.
- **No guessing.** Slow piece? Drop it and say "evidence is inconclusive." Same rule as §4.5: lose capability, never lose trust. Liability still sits with the physician — the product is information, not advice — but honesty is why they come back mid-chart.

That mid-chart part matters. Since the Epic embeds at Sutter Health and Mount Sinai, queries arrive short, urgent, clustered by specialty — "afib dosing ckd" at 7am rounds, not full sentences. Routing plus section-level cache is what makes those 3-word queries answerable. Distribution changed the workload; orchestration absorbed it.

Limitation: the "conductor + specialist models" topology in secondary analyses is unconfirmed [I]. *Some* routing must exist to hold quality across 160+ subspecialties — shape is reconstruction, need is not.

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
