---
layout: single
sidebar: true
author_profile: true
title: "Be Creative with Dependency Flow Diagram for Python Modules🤖"
excerpt: "Creating the dependency flow diagram on codebase is not an easy task. Efforts grow exponentially with additional scripts."
description: "Creating the dependency flow diagram on the codebase is not an easy task. Efforts grow exponentially with additional scripts."
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

Hi There,

Are you overwhelmed by the complexity of code repositories with deep layers of nested folders? 
If so, this post aims to offer some guidance to steer you in the right direction. I've personally felt that sinking 
feeling when trying to navigate through interconnected modules within nested structures. While we can track dependencies to some extent, it's easy to lose our way in the labyrinth of folders.

There are a couple of tools available, such as [`pydeps`](https://pydeps.readthedocs.io/en/latest/) or [`ModuleFinder`](https://docs.python.org/3/library/modulefinder.html), but they can be a bit daunting to
start with. For instance, using `pydeps` requires having `Graphviz` installed, which can be quite a hassle on Windows.

However, in this era of advanced language models like *Gemini 1.5 Pro* and *Claude Opus*, 
with their expansive context windows, we have a powerful resource at our disposal. If we can fit the 
entire code repository within the context window of these models, we can greatly simplify our exploration
and understanding of the codebase.

Let's understand the process as shown below:

<p align="center">
  <img width="500" height="200" src="/images_1/LLM_flow.PNG">
</p>

## Files to Prompt

x.com is the best source of resources for like-minded people provided you follow the right people. I discovered the post related to `files-to-prompt` repo. by [simon](https://twitter.com/simonw). It is a lightweight module to concatenate a 
directory full of files into a single prompt. I just had to modify it to save the prompt as a text file. You can find the module at [repo](https://github.com/simonw/files-to-prompt/tree/main). It takes the path/to/directory and saves the prompt file with minimum modification. 

If you have a directory structure as below:
```python
my_directory/
├── file1.txt
├── file2.txt
├── .hidden_file.txt
└── subdirectory/
    └── file3.txt
```

The output of the `files-to-prompt my_directory` will be (but in a terminal, modify code to save .txt file):
```python
my_directory/file1.txt
---
Contents of file1.txt
---
my_directory/file2.txt
---
Contents of file2.txt
---
my_directory/subdirectory/file3.txt
---
Contents of file3.txt
---
```

## Gemini 1.5 Pro 

The massive context window of Gemini 1.5 Pro is enough to pass mid-size repository content. You can upload the `.txt` file to Gemini 1.5 Pro and ask LLM to provide the dependency flow of modules. 

```python
graph LR
    subgraph app
        A[main.py] --> B[models.py]
        A --> C[crud.py]
        A --> D[utils.py]
        subgraph core
            B --> E[config.py]
            C --> E
            D --> E
            E --> F[db.py]
            E --> G[security.py]
        end
        subgraph api
            A --> H[api/main.py]
            H --> I[deps.py]
            I --> F
            I --> G
            H --> J[routes]
            J --> I
            J --> B
            J --> C
        end
    end
    A --> K[alembic.ini]
    A --> L[prestart.sh]

```

## Mermaid Code

[Mermaidflow](https://www.mermaidflow.app/editor)


