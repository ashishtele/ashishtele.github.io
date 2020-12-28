---
layout: single
title: Market Mix Modeling using Pycaret and Streamlit!!
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
  teaser: /images/MMM1.PNG
  image: /images/MMM1.PNG
  caption: "courtesy: digitalmarketingcommunity.com"
gallery:

  - image_path: ''
    url: ''
    title: ''
---
Hi All,

The holiday break is a great time to learn something new and impactful. As always, I chose technical stuff over the rest 😬. I had two things to explore and use effectively. The first one is the package ['PyCaret'](https://pycaret.readthedocs.io/en/latest/index.html). As per the documentation, it is an open-source, low-code machine learning python library that automated the machine learning workflows. There are many salient features you can explore.

I think the most profound way to explore and learn new things is to apply the new learnings to some business problem. I decided to choose 'Marketing mix modeling' for that. Marketing mix modeling (MMM) is a statistical analysis such as multivariate regressions on sales and marketing time series data to estimate the impact of various marketing tactics (marketing mix) on sales and then forecast the impact of future sets of tactics. It is often used to optimize advertising mix and promotional tactics with respect to sales revenue or profit. [wiki](https://en.wikipedia.org/wiki/Marketing_mix_modeling)

The dataset I leveraged for this is [Advertising and sales](https://www.kaggle.com/sazid28/advertising.csv). It is a concise dataset with three independent features and 'Sales' as a target variable.


```ruby
# Loading required packages
import pandas as pd
import numpy as np
import os

path = "D:\Python Files"
file_name = "Advertising.xlsx"
print(os.path.join(path,file_name))

input_file = os.path.join(path,file_name)

# Load the data
def load_data():
    data = pd.read_excel(input_file, engine='openpyxl')
    print(data.shape)
    return data
```
The data does not contain any missing values. The dataset size is (200,5). 

<p align="center">
  <img width="250" height="200" src="/images/MMM2.PNG">
</p>

Let's import the required modules of pycaret. We can check the transformations and explore more about the pipeline using 'get_config()'.

```ruby
# Importing the pycaret modules
from pycaret.regression import *
from pycaret.utils import version

# Check version
def version_check():
    print(version())
    return None
    
help(get_config)
get_config('prep_pipe')

```
I set up the function pipeline in the required sequence. As it is a regression modeling problem, we can find the detailed documentation at [PyCaret](https://pycaret.readthedocs.io/en/latest/api/regression.html) site. 

```ruby

if __name__ == '__main__':
    # Checking version
    version_check()
    data = load_data()

    # check missing values
    data.isna().sum()

    # Data shape
    data.shape

    # column names
    print(data.columns)

    # Setup run
    s = setup(data=data,
              target='Sales',
              ignore_features=['Sr'],
              transformation=True,
              transform_target=True,
              normalize=True)

    lr = create_model('lr')
    tuned_lr = tune_model(lr)

    plot_model(tuned_lr, plot="residuals", save=True)

```
