---
layout: single
title: USA Traffic Accidents!!
author: Ashish Tele
excerpt: "This blog highlights few findings from a countrywide traffic accident dataset (USA), collected from February 2016 to December 2019, using several data providers, including two APIs which provide streaming traffic event data. There are about 3.0 million accident records in this dataset."
description: "This blog highlights few findings from a countrywide traffic accident dataset (USA), collected from February 2016 to December 2019, using several data providers, including two APIs which provide streaming traffic event data. There are about 3.0 million accident records in this dataset."
permalink:
comments: true
tags: ["Data Science","R","Data Mining","Accidents","USA"]
published: true
comments: true
author_profile: false
header:
  teaserlogo:
  teaser: /images/US_5.PNG
  image: /images/US_5.PNG
  caption:
gallery:

  - image_path: ''
    url: ''
    title: ''
---
Happy New Year!!!

Recently I came across a dataset on [Kaggle](https://www.kaggle.com/sobhanmoosavi/us-accidents) about USA traffic accidents (2016-19). As per the [Kaggle](https://www.kaggle.com/sobhanmoosavi/us-accidents), "This is a countrywide traffic accident dataset, which covers 49 states of the United States. The data is collected from February 2016 to March 2019, using several data providers, including two APIs which provide streaming traffic event data. These APIs broadcast traffic events captured by a variety of entities, such as the US and state departments of transportation, law enforcement agencies, traffic cameras, and traffic sensors within the road-networks. Currently, there are about 2.25 million accident records in this dataset."

I found this dataset very interesting because of the data size and efforts authors put to gather the data. A huge shout out to them! There are many notebooks available on Kaggle for reference purposes. I explored the dataset using RStudio.

**Acknowledgments**

* Please cite the following papers if you use this dataset:
  Moosavi, Sobhan, Mohammad Hossein Samavatian, Srinivasan Parthasarathy, and Rajiv Ramnath. [“A Countrywide Traffic Accident Dataset.”](https://arxiv.org/abs/1906.05409), 2019.

* Moosavi, Sobhan, Mohammad Hossein Samavatian, Srinivasan Parthasarathy, Radu Teodorescu, and Rajiv Ramnath. ["Accident Risk Prediction based on Heterogeneous Sparse Data: New Dataset and Insights."](https://arxiv.org/abs/1906.05409) In Proceedings of the 27th ACM SIGSPATIAL International Conference on Advances in Geographic Information Systems, ACM, 2019.

**USA Traffic Accidents by States (2016-19)**

As we can see, **California** tops the chart with the maximum number of traffic accidents in the period 2016-19. **California** has recorded more than double traffic accidents than that recorded in **Texas**.

<p align="center">
  <img width="650" height="500" src="/images/US_1.PNG">
</p>


<p align="center">
  <img width="650" height="500" src="/images/US_2.PNG">
</p>


**USA Traffic Accidents by Counties (2016-19)**

**Lod Angeles** has recorded whopping **172K** traffic accidents during this time period. LA is followed by **Harris**(TX) and **Mecklenburg**(NC). 

<p align="center">
  <img width="650" height="400" src="/images/US_3.PNG">
</p>

**USA Traffic Accidents by Severity (2016-19)**

**South Dakota** and **Wyoming** have high average traffic accident severity among all the states. 

<p align="center">
  <img width="650" height="400" src="/images/US_4.PNG">
</p>


**USA Traffic Accidents by Weather Conditions (2016-19)**

**Clear** weather condition has over **800K** traffic accidents recorded, but when we look for **overcast & cloudy** weather consitions together, they have over **1M** traffic accidents recorded.

<p align="center">
  <img width="650" height="500" src="/images/US_6.PNG">
</p>

<details>
<summary>
<a class="btnfire small stroke"><em class="fas fa-chevron-circle-down"></em>&nbsp;&nbsp;Show Code</a>    
</summary>

<p align="center">
  <img width="600" height="600" src="/images/code1.PNG">
</p>

</details>
