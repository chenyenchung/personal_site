---
title: Strangled by factors
author: Yen-Chung Chen
date: '2019-03-28'
slug: strangled-by-factors
categories:
  - R
tags:
  - R
image:
  caption: 'Photo by [Matthew Henry](https://unsplash.com/@matthewhenry) on [Unsplash](https://unsplash.com/)'
  focal_point: ''
---

I am exaggerating, but sometimes `stringsAsFactors` is almost this
deadly. I work with genomic data, and a common quest in my job is to
identify interesting features (in most cases, genes) from a pool of
25,000+.

To climb onto giants’ shoulders, genes that were repoted to be important
in a certain process, say cell fate determination, are invaluable, and
these genes often come in the supplementary tables of the original
papers.

Reading the supplments into R and using those for analysis look dead
simple, but this is when a wrong setting of `stringsAsFactors` can bite
one hard.

I’ll demonstrate this with everyone’s favorite example set: `mtcars`.

Imagine it was reported that Honda Civic and Volvo 142E are particularly
safe in a crash scene, and we want to fetch their information from
`mtcars` for some detailed analysis. We notice he paper that reported
*Honda Civic* and *Volvo 142E* provide a csv file containing the models
that found like this:

<table>
<caption>Models that are robust in crash</caption>
<thead>
<tr class="header">
<th style="text-align: left;">Model</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;">Honda Civic</td>
</tr>
<tr class="even">
<td style="text-align: left;">Volvo 142E</td>
</tr>
</tbody>
</table>

Now, I could not wait to find what are the specs of these models! Let’s
load the table and do some analysis!

    candidate_models <- read.csv(file = "example.csv", 
                                 header = TRUE)
    print(candidate_models)

    ##         Model
    ## 1 Honda Civic
    ## 2  Volvo 142E

It looks great, so we can finally get the data we want.

    print(mtcars[candidate_models$Model, ])

    ##              mpg cyl  disp  hp drat    wt  qsec vs am gear carb
    ## Honda Civic 30.4   4  75.7  52 4.93 1.615 18.52  1  1    4    2
    ## Volvo 142E  21.4   4 121.0 109 4.11 2.780 18.60  1  1    4    2

Oh no. I get two completely different rows though I even `print` the
candidates after reading the csv file.

This weird phenomenon results from the way factor works: A `factor` is
categorical and coded by integers under the table, but displayed as
character strings (`levels`). So, when I thought I was filtering rows
with Honda Civic and Volvo 142E, I was actually doing
`mtcars[c(1,2), ]`.

    head(mtcars)

    ##                    mpg cyl disp  hp drat    wt  qsec vs am gear carb
    ## Mazda RX4         21.0   6  160 110 3.90 2.620 16.46  0  1    4    4
    ## Mazda RX4 Wag     21.0   6  160 110 3.90 2.875 17.02  0  1    4    4
    ## Datsun 710        22.8   4  108  93 3.85 2.320 18.61  1  1    4    1
    ## Hornet 4 Drive    21.4   6  258 110 3.08 3.215 19.44  1  0    3    1
    ## Hornet Sportabout 18.7   8  360 175 3.15 3.440 17.02  0  0    3    2
    ## Valiant           18.1   6  225 105 2.76 3.460 20.22  1  0    3    1

In this example, it might be so obvious that you start wondering why
people even see this as a problem, but when you are facing several
dozens of candidates among thousands of features, this kind of errors
can go unnoticed for really long.

To prevent this from happening, it is good to make it a habit to set
`stringsAsFactors = FALSE`. To inspect the data you load, `str()` often
provides more information than `print()` or `head()` (On the other hand,
if you work with a `tibble`, `print()` shows variable types by default.)

    str(candidate_models)

    ## 'data.frame':    2 obs. of  1 variable:
    ##  $ Model: chr  "Honda Civic" "Volvo 142E"
