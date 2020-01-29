---
layout: single
title: "The Ground Water Crisis in India!!"
author: Ashish Tele
excerpt: "This blog highlights few findings from a countrywide traffic accident dataset (USA), collected from February 2016 to December 2019, using several data providers, including two APIs which provide streaming traffic event data. There are about 3.0 million accident records in this dataset."
description: "This blog highlights few findings from a countrywide traffic accident dataset (USA), collected from February 2016 to December 2019, using several data providers, including two APIs which provide streaming traffic event data. There are about 3.0 million accident records in this dataset."
permalink:
comments: true
tags: ["Data Science","Ground","Pyhton","R"," Dashboard","DS","water","India"]
published: true
comments: true
author_profile: false
header:
  teaserlogo:
  teaser: /images/India-water-crisis.png
  image: /images/India-water-crisis.png
  caption:
---
I have been a big fan of open government data sources such as [data.gov.in](https://data.gov.in/) and [data.gov](https://www.data.gov/). Recently I came across a data source called [Dynamic Ground Water Resources](https://data.gov.in/resources/district-wise-dynamic-ground-water-resources-march-2013). It has rich information about groundwater recharge (rainfall) and discharge (draft), The data column definitions were new to me so I have added
them for reference purposes.

**Groundwater draft**: It is the quantity of **groundwater** withdrawn artificially or naturally from the aquifers in a study area, during a certain period. The outflow from the system is mainly considered through the **groundwater draft**. [Ref](https://shodhganga.inflibnet.ac.in/bitstream/10603/70835/14/14_chapter%205%20groundwater.pdf)

**HaM (hectare-meter)**: A volume of 10000 cubic meters created by flooding an area of one hectare to a depth of one meter, thus creating a volume one hectare by one meter. [Ref](http://www.kylesconverter.com/volume/hectare-meters-to-cubic-meters)

It contains the information of **662** Indian districts. The overall data quality is good. It does not have many **NA** values. The column names (metric) are self-defining. The information is available as of **March 2013**. 

The below chart shows the number of districts by states and UTs studied to collect the groundwater data. **Uttar Pradesh** has most districts studied for this research.

![center](/images/gw1.PNG){: .align-center}

**Paschim Medinipore** district in West Bengal received the highest rainfall during monsoon season in India. Interestingly, the top 3 districts belong to **West Bengal**.

![center](/images/gw2.PNG){: .align-center}

The below heatmap shows the districts with comparatively high groundwater availability in HaM. We can see the belt across the northeastern part of India. The districts falling under this belt had a high density of groundwater level in **2013**.

![center](/images/gw3.PNG){: .align-center}

When we see the average annual groundwater availability (HaM) by states, **Telangana** and **Andra Pradesh** take places in the top list. The numbers contradict with the current google searches. As per [the report](https://www.thehindu.com/news/cities/Hyderabad/telangana-sees-sharp-drop-in-groundwater-table/article28160098.ece), Telangana sees a sharp drop in the groundwater table.

![center](/images/gw4.PNG){: .align-center}

Let's see what does projected demand for Domestic and Industrial Uses up to 2025 say. We have information about the current draft due to Domestic and Industrial water supply needs (2013) and projected demand (2025) for it. The below chart shows districts with the most % increase in the demand for Domestic and Industrial uses. 

![center](/images/gw5.PNG){: .align-center}

As you can in the above chart, these districts are expected to see a huge spike in the demand for domestic and industrial uses. Interestingly, all top districts belong to **Manipur** and **Meghalaya** states from northeastern India.

Let's check out an important metric called a stage of groundwater development.

**The stage of groundwater development** is a ratio of Annual Ground Water Draft and Net Annual Ground-Water Availability in percentage.
[Ref](http://cgwb.gov.in/faq.html). The reference page gives details of the criteria for the categorization of assessment units. We will create a factor column for an analysis purpose.

The below chart shows the overexploited districts of India. The size of the bubble shows how big exploitation is. I filtered the districts with the stage of groundwater development is more than **100%**. **Kala Amb** district of **Himachal Pradesh** has the most stage of groundwater development of astounding **411%**.

![center](/images/gw6.PNG){: .align-center}

I created the categories as mentioned by Central Ground Water Board. I then developed a **Power BI** dashboard where we can filter the states and districts based on the category. Again, the bubble size determines the extent of exploitation. 

![center](/images/gw7.PNG){: .align-center}

1. **Delhi** has the highest average stage of groundwater development followed by **Punjab** and **Haryana**.
2. **Karnataka** and **Tamilnadu** have overexploitation in South India.
3. **16%** of Indian districts are overexploited (2013). The number must have skyrocketed by now.

Thank you for reading this article!!

