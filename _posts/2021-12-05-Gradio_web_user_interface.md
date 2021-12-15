---
layout: single
sidebar: true
author_profile: true
title: Gradio - Web Interface to Your ML Project in MLOps!
excerpt: "Gradio is the fastest way to demo ML model with a friendly web interface."
description: "Gradio is the fastest way to demo ML model with a friendly web interface."
comments: true
tags: ["Python","Data Scientist","USA","MLOps","Machine Learning"]
published: true
comments: true
header:
  teaserlogo:
  teaser: /images/gradio.png
  image: /images/gradio.png
  caption: "courtesy: https://gradio.app/"
gallery:

  - image_path: ''
    url: ''
    title: ''
---
Hey All,

[Gradio](https://gradio.app/) is an open-source python library that allows us to create an easy-to-use, customizable user interface for our ML models in just a few lines of code. We can integrate the GUI into our Python script, or we can share the link with anyone.

We have a couple of alternatives available such as Streamlit, Flask, etc to interface model outputs. I think having a UI for ML output provides a layer of translation from technical to layman language. It becomes very easy to demonstrate the power of the ML model to stakeholders by showing the working MVP (MLP !) by changing the values on the UI. I found Streamlit and Gradio very easy to code, quick to spin up, and flashy to impress!

Let's start pulling in code snippets. The functions are self-defined and easy to understand. 

```ruby

# Importing required packages
import gradio as gr
import pickle
import os
import numpy as np
import yaml
import joblib

# loading the trained model
params_path = 'params.yaml'
 
class NotANumber(Exception):
    def __init__(self, message = "Values entered are not Numerical"):
        self.message = message
        super().__init__(self.message)

# Read parameters from config file
def read_params(config_path):
    with open(config_path, 'r') as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def predict(data):
    """
    Dict. values to predict the output
    output: yes/no
    """
    config = read_params(params_path)
    model_dir_path = config['model_webapp_dir']
    model = joblib.load(model_dir_path)
    prediction = model.predict(data).tolist()[0]
    return prediction  

def validate_input(dict_request):
    for _, val in dict_request.items():
        try:
            val = float(val)
        except Exception as e:
            raise NotANumber

    return True

def form_response(vmail_msg, tot_day_calls, tot_eve_min, tot_eve_chr, tot_int_min, cust_sev_calls):
    dict_request = {'vmail_msg': vmail_msg, 
                'tot_day_calls': tot_day_calls, 
                'tot_eve_min': tot_eve_min, 
                'tot_eve_chr': tot_eve_chr, 
                'tot_int_min': tot_int_min, 
                'cust_sev_calls': cust_sev_calls}
    try:
        if validate_input(dict_request):
            data = dict_request.values()
            data = [list(map(float, data))]
            response = predict(data)
            return response
    except NotANumber as e:
        response = str(e)
        return response

```
The code for Gradio is concise and very similar to Streamlit as we have seen in the previous post. I have created a set of sliders with minimum and maximum values. I then passed the slider values as a list to **form_response()** function under **Interface()**.

```ruby
# Slider creation for Gradio
vmail_msg = gr.inputs.Slider(label = 'Number vmail messages',minimum = 1, maximum = 30)
tot_day_calls = gr.inputs.Slider(label = 'Total day calls',minimum = 1, maximum = 30)
tot_eve_min = gr.inputs.Slider(label = 'Total eve minutes',minimum = 1, maximum = 30) 
tot_eve_chr = gr.inputs.Slider(label = 'Total eve charge',minimum = 1, maximum = 30)
tot_int_min = gr.inputs.Slider(label = 'Total Intl minutes',minimum = 1, maximum = 30)
cust_sev_calls = gr.inputs.Slider(label = 'Customer service calls',minimum = 1, maximum = 30)


gr.Interface(form_response,
            inputs = [vmail_msg, tot_day_calls, tot_eve_min, tot_eve_chr, tot_int_min, cust_sev_calls],
            outputs = 'label',
            live = True).launch()
```


<p align="center">
  <img width="750" height="450" src="/images/gradio_1.png">
</p>
