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

Thank you!!
