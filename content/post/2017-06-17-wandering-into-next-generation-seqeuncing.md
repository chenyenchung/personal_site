---
title: Wandering into next-generation seqeuncing
author: Yen-Chung Chen
date: '2017-06-17'
slug: wandering-into-next-generation-seqeuncing
categories:
  - Random thoughts
tags:
  - NGS
image:
  caption: ''
  focal_point: ''
---
### No Longer That "Next" Generation

When I was doing my undergraduate project, microarray was like black
magic that turned the labyrinth of gene expression into colorful heatmap
and brought your paper into top-notch journals. Several years later,
when I came back from my clinical internship to life science, I was
overwhelmed. Microarray became as common as microwave, and people
started using next-generation sequencing to check everything. It's like
every single word I've learned in class now has to be followed by -seq.
RNA-seq, ChIP-seq, DNaseI-seq..., they are simply everywhere.

When microarray was introduced, I was convinced that we were finally
able to study not only the trees but also the forest as a whole, but now
with all the seqs, I further accept that when we thought we might be
studying the whole forest with microarray, we were actually near-sighted
and thus stuck in low resolution. (I believe we would still be
near-sighted even with NGS. I assume before defining the question really
well, it's impossible to say if we have enough resolution.)

Well, it should be a nice thing to see clearer and broader.
Nevertheless, during my literature wandering, I realize that although
next-generation sequencing is genome-wide by default, it is hard for a
paper to cover that much, and you are deemed to end up with curiosity
piling up, wondering what's out there in the dataset.

### "If You Build It, They Will..."

I must admit I am not the kind of person driven by pure curiosity, so I
have not really tried to analyze sequencing data until my own project
stumbled, and some published dataset seemed to hold some hint.

"That shouldn't be too hard." I told myself. It was just looking into
protein binding in some locus, and the authors should have already done
the difficult part for me.

Well, not actually. I failed to find any guide for dummies. Many of the
material I found was either so detailed and focused that I identified
nowhere to start with, or so brief that I felt like I was watching Bob
Ross painting.

This might be a result of wrong keywords to Google, or some helpful
guide just escaped my browse. Anyway, the best thing I could found was
in Japanese. It seems that this Mr. Takatsugu Kosugi also tried to find
a way out in analyzing ChIP-seq result, and took some note in his
[blog](http://ngsdamemorandum.blogspot.tw), which gave me a good start.

So, here I am, still experimenting and having already destroyed my Linux
virtual machine once. I write this blog to leave my own breadcrumb
trail, which hopefully helps the future me and enhances the chance of
some newbie hitting on a blog entry that gives some little hint.

The first thing to clarify here would be "Do I own a machine that is
capable for sequencing data analysis?" The scenario is doing everything
on Linux in a virtual machine. In my case, aligning sequencing result to
reference genome would be the bottleneck, and here are how long it takes
to align 10 million reads with
[Bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml):

-   **100 hours** on a Core i5--2500 (3.30 GHz) machine, with 3 GB RAM
    allocated to the virtual machine
-   **15 minutes** on a Core i5--4570R (2.70 GHz) machine, with 8 GB RAM
    allocated to the virtual machine

I went on to look up a little bit. Bowtie2 puts the whole reference
genome into RAM, which takes up more than 2 GB, and it needs some more
to work on. If you are going to do something more complicated, like
single-cell sequencing alignment, the minimal RAM requirement surges to
16+ GB. With enough working space, the sequence is then processed in
every CPU cycle, so CPU also matters.

My impression now is that RAM size matters more than CPU for ChIP-seq in
alignment, and I guess most recent computers are capable of completing
the analysis pipeline within a reasonable time (say a couple of days).
So if you are interested in trying, and you have a computer with \> 8 GB
RAM, I'll say that a green light for trying.
