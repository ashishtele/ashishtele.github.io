---
layout: single
title: Automated Marketing Mix Modeling using Robyn!
author: Ashish Tele
excerpt: "Robyn is an automated Marketing Mix Modeling code. It aims to reduce human bias by means of ridge regression and revolutionary algorithms."
description: "Robyn is an automated Marketing Mix Modeling code. It aims to reduce human bias by means of ridge regression and revolutionary algorithms."
comments: true
tags: ["Data Science","R","Data Scientist","India","USA","MMM","Python","Market Mix Modeling"]
published: true
comments: true
author_profile: false
header:
  teaserlogo:
  teaser: /images/MMM11.PNG
  image: /images/MMM11.PNG
  caption: "courtesy: Myself 😬"
gallery:

  - image_path: ''
    url: ''
    title: ''
---
Hi All,

I am returning with a new post on Marketing Mix Modeling. I came across a new release on MMM from Facebook. According to FB team, Robyn reduces human bias by means of ridge regression and evolutionary algorithms, aligns with the ground-truth, enables actionable decision making providing a budget allocator and diminishing returns curves, and ensures privacy. 

<p align="center">
  <img width="650" height="250" src="/images/MMM12.PNG">
</p>

I tried to create a process flow for an illustration purpose. You can refer [Robyn](https://github.com/facebookexperimental/Robyn) documentation which in itself is a great source. The entire process can be divided into 3 major parts:

**1. Scripting files (.R) and data input files (.CSV):**

The Facebook team has provided scripting files that contain feature engineering, modeling functions, budget allocation distribution, and plotting. The code is written in the R language. The other set of files are the raw data files. As shown in the diagram, the revenue and spend master file can be created using multiple in-house and third-party shared files. I have used data coming from multiple sources to generate the master file with different marketing channels, investment, impressions to determine the size and impact of marketing campaigns. The other file is for holidays and special events. We can add the special events as per our requirements and business needs. The holidays' file provided by Facebook is already exhaustive enough.

The next important thing is to set variables:
 1. Set Country
 2. Set Date variable
 3. Set dependent variable and type 
 4. Set Prophet and Baseline variables
 5. Set Media variable and Spend variable

**2. Global Model Parameters:**

We can set the number of cores for parallel computing. The next step is to set the data training and validation sizes. The best thing I discovered is the [Bhattacharyya coefficient](https://en.wikipedia.org/wiki/Bhattacharyya_distance). It is of the amount of overlap between the two statistical samples. The higher the Bhattacharyya coefficient, the more similar the train and test data splits. We can choose an adstocking method between **Geometric** and **Weibull**. Robyn uses **Nevergrad** optimization library to find optimum values for coefficients. 

**3. Result Plots:**

Once we run the iterations, the model creates the different charts that will help assess the best models and scores for the contribution of marketing channels.

Continued...

Thanks for reading!
Ashish
