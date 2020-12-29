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

```ruby
data = load_data()

min_TV = np.float(data['TV'].min())
max_TV = np.float(data['TV'].max())

min_Radio = np.float(data['Radio'].min())
max_Radio = np.float(data['Radio'].max())

min_News = np.float(data['Newspaper'].min())
max_News = np.float(data['Newspaper'].max())
```
In the above snippet, we are finding the minimum and maximum values of each marketing feature so that we can leverage it for the slider range.

```ruby

def run():

    image = Image.open("D:\Python Files\Image_MMM.PNG")

    st.sidebar.markdown("# Selection")
    add_selectbox = st.sidebar.selectbox("How would you like to predict?", ("Online","Batch"))

    st.sidebar.info('This is to predict sales based on marketing components.')
    st.sidebar.image(image, use_column_width=True)
    st.sidebar.success('https://ashishtele.github.io/')

    st.title("Market Mix Modeling")

    if add_selectbox == 'Online':

        TV = st.slider("Value for TV:",
                       min_value=min_TV,
                       max_value=max_TV)

        Radio = st.slider("Value for Radio:",
                       min_value=min_Radio,
                       max_value=max_Radio)

        News = st.slider("Value for News:",
                          min_value=min_News,
                          max_value=max_News)

        output = ""

        input_dict = {'TV': TV, 'Radio': Radio, 'Newspaper': News}
        input_df = pd.DataFrame([input_dict])

        if st.button('Predict'):
            output = predict(model=model, input_df=input_df)
            output = '$' + str(output)

        st.success('The sales is {}'.format(output))

    if add_selectbox == 'Batch':

        file_upload = st.file_uploader("Upload csv file for predictions", type = ["csv"])

        if file_upload is not None:
            data = pd.read_csv(file_upload)
            predictions = predict_model(estimator=model, data=data)
            st.write(predictions)

    if st.sidebar.button("Show Code"):
        st.code(get_data_as_string(file))
 ```
 
 The above code snippet is self-explanatory. We are adding the different components to build the web app. We build a sidebar, add images and URLs. We provide a selection for 'online' or 'Batch' prediction. Based on the prediction type selection (Online, Batch), we execute either of two code blocks. 

**Online type:** We collect the user input values in variables through sliders and create a pandas dataframe *input_df*. We pass it to *predict()* function and receive the point prediction. When we click on **Predict** button in the web app, the success message displays the result:

<span style="color:green"> The sales is $X.XX </span>
