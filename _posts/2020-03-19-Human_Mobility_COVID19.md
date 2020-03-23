---
layout: single
title: Human Mobility data and COVID-19
author: Ashish Tele
excerpt: "Human mobility data has been pivotal in many fields. We can leverage the mobility data to track current issues."
description: "Human mobility data has been pivotal in many fields. We can leverage the mobility data to track current issues."
permalink:
comments: true
tags: ["Data Science","R","Data Mining","Optimization","USA","Image"]
published: true
comments: true
author_profile: false
header:
  teaserlogo:
  teaser: /images/covid19.jpg
  image: /images/covid19.jpg
  caption: "courtesy: gcn.com"
gallery:

  - image_path: ''
    url: ''
    title: ''
---

Hi All,

I was researching about using human mobility data for retail data science work. [Carto](https://carto.com/) works in spatially focused retail analytics. They use human mobility data to answer:

1. Reduce traffic congestion
2. Insights on commuting patterns
3. Incident responses

I am writing this blog when **COVID-19** is at its peak in **Itlay** and **Spain**. As per the research, the **USA** and **India** are 8-10 days behind the curve observed in Itlay and Spain if the required precautions are overlooked. 

I was reading a couple of articles from India where the person who was asked to self-quarantine, disobeyed the rule and traveled through public transportation. The person endangered the lives of many people including oneself. It becomes difficult to retrace the route a person used before getting identified. Also, it is an arduous job for the officials to understand and estimate how many people did come in contact with the probably infected person. 

**Can we not use anonymized human mobility data to check probable spread?**

I came across an article by [Google AI](https://ai.googleblog.com/2019/11/new-insights-into-human-mobility-with.html) which mentions how human mobility data can be used for predicting epidemics. Data is completely anonymized and hence the user information is secured. 

While writing this blog, the Singapore government released a mobile application named [TraceTogether](https://twitter.com/GovTechSG). It is a very innovative approach to keep people safe provided an infected patient obliges. It is a Bluetooth technology-based application that estimates proximity between users.

Can we not implement something:

1. As most of the positive cases in India have out of country travel history, ask each traveler to register once mobile number or allow the government to record the location history of traveler (ANONYMIZED) until the COVID-19 test results come.
2. Human mobility (cellular data) of each traveler will be out of the system if the test comes negative. 
3. If the test comes positive, then the patient can be traced through mobility data or GPS. 
4. Not only this, but the journey of the patient can also be simulated using the data points. The possible exposure to the crowd can be estimated. Also, a general advisory can be circulated among the people who were there when the patient traveled.
