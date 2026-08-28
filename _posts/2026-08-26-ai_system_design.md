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

## 1. The Product, Stated as a System Contract

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

The correctness constraint is the load-bearing wall of the entire design. It dictates retrieval-first architecture, citation enforcement at generation time, and fail-degraded failure semantics. Most consumer RAG systems treat citations as decoration; OpenEvidence treats them as a *precondition for emitting a token*. That single decision propagates through every layer below.

