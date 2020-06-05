---
title: 'Single or double?: AND operator and OR operator in R'
author: Yen-Chung Chen
date: '2018-09-21'
slug: single-or-double-and-operator-and-or-operator-in-r
categories:
  - R
tags:
  - R
image:
  caption: ''
  focal_point: ''
---
One classmate complained about having trouble subsetting a data frame to
keep non-zero rows, like:

```
# I don't want rows of zero here!
non_zero <- rna_seq[wt != 0 && mutant != 0 && resq !=0, ]
```

This did not work as expected. The culprit here was the logical operator
`&&`. There are two versions of AND and OR in R, `&&`, `&`, `||`, `|`,
and just like my friend, I also find it difficult to tell them apart and
suffer for very long.

In R, the short version, `&` and `|`, are logical Boolean operators
without short-circuiting. That means that they evaluate every elements
they are passed. If you want to do logical comparison, they should work
exactly as you expected, in the same fashion of `+` or `-`.

```
c(TRUE, FALSE, FALSE) & c(TRUE, TRUE, TRUE)
# If you run it in console
# [1]  TRUE FALSE FALSE

FALSE & what_ever_variable

# This expression is always evaluated false
# But & will still evaluate what_ever_variable before returning

# If you run it in console
# Error: object 'what_ever_variable' not found
```

On the other hand, the long version `&&` and `||` will always *return
only* ***one*** *value, either* `TRUE` *or* `FALSE`. Regardless of the
length of the objects you are passing to it, they only evaluate the
first element, and do it with short-circuiting.

```
c(TRUE, FALSE, FALSE) && c(TRUE, TRUE, TRUE)
# If you run it in console
# [1] TRUE

FALSE && what_ever_variable

# With short-circuiting, && returns FALSE right after it
# gets passed FALSE and does not care what what_ever_variable is

# If you run it in console
# [1] FALSE
```

The confusion might come from the inconsistency when choosing these
operators in different languages. For example, in C, `&` performs
bitwise AND, while `&&` does Boolean logical AND.
