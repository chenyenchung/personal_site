---
title: Appending a string before the URL of a current tab
author: Yen-Chung Chen
date: '2018-08-30'
slug: appending-a-string-before-the-url-of-a-current-tab
categories:
  - Tricks
tags: []
image:
  caption: ''
  focal_point: ''
---
In my field, many of the literatures are behind the paywall. Though my
institute get subscription for most of them, I am sometimes not in the
lab when I need to check something.

In such cases, usually VPN services could save my day, but I usually get
impatient when VPN is connecting.

Luckily, my school also provide an alternative to use library proxy to
access those papers. It works by prepending the link of the paper with
`http://proxy.library.some-university.edu/login?url=`. This works quite
well for me except for the fact that I need to either type or copy-paste
this prefix every time.

I am lazy, so I googled and learned using Javascript in a bookmark could
prepend the URL of current tab (actually, windown) with any string, and
here’s the magic I need:

```
javascript:window.location.href='[The thing you want to append]'+window.location.href
```
