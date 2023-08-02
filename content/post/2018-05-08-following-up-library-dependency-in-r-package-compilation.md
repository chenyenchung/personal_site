---
title: Following up library dependency in R package compilation
author: Yen-Chung Chen
date: '2018-05-08'
slug: following-up-library-dependency-in-r-package-compilation
categories:
  - R
tags:
  - R
  - Dependency
image:
  caption: ''
  focal_point: ''
---
Hello there.

I had not anticipated to encounter this problem again so soon, but I did
when I was installing yet another package on my own laptop.

```R
ld: warning: directory not found for option '-L/usr/local/gfortran/lib/gcc/x86_64-apple-darwin15/6.1.0'
ld: warning: directory not found for option '-L/usr/local/gfortran/lib'
ld: library not found for -lgfortran
clang: error: linker command failed with exit code 1 (use -v to see invocation)
```

This prompted to think again about the issues [I grunted about the other
day]({{< ref "/post/2018-05-04-run-seurat-an-r-package-in-a-notebook-interface-on-a-server-without-root" >}}).
Back then, I could not install some packages because R can not locate
`libgfortran` during package compilation, and my work-around was install
via Conda, which seems to provide compiled binary version.

## What tells R where to find compilers and libraries?

I (belatedly) find out R have a configuration file in
`/Library/Frameworks/R.framework/Resources/etc/Makeconf`, and sometimes
when Conda/Homebrew or other package managers install new compilers or
libraries, it might not get updated.

This is *exactly* the source of my problem. It is suggested [a user
could create
a](https://stackoverflow.com/questions/40092423/r-package-with-fortran-source-code-how-to-make-makevars-file-under-pkgname-s)
`Makevars` [file in the same
directory](https://stackoverflow.com/questions/40092423/r-package-with-fortran-source-code-how-to-make-makevars-file-under-pkgname-s),
which would then be read with a higher priority, but it somehow does not
work on my laptop.

As a result, I commented out the original setting in `Makeconf` and installed 
`gcc` from `homebrew`. Now, I have `gfortran` incorporated into the homebrew 
version of `gcc`, which could also replace `clang` from Xcode to support 
`OpenMP`.

The changes in my `Makeconf` file as a result is:

```sh
# Use Homebrew gcc for OpenMP support
CC = gcc-8
# CC = clang # Original setting
...
# Use Homebrew gcc for OpenMP support
CXX = g++-8
# CXX = clang++ # Original setting
...
# Ask R to find the Homebrew copy of gcc
FLIBS = -L/usr/local/lib/gcc/8/gcc/x86_64-apple-darwin17.5.0/8.1.0 -L/usr/local/lib/gcc/8 -lgfortran -lquadmath -lm
# The original one
# FLIBS =  -L/usr/local/gfortran/lib/gcc/x86_64-apple-darwin15/6.1.0 -L/usr/local/gfortran/lib -lgfortran -lquadmath -lm
```

This fixed my problem of R package compilation.

```R
# SessionInfo at the time of writing

> sessionInfo()
R version 3.4.4 (2018-03-15)
Platform: x86_64-apple-darwin15.6.0 (64-bit)
Running under: macOS High Sierra 10.13.4

Matrix products: default
BLAS: /System/Library/Frameworks/Accelerate.framework/Versions/A/Frameworks/vecLib.framework/Versions/A/libBLAS.dylib
LAPACK: /Library/Frameworks/R.framework/Versions/3.4/Resources/lib/libRlapack.dylib

locale:
[1] en_US.UTF-8/en_US.UTF-8/en_US.UTF-8/C/en_US.UTF-8/en_US.UTF-8

attached base packages:
[1] stats     graphics  grDevices utils     datasets  methods   base

loaded via a namespace (and not attached):
[1] compiler_3.4.4 tools_3.4.4    yaml_2.1.19
```
