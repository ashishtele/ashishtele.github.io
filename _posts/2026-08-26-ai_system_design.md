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
  teaser: /images_1/R_harness.png
  image: /images_1/R_harness.png
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

## <span style="color: #4ECDC4;">2. Capacity Estimation (Back of Envelope)</span>

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

## <span style="color: #95E1D3;">3. High-Level Architecture</span>

![Hybrid Architecture](/images_1/openevidence.png)

---
