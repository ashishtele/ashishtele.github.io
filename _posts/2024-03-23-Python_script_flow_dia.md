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
  <img width="650" height="275" src="/images_1/LLM_flow.PNG">
</p>

## Files to Prompt

x.com is the best source of resources for like-minded people provided you follow the right people. I discovered the post related to `files-to-prompt` repo. by [simon](https://twitter.com/simonw). It is a lightweight module to concatenate a 
directory full of files into a single prompt. I just had to modify it to save the prompt as a text file. You can find the module at [repo](https://github.com/simonw/files-to-prompt/tree/main). It takes the path/to/directory and saves the prompt file with minimum modification. I do have a version of an output file with `imports` only.

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

**Prompt**
~~~
List of files to analyze is given between <list_files></list_files>. They must be in output.
Create the flow dependency among the modules carefully. Think step by step and then traverse. 
Follow import statements carefully to link modules. 
No need to include third-party modules such as fastapi, pydantic, jinja, jose etc

You can avoid tests, alembic folder. 

<example>
models.py does not import any module from app. (first-party module),so it becomes source node
config.py does not import any module from app. (first-party module),so it becomes source node
security.py imports only from app.core.config (first-party module),so flow becomes congig.py -> security.py
crud.py imports from app.core.security and app.models (both part of first-party modules), so flow becomes congig.py -> security.py -> crud.py and models.py -> crud.py
</example>

Generate DOT code based on the <context>
~~~

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

[Mermaid](https://mermaid.js.org/intro/) lets you create diagrams and visualizations using text and code.

It is a JavaScript-based diagramming and charting tool that renders Markdown-inspired text definitions to create and modify diagrams dynamically.

[Mermaidflow](https://www.mermaidflow.app/editor) is an online editor to play with the code.


<p align="center">
  <img width="750" height="350" src="/images_1/mermaid.PNG">
</p>


## Graphviz

[Graphviz](https://graphviz.org/) is a powerful open-source graph visualization software. It provides a collection of tools for creating and manipulating graphs and diagrams. Graphviz uses the DOT language to describe graphs, which is a simple text-based language for specifying the structure of graphs.

Graphviz can be used to visualize various types of graphs, including:

1. Directed and undirected graphs
2. Trees and hierarchical structures
3. Flowcharts and network diagrams
4. Entity-relationship diagrams

With Graphviz, you can generate high-quality visual representations of complex data structures and relationships, which can be useful for analysis, communication, and documentation purposes.

```python
digraph ModulesFlow {
    // Nodes
    node [shape=box, style=filled, color=lightblue1];
    "backend_pre_start.py";
    "crud.py";
    "initial_data.py";
    "main.py";
    "models.py";
    "tests_pre_start.py";
    "utils.py";
    "deps.py";
    "items.py";
    "login.py";
    "users.py";
    "config.py";
    "db.py";
    "security.py";

    // Dependencies
    "backend_pre_start.py" -> "db.py";
    "db.py" -> "initial_data.py";
    "initial_data.py" -> "db.py";
    "db.py" -> "main.py";
    "main.py" -> "utils.py";
    "main.py" -> "items.py";
    "main.py" -> "login.py";
    "main.py" -> "users.py";
    "items.py" -> "deps.py";
    "items.py" -> "models.py";
    "login.py" -> "deps.py";
    "login.py" -> "utils.py";
    "login.py" -> "models.py";
    "users.py" -> "deps.py";
    "users.py" -> "utils.py";
    "users.py" -> "models.py";
    "utils.py" -> "config.py";
    "test_backend_pre_start.py" -> "backend_pre_start.py";
    "test_test_pre_start.py" -> "tests_pre_start.py";
    "test_items.py" -> "items.py";
    "test_login.py" -> "login.py";
    "test_users.py" -> "users.py";
    "test_user.py" -> "security.py";

    ||
    //
    ||

    // Additional settings
    edge [color=gray40];
    edge [color=gray40];
}
```
<p align="center">
  <img width="750" height="350" src="/images_1/graphviz.PNG">
</p>


## D2

[Declarative Diagramming](https://d2lang.com/) is the fastest and easiest way to get a mental model from your head onto the screen. We can generate the D2 code by providing the same `prompt` and `<context>` by changing just one word. There are multiple free [online editors](https://play.d2lang.com/) to create with D2.

<p align="center">
  <img width="750" height="350" src="/images_1/d2.PNG">
</p>

## LLM Hallucination

* Gemini 1.5 Pro: The current version of `Gemini 1.5 Pro` through `Google AI Studio` hallucinates a lot. It has a default `temperature` of 2 (date: 03/23/2024) and can not be adjusted. It apologizes a lot!
* ChatGPT: It did good work at generating a `DOT` file.

## Pydeps

> pydeps --max-bacon 4 --exclude fastapi starlette pydantic pydantic_core typing_extensions --show-dot --no-show main.py > githb.dot




