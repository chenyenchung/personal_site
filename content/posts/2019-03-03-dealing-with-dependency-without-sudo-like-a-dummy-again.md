---
title: Dealing with dependency without sudo like a dummy (again)
author: Yen-Chung Chen
date: '2019-03-03'
slug: dealing-with-dependency-without-sudo-like-a-dummy-again
categories:
  - R
tags:
  - R
  - Dependency
image:
  caption: ''
  focal_point: ''
---
The more I work with Linux, the more I encounter dependency issues. This
is of course not too big a surprise, but it can be painful especially
when you aren’t sudo, so the most obvious solution does not work for
you.

Don’t misunderstand me. `sudo` is definitely not something to play with
when we don’t know what we are doing, and access control does a terrific
job preventing me from shooting my own foot (or worse, other’s foot)
from time to time. It is just that it also prevents me from shooting
something that ought to be shot.

In terms of dependency, my usual workaround is to install things locally
in `$HOME/.local`. I think this is also the default place R and Python
turn to when installing packages locally. This should work just fine if
I remember to add `$HOME/.local/bin` to my `$PATH`. Unfortunately, if
you not only *use* something but also have to *compile* it from time to
time, there’s more things to worry about.

Generally, my compilation fails when there are some shared library is
missing, and as someone who is totally green in this, some files that
are often missing are shared object (.so) files and header files (.h).
They would usually be mentioned in the error messages when your
compilation fails. In some cases, package configuration files (.pc)
would also be gone.

The following suggestions might work if you have actually installed the
required library but `make` failed to find it:

  - If a .so file is missing, try:  
    `./configure LDFLAGS="-L [where your library is]"` (Example path:
    `$HOME/.local/lib`)
  - If a .h file is missing, try:  
    `CPPFLAGS=”-I [where your library is]”` (Example path:
    `$HOME/.local/include`)
