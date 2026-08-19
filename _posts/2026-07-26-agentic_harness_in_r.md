---
layout: single
sidebar: true
author_profile: true
title: "Why Building a Harness Is an Art"
excerpt: "Why I Thought of Building an Agentic Harness in R"
description: "R ecosystem is behind when compared with Python in terms of harness engineering. There are many reasons to it.."
tags: ["LLM", "AGI", "Python", "R"]
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

Everyone is building agents. Far fewer people are thinking about what holds those agents together. The more I worked with AI agents, the more I realized that building an agent is only half the problem. An LLM can reason, call tools, write code, and make decisions—but turning those capabilities into a reliable agentic system requires a lot more: context management, tool orchestration, state, memory, retries, observability, and compaction. I started thinking of this surrounding layer as an agentic harness: the infrastructure that turns a capable model into a reliable, usable system. And then came the obvious question for me: **why not build that harness in R?**

There is an interesting asymmetry in the current AI ecosystem. If you want to build an agent, Python is usually the obvious choice. Not because Python has a special ability to make an LLM reason, but because an enormous amount of infrastructure has accumulated around it: model SDKs, tool calling, orchestration, memory, structured outputs, evaluation, tracing, code execution, MCP integrations, vector databases, and increasingly sophisticated agent runtimes.

R is in a different position. R can talk to models. R can manipulate data. R can call APIs, execute code, work with databases, build applications, and do the statistical and analytical work that made it one of the most important languages in data science. But something feels different when you try to build a system around an LLM rather than simply call one. The missing piece isn't necessarily an LLM interface. It is the harness. The model is not the agent. One of the easiest mistakes to make when building AI applications is to equate the model with the agent. An LLM gives you a reasoning engine. But an agentic application needs much more around it.

A useful mental model is:

**Model + Context + Tools + Runtime + State + Control Loop = Agent**

The model decides what it wants to do. The harness makes that decision executable. It decides which tool to invoke, how arguments are validated, what happens when the tool fails, what information comes back into context, how much context should be retained, when old information should be compressed, how execution should be observed, and when the loop should stop.

This distinction becomes increasingly important as agents become more capable.

Lets take an example of Pi (my favorite) agent harness. It exposes only four core tools, has less than 1000 tokens of system prompt, and supports high extensibility. I closely observed and played with many coding agents and harnesses. I have [Hermes agent](https://github.com/nousresearch/hermes-agent), running 24X7 (it has its own machine). Each harness has its own pros and cons, but we should look out for the trade off. 

If we observe in industry, all AI labs are coming up with their own harnesses. Many companies are adopting Claude code, Codex for running coding agents and trying to optimize for the LLM usage. But there is a more nuanced underlying pattern. Lets have a look at this chart:

<p align="center">
  <img width="750" height="500" src="/images_1/LLM_cost.PNG">
</p>

*Pi agent is ~7x cheaper compared to Claude code keeping the model same per successful task!*

So only switching the models and keeping the harness same does not look an optimized strategy. I observed user traces and observed it follows pareto chart in terms of complexity of questions asked. Most of the user questions are very simple and can be answered by frontier-1 tier models like Gemini 3.7 flash, GPT 5.5 nano etc. Developers do ask some complex questions where SOTA models are required but then pairing it with herness like Pi can optimize for intelligence per dollar.

Pi and many other harnesses provided a lot of valuable implementation patterns. What I found interesting was that good harnesses are often surprisingly small at the core.

This led me to a simple realization:

**The goal of a harness is not to make the agent more complicated. It is to make the model more effective.**

Every feature has a cost.

* More tools → larger decision space.
  
* More context → more tokens and noise.

* More memory → more irrelevant information.

* More agents → more coordination overhead.
  
* More orchestration → more things to debug.

So the interesting problem is not *how many capabilities can we add?*

It is:

> **What is the minimum machinery required to make the model reliably useful?**

That is what I mean by harness engineering.

### The harness as a control system

I think of the harness as a relatively thin control layer around the model:

```text
              ┌──────────────┐
              │     Model    │
              │    Reason    │
              └───────┬──────┘
                      │
                      ▼
              ┌──────────────┐
              │   Harness    │
              │              │
              │ Context      │
              │ Tools        │
              │ State        │
              │ Control loop │
              │ Compaction   │
              │ Observability│
              └───────┬──────┘
                      │
             ┌────────┼────────┐
             ▼        ▼        ▼
           Files     R      Database
```

The model decides. The harness makes the decision executable. It decides what the model sees, what it can do, what happens after a tool call, what gets remembered, what gets discarded, and when the loop should stop.

### Context is probably the hardest part

The more I work with agents, the less I think about "prompt engineering" and the more I think about **context engineering**.

The question is no longer:

> What prompt should I give the model?

It is:

> **What should the model know at this exact moment?**

A coding agent may have thousands of lines of conversation, tool output, files, errors, and previous decisions available. Sending everything back is wasteful. Summarizing everything is dangerous. The harness needs to preserve the information that matters for the next decision. This is why compaction is not simply summarization.

It is **state compression**.

### And then there is model economics

The other thing I find fascinating is that we are increasingly treating model selection as a harness problem. Not every task deserves the smartest model. A typical user trace probably looks something like a Pareto distribution: lots of simple requests and a small number of genuinely difficult ones.

Why spend frontier-model inference on:

> "Rename this variable."

when a much cheaper model can do it? But when the task becomes:

> "Understand this unfamiliar codebase, identify the architectural problem, refactor it, run the tests, and fix the failures."

then spending more inference compute makes sense. So the harness can become a **model router**.

```text
User
 │
 ▼
Harness
 │
 ├── simple ──► cheap/fast model
 │
 └── complex ─► frontier model
```

The interesting metric is therefore not simply intelligence. It is something closer to:

**useful intelligence / dollar**

And this is where harnesses can create surprisingly large differences even when using the same underlying model.

### Why R?

This brings me back to the original question. Why build this in R? Not because R needs to become Python and definitely not because R needs another giant agent framework. I think R has a more interesting opportunity.

R already lives where a large class of agents will eventually operate: **data**.

Tables.
Databases.
Statistics.
Visualization.
Experiments.
Reports.
Reproducible analysis.

The missing layer is the runtime that lets an LLM reliably operate on all of this. That is the harness. 

Thank you!!
