---
title: 'Dependency issue: In Conda, with SCENIC'
author: Yen-Chung Chen
date: '2019-08-04'
slug: dependency-issue-in-conda
categories: 
  - HPC
tags:
  - Dependency
  - Python
  - Conda
image:
  caption: ''
  focal_point: ''
---

I've been working with [pySCENIC](https://github.com/aertslab/pySCENIC) in the 
recent couples of months. It's a tool that is meant to uncover gene sets that are 
controlled by transcription factors and suggests the underlying logic of how 
genes are regulated. It takes gene expression data from single-cell RNA 
sequencing and seems to be fairly easy to use.

So, what took me several months? I did my preliminary run with [their R 
implementaion](https://github.com/aertslab/SCENIC), which was released earlier 
in [the original reference](https://www.nature.com/articles/nmeth.4463). It was 
well-documented and ran smoothly over a set of 10,000 cells. Nonetheless, it 
did not scale well. With 100,000 cells, it could take a month to run. The 
authors are very aware of this and kindly re-implemented it in Python, which 
is approximately more efficient by two orders of magnitude in my case.

Everything should be smooth in theory, but in practice, I encountered [a 
dependency issue]({{< ref "/post/2019-04-05-psutil-python-and-icc" >}}) at the first step when I 
`pip install`ed the package.

After finding a way out of the compilation issue, I experienced repeated 
segmentation faults running the analysis. Since it ran successfully once, I 
thought that it was something wrong with my main analysis, but it turned out 
to be that later versions of `dask` is not compatible with the package itself.

It was then I painfully learned that I should really manage my analysis with 
virtual environments. I found the authors provided a YAML environment file in 
the repository, so I tried to use it. `conda` complained. It said that 
`mkl-random` was not compatible with `openblas`, so it could do nothing here.

I played with the versions of packages a little bit and was able to run my 
analysis with a bunch of warning messages, and after two weeks, after I tried 
to enable jupyter notebook in the environment, the dependency was broken again. 

I started over, but I forgot what I did to the versions so I failed to restore 
a setting that enables my analysis. Then I came across 
[a thread at StackOverflow](https://stackoverflow.com/questions/53138055/updating-a-conda-environment-only-through-conda-forge-channel) saying `numpy` from the default channel 
was somehow creating a mess with `openblas` and `mkl`. Per the suggestion in 
the above therad, I added a line in the YAML, prioritizing `conda-forge` over 
`defaults`, and magically the original environment file from the authors runs 
without any additional adjustments.

The morale of the story:

1. Dependencies should always be managed and documented when possible. It's 
much harder, if possible at all, to trace it down from error messages. I was able to 
find `dask` causing segmentation faults, but it was sheer luck that I tried to start 
everything over with a clean environment and finally opted in to use `conda`.

2. Even with dependencies provided (like a `conda` environment file), there 
could be local settings that was not in it. In my case, the authors could have 
set `conda-forge` as the preferred channel in `$HOME/.condarc` and forgot about 
it.

3. Maybe I should create a dependency tag because that seems like the main 
theme of this blog, right?
