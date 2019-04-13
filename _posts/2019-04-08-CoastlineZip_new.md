---
layout: posts
title: "Coastline Zip Codes (USA) - New Approach"
date: 2019-04-09 12:00:00 -0400
comments: true
tags: "Zip"
---
Hi All,

The last blog gives an approach to find the coastline zip codes. I followed the relative distances calculation approach to find the zip codes. I came across "Natural Earth" and an R package 'rnaturalearth' which is the API to the site. 

The piece of code gives the Latitude and Longitude coordinates of the coastline zip codes:

```{r}
library(tidyverse)
library(sf)
library(raster)
library(rnaturalearth)
library(rgeos)

USA <- ne_countries(scale = 110, 
                    country = "United States of America", 
                    returnclass = "sf")
USA_lat_long <- st_transform(USA, 
                             "+proj=longlat +ellps=WGS84 +datum=WGS84")
USA_df_lat <- st_coordinates(USA_lat_long) %>% 
  data.frame() %>% 
  dplyr::rename(long = X, lat = Y) %>% 
  dplyr::select(lat,long)

```
I used Mapbox for map visualization. Below graph shows the coastline boundary (including Alaska).


![center](/images/zip1.PNG)
