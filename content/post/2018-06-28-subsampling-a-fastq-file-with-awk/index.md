---
title: Subsampling a fastq file with awk
author: Yen-Chung Chen
date: '2018-06-28'
slug: subsampling-a-fastq-file-with-awk
categories:
  - NGS
tags:
  - NGS
  - Linux
  - awk
image:
  caption: ''
  focal_point: ''
---
## What you are going to find here

1.  A minimal introduction of the `awk` command in Linux
    and Mac (For Mac user, installing GNU awk might be necessary. It
    introduced some new functions like sorting an array with
    `asort()`.)
2.  An `awk` command that would randomly subsample **k**
    reads from a given fastq file of a pair-ended sequencing.

## Why I am making this note

In single cell RNA-sequencing, there seems to be no good way telling how
deep you should sequence to date. Required sequencing depth should
adequately capture library complexity, which is largely determined by
the technique used to collect and barcode the single cell sample, and
practically, we only need as much information as we need to uncover the
underlying heterogeneity in the sample. [Some people went very far to a
minimum of 5,000,000 reads per
cell](https://www.nature.com/neuro/journal/v19/n2/pdf/nn.4216.pdf),
while [some people suggested a much humbler number of 300,000 reads
minimum per cell should
suffice](https://doi.org/10.1016/j.cell.2017.10.019). With this huge
variation, it might be best to decide empirically which fits your need.

Before I could actually try that, I realized I haven’t really seen R as
a programming language. That is, I feel comfortable with doing analysis
in R but think little about how it is computing my stuffs. This time, I
finally realized I don’t know how to ask R to process a file
sequentially when I tried to subsample a fastq file that was larger than
my RAM.

I googled, and `awk` jumped as a somewhat popular answer. I quickly
decided to do this subsampling with it for two reasons:

1.  `awk` commands look quite short.
2.  People I know are good in analysis use `awk` well,
    and I want to be like them. (Yeah, I know it’s just an illusion that
    I would become like them just by merely learning `awk`, but learning
    new things is alway fulfilling.)

It turned out `awk` is quite neat, so I decided to take a quite note
here. Many of this note is adapted from [the official guide
of](https://www.gnu.org/software/gawk/manual/gawk.html#Getting-Started)
`gawk`, the GNU implementation of `awk`.

First, I’ll pipe the results of `ls -l` for `awk` to process. The goal
here is to **print a user-defined variable *k*, and then print every
entry of the result of** `ls -l` **as long as its owner is root.**

![A minimal awk command for me to get acquainted
with](img/2018_06_28_awk_ex1.png)

```
# Command for easy copy and paste
ls -l | awk -v k=3 'BEGIN{print k} $3 == "root" {print $0} END{}'
```

Just like any other command in \*nix system, `awk` takes options right
after it. `-v` declares a variable here, and I need this because I’ll
use this option to set the goal number of reads yielded from
subsampling.

Then, the program part of `awk` is enclosed by a pair of single quote,
and inside the quote, every part is comprised of a pattern and an
action, which would be executed if the pattern is matched.

`BEGIN` is a special rule in `awk` pattern, the code enclosed by
brackets after it would only be run once *before the file* ***begin***
*being processed*. As a result, the example command would first print
*k*, which is 3, before everything.

![Fields in awk are referred to
as $N](img/2018_06_28_awk_ex2.png)

When `awk` reads a file, it automatically separates every row of the
file into fields. A field is pretty similar to the idea of a column of a
data frame in R. The thing separating the fields could be set with
option -F (`awk -F "," ...` sets the field separator as a comma) or
simply assign it to built-in variable `FS` (`awk 'BEGIN{FS=","}...'`
also sets the field separator as a comma).

Now, the short command becomes more readable: we set a variable k as 3,
and then before processing the data from `ls -l`, print k first. Then,
if field 3 ($3) is “root”, print that row for us.

**Subsampling a fastq file**

When I was googling, I found [a kind
tutorial](https://www.notion.so/yenchungchen/Downsampling-fastq-for-verification-of-impact-of-sample-size-aafe40dd66704b1e957faee7ccc00a1e#fe176c935900425195fc68f3e55a907a)
on how to do this. Thanks to it, I got a thing to start from and watch
in awe how smart [reservoir
sampling](http://Reservoir%20sampling%20-%20Wikipedia) is.

The original command from the tutorial is:

```
paste forward.fastq reverse.fastq | awk '{ printf("%s",$0); n++; if(n%4==0) { printf("\n");} else { printf("\t");} }' |
awk -v k=10000 'BEGIN{srand(systime() + PROCINFO["pid"]);}{s=x++<k?x- 1:int(rand()*x);if(s<k)R[s]=$0}END{for(i in R)print R[i]}' |
awk -F"\t" '{print $1"\n"$3"\n"$5"\n"$7 > "forward_sub.fastq";print $2"\n"$4"\n"$6"\n"$8 > "reverse_sub.fastq"}'
```

This command will:

1.  `paste` the fastq to keep the paired reads together.
2.  Use `awk` to concatenate every 4 lines in one line,
    separated by tab (Because in a fastq file, a read is comprised of 4
    lines).
3.  Let’s say I want only 10,000 reads: I set k as
    10,000. In the `BEGIN` block, and I set random seed with `srand()`.
    Then, it’s show time for reservoir sampling: I take the **first k-1
    row**, and then for every coming row, the nth row has a chance of
    k/n of being selected and stored in an array `R`.
4.  Because we concatenated first the two files with
    `paste` and then `awk` in step 2, we now use `awk` again to extract
    every odd field (forward read) and even field (reverse read)
    separately, and redirect them into forward\_sub.fastq and
    reverse\_sub.fastq respectively.

This script troubled me a bit because it sometimes draws k samples and
other times only k-1 samples, so I ended up checking the definition of
the sampling method and felt it is more appropriate to take the first k
row instead of k-1 row in step 3.

Another challenge I encountered is that, in the command above, the
selected k reads were stored in an array until the end of the program.
If k reads already outsize your RAM, the command failed somewhere when
there was no longer any space for the array to grow (with an odd error
message `killed`).

My solution here is to draw sample to generate a list of picked lines
first, and then for every line, we check if it is picked. If it is, we
write it to a file. After that, we do aforementioned step 4 to extract
the fields into separate fastq files.

```
paste forward.fastq reverse.fastq |\
awk '{ printf("%s",$0); n++; if(n%4==0) { printf("\n");} else { printf("\t");} }' |\

# Pick random sample from line numbers first
awk -v k=423549353 'BEGIN{ srand(systime() + PROCINFO["pid"]);\
for(i = 1; i <=847098706 ; i++) { s= i<=k?i-1:int(rand()*i);\
if(s<k) R[s]=i}; n=asort(R)}\

# Check the line numbers
{if(NR==1) co=1; if(NR == R[co]) {print $0 >> "temp.fastq";co++}}'

# Reformat the subsampled file
awk -F"\t" '{print $1"\n"$3"\n"$5"\n"$7 > "forward_sub.fastq";\print $2"\n"$4"\n"$6"\n"$8 > "reverse_sub.fastq"}' temp.fastq
```

---

Last update: 2022-06-04

Special thanks to Tien Du for catching a syntax error in this post!
