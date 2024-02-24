---
layout: single
sidebar: true
author_profile: true
title: "Pair Programming with a Large Language Model"
excerpt: "Pair programming stands out as a collaborative practice that has gained significant traction"
description: "Pair programming stands out as a collaborative practice that has gained significant traction."
comments: true
tags: ["VertexAI", "Data Scientist", "AUTOML", "LLM", "Machine Learning", "ML System Design"]
published: true
comments: true
header:
  teaserlogo:
  teaser: /images_1/pair_pro.jpg
  image: /images_1/pair_pro.jpg
  caption: "courtesy: Gemini"
gallery:

  - image_path: ''
    url: ''
    title: ''
---

Hi All,

I recently completed a course titled "Pair Programming with an LLM" offered by [Laurence Moroney](https://laurencemoroney.com/), available on deeplearning.ai. The course proved immensely beneficial, providing valuable insights into collaborative programming with Language Models (LLMs).

Within our organization, which heavily utilizes Google technologies, we rely on PaLM and Gemini frameworks for addressing various generative AI use cases. Laurence imparted practical insights that I can readily implement within the organization, empowering me to enhance my skills and effectively train others.

```python
from google.api_core import retry
@retry.Retry()
def generate_text(prompt,
                  model=model_bison,
                  temperature=0.0):
    return palm.generate_text(prompt=prompt,
                              model=model,
                              temperature=temperature)

prompt = "Show me how to iterate across a list in Python."
VS
prompt = "write code to iterate across a list in Python"

completion = generate_text(prompt)
print(completion.result)
```

A few suggestions and recommendations:

1. `generateText` is currently recommended for coding-related prompts

2. The `@retry` decorator helps you to retry the API call if it fails

3. Set the `temperature` to `0.0` so that the model returns the same output (completion) if given the same input (the prompt)

4. The words `"show me"`tend to encourage the PaLM LLM to give more details and explanations compared to if you were to ask `"write code to ...`

```python
from google.api_core import retry

# The @retry decorator helps you to retry the API call if it fails.
@retry.Retry()
def generate_text(prompt, 
                  model=model_bison, 
                  temperature=0.0):
    return palm.generate_text(prompt=prompt,
                              model=model,
                              temperature=temperature)

## Prompt template							  
prompt_template = """
{priming}

{question}

{decorator}

Your solution:
"""

priming_text = "You are an expert at writing clear, concise, Python code."

question = "create a doubly linked list"

# Option 1:
decorator = "Work through it step by step, and show your work. One step per line."

# Option 2:
decorator = "Insert comments for each line of code."


prompt = prompt_template.format(priming=priming_text,
                                question=question,
                                decorator=decorator)
								
								
print(prompt)
completion = generate_text(prompt)
print(completion.result)

```
Prompt template:-

1. **Priming:** Getting the LLM ready for the type of task you'll ask it to do.

2. **Question:** The specific task.

3. **Decorator:** How to provide or format the output.

For generating code, we may want to experiment with other wording that would make sense if we were asking a developer the same question.

## Improving Existing Code

An LLM can help you rewrite your code in the way that's recommended for that particular language.

```python
from google.api_core import retry

@retry.Retry()
def generate_text(prompt, 
                  model=model_bison, 
                  temperature=0.0):
    return palm.generate_text(prompt=prompt,
                              model=model,
                              temperature=temperature)

# Option 1:
prompt_template = """
I don't think this code is the best way to do it in Python, can you help me?

{question}

Please explain, in detail, what you did to improve it.
"""

# Option 2:
prompt_template = """
I don't think this code is the best way to do it in Python, can you help me?

{question}

Please explore multiple ways of solving the problem, and explain each.
"""

question = """
def func_x(array)
  for i in range(len(array)):
    print(array[i])
"""

completion = generate_text(
    prompt = prompt_template.format(question=question)
)
print(completion.result)

```

## Simplify code


```python
prompt_template = """
Can you please simplify this code for a linked list in Python? \n
You are an expert in Pythonic code.

{question}

Please comment on each line in detail, \n
and explain in detail what you did to modify it, and why.
"""

question = """
class Node:
  def __init__(self, dataval=None):
    self.dataval = dataval
    self.nextval = None

class SLinkedList:
  def __init__(self):
    self.headval = None

list1 = SLinkedList()
list1.headval = Node("Mon")
e2 = Node("Tue")
e3 = Node("Wed")
list1.headval.nextval = e2
e2.nextval = e3
"""

completion = generate_text(
    prompt = prompt_template.format(question=question)
)
print(completion.result)

```


Thanks,
Ashish

