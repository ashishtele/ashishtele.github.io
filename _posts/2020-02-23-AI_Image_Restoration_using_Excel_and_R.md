---
layout: single
title: AI Image Restoration using Excel and R
author: Ashish Tele
excerpt: "When you encounter an old image which is damaged, being a data scientist, you need to find a way to restore the image."
description: "When you encounter an old image which is damaged, being a data scientist, you need to find a way to restore the image."
permalink:
comments: true
tags: ["Data Science","R","Data Mining","Optimization","USA","Image"]
published: true
comments: true
author_profile: false
header:
  teaserlogo:
  teaser: /images/image_ai1.PNG
  image: /images/image_ai1.PNG
  caption: "courtesy: usmsystems.com"
gallery:

  - image_path: ''
    url: ''
    title: ''
---

In 2015, I received a case study with an open problem asking to find an answer, that is all. It had an excel with a big sparse matrix. It was an image processing problem. I submitted a naive answer but the fastest to reach. I solved it in Excel with conditional formatting 😂. I think they were not expecting this approach but I came across a baseline solution with minimal resources. When I put conditional formatting on the matrix and zoom out the Excel to 10%, I arrived the answer 💪. Not all solutions need advanced approaches, common sense is important. 

When I was going through my archive, I found this picture. My old picture but in deformed condition. I tried many online portals to bring it back to original, but most of them can't restore it to the original. So, finally, get your hands dirty!

<p align="center">
  <img width="300" height="453" src="/images/me.jpeg">
</p>

Let us import the image and extarct the grayscale. Find the R code snippet below. I averaged out the values to fetch the grayscale values. Final line of code is user defined function to copy the data in clipboard then pasting in Excel.

```ruby

library(raster)
library(dplyr)
library(tidyverse)
library(tibble)

color_image <- brick("E:\\Study\\Power_BI\\me.jpeg")
color_values <- getValues(color_image)

# Dimensions of the image
img_width <- 400
img_heigh <- 533

color_table <- as.data.frame(color_values)
color_table$avg <- (color_table$me.1 + color_table$me.2 + color_table$me.3)/3

append_vector <- rep(1:img_width,img_heigh)
append_vector1 <- rep(1:img_heigh, each = 400)
  
color_table$rank <- append_vector
color_table$sr_no <- append_vector1

color_table$me.1 <- NULL
color_table$me.2 <- NULL
color_table$me.3 <- NULL

color_table %>% 
  tidyr::spread(rank, avg) -> color_table1

color_table1$sr_no <- NULL

# Copying the large matric in Excel
copy(color_table1)

```
Once I converted it to grayscale and pasted the matrix in Excel, these are the steps I followed:

1. Shortening the Column width (Alt + O + C + W) to **1**.
2. Shortening the Row height (Alt + O + R + E) to **5**.
3. Zooming out the excel to **10%**.

This is how it looks in Excel!! We can see the **white** patches on the picture predominantly. 

<p align="center">
  <img width="300" height="453" src="/images/me1.PNG">
</p>

Now it is time to try for different **kernels** to smoothen the image. I tried two approached:

1. Using a 3X3 kernel to fill the center value.
2. Using the values of 24 cells around the targeted cell to fill it.

<p align="center">
  <img width="700" height="300" src="/images/kernel1.PNG">
</p>

If you see the below screenshot, you can trace precedents using Excel formulas. Each output cell is calculated by multiplying the kernel and the original image matrix. It is a kind of **Convolution** in Excel.


<p align="center">
  <img width="500" height="200" src="/images/kernel4.PNG">
</p>
