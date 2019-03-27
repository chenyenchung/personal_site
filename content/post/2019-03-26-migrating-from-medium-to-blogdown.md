---
title: Migrating from Medium to Blogdown
author: Yen-Chung Chen
date: '2019-03-26'
slug: migrating-from-medium-to-blogdown
categories:
  - R
  - Tricks
tags:
  - R
  - markdown
image:
  caption: ''
  focal_point: ''
---
After struggling for a while, I decided to move from Medium and switch to 
`blogdown`. While Medium is a beautiful platform for blogging, its philosophy 
seems to fit less well when there are more than articles to host.

I came to realize that my expectation for a blog is not only to keep notes, but 
also to demonstrate projects and provide a brief biography. In short, I wanted 
a website instead of a blog, and `blogdown` seems to provide an appropriate 
amount of versatility.

Besides, `R` is one of my favorite work horses, and many of my articles are 
naturally about it. This makes `blogdown` even more attractive for me because 
now my small experiments can be in exactly the same format as my blog entry: 
`R Markdown`.

Medium provides a nice downloading service, which gives you all your posts in 
html. To convert them to markdown, I used this shell script:

```sh
#!/bin/bash
for i in *.html
do
  pandoc -f html -t gfm ${i} |\
  sed -e 's/<.span>//g' |\
  sed -e 's/<span.*>//g' |\
  sed -e 's/^```.*/```/g' > "${i}.md"
done
```

`pandoc` shold take care of most of the conversion here, and what were left 
include:

1. Bullet lists in Medium seems to be formatted in a markdown incompatible way, 
leaving `<span id = ...>` and `</span>` flanking each item.
2. The code fences (```) are followed by curly-bracket-flanked characters.

The shell script removes the `<span></span>` and leaves only the code fences 
but eliminates anything after it.

In my case, the only thing I have to do is to replace header and footer from
Medium manually to make it fit into a `blogdown` site. This is also somewhat 
tedious, but I don't have that many posts now so I did not take the time to 
automate that part too. 
