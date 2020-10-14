.. _ngs-annotations:

*****************
Genome annotation
*****************

xxxx


Introduction
############

xxxx


Learning objectives
###################

xxxx




Assembly completeness
#####################


Busco
.....

Refer to the previous section where we performed de novo assembly.


Although quast output a range of metric to assess how contiguous our assembly is, having a long N50 does not guarantee a good assembly: it could be riddled by misassemblies!

We will run Busco to try to find marker genes in our assembly.
Marker genes are conserved across a range of species and finding intact conserved genes in our assembly would be a good indication of its quality

First we need to download and unpack the bacterial datasets used by busco

wget http://busco.ezlab.org/datasets/bacteria_odb9.tar.gz
tar xzf bacteria_odb9.tar.gz

then we can run busco with

BUSCO.py -i m_genitalium.fasta -l bacteria_odb9 -o busco_genitalium -m genome
