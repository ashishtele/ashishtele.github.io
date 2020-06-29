---
layout: single
title: Refer this if you need PySpark or SparkR code snippets!
author: Ashish Tele
excerpt: "We need to change the table formats from spark dataframes to pandas or R dataframe when we prefer SQL, Python, and R in the same notebook. I had to search online a lot these code snippets."
description: "We need to change the table formats from spark dataframes to pandas or R dataframe when we prefer SQL, Python, and R in the same notebook. I had to search online a lot these code snippets."
permalink:
comments: true
tags: ["Data Science","R","Data Scientist","India","USA","PySpark","Python"]
published: true
comments: true
author_profile: false
header:
  teaserlogo:
  teaser: /images/pyspark.png
  image: /images/pyspark.png
  caption: "courtesy: Cambridge Spark"
gallery:

  - image_path: ''
    url: ''
    title: ''
---
Hi All,

Lately, I started coding extensively on Databricks (Microsoft Azure) using PySpark and SparkR. The platform is versatile as we can use the language of our preference interchangeably. I prefer R (a personal favorite) over Python. I find data cleaning, data transformation (dplyr), and visualization very intuitive in R. PySpark syntax are also easy to grasp. I want to highlight some of my findings and a few of the great resources I came across.

```ruby
library(dplyr)
library(SparkR)

SparkR_frame <- sql("select * from 
                     zip_codes")
R_dataframe <- collect(SparkR_frame)

```
The above code snippet is very simple to interpret, but when you run it, you would encounter an error which difficult to understand on databricks. **collect()** was masked by the **dplyr** package and couldn't convert to R data frame for me. Including package name before method/function would return the desired result.

```ruby
R_dataframe <- SparkR::collect(SparkR_frame)
```

I reached out to [Bryan Cafferky](https://www.linkedin.com/in/bryancafferky/) on LinkedIn asking for help after watching his ['Azure Databricks with R: Deep Dive'](https://www.youtube.com/watch?v=-vekHiJdQ1Y) video on Youtube. He provided an example to convert SQL spark dataframe to SparkR dataframe. Finally, the trial and error method resolved this simple conflict.

1. If you have a table in Azure Databricks database (library), you can directly query the table in a notebook by adding **%sql** at the top of the cell and executing the query.

```ruby
%sql

select * from database.table_name 

# Ctrl + Enter: Shortcut to run
```
