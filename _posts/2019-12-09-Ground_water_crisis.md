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

The below chart shows the number of districts by states and UTs studied to collect the groundwater data. **Uttar Pradesh** has most districts studied for this research.

![center](/images/gw1.PNG)

**Paschim Medinipore** district in West Bengal received the highest rainfall during monsoon season in India. Interestingly, the top 3 districts belong to **West Bengal**.

![center](/images/gw2.PNG)

The below heatmap shows the districts with comparatively high groundwater availability in HaM. We can see the belt across the northeastern part of India. The districts falling under this belt had a high density of groundwater level in **2013**.

![center](/images/gw3.PNG)

When we see the average annual groundwater availability (HaM) by states, **Telangana** and **Andra Pradesh** take places in the top list. The numbers contradict with the current google searches. As per [the report](https://www.thehindu.com/news/cities/Hyderabad/telangana-sees-sharp-drop-in-groundwater-table/article28160098.ece), Telangana sees a sharp drop in the groundwater table.

![center](/images/gw4.PNG)

Let's see what does projected demand for Domestic and Industrial Uses up to 2025 say. We have information about the current draft due to Domestic and Industrial water supply needs (2013) and projected demand (2025) for it. The below chart shows districts with the most increase in the demand for Domestic and Industrial uses. 

![center](/images/gw5.PNG)

As you can in the above chart, these districts are expected to see a huge spike in the demand for domestic and industrial uses. Interestingly, all top districts belong to **Manipur** and **Meghalaya** states from northeastern India.
