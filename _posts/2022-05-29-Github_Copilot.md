---
layout: single
sidebar: true
author_profile: true
title: Improve your code search by 2x using Github Copilot!.
excerpt: "GitHub Copilot is an AI pair programmer that helps you write code faster and with less work."
description: "GitHub Copilot is an AI pair programmer that helps you write code faster and with less work. GitHub Copilot is an artificial intelligence tool developed by GitHub and OpenAI to assist users by autocompleting code"
comments: true
tags: ["Python","Github","Copilot","MLOps","Machine Learning","ML System Design"]
published: true
comments: true
header:
  teaserlogo:
  teaser: /images/copilot.png
  image: /images/copilot.png
  caption: "courtesy: https://copilot.github.com/"
gallery:

  - image_path: ''
    url: ''
    title: ''
---
Hey there,

If you are a programming nerd, then you must have heard about the [Github Copilot](https://copilot.github.com/) initiate. The project claims it as 'Your AI pair programmer'. 
I had to wait a long to  access to the technical preview. I use it regularly on my personal laptop as an extension for VS Code and so far, I have been enjoying it!

Those who don't know, it is an AI pair programmer that helps to code faster. It draws context from comments and code to suggest lines of code . It is powered by OpenAI Codex and was trained on publicly available souce code and natural language. It does not write perfect code rather tries to understand intent and generate the best code it can. 

A few of the peculiar use cases:

1. Write a comment describing the logic you want and the copilot will assemble code for you. Consider a simple example of converting string to datetime. I wrote a comment in plain english and the copilot started suggesting the plausible options.

<p align="center">
  <img src="https://raw.githubusercontent.com/ashishtele/ashishtele.github.io/master/images/copilot1.gif" width=750>
</p>

2. Produce a boilerplate and repetitive code by feeding a few examples e.g. list of months, SQL CTE, code indentation, etc.

3. Getting an alternative to the written code. There are a couple of options to get the next suggestion. We can see the alternative option or multiple suggestions using 'Ctrl+Enter'.

4. Writing unit tests using copilot suggestions is one of the most creative usages I found. Unit tests are time-consuming and hence mostly overlooked during MLOps. Copilot can be very handy in such scenarios. e.g., I have a read_params() function which takes config_path and returns a dictionary of parameters. Once I have the function defined, I wrote the comment for Copilot to suggest the unit test case(s) for the read_params() and the result is as below:

<p align="center">
  <img src="https://raw.githubusercontent.com/ashishtele/ashishtele.github.io/master/images/tests.gif" width=750>
</p>

5. Code without spending most of your time searching the web. It is one of my favorite options. It saves a lot of time. As shown below, we need to write draw_distribution_plot() to get the code along with docstrings. 

<p align="center">
  <img src="https://raw.githubusercontent.com/ashishtele/ashishtele.github.io/master/images/dis_plot.gif" width=750>
</p>

[GitHub Copilot X](https://github.blog/2023-03-22-github-copilot-x-the-ai-powered-developer-experience/) is adopting OpenAI’s new GPT-4 model. They are introducing chat and voice for Copilot, and bringing Copilot to pull requests, the command line, and docs to answer questions on your projects

I will keep adding the use cases if I come across any!

Thank you!!
