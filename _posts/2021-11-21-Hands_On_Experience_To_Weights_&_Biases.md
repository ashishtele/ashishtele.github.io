---
layout: single
sidebar: true
author_profile: true
title: Hands-On Experience To Weights and Biases (MLOps)!
excerpt: "Weights and Biases is a MLOps platform. It can be used for experiment tracking, dataset versioning, and model management."
description: "Weights and Biases is a MLOps platform. It can be used for experiment tracking, dataset versioning, and model management."
comments: true
tags: ["Data Science","R","Data Scientist","USA","MLOps","Machine Learning"]
published: true
comments: true
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

Once we have 'wandb' installed, run the below line of code and enter the authorization key copied from the weights and biases portal.

```ruby
# wandb login with API token
wandb.login()
```

All the required helper functions are included in a single python script for demonstration purposes. I added docstrings in functions to provide a brief overview. I am reading a config file, loading train, and test datasets, separating features and targets, and defining the **accuracy measures**.

```ruby
def read_params(config_path):
    """
    read parameters from the params.yaml file
    input: params.yaml location
    output: parameters as dictionary
    """
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def accuracymeasures(y_test,predictions,avg_method):
    """
    calculate accuracy measures
    input: y_test, predictions, avg_method
    output: accuracy measures
    """
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, average=avg_method)
    recall = recall_score(y_test, predictions, average=avg_method)
    f1score = f1_score(y_test, predictions, average=avg_method)
    target_names = ['0','1']
    print("Classification report")
    print("---------------------","\n")
    print(classification_report(y_test, predictions,target_names=target_names),"\n")
    print("Confusion Matrix")
    print("---------------------","\n")
    print(confusion_matrix(y_test, predictions),"\n")

    print("Accuracy Measures")
    print("---------------------","\n")
    print("Accuracy: ", accuracy)
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F1 Score: ", f1score)

    return accuracy,precision,recall,f1score

def get_featatures_and_target(df,target):
    """
    Get features and target variables seperately from given dataframe and target 
    input: dataframe and target column
    output: two dataframes for x and y 
    """
    x=df.drop(target,axis=1)
    y=df[[target]]
    return x,y    

def split_data(config_path):
    """
    split data into train and test
    input: config_path
    output: train and test dataframes
    """
    config = read_params(config_path)
    train_data_path = config["processed_data_config"]["train_data_csv"]
    test_data_path = config["processed_data_config"]["test_data_csv"]
    target = config["raw_data_config"]["target"]
    max_depth=config["random_forest"]["max_depth"]
    n_estimators=config["random_forest"]["n_estimators"]

    train = pd.read_csv(train_data_path, sep=",")
    test = pd.read_csv(test_data_path, sep=",")
    train_x,train_y=get_featatures_and_target(train,target)
    test_x,test_y=get_featatures_and_target(test,target)

    return train_x,train_y,test_x,test_y,max_depth,n_estimators
```
