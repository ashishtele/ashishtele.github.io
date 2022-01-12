---
layout: single
sidebar: true
author_profile: true
title: Open Source options to your MLOps stack.
excerpt: "If you are an MLOps domain follower, I need not tell you the explosion we have been witnessing in this field."
description: "If you are an MLOps domain follower, I need not tell you the explosion we have been witnessing in this field. The field is growing leaps and bounds. Startups are securing seed fundings like never before."
comments: true
tags: ["Python","Data Scientist","USA","MLOps","Machine Learning"]
published: true
comments: true
header:
  teaserlogo:
  teaser: /images/mlops.png
  image: /images/mlops.png
  caption: "courtesy: https://cloud.redhat.com/"
gallery:

  - image_path: ''
    url: ''
    title: ''
---

Hey All,

First blog of 2022! 💪

Let me put the latest web search trend of MLOps. It has been picking up in recent years. Any guesses which country is leading the march? CHINA! We have been witnessing MLOps explosive in the US, but unware of China. Let's try to see what are the open-source building blocks we have and how can we leverage them to build a reliable data & ML stack. We have multiple options at each stage, but we will keep it open-source-focused. 

# Data Stack

The purpose of the data stack is to source data from an external system, load it in a warehouse/lakehouse, and massage it for the next journey. It can work in either of these fashions: ETL or ELT. Many companies are moving to ELT (Extract, Load, and Transform) paradigm for multiple reasons.

I was researching the modern data stack and came across [Airbyte](https://airbyte.com/), an open-source data integration solution. It eases data integration and is getting traction in the industry. I created below data stack which we mostly come across while working on small to mid-size projects. [Fivetran](https://www.fivetran.com/) is an alternative, but it is closed-source. We can create connections in Airbyte/Fivetran for the required data sources and assign the target location (mostly datalake/datawarehouse). I have referred BQ as an option. We can schedule the data load pipeline through Airflow or Prefect. I have previous blog posts on [Prefect](https://ashishtele.github.io/2021/11/Prefect_DS_Pipeline.html) for reference. I found it easy to use and schedule. Once we have data stored in BQ, the data analysis can be performed using simple SQL or dbt (SQL + Versioning). 

<p align="center">
  <img width="750" height="450" src="/images/mlops_data.PNG">
</p>
