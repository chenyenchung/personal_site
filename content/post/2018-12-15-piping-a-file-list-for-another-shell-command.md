---
title: Piping a file list for another shell command
author: Yen-Chung Chen
date: '2018-12-15'
slug: piping-a-file-list-for-another-shell-command
categories:
  - Command line tricks
tags:
  - Linux
image:
  caption: ''
  focal_point: ''
---
Being a student again takes a longer while than I expected to get used
to, which gives me a long hiatus in my posting, but also puts me in a
different and stimulating environment.

This post was inspired by a question from my colleague, who want to
first find some file entries and then merge them into a file, so the
initial attempt was:

```
# There are 6 files in my example directory
> ls
1.txt  2.txt  3.txt  a.txt  b.txt  c.txt

# Let's say we are looking for only those with lower case alphabetical names
> find . -regex "./[a-z].txt"
./c.txt
./b.txt
./a.txt
```

After getting the list of file names , it might be tempting to pipe this
result to `cat` and then to a text file like:

```
find . -regex “./[a-z].txt" | cat > "merged.txt"
```

But this is only giving you the list of file names in `merged.txt`
because it is actually `./c.txt\n./b.txt\n./a.txt` (`\n` is the new-line
character) being piped to `cat`. Though `cat` does try to find a file
matching this name, there is obviously none in this directory, and `cat`
has no other choice but printing the string it receives as it is.

I am bad at terminal commands, so the first thing I came up with was to
use `awk` to send the file names one by one to `cat` with `system()`,
which makes a system call in `awk` scripts.

```
# Awk will pass each file name to the system call (cat $0)
# and *append* it to a file because now the results are processed separately and will overwrite each other if we use > instead of >>

find . -regex “./[a-z].txt" | awk '{system("cat " $0 " >> 'merged.txt'")}'
```

This worked, but the use of `awk` seemed like an overkill.

I later noticed `xargs`, which takes standard input, splits it by blanks
or new lines and sends the resulting list to a command. This looked like
exactly the thing I wanted.

Indeed, `find . -regex “./[a-z].txt" | xargs cat >> "merged.txt"` does
exactly the same thing in a more elegant way. Additionally, `xargs` is
of course more versatile than that.

  - If you get a file containing the list, it can read
    from file directly (`xargs -s`).
    from file directly (`xargs -s`).
  - If you are unsure what `xargs` is going to do, `-p`
    turns it interactive, and it prints the command that is elicited by
    `xargs` and asks whether you want to run it.
    `xargs` and asks whether you want to run it.
  - If you just want to know what command `xargs`
    elicits, `-t` prints the command (to `stderr`) before it is actually
    running without asking.
    running without asking.
