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

Let's import the required libraries and datasets. I am using the same datasets that I have been using for the last few articles. The dataset is available at [Kaggle](https://www.kaggle.com/c/customer-churn-prediction-2020/data?select=train.csv). It is a simple classification example to predict whether a customer will change telco provider. I faced a setback while using **interpret** in python scripting (.py), so I used .ipynb for the scripting.

```ruby
import numpy as np
import ipykernel as ipy
import pandas as pd
import yaml
import argparse
import typing
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score,recall_score,accuracy_score,precision_score,confusion_matrix,classification_report
from interpret.glassbox import ExplainableBoostingClassifier
from interpret import show
from interpret.provider import InlineProvider
from interpret import set_visualize_provider
set_visualize_provider(InlineProvider())
from interpret.data import ClassHistogram
from interpret import show, preserve, show_link, set_show_addr
```
Import the train, test datasets, and split them into independent and dependent. 

```ruby
df = pd.read_csv('C:\\Users\\ashis\\OneDrive\\Desktop\\MLOps\\churn_model\\data\\processed\\churn_train.csv')
df_test = pd.read_csv('C:\\Users\\ashis\\OneDrive\\Desktop\\MLOps\\churn_model\\data\\processed\\churn_test.csv')
df.head()

train_x = df[[col for col in df.columns if col not in ['churn']]]
train_y = df['churn']
test_x = df_test[[col for col in df_test.columns if col not in ['churn']]]
test_y = df_test['churn']

print(f'train shape: {train_x.shape}')
print(f'test shape: {test_x.shape}')
```
Build a EBC and try a global explainability on the trained model. I had the set-up IP address and port number as the default address was different.

```ruby
# Fit an Explainable Boosting Machine
ebm = ExplainableBoostingClassifier()
ebm.fit(train_x, train_y)

ebm_global = ebm.explain_global(name = 'EBM')
#preserve(ebm_global, 'number_customer_service_calls', 'number_customer_service_calls.html')
set_show_addr(("127.0.0.1", 5000))
show(ebm_global)
```
The result is a plotly interactive graph. I created a gif to show various options available. When we select 'summary' option in the dropdown, it gives overall feature importance. The feature 'number_customer_service_calls' has the maximum feature importance. When we select 'number_customer_service_calls' in the dropdown, it gives a score for a complete feature range. As the 'number_customer_service_calls' value increases, the score also increases, i.e., higher chances of churning. 

<p align="center">
  <img src="https://raw.githubusercontent.com/ashishtele/ashishtele.github.io/master/images/EBM_1.gif" width=650>
</p>
