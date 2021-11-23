---
layout: single
title: Hands-On Experience To Weights and Biases (MLOps)!
author: Ashish Tele
excerpt: "Weights and Biases is a MLOps platform. It can be used for experiment tracking, dataset versioning, and model management."
description: "Weights and Biases is a MLOps platform. It can be used for experiment tracking, dataset versioning, and model management."
comments: true
tags: ["Data Science","R","Data Scientist","USA","MLOps","Machine Learning"]
published: true
comments: true
author_profile: false
header:
  teaserlogo:
  teaser: /images/wandb.png
  image: /images/wandb.png
  caption: "courtesy: https://wandb.ai/site"
gallery:

  - image_path: ''
    url: ''
    title: ''
---

Hi All,

[Weights & Biases](https://docs.wandb.ai/) is a ML platform. As per the site, W&B's tools can be used to:
Track experiments
Version and iterate on datasets
Evaluate model perfomance
Reproduce models
Visualize results

As a part of the End to End MLOps project, I worked on MLFlow to track the model artifacts, hyperparameters, etc. I have also worked on MLFlow + Databricks combo at the enterprise level and found it very helpful. [MLFlow](https://mlflow.org/) is one of the experiment tracking tools out there in the market. Neptune and Wandb.ai are the other two promising entries. I thought of giving a try to W&B to see its functionality. 

The best thing about W&B that I found among many others is [quick setup](https://docs.wandb.ai/quickstart). The W&B team has made user onboarding hassle-free. It is very important to have smooth user onboarding and activation in the product journey where W&B has nailed it. The library is free for personal use and experimentation!!

Steps are:
1. Free W&B account creation and authorization key generation 
2. Installing 'wandb'
3. Log in to the W&B account using an API token

Let's code a simple example and log the metrics, artifacts, etc. to check model performance. I have taken a simple classification example to predict whether a customer will change telco provider. The dataset is available on [kaggle](https://www.kaggle.com/c/customer-churn-prediction-2020/data?select=train.csv). The evaluation criterion is **Accuracy**. The below walkthrough does not include all columns from the raw dataset. Also, the basic models are fit to check the MLOps functionality without much hyperparameter tuning. 

Let's import libraries required for data analysis, model building, and model tracking. 

```ruby
# Importing required libraries for analysis
import json
import yaml
import joblib
import argparse
import wandb
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import f1_score,recall_score,accuracy_score,precision_score,confusion_matrix,classification_report

import warnings
from sklearn.exceptions import ConvergenceWarning
warnings.filterwarnings("ignore", category=ConvergenceWarning)
```

