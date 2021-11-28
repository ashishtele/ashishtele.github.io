---
layout: single
sidebar: true
author_profile: true
title: InterpretML - Great to have tool 🛠️ in MLOps toolkit 🧰 !
excerpt: "InterpretML is an open-source package by Microsoft that encompass SOTA ML interpretability techniques."
description: "InterpretML is an open-source package by Microsoft that encompass SOTA ML interpretability techniques."
comments: true
tags: ["Python","Data Scientist","USA","MLOps","Machine Learning"]
published: true
comments: true
header:
  teaserlogo:
  teaser: /images/interpret.png
  image: /images/interpret.png
  caption: "courtesy: https://interpret.ml/"
gallery:

  - image_path: ''
    url: ''
    title: ''
---
Hi All,

[InterpretML](https://github.com/interpretml/interpret) is an open-source package by Microsoft that encompasses SOTA ML interpretability techniques. It works for two categories:
Glassbox models: The ML models that are designed for interpretability such as linear models, GAMs.
Blackbox models: PDP, LIME techniques for explaining existing systems.

Microsoft Research has developed an interpretable model named Explainable Boosting Machine (EBM). It is a GAMs + bagging/boosting (GAMs on steroids!) in simple terms. The link to the paper is [here](https://arxiv.org/pdf/1909.09223.pdf).  As mentioned in the paper, EBM is a generalized additive model which learns each feature function **f** using modern machine learning techniques such as boosting and bagging. EBM can also detect and include pairwise interaction terms as shown.

<p align="center">
  <img width="650" height="300" src="/images/EBM.png">
</p>

If you see the original definition of GAM from [wikipedia](https://en.wikipedia.org/wiki/Generalized_additive_model), the functions **f** may be parametric, non-parametric, or semi-parametric (smooth functions).

<p align="center">
  <img width="750" height="100" src="/images/EBM1.png">
</p>


<img src="https://github.com/ashishtele/ashishtele.github.io/tree/master/images/EBM_1.gif" alt="zigzag" />
