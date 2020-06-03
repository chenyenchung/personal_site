---
title: 'Compiling with libxml in MacOS Catalina'
author: Yen-Chung Chen
date: '2020-06-03'
slug: libxml-in-MacOS
categories: 
  - R
  - Software
tags:
  - compile
  - dependency
  - macOS
  - R
image:
  caption: 'Photo by [Ben Stern](https://unsplash.com/@benst287) on [Unsplash](https://unsplash.com)'
  focal_point: ''
---

## The problem

When compiling Emacs 28.05, `make bootstrap` failed with `fatal error: 'libxml/tree.h' file not found` while `autogen.sh` and `configure` were successfully executed.

## Troubleshooting

The error message pointed out the culprit, `libxml`. It is not a part of the MacOS nor the Xcode command line tools now, but I have installed it with `homebrew` a while ago (because the `xml` package in R also depends on it, and [I struggled quite a while with it](/2018/08/02/installing-r-package-xml-on-macos-10-13-6/).)

To tell the compiler where to find `libxml`, I first tried to set `LDFLAGS="-L /usr/local/opt/libxml2/lib"` and `CPPFLAGS="-I /usr/local/opt/libxml2/include"`. I made two mistakes here: First, I edit `src/Makefile` instead of the one in the `emacs` directory. However, it does not matter after all because `make bootstrap` attempts to compile in a clean state and the old Makefile that I edited is removed before compiling.

Google lead me to [this very help post](https://github.com/remacs/remacs/issues/886#issuecomment-426598679) in which db48x pointed out that if `./configure` knows where the package configuration is, it will set the flags accordingly. We can set `export PKG_CONFIG_PATH="/usr/local/opt/libxml2/lib/pkgconfig:$PKG_CONFIG_PATH` to tell `./configure` where `libxml2` is.

Curiously, when I set `PKG_CONFIG_PATH` in R (`Sys.setenv("PKG_CONFIG_PATH"="/usr/local/opt/libxml2/lib/pkgconfig:$PKG_CONFIG_PATH")`), installing `XML` from source still fails with the following error message:

> You are trying to use a version 2.* edition of libxml but an incompatible library. The header files and library seem to be mismatched. If you have specified LIBXML_INCDIR, make certain to also specify an appropriate LIBXML_LIBDIR if the libxml2 library is not in the default directories.

On the other hand, the solution in the previous post still works: `Sys.setenv(XML_CONFIG = "/usr/local/opt/libxml2/bin/xml2-config")`. I tried both the Xcode copy (in `/usr/local/opt`) and the `homebrew` copy (in `/usr/local/Cellar`), and both worked. Note that if you update the `homebrew` copy regularly, you'll need to change the path because the path contains the version number (for example, `/usr/local/Cellar/libxml2/2.9.10_1/`).
