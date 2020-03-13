---
layout: single
title: Cannibalization Effect in Optimization
author: Ashish Tele
excerpt: "It is very important to incorporate the cannibalization effect in realtime optimization problems. This post describes my approach from scratch in developing the methodology."
description: "It is very important to incorporate the cannibalization effect in realtime optimization problems. This post describes my approach from scratch in developing the methodology."
permalink:
comments: true
tags: ["Data Science","R","Data Mining","Optimization","USA"]
published: true
comments: true
author_profile: false
header:
  teaserlogo:
  teaser: /images/opti.PNG
  image: /images/opti.PNG
  caption: "courtesy: Khan Academy"
gallery:

  - image_path: ''
    url: ''
    title: ''
---
Hi All,

Optimization is one of my favorite topics to brainstorm. I was working on an optimization problem where I had to incorporate a cannibalization effect. 

**Cannibalization Effect:** [Cannibalization](https://link.springer.com/article/10.1057/rpm.2012.22) is a challenger for any pricing strategist as the topic refers to the reduction in sales volume or revenue as a result of the introduction of a new product or service. For example, when Coca Cola introduced Coke Zero to compete alongside Diet Coke the introduction would have impacted the product. [Ref](https://link.springer.com/article/10.1057/rpm.2012.22)  

I have highlighted my implementation methodology in this post. I have taken an example of a store and supporting calculations. Consider than we have 6 products in a store as shown. We can introduce 3 new products and replace existing products based on the revenue performace. We can come up to **probable addition** product list by different techniques.

<p align="center">
  <img width="250" height="250" src="/images/store1.PNG">
</p>

The below screenshot shows cannibalization coefficients both for addition and deletion. e.g. when the product P1 is removed as a part of optimization, its revenue R1 is split among other products and the product P2 would receive R1xRC2 addition revenue and so on. The situation is similar when a new product is added.

<p align="center">
  <img width="500" height="250" src="/images/store2.PNG">
</p>

 The below image shows an example of selection criteria. We are trying to remove product P1 and add product P7. The final revenue is the summation of individual product revenue and the components of actual revenue.

<p align="center">
  <img width="500" height="90" src="/images/store3.PNG">
</p>

In the given example, we have 6 products in the store and 3 probable additions. So each product will have 3 probable substitions and total 6x3 = 18 combinations.
