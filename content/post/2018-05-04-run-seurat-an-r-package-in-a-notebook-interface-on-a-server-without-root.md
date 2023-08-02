---
title: Run Seurat (an R Package) in a notebook interface on a server without root
author: Yen-Chung Chen
date: '2018-05-04'
slug: run-seurat-an-r-package-in-a-notebook-interface-on-a-server-without-root
categories:
  - R
tags:
  - R
  - Linux
  - Dependency
image:
  caption: ''
  focal_point: ''
---

After a while of playing around, I’ll say the best way to use R with a
Notebook-style interface on a server where you are no superuser would be
using Anaconda, and then run R inside Anaconda to get whatever package
you need. It is designed to run for a normal user, so there’s no need
for superuser permission, and dependency issue is also taken care of
most of the time.

If you get the permission on server and are comfortable with R Studio, R
Studio Server might be a even better option. That is because even if the
packages are in [Conda R](https://anaconda.org/r), [Conda
Forge](https://conda-forge.org), or
[Bioconda](https://bioconda.github.io/), sometimes they are out of date,
which might break dependencies, and `conda skeleton` and `conda build`
unfortunately come with a lot of dependency issue as well. Besides, the
visualization of environment and integration of documentation is better
in R Studio for me.

What worked for me starts from creating a new environment in Anaconda
and install the `r-essentials`, which should provide a platform ready
for`  jupyter notebook `.

```sh
conda create --name R
conda install -c r r-essentials
```

One thing to be noted is that sometimes the packages on Conda are not
up-to-date, and that would create some version issue for the R packages,
so you might check on different channels to see if there’s something you
need with version number in mind. It might be simpler to just use
`install.packages()`in the R environment directly though.

R seemed not to know where to find the libraries installed by Conda, and
it turned out I also needed to `export LD_LIBRARY_PATH=[Conda lib path
for the virtual environment]` to let the compiler function properly.
Even with the path set, ` igraph  `failed its compilation in R console,
and `conda install -c r r-igraph` fixed that.

After that, I am finally good to go with Jupyter Notebook running R.

The takehome message for me is that it could be complicated to install
required libraries to user directory, and the dependencies for these are
often too long to be manually managed. I found out I needed `cmake` to
install something, but when I tried to install `cmake` from source, it
warned me that a compiler supporting C++11 was not found, and then I
tried to get new version of `gcc` but the configure file of `cmake`
still could not find that copy of `gcc`…

I spent almost 3 days in this maze of dependencies, and though I felt I
learned a lot, I was not able to fix things this way. Anyway, I guess
that why we need package management. You could find other unsuccessful
attempts below if you are interersted.

## Attempt 1: Setting up Rkernal with IPython Notebook in Anaconda

Anaconda keeps an independent copy of R when it is installed with `conda
install -c r r-essentials`. I wanted to install the latest version
instead of [the conda version of
Seurat](https://anaconda.org/bioconda/r-seurat), so I googled for *how
to install packages from CRAN in Conda* and find [this
article](https://stackoverflow.com/questions/34705917/conda-how-to-install-r-packages-that-are-not-available-in-r-essentials).
According to the thread, I tried to do something like
`install.packages(“Seurat”, lib = [conda R path])` from my user copy
of R.

There is actually a great reason against this
approach — `install.packages()`decides whether to install
dependencies based on *the installed ones*, so if you run
`install.packages()` from another copy of R, the dependency would be a
mess.

I tried to use the Conda copy of R, and do` 
install.packages(“Seurat”) `, and found out…

```R
ERROR: dependencies ‘igraph’, ‘diffusionMap’ are not available for package ‘Seurat’
* removing ‘[My Conda path]/R/library/Seurat’
```

It turned out `igraph` was not compiled successfully and seems to be a
result of system library dependency issue according to [this
thread](https://stackoverflow.com/questions/45318188/getting-error-in-function-igraph-write-graph-graphml-while-installing-igrap),
and I would need `libssl-dev`, `libcurl4-openssl-dev`, and
`libssh2–1-dev`, and I gave up here because I saw a labyrinth of
dependencies here.

## Attempt 2: Install Rstudio Server without root

If I could do it, I would be able to use the user copy of R, which I am
okay with, and I like R Studio quite a lot. Long story short.
Installation is possible, but execution is not. Basically you could
follow the official instruction, and finish with `make install
prefix=[somewhere you can write]`. Nonetheless, *starting a server
unsurprisingly requires you to be root.*

One additional hilarious thing here is that we did not have `cmake` on
that server, and when I tried to install a copy, it failed because no
C++ compiler supporting C++11 is available (though `which g++`showed
a nice one.) Until I am done through all these, I noticed that there was
already a copy of rstudio-server on the machine I used.

## Attempt 3: Make Jupyter Notebook use my user copy of R

I entered R console, and tried
`devtools::install_github(“IRkernel/IRkernel”)`. Guess what, it failed
with an error message of: `Installation failed: An unknown option was
passed in to libcurl`.

Alas. A bit troubleshooting indicated that I might have some version
issue for libcurl, but I don’t know which.

Alternatively, I tried to use `install.packages(“JuniperKernel”)`, which
should serve the same function as `IRkernel`, but it also has its
dependency issue: it requires `gdtools`, which won’t compile without
`cairo`. `cairo`requires `libpng` and `pixman`. I tried to install from
source of [libpng](http://www.libpng.org/pub/png/libpng.html) and
[pixman](https://www.cairographics.org/releases/) with `./configure &&
make && make install prefix=$HOME/.local/bin`, but`pixman` kept
complaining about unable to find `png.h`. I was not capable of fixing
this and turned to other options, but I am still curious how could I fix
this.

## Attempt 4: Fine, I’ll just go with the Conda package

Now it seems that my hope to use `Seurat` on CRAN is not that wise, and
my dataset is in fact compatible with `Seurat v2.2.0` on bioconda.
Perhaps this would be a much more efficient work-around.

Since it is in the bioconda repository, I need to set the channel first.

```sh
conda config — add channels defaults
conda config — add channels conda-forge
conda config — add channels bioconda
```

and then `conda install -c bioconda r-seurat`.

What I got was:

```sh
UnsatisfiableError: The following specifications were found to be in conflict:
- r-reprex
- r-seurat
```

Checking dependency with `conda info r-seurat` showed that it requires
ver 3.4.1 of `r-base`, while `r-reprex` need \>3.4.3. This prevented me
from down-versioning `r-base`.

Instead, I built `Seurat` from CRAN with `conda skeleton cran Seurat`.
Interestingly, it saved the recipe in `[pwd]/r-seurat` instead of
`[pwd]/Seurat`. With `conda build r-seurat`, guess what I got?

```r
Error : object ‘map_dfr’ is not exported by ‘namespace:purrr’
ERROR: lazy loading failed for package ‘Seurat’
subprocess.CalledProcessError: Command ‘[‘/bin/bash’, ‘-e’, ‘[pwd]/anaconda/conda-bld/r-seurat_1525165846607/work/conda_build.sh’]’ returned non-zero exit status 1.
```

It turned out `Seurat` required `purrr::map_dfr()`, which was introduced
in newer version than what is on bioconda. A new version of `purrr` from
Conda-forge fixed this, but then there was compilaton error mentioned
earlier in this blog.
