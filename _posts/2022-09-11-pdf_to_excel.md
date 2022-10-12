---
layout: single
sidebar: true
author_profile: true
title: PDF to Excel using an amazing pdfplumber.
excerpt: "Plumb a PDF for detailed information about each text character, rectangle, and line."
description: "Plumb a PDF for detailed information about each text character, rectangle, and line. Works best on machine-generated, rather than scanned, PDFs."
comments: true
tags: ["Python","Github","pdf","MLOps","Machine Learning","ML System Design"]
published: true
comments: true
header:
  teaserlogo:
  teaser: /images/pdftoexcel.png
  image: /images/pdftoexcel.png
  caption: "courtesy: https://pdftables.com/"
gallery:

  - image_path: ''
    url: ''
    title: ''
---
Hi All,

We must have come across a situation at least once where we have to copy and paste rows of data out of PDF files. The manual approach of copy-paste works reasonably well for tabular data and a couple of pages. Tabula is a tool that allows extracting data into a CSV or Excel using simple interface. 

I came across a scenario where I had to fetch tabular data from a pdf document of ~3000 pages. [Tabula](https://tabula.technology/) was my first choice to extract data, but it was difficult to get standard format. The main issue was with the table header. I came across a better option while researching named pdfplumber.

```ruby
# checking java version
!java -version

!pip install -q pdfplumber

# Importing .pdf file
import pdfplumber
import pandas as pd

pdf = pdfplumber.open("/content/All Admitted Candidates List MBBS_BDS & BSC NURSIN.pdf")
p0 = pdf.pages[0]

# Checking last page
p0 = pdf.pages[3056]

# Checking imported rows
table = p0.extract_table()
table[:3]

# Checking rows and header
df = pd.DataFrame(table[2:], columns=table[1])

# Write a loop to combine the dataframes

list_of_df = []

for i in range(3057):
  temp = pdf.pages[i]
  table = temp.extract_table()
  df = pd.DataFrame(table[2:], columns=table[1])
  list_of_df.append(df)
len(list_of_df)

complete_df = pd.concat(list_of_df)
complete_df.reset_index(drop=True, inplace= True)

# Saving the results in excel
complete_df.to_excel('MBBS_list.xlsx')

```

Thank you!
