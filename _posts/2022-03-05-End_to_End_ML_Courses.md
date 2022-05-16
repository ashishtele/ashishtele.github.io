---
layout: single
sidebar: true
author_profile: true
title: Commendable Sources for MLOps and ML System Design Journey.
excerpt: "MLOps is a new field. There are myriad options to explore, but we don't have enough out to refer."
description: "MLOps is a new field. There are myriad options to explore, but we don't have enough out to refer. I tried to connect with many people over the period to learn and gather the best resources."
comments: true
tags: ["Python","Data Scientist","USA","MLOps","Machine Learning","ML System Design"]
published: true
comments: true
header:
  teaserlogo:
  teaser: /images/mlops.png
  image: /images/mlops.png
  caption: "courtesy: https://cloud.redhat.com/"
gallery:

  - image_path: ''
    url: ''
    title: ''
---
MLOps is a newly minted word. As per Wikipedia, "MLOps or ML Ops is a set of practices that aims to deploy and maintain machine learning models in production reliably and efficiently. The word is a compound of "machine learning" and the continuous development practice of DevOps in the software field". Companies are flocking to go behind it. Myriad PaaS startups are offering end-to-end services. MLOps market is projected to reach [$126 billion](https://neu.ro/2021-mlops-platforms-vendor-analysis-report/) by 2025.

I want to highlight a few resources that are useful for the MLOps journey. I reached out to many people, searched on Github and Reddit, joined multiple Discord channels, followed many researchers on Twitter to gather some of these. I hope you will find it useful as well. If you have anything to append to this ever-growing list, please feel free to leave a comment.

## [CS 329S: Machine Learning Systems Design](https://stanford-cs329s.github.io/syllabus.html)

This course is unquestionably the most unique, first-of-its-kind machine learning system design course. The course is taught by [Chip](https://twitter.com/chipro) at Stanford. It touches all aspects of ML system design with practical examples and significance. I found lecture notes comprehensive to refresh ML system design basics. We should be grateful to them for making it available for FREE.

## [Hidden Technical Debt in Machine Learning Systems](https://proceedings.neurips.cc/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf)

People who are in the ML system design field or are interested in MLOps must have come across this paper or its reference. Many blogs give credit to this paper (2015) by Google for highlighting the importance of infrastructure in real-world ML systems. It explains that the maintenance costs in real-world ML systems are massive and can not be decoupled from the ML ecosystem.

<p align="center">
  <img width="550" height="300" src="/images/mlops_res1.PNG">
</p>

## [Machine Learning Operations by DTU MLOps](https://skaftenicki.github.io/dtu_mlops/)

One of the detailed MLOps courses is available for FREE at [DTU](https://kurser.dtu.dk/course/02476). The main focus is on exercises with emphasis on practical tools and coding skills for machine learning in production. It introduces a number of coding practices that will help organize, scale, monitor, and deploy machine learning models either in a research or production setting. It provides hands-on experience with a number of frameworks, both local and in the cloud, for doing large-scale machine learning models.

The course objectives:

* Organize code in an efficient way for easy maintainability and shareability (Git, Code structure, Debugging, Profiling, Experiment Logging)
* Understand the importance of reproducibility and how to create reproducible containerized applications and experiments (Docker, Config files)
* Capable of using version control to efficiently collaborate on code development (Github, DVC)
* Knowledge of continuous integration (CI) and continuous machine learning (CML) for automating code development
* Being able to debug, profile, visualize and monitor multiple experiments to assess model performance (GCP Monitoring)
* Capable of using online cloud-based computing services to scale experiments (Local, Cloud deployment, Data Drifting)
* Demonstrate knowledge about different distributed training paradigms within machine learning and how to apply them (Distributed Data Loading, Distributed Training)
* Deploy machine learning models, both locally and in the cloud

Bonus point: MEMES!!

## [Machine Learning Ops Roundup](https://mlopsroundup.substack.com/p/issue-15-ai-for-self-driving-at-tesla?s=r&sort=community)

MLOps roundup is a monthly newsletter that brings together the best articles, news, and papers about ML resources. It is curated by [Nihit Desai](https://twitter.com/nihit_desai) and [Rishabh Bhargava](https://twitter.com/rish_bhargava).  I always found it a very informative and common placeholder for all the MLOps news and advancement. At the time of writing this part of the blog, there are 30 newsletters filled with a ton of information. It is a treat for an MLops nerd!

## [University of Cincinnati Business Analytics Course](http://uc-r.github.io/predictive)

If you are a R nerd and looking for a quality course in machine learning, [UC R Programming](https://twitter.com/LindnerCollege) is the place. It has great explanations about all basic algorithms such as Linear Regression, Naive Bayes, Random Forest etc. [Preparing for Regression Problems](http://uc-r.github.io/regression_preparation) introduces crisp concepts necessary for any type of supervised machine learning model.

## [ML System Design by University of Minnesota](https://mlsystemdesign-6490.github.io/)

The ML System Design is offered by the University of Minnesota and taught by [HAMZA FAROOQ](https://www.linkedin.com/in/hamzafarooq/). Hamza is a Data Science Manager at Google and an adjunct professor at the University of Minnesota. The last time when I emailed Hamza, he stated that the course material will be made available on Github.

## [Machine Learning Design Patterns](https://www.amazon.com/Machine-Learning-Design-Patterns-Preparation/dp/1098115783/ref=pd_lpo_1?pd_rd_i=1098115783&psc=1)

It is one of the great books on MLOps. It provides solutions to Common Challenges in Data Preparation, Model Building, and MLOps. 
The design patterns capture best practices and solutions to recurring problems in machine learning. It provides explanations of 30 patterns for data and problem representation, operationalization, repeatability, reproducibility, flexibility, explainability, and fairness.

It will help you how to:

* Identify and mitigate common challenges when training, evaluating and deploying ML models
* Choose the right model type for specific problems
* Deploy scalable ML systems that you can retrain and update to reflect new data
* Interpret model predictions for stakeholders and ensure models are treating users fairly

## [Machine Learning Operations](https://ml-ops.org/#gettingstarted)

It provides an end-to-end ML development process to design, build and manage reproducible, testable, and evolvable ML-powered software.

A few noteworthy reads on the website:

1. Motivation for MLOps
2. End-to-End ML workflow lifecycle
3. MLOps Principles
4. CRISP-ML
5. ML Model Governance

I will keep adding content to the same post!! Thank you for reading.

## [Made With ML](https://madewithml.com/)

As the repository states, "Learn how to apply ML to build a production-grade product and deliver value." It is a great resource for software engineers, data scientists, and product managers. It has hands-on, intuition-first, software engineering, and focused yet holistic content.

* Purpose
* Data
* Modeling
* Scripting
* Interfaces
* Testing
* Reproducibility
* Production

## [MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp)

It teaches the practical aspects of productionizing ML services: collecting requirements to model deployment and monitoring. The course has just started!!
