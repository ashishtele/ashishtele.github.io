---
layout: single
title: Coastline Zip Codes (USA) - New Approach
author: Ashish Tele
excerpt: "While working on a project, we came across a scenario where we had to find the coastline zipcode. 
This post explains the approach I used."
description: "While working on a project, we came across a scenario where we had to find the coastline zipcode. 
This post explains the approach I used."
permalink:
comments: true
tags:   ["Data Science","USA","Machine Learning (ML)","Data Mining","Data Engineering","Pyhton","R","Zip","Zip code","Coastline","America"]
published: true
comments: true
author_profile: false
header:
  teaserlogo:
  teaser: /images/US_map1.PNG
  image: /images/US_map1.PNG
  caption: "courtesy: https://weather.com/"
gallery:
  - image_path: ''
    url: ''
    title: ''
---
The last blog gives an approach to find the coastline zip codes. I followed the relative distances calculation approach to find the zip codes. I came across ['Natural Earth'](https://www.naturalearthdata.com/) and an R package ['rnaturalearth'](https://cran.r-project.org/web/packages/rnaturalearth/README.html) which is the API to the site. 

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
The CSV file extract is available on my github page to download.

I used [Mapbox](https://docs.mapbox.com/help/tutorials/power-bi/) for map visualization. Below graph shows the coastline boundary (including Alaska).

![center](/images/coast_zip.PNG)

Once I had the coastline lat and long, I wrote SQL query conditioned on lat and long (e.g. lat - 0.02 > zip_lat > lat + 0.02) to fetch the ZIP codes. It gave a good match to pull ZIP codes. The below graph shows the boundary highlighting the ZIP codes (excluding Alaska) 

![center](/images/zip1.PNG)


The below piece of code gives the distance in Km from the coastline coordinates. The distance can be used as a filter on the dashboard as shown. 

```ruby
# Distance calculations
USA <- ne_countries(scale = 110, 
                    country = "United States of America", 
                    returnclass = "sf")
proj4string(USA)
USA <- st_transform(USA, 3055)
# Grid formation
grid <- st_make_grid(USA, 
                     cellsize = 50000, 
                     what = "centers")
grid <- st_intersection(grid, USA)
plot(grid)

USA_cast <- st_cast(USA, "MULTILINESTRING")
distance <- st_distance(USA_cast, grid)

df <- data.frame(dist = as.vector(distance)/1000,
                 st_coordinates(grid))


# Converting to required projection (longlat)
dfcoor <- df
coordinates(dfcoor) <- ~X+Y
proj4string(dfcoor) <- CRS("+proj=utm +zone=27 +ellps=intl +towgs84=-73,47,-83,0,0,0,0 +units=m +no_defs")
dfcoor_lat <- spTransform(dfcoor, 
                          CRS("+proj=longlat +ellps=WGS84 +datum=WGS84"))
df_lat <- coordinates(dfcoor_lat) %>% 
  data.frame() %>% 
  rename(long = X, lat = Y)

# Combining the tables
USA_dataset <- cbind(df, df_lat)
write.csv(USA_dataset, "E:\\Study\\Power_BI\\USA_dataset.csv")
```

The below piece of code gives the distance in Km from the coastline coordinates. The distance can be used as a filter on the dashboard as shown. 

![center](/images/distance_report.PNG)

The USA_dataset which includes the distance values is available on my github page. 

Thank you for reading the post!
