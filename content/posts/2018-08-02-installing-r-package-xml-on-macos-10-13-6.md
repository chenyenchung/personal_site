---
title: Installing R package XML on MacOS 10.13.6
author: Yen-Chung Chen
date: '2018-08-02'
slug: installing-r-package-xml-on-macos-10-13-6
categories:
  - R
tags:
  - R
image:
  caption: ''
  focal_point: ''
---
I updated my R packages the other day, and not surprisingly, one package
failed to compile. This time, it was
[XML](https://cran.r-project.org/web/packages/XML/index.html). The error
message suggested `configure: error: “libxml not found”`, but homebrew
suggested I had installed `libxml2` and had it up-to-date.

By running `./configure` manually and after some googling, I realized
the compiler went to `/usr/bin/xml2-config` instead of the homebrew
version, and thanks to [this thread on
StackOverflow](https://stackoverflow.com/questions/40682615/cannot-install-xml-package-in-r),
I learned that the compiler would be directed to the correct copy of
`libxml2` if I set the environmental variable `XML_CONFIG`.

So, running `Sys.setenv(XML_CONFIG =
"/usr/local/Cellar/libxml2/2.9.7/bin/xml2-config")` in R console helped
me successfully compile `XML`.

The cause of this problem might be that I did not install Xcode in my
computer, which seems to come with a proper version of `libxml2` to
replace the one coming with the system, and according to the
installation message of `libxml2`, `libxml2` *from homebrew is keg-only,
which means it was not symlinked into*`  /usr/local `*, because macOS
already provides this software and installing another version in
parallel can cause all kinds of trouble.* Consequently , the compiler
turned to the system copy of `libxml2`, causing failed compilation.

Of course, this problem could also be fixed by choosing to install from
binary.

```
R version 3.4.4 (2018-03-15)
Platform: x86_64-apple-darwin15.6.0 (64-bit)
Running under: macOS High Sierra 10.13.6

Matrix products: default
BLAS: /System/Library/Frameworks/Accelerate.framework/Versions/A/Frameworks/vecLib.framework/Versions/A/libBLAS.dylib
LAPACK: /Library/Frameworks/R.framework/Versions/3.4/Resources/lib/libRlapack.dylib

locale:
[1] en_US.UTF-8/en_US.UTF-8/en_US.UTF-8/C/en_US.UTF-8/en_US.UTF-8

attached base packages:
[1] stats     graphics  grDevices utils     datasets  methods   base

loaded via a namespace (and not attached):
[1] compiler_3.4.4 tools_3.4.4    yaml_2.2.0
```
