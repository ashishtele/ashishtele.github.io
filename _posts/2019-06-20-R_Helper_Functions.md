---
layout: posts
title: "R Helper Functions - Expedite your work"
date: 2019-06-20 12:00:00 -0400
comments: true
tags: "R"
---
Hi All, I am adding the code snippets which I often use. It is always a good practice to create and 
maintain the custom functions in R and Python. We can attach the used defined functions' file at the
top of the main script.

### 1. System Time
```{r}

st <- function() 
      {Sys.time()}

```
### 2. Working with NAs
```{r}

if.na <- function(x,y) 
        {ifelse(is.na(x),y,x)}

if.na.0 <- function(x) 
        {ifelse(is.na(x),0,x)}

```
