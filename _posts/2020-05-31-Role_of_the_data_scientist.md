---
layout: single
title: Role of the Data Scientist
author: Ashish Tele
excerpt: "The role of the data scientist is not always well defined and well structured. People have various views regarding this role."
description: "The role of the data scientist is not always well defined and well structured. People have various views regarding this role."
permalink:
comments: true
tags: ["Data Science","R","Data Scientist","India","USA","Role"]
published: true
comments: true
author_profile: false
header:
  teaserlogo:
  teaser: /images/cover_DS.png
  image: /images/cover_DS.png
  caption: "courtesy: houseofbots.com"
gallery:

  - image_path: ''
    url: ''
    title: ''
---
Hi All,

I came across the article ["The Role of the Data Scientist"](https://blog.rstudio.com/2020/05/27/role-of-the-data-scientist/) by Carl and Sean. They have raised a few burning questions about the data scientist role such as:

1. Will automation replace the data scientist role?
2. Does 'intuition' still play a pivotal role in the industry or the data-driven approach is well received?
3. Has the data scientist role plateaued?

Carl and Sean made a very impactful point on why organizations need data scientists more than ever. The most resonating point for me is, **'Identifying and solving hard problems can't be automated !'**. Why?

1. As Carl and Sean mention, the data extraction and visualization of structured data can be automated using different tools. The problems are well defined and understood in these scenarios. 

2. The well-defined problems with structured data can be automated by making data pipelines, model development, and deploying in production. We have seen enormous test cases leveraging it.

3. But what about the real-life problems which are difficult to comprehend and with minimal references from the past. We encounter such cases in healthcare, NPL, imaging, scenario planning, etc.

4. One of the examples I can give is of demand forecasting in the COVID19 pandemic period. It is an unprecedented problem. We had a few outbreaks, the global recession, etc but the COIVD19 outbreak has locked the people in homes and changed the buying pattern.

5. Forecasting the demand in the COVID19 period is different when compared to traditional forecasting problems. Albeit having enough sales/demand data, the deciding factors such as COVID cases, Unemployment claims, mobility, states opening dates have limited historical data.  

6. Limited historical data of regressors make the short-term forecast reasonably unpredictable. The confidence intervals are wider, making the strategic decisions difficult. 

7. Solving this problem and putting in production is difficult as with each new data point, the output varies drastically at various granularity. The COVID cases follow different trends during weekdays and weekends changing the short-term forecast. States' post-opening response is different than the pre-lockdown phase. We know more see the panic buying now. Capturing this transition in the model is a dynamic process. 

8. As the post mentions, the results provided by the Data Scientists should be credible, agile, and durable. Data Scientists need to create models that can be explained to the peer group. Agility is important to address a real-world problem such as COVID19 forecasting etc. which required multiple iterations. Durable results are the ones that survive the methodology, not the technology improvement,eg., Market Mix Modeling.

Thank you!
