---
title: Remote connection to Jupyter Notebook
author: Yen-Chung Chen
date: '2018-05-13'
slug: remote-connection-to-jupyter-notebook
categories:
  - HPC
tags:
  - Linux
  - R
image:
  caption: ''
  focal_point: ''
---
Recently, I analyzed a few single cell RNA-seq datasets and experimented
with several new tools from recent publication. While it was fun, most
datasets were just too large for my poor laptop to process, and I relied
a lot on our server.

I have to admit I am not too good an analyst and am spoiled by the
freedom interpreted languages provided — to try and error line by line.
However, this freedom would be gone if I have to do run my analysis like
`Rscript my-analysis.R` or `python my-analysis.py`. Besides, an
interactive interface to play and receive feedback immediately would
also make learning new tools easier.

So, [I decided to use Jupyter Notebook because I am not allowed to run
RStudio Server
here](https://medium.com/biosyntax/run-seurat-an-r-package-in-a-notebook-interface-on-a-server-without-root-65d6365311c3).
Here’s a brief note of how I did it.

First, I connect to the server via SSH, and then run `jupyter notebook --no-browser --port 8889` (as [this nice tutorial
suggested](https://coderwall.com/p/ohk6cg/remote-access-to-ipython-notebooks-via-ssh)).
This would start a Jupyter server, which could be then channelled back
to my own machine via SSH. In another terminal session, this time on my
own machine, `ssh -N -L localhost:8888:localhost:8889 username@server.address` would channel whatever from port 8889 of the remote server to localhost:8888.

Open the browser, connect to `localhost:8888`, and I am ready to go.

Usually I would play with a smaller dataset to form my analysis. Then, I
load the real dataset to the notebook and run the whole thing. For this
one, I don’t really want to see it run but only am interested in the
result, so I would do it with`jupyter nbconvert --ExecutePreprocessor.timeout=-1 --to notebook --execute myanalysis.ipynb`. It runs Jupyter notebook in command line, and the
`--ExecutePreprocessor.timeout` decides after how long `jupyter
nbconvert` should give up on running a cell. In my case, a cell could
run for hours, so I set it to -1, allowing a cell to run forever. This
is important because the default is something like 30 minutes.

Similar idea works for Rmarkdown. I draft my analysis with a smaller
dataset in my local RStudio, upload the .Rmd file, start R session on
the server, and `rmarkdown::render("myanalysis.Rmd")` would do the
trick.

Just remember to use `screen` or `tmux` to before running your analysis
so it would keep going when you close your SSH connection, and when you
are done, both Jupyter notebook and SSH channelling could be turned off
with `^C`.
