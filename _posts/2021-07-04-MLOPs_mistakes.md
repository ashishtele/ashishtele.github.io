---
layout: single
title: Mistakes to avoid in MLOps!
author: Ashish Tele
excerpt: "Many companies are developing and deploying machine learning models at scale across the enterprise. The bank of BNY Mellon has shared the lessons in the form of antipatterns."
description: "Many companies are developing and deploying machine learning models at scale across the enterprise. The bank of BNY Mellon has shared the lessons in the form of antipatterns."
comments: true
tags: ["Data Science","R","Data Scientist","USA","MLOps","Machine Learning"]
published: true
comments: true
author_profile: false
header:
  teaserlogo:
  teaser: /images/mlops.png
  image: /images/mlops.png
  caption: "courtesy: https://www.arrikto.com/"
gallery:

  - image_path: ''
    url: ''
    title: ''
---

Hi All,

Recently I came across a paper on [Arxiv Sanity](http://www.arxiv-sanity.com/) named [Using AntiPatterns to avoid MLOps Mistakes](https://arxiv.org/abs/2107.00079v1). The authors describe the lessons learned from developing and deploying machine learning models at scale across the enterprise. BNY Mellon presented the learnings in the form of antipatterns. I think the lessons are vital for not only the financial analytics applications but also all the industries.

I found a few points noteworthy to be noted. The authors mention "It is imperative that the part of a learning pipeline concerned with hyper-parameter optimization be explicitly and painstakingly documented so as to be reproducible and easily adaptable." From my experience, MLflow helped me to save the parameters and artifacts to track the model performance and help to reproduce the results.

Thanks
