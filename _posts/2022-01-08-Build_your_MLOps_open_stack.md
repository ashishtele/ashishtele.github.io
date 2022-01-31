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

We can take advantage of [dbt + Airflow + Great Expectations](https://github.com/spbail/dag-stack) trio. [Great Expectations](https://greatexpectations.io/) is an open-source data quality solution. I found it very helpful both for personal and professional work. I tried [TFDV](https://www.tensorflow.org/tfx/data_validation/get_started) and [Great Expectations](https://greatexpectations.io/) for data validation and data quality checks in my MLOps pipeline on GCP. I am looking after using [deepchecks](https://github.com/deepchecks/deepchecks) for upcoming projects. We can deploy this Airflow DAG on Cloud Composer.

Now we have options such as [Looker](https://looker.com/google-cloud), [Superset](https://superset.apache.org/), and a recent addition of [Lightdash](https://github.com/lightdash/lightdash) for exploratory analysis. We can use [Tableau](https://www.tableau.com/) and/or [Power BI](https://powerbi.microsoft.com/en-us/) as well. A lot of options out there! I use [Data Studio](https://analytics.google.com/analytics/academy/course/10) and [Power BI](https://powerbi.microsoft.com/en-us/) for most of my work.

<p align="center">
  <img width="750" height="450" src="/images/mlops_data.PNG">
</p>

# ML Stack

<p align="center">
  <img width="750" height="450" src="/images/mlops_data1.PNG">
</p>

Let's assume we have structured data in Google BQ. We have multiple options to optimize the data storage in BQ based on the applications. The [materialized views](https://cloud.google.com/bigquery/docs/materialized-views-best-practices) are worth exploring for increased performance and efficiency. As per Google, "Queries that use materialized views are generally faster and consume fewer resources than queries that retrieve the same data only from the base table. Materialized views can significantly improve the performance of workloads that have the characteristic of common and repeated queries."

When it comes to data validation, it is an integral part of MLOps and can be added at multiple milestones. We have many promising options to choose. [Great Expectations](https://greatexpectations.io/blog/ml-ops-great-expectations/) is one of such options. We can start using it in the Jupyter notebook and eventually make it a standard option in MLOps. It has a great option of creating an Expectation Suites to validate the new data along with Data Docs. It can also be seamlessly integrated into workflow orchestration frameworks such as Airflow and Prefect. [TFDV](https://www.tensorflow.org/tfx/data_validation/get_started) is also a useful alternative for descriptive statistics and schema reinforcement. I found GE easy to use and share.
