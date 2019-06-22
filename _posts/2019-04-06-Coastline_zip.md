---
layout: posts
title: "Coastline Zip Codes (USA)"
date: 2019-04-06 12:00:00 -0400
comments: true
tags: "Zip"
---

Hi All,
We came across a situation where we had to find the zip codes across US coastline. The consumer behavior and buying patterns are different across the coastline. We need to make strategies and give promotions accordingly.  Finding the zip codes closer to the coastline is difficult and we don't have a direct approach to search the zips.

I tried to find the coastline zips by calculating the distances from different reference points. I used the geographical centers of the USA, the geographical centers of the coastline US states, and three reference points in the ocean. The distances between lat and long using below formula:

=ACOS(COS(RADIANS(90-Lat1)) *COS(RADIANS(90-Lat2)) +SIN(RADIANS(90-Lat1)) *SIN(RADIANS(90-Lat2)) *COS(RADIANS(Long1-Long2))) *6371.

[Reference](http://bluemm.blogspot.com/2007/01/excel-formula-to-calculate-distance.html)

The data for the united state's zip codes are downloaded from [zipcodes.org](http://bluemm.blogspot.com/2007/01/excel-formula-to-calculate-distance.html). 
It gives the list of all zip codes across the USA and respective lat and long. I referred [Wikipedia](https://en.wikipedia.org/wiki/Geographic_center_of_the_United_States) 
to find the geographical center of the USA and the geographical centers of the coastline US states. Also, I used the reference points in the oceans: 
1. North Pacific Ocean
2. North Atlantic Ocean
3. Gulf of Mexico

Distance Calculations:
1. US geographical center to each zip:
This distance should be maximum for the coastline zip codes, but it gives the circular curve which needs additional calculations.

2. The geographical centers of the coastline US states to each zip:
This distance should also be maximum for the coastline zip codes with a condition: the distance between the US geographical center to each state geographical center should be greater than that between the US geographical center to each zip. It is included as a flag on the dashboard.
I did the calculation to scale the distances as it differs for each state. 

3. The ocean reference points to each zip:
This distance should be minimum for the coastline zip codes. It also gives the circular curvatures, but the combinations of the other two calculations give the required zip codes.

Please find the below screenshot for Texas reason:

![center](/images/ZIP.PNG)

 
