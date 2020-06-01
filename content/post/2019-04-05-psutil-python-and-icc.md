---
title: psutil, python, and icc
author: Yen-Chung Chen
date: '2019-04-05'
slug: psutil-python-and-icc
categories:
  - HPC
tags:
  - Python
  - compile
image:
  caption: ''
  focal_point: ''
---
I used to dislike dependency management because there are so many things that 
require root or are mysteriously incompatible with each other. However, I 
recently came to realize that the existence of dependency itself is a delicate 
and elegant system despite being messy at times.

The recent occasion that reminded me the beauty of dependency was to install 
`psutil` on an HPC. It ran `CentOS 7`, and I had `Python 3.7.3` with 
`pip 19.0.3` on it. It should have been a straightforward task: Typing 
`pip install psutil --user`, and everthing taken care of.

Except that that was not the case. `pip` complained:

```terminal
icc -fno-strict-aliasing -Wsign-compare -Wunreachable-code -DNDEBUG -g -O3 -Wall -Wstrict-prototypes -fPIC -DPSUTIL_POSIX=1 -DPSUTIL_VERSION=561 -DPSUTIL_LINUX=1 -I/share/apps/python3/3.6.3/intel/include/python3.6m -c psutil/_psutil_common.c -o build/temp.linux-x86_64-3.6/psutil/_psutil_common.o

unable to execute 'icc': No such file or directory
```

"Obviously `pip` is using the wrong compiler, but no big deal." I thought. 
After all, I did have a C compiler on HPC, `GCC 4.8.5`, so I re-run 
`pip install` with the environment variable `CC` set: 
`env CC=/usr/bin/gcc pip install psutil --user`.

It turned out I was wrong. The same error message persisted, so I dove into 
StackOverflow for an explanation of this, and found 
[one thread](https://stackoverflow.com/questions/16737260/how-to-tell-distutils-to-use-gcc), 
in which Philip Kearns kindly pointed out that `psutil` is not always 
respecting `CC`.

With this information, I was finally able to fix things (in an ugly way 
though). I have `$HOME/.local/bin` in my `$PATH` and it is prior to `/usr/bin`, 
so I was able to make a symbolic link (
`ln -s /usr/bin/gcc $HOME/.local/bin/icc` in `$HOME/.local/bin` to fool 
`psutil` by providing `gcc` when it asked for `icc`.

This did solve the issue. 

I still don't know why `psutil` ignores `CC`, or why it tries to find `icc` 
instead of `cc` or something else, but I did learn that dependency and 
environment variables for compiling should not be taken for granted. Even one 
line of code ignoring the convention and hard-coded something that was not 
mentioned as a dependency could be hard to troubleshoot. I was lucky that 
`psutil` just needed some common C compiling functionality instead of something 
specific for `icc`, or it could be a thousand times harder to find out what 
went wrong.
