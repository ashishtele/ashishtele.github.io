---
layout: single
title: My way of structuring files for Data Science Project!
author: Ashish Tele
excerpt: "Many of us came across cookiecutter project template, but it is a kind of over kill for small to medium projects. I tried to create my own folder structure for DS projects."
description: "Many of us came across cookiecutter project template, but it is a kind of over kill for small to medium projects. I tried to create my own folder structure for DS projects."
comments: true
tags: ["Data Science","R","Data Scientist","USA","MLOps","Machine Learning","Cookiecutter"]
published: true
comments: true
author_profile: false
header:
  teaserlogo:
  teaser: /images/DS-project-layout.png
  image: /images/DS-project-layout.png
  caption: "courtesy: neptune.ai"
gallery:

  - image_path: ''
    url: ''
    title: ''
---

Hello,

I recently made a transition from the Azure + Databricks platform to GCP (Google Cloud). So far I am enjoying the capabilities that GCP offer to Data Scientists and Machine Learning Engineers. Vertex AI and the recent introduction of the [Vertex AI workbench](https://cloud.google.com/vertex-ai/docs/workbench) show the commitment from Google towards ML/AI practitioners. 

Most of you must have come across ['cookiecutter'](https://github.com/cookiecutter/cookiecutter), a project template for data science projects. It is a fantastic template format for ML projects, but it feels overwhelming for small DS projects. I tried to leverage the format for some of my initial DS projects, but could not use all the capabilities under it. I searched a lot to find the best fit for my projects, but there is no perfect way to do it. Finally, after researching and referring to multiple open source projects, I  wireframed my own! 

[Data Science for Social Good](https://github.com/dssg) has many projects and pipelines they follow. The typical workflow I also use as per the diagram. Excuse my handwriting here. I am learning to use [XP-PEN](https://www.xp-pen.com/).

<p align="center">
  <img width="650" height="450" src="/images/Folder_str.png">
</p>

## 1. Prototyping in Jupyter notebook:

I think most of us do it. Whenever we start working on any project, the first thing we do is to spin up the cluster, create a jupyter notebook, and start writing code. I put comments in markdown and working code in cells. The code is not necessarily optimized. Once I have a working prototype (data imports + EDA + Features + base model), I am good to go towards modularity.
The sad part is that many keep their final code in the same format.
