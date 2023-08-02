---
title: Transcriptomically reserved identities for fly olfactory projection neuron
author: Yen-Chung Chen
date: '2018-05-11'
slug: transcriptomically-reserved-identities-for-fly-olfactory-projection-neuron
categories:
  - Journal club
tags:
  - Neural diversity
image:
  caption: ''
  focal_point: ''
---
> Original article:  
> Li, H. *et al.* [Classifying Drosophila Olfactory Projection Neuron
> Subtypes by Single-Cell RNA
> Sequencing](https://doi.org/10.1016/j.cell.2017.10.019). *Cell*
> 171,1206.e22–1207 (2017).

The complexity of the nervous system has fascinated scientists for
centries. We knew that injuring different part of the brain or spinal
cord leads to distinctive function impairment, and we observed neurons
with different shape and size.

Since the rise of molecular biology, people have been longing to find an
explanation of this diversity that fits the central dogma: Genes
corresponding to these unique cells have been identified, and people
hypothesize the diversity is hardwired in genetic program and executed
so that the position, number, and connectivity are precisely regulated.
Nevertheless, whether gene expression is the cause or consequence of
functional diversity in the nervous system remains largely an unanswered
question. In the recent boom of single cell RNA-seq studies, many
researchers have tried to solve the myth by the newly invented power,
and this article from Li *et al*.is among those attempts.

The story is quite concise and frank, in the sense of exposing the
questions raised by observations and their attempt to address them,
which are not always successful, to the reader.

Based on previous understanding of olfactory projecting neuron in fly,
they tried and dismissed general clustering method and developed [their
own](https://github.com/felixhorns/FlyPN). The techinical advance in
data collection and generation like single cell RNA-seq could drive the
development of analytic tools, but before the tools become mature, it is
inevitable to apply what one already know to retrospectively decide
whether the analysis was done *right*.

Are the identities identified in the study real? The authors again
turned to their prior knowledge and showed the clustering identities
corresponded to known populations of projection neurons. Then, with the
powerful genetic tools in fly, they identified a gene marking a
population that looked like the DC2 neurons, and another, which mapped
to 4 clusters, and two of them might represent DC3 and VA1d neurons *in vivo*. Trying to find more genes that separate these two clusters was
not completely fruitful: Genes found were able to distinguish the
populations of interest, but they were also expressed in other
projection neurons, which greatly complicated the identification of each
subtypes when marker genes overlap a lot. They in turn proposed a model
of combinatorial gene *barcodes* to delineate the functionally different
population, but they did not show how well this model reflects the real
world..

The authors also made efforts to establish the link between
transcriptomic identity and function. They found a transcription factor
that was not known to regulate neural function before and was expressed
in a subpopulation of projection neurons, the adPNs, that project to a
defined brain region. The authors showed that when the transcription
factor was mis-expressed in the neurons that would otherwise not express
it, the neurons with mis-expression targeted to the same region as adPN
did, which corroborated the role of this transcription factor as a
determinant of neurite guidance. This is a neat way to show the link
between transcriptome diversity and function, but it also seems like
that the current analysis is not ready yet to identify this kind of
functionally important gene for each single cluster because the authors
was not able to but picked a transcription factor that is expressed in
almost half of their clusters.

Finally, the authors collected projection neurons from different stages
in development and showed that the diversity of single cell
transcriptome peaked at the time when connection was forming. Though it
is not surprising that the diversity is transient because unnecessary
diversity could be too costly to maintain after connections had been
formed, this is the first study actually showing that as far as I know.

The take-home messages here are:

1.  Because conclusive answer is rare, try your best to
    make educated guess in analysis.
2.  Frame a coherent hypothesis according to both
    significance and the questions that need to be addressed. (It is
    cliché, but in many articles, the struggle to achieve this is just
    packed too well for me to realize that it did happen.)
3.  Customizing methods is tedious, but it could pay off
    as additional novelty and might not be avoidable at the end of the
    day.
