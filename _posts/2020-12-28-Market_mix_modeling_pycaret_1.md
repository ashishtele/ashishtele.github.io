---
layout: single
title: Market Mix Modeling using Pycaret and Streamlit (part 2)!!
author: Ashish Tele
excerpt: "MMM solutions are an integral part of the marketing analytics team. We need to develop, run, and deploy multiple models of MMM analysis. It makes expediting the market mix modeling important."
description: "MMM solutions are an integral part of the marketing analytics team. We need to develop, run, and deploy multiple models of MMM analysis. It makes expediting the market mix modeling important."
permalink:
comments: true
tags: ["Data Science","R","Data Scientist","India","USA","MMM","Python","Market Mix Modeling"]
published: true
comments: true
author_profile: false
header:
  teaserlogo:
  teaser: /images/MMM3.PNG
  image: /images/MMM3.PNG
  caption: "courtesy: Myself 😬"
gallery:

  - image_path: ''
    url: ''
    title: ''
---
Hi there,

This post is an extension of my previous post [Market Mix Modeling using Pycaret and Streamlit (part 1)](https://ashishtele.github.io/2020/12/Market_mix_modeling_pycaret.html). We will see how can we build a sharable web app in minutes using [Streamlit](https://www.streamlit.io/). Streamlit is a Python-based, open-source platform to build and share data apps. The best thing is that the syntax is very intuitive.

```ruby
# Loading the required packages and modules
from pycaret.regression import load_model, predict_model
import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image

# Load the saved model
model = load_model('saved_MMM_lr')

# Prediction function
def predict(model, input_df):
    predictions_df = predict_model(estimator=model, data=input_df)
    predictions = predictions_df['Label'][0]
    return predictions

# Read the .py file for 'show code' button
file = "C:\\Users\\ashis\\PycharmProjects\\MMM\\main.py"
def get_data_as_string(file):
    return open(file,"r").read()

# Data load
path = "D:\Python Files"
file_name = "Advertising.xlsx"
input_file = os.path.join(path,file_name)
def load_data():
    data = pd.read_excel(input_file, engine='openpyxl')
    return data

```

1. **load_model():** We load the saved model (.pkl) file from the last post. We use this model for point (online) or batch prediction. 

2. **predict():** We use this function for point prediction. We leverage <span style="color:blue"> predict_model() </span> function for prediction and picking the 'Label' value as a prediction.

3. **get_data_as_string():** We have a **show code** button on the web app which shows the python code once clicked. This function helps to pull the .py file as a string and decode it to 'utf-8'

4. **load_data():** This function loads the input data. I leverage this data to get the upper and lower limits for the sliders. 
