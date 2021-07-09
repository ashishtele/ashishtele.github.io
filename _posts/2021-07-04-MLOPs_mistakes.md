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

I found a few points noteworthy to be mentioned. The authors mention "It is imperative that the part of a learning pipeline concerned with hyper-parameter optimization be explicitly and painstakingly documented so as to be reproducible and easily adaptable." From my experience, MLflow helped me to save the parameters and artifacts to track the model performance and help reproduce the results.

In the financial analytics context, the Authors found the KISS principle helpful. In their words, it encourages developers to try simple models first and conduct an exhaustive comparison of models before advocating for specific methodologies. KISS stands for 'Keep it simple, stupid. It is a design principle which states that designs should be as simple as possible. I think the KISS principle is valid for almost all the verticals. It may be because of multiple reasons such as complexity, incremental performance improvement, infrastructure limitations, latency and throughput trade-off, etc. 

Repeated testing against the known test set, modify their model accordingly to improve performance on the known test set is called [HARKing](https://en.wikipedia.org/wiki/HARKing) (Hypothesizing After Results are Known). It leads to implicit data leakage. It has potential effects of over-fitting and selection bias in performance evaluation. The acronym HARKing is borrowed from psychology.

As per the Authors, In addition to explainability, **conveying uncertainty** can be a significant contributor to ensuring trust in ML pipelines. There has been a lot of research going on in the field of explainable AI/ML, but conveying uncertainty is equally important. Explainability can not be perfect as it will have a component of uncertainty in it.

Thanks
