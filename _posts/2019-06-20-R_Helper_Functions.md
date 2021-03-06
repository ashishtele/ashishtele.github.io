---
layout: single
title: "R Helper Functions - Expedite your work"
author: Ashish Tele
comments: true
excerpt: "R helper functions make easier to read programs. We can reuse the computations and code snippet. It is best to create a list of helper functions and source them whenever we run the program."
description: "R helper functions make easier to read programs. We can reuse the computations and code snippet. It is best to create a list of helper functions and source them whenever we run the program."
tags: ["Data Science","Earthquake","Machine Learning (ML)","Artificial Intelligence (AI)","Data Mining","Data Engineering","Pyhton","R","SAS","NY","Helper Function","Rockstar R"]
published: true
comments: true
author_profile: false
header:
  teaserlogo:
  teaser: /images/robot.PNG
  image: /images/robot.PNG
  caption:
gallery:
  - image_path: ''
    url: ''
    title: ''
---
Hi All, 
I am adding the code snippets which I often use. It is always a good practice to create and 
maintain the custom functions in R and Python. We can attach the user-defined functions' file at the
top of the main script.

### 1. System Time
```ruby

st <- function() 
      {Sys.time()}

```
### 2. Working with NAs
```ruby

if.na <- function(x,y) 
        {ifelse(is.na(x),y,x)}

if.na.0 <- function(x) 
        {ifelse(is.na(x),0,x)}

```

We often require to modify the number formats by converting to text string.

### 3. Number Format (Percent & Comma)
```ruby

percent <- function(x, digits = 1, format = "f", ...) 
{
  paste0(formatC(100 * x, format = format, digits = digits, ...), "%")
}

comma <- function(x, digits = 0, format = "f", ...) 
{
  format(x, big.mark=",", digits=digits)
}

```
When we need to count the missing and duplicate records in the data, we can use the below lines of code:
### 4. Missing and Duplicate
```ruby

countMissing <- function(x) 
{
  ## calculate counts
  missing = sum(is.na(x))
  if (mode(x) == "character") 
  emptyStrings = sum(x=="", na.rm=TRUE) 
  else emptyStrings = 0
  totalRows = NROW(x)
  nonMissing = totalRows - missing - emptyStrings
  
  ## present results
  cat("#           TOTAL ROWS: ", totalRows, " (", percent(totalRows/NROW(x)), ")\n", sep="")
  cat("# Missing Values (NAs): ", missing, " (", percent(missing/NROW(x)), ")\n", sep="")
  cat("# Empty Strings (\"\"): ", emptyStrings, " (", percent(emptyStrings/NROW(x)), ")\n", sep="")
  cat("   # Non-missing Value: ", nonMissing, " (", percent(nonMissing/NROW(x)), ")\n", sep="")
  cat("   #      Mode & Class: ", mode(x), ", ", class(x), "\n", sep="")
}

```
```ruby
countDups <- function(x) 
{
  cat("    Rows of Data: ", NROW(x), "\n", sep="")  
  cat("   Unique Values: ", length(unique(x)), "\n", sep="")
  cat("Duplicate Values: ", sum(duplicated(x)), "\n", sep="")
  cat("  Missing Values: ", sum(is.na(x)), " (", percent(sum(is.na(x))/NROW(x)), ")\n", sep="")
  cat("    Mode & Class: ", mode(x), ", ", class(x), "\n", sep="")
}

```
I will keep updating this post with more helper functions. Please drop a comment if you need more helper functions.

Thank you!.
