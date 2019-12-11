---
layout: posts
title: "The Ground Water Crisis in India!!"
date: 2019-12-09 12:00:00-0400
comments: true
tags: ["Data Science","Chart","reports","Artificial Intelligence (AI)","Data Mining","Ground","Pyhton","R","SAS"," Dashboard","DS","water","India"]
---
I have been a big fan of open government data sources such as [data.gov.in](https://data.gov.in/) and [data.gov](https://www.data.gov/). Recently I came across a data source called [Dynamic Ground Water Resources](https://data.gov.in/resources/district-wise-dynamic-ground-water-resources-march-2013). It has rich information about groundwater recharge (rainfall) and discharge (draft), The data column definitions were new to me so I have added
them for reference purposes.

**Groundwater draft**: It is the quantity of **groundwater** withdrawn artificially or naturally from the aquifers in a study area, during a certain period. The outflow from the system is considered mainly through the **groundwater draft**. [Ref](https://shodhganga.inflibnet.ac.in/bitstream/10603/70835/14/14_chapter%205%20groundwater.pdf)

**HaM (hectare-meter)**: A volume of 10000 cubic meters created by flooding an area of one hectare to a depth of one meter, thus creating a volume one hectare by one meter. [Ref](http://www.kylesconverter.com/volume/hectare-meters-to-cubic-meters)

It contains the information of **662** Indian districts. The overall data quality is good. It does not have many **NA** values. The column names (metric) are self-defining. The information is available as of **March 2013**. 

The below chart shows the number of districts by states and UTs studied to collect the ground water data. **Uttar Pradesh** has most districts studied for this research.

![center](/images/gw1.PNG)

**Paschim Medinipore** district in West Bengal received highest rainfaill during monsoon season in India. Interestingly, top 3 districts are belong to **West Bengal**.

![center](/images/gw2.PNG)

