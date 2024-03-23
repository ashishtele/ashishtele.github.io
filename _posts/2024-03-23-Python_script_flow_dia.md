---
layout: single
sidebar: true
author_profile: true
title: "Be Creative with Dependency Flow Diagram for Python Modules🤖"
excerpt: "Creating the dependency flow diagram on codebase is not an easy task. Efforts grow exponentially with additional scripts."
description: "Creating the dependency flow diagram on the codebase is not an easy task. Efforts grow exponentially with additional scripts."
comments: true
tags: ["VertexAI", "Data Scientist", "AUTOML", "LLM", "Machine Learning", "ML System Design"]
published: true
comments: true
header:
  teaserlogo:
  teaser: /images_1/pair_pro.jpg
  image: /images_1/pair_pro.jpg
  caption: "courtesy: Gemini"
gallery:

  - image_path: ''
    url: ''
    title: ''
---

Hi There,

Are you overwhelmed by the complexity of code repositories with deep layers of nested folders? 
If so, this post aims to offer some guidance to steer you in the right direction. I've personally felt that sinking 
feeling when trying to navigate through interconnected modules within nested structures. While we can track dependencies to some extent, it's easy to lose our way in the labyrinth of folders.

There are a couple of tools available, such as `pydeps` or `ModuleFinder`, but they can be a bit daunting to
start with. For instance, using `pydeps` requires having `Graphviz` installed, which can be quite a hassle on Windows.

However, in this era of advanced language models like *Gemini 1.5 Pro* and *Claude Opus*, 
with their expansive context windows, we have a powerful resource at our disposal. If we can fit the 
entire code repository within the context window of these models, we can greatly simplify our exploration
and understanding of the codebase.

<p align="center">
  <img width="500" height="200" src="/images_1/LLM_flow.PNG">
</p>


