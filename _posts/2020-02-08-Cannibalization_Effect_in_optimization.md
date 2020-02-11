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

I have highlighted my implementation methodology in this post. I have taken an example of a store and supporting calculations. 
