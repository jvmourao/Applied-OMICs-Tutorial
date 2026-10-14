.. _quality-thresholds:

******************
Quality thresholds
******************

Before you interpret the results of a genome (e.g., AMR genes, typing, plasmids), you must check that the data and the assembly have enough quality. This page summarises all the thresholds used in this Tutorial, which are based on the ISO 23418:2022 standard [ISO23418]_ and, for the species-specific values, on `QualiBact <https://qualibact.org/>`_. Each section of the Tutorial has a **"Does your sample pass?"** step, with the commands to check them.

* **Critical**: if the sample (or the assembly) does not pass (**FAIL**), it should not be used; e.g., it should be sequenced again.
* **Non-critical**: the metric is determined, but if the sample does not pass (**WARNING**), it can still be used. Look at its results more carefully.

.. note::
   These thresholds are for **Illumina** reads and bacterial isolates. They are a guidance: always check the requirements of your study, and the most recent values for your species.


Reads
#####

.. csv-table::
   :header: "Metric", "Definition", "Threshold", "Criticality", "Tool"
   :widths: 18, 27, 30, 12, 13

   "%Q≥30", "Bases with Phred quality ≥ 30, before trimming", "≥ 80% (2x150 bp and shorter); ≥ 75% (2x250 bp and shorter); ≥ 70% (2x300 bp and shorter)", "Critical", "fastp"
   "GC content (ΔGC)", "GC content of the clean reads vs. the expected GC content of the species", "< 4% deviation (e.g., *E. coli* 50.6%: 46.6–54.6%)", "Critical", "fastp"
   "Read-length distribution", "Lengths of the reads before trimming", "2x150 bp: > 95% with 150 bp; 2x250 bp: > 90% with 250 bp; 2x300 bp: < 5% shorter than 120 bp and > 50% longer than 150 bp, or > 90% with 300 bp", "Non-critical", "awk (raw reads)"
   "Residual adapters", "% of the reads with adapters after trimming", "≤ 0.1%", "Non-critical", "FastQC"
   "Ambiguous bases (%N)", "% of Ns in the reads after trimming", "< 0.1%", "Non-critical", "awk (clean reads)"


Coverage
########

.. csv-table::
   :header: "Metric", "Definition", "Threshold", "Criticality", "Tool"
   :widths: 18, 27, 30, 12, 13

   "Depth of coverage", "Median number of reads that cover each base of the reference genome", "≥ 30x (routine); ≥ 50x (outbreak SNP analysis); ≥ 80x (*Campylobacter* with the Nextera XT kit)", "Critical", "BWA + SAMtools"
   "Breadth of coverage", "% of the reference genome covered by ≥ 10 reads", "≥ 95% (routine); ≥ 95–98% (outbreak SNP analysis)", "Critical", "BWA + SAMtools"

.. note::
   ISO 23418:2022 [ISO23418]_ recommends a depth of at least 20x, depending on the application and on the microorganism. For the detection of variants, ISO 20397-2:2021 [ISO20397]_ indicates 15x for homozygous SNVs, 33x for heterozygous SNVs and 60x for insertions and deletions (indels).


Species and contamination
#########################

.. csv-table::
   :header: "Metric", "Definition", "Threshold", "Criticality", "Tool"
   :widths: 18, 27, 30, 12, 13

   "Inter-species contamination and species confirmation", "% of the clean reads classified as the expected species (and genus)", "≥ 90% of the reads as the target species; if not, ≥ 90% as the target genus **and** ≥ 75% as the target species (*Escherichia* and *Shigella* counted as one genus)", "Critical", "Kraken2 + Bracken"
   "Intraspecies mixture", "More than one allele in single-copy core genes", "No multiple-allele calls (flag the sample if any)", "Non-critical", "ConFindr"


Assembly
########

.. csv-table::
   :header: "Metric", "Definition", "Threshold", "Criticality", "Tool"
   :widths: 18, 27, 30, 12, 13

   "Completeness", "% of the expected single-copy marker genes present", "≥ 95%", "Critical", "CheckM2"
   "Contamination", "% of the marker genes present in more than one copy", "≤ 5%", "Critical", "CheckM2"
   "Genome size", "Total length of the assembly", "Within the range of the species (QualiBact)", "Critical", "QUAST"
   "N50 and number of contigs", "Contiguity of the assembly", "Within the range of the species (QualiBact)", "Non-critical", "QUAST"
   "GC content", "GC content of the assembly", "Within the range of the species (QualiBact)", "Non-critical", "QUAST"
   "Ambiguous bases", "Ns per 100 kb of the assembly", "≤ 100 (preferably close to 0)", "Non-critical", "QUAST"

.. csv-table:: Species ranges of QualiBact (qualibact-v1.0) for the species of this Tutorial
   :header: "Metric", "*Escherichia coli*", "*Salmonella enterica*"
   :widths: 30, 35, 35

   "Genome size (bp)", "4,100,000–6,300,000", "4,400,000–5,900,000"
   "GC content (%)", "50.0–51.2", "51.1–52.4"
   "N50 (bp)", "≥ 20,000", "≥ 64,000"
   "Number of contigs", "≤ 670", "≤ 190"

The ranges of other species are available on the `QualiBact <https://qualibact.org/species/>`_ website.

.. note::
   The completeness and contamination are always evaluated with |checkm2|. QualiBact also gives completeness and contamination ranges, but they were calculated with CheckM, so they are not used in this Tutorial.


Detection of genes
##################

These are not quality thresholds, but the minimum identity and coverage used in this Tutorial to report a gene.

.. csv-table::
   :header: "Tool", "Identity", "Coverage"
   :widths: 40, 30, 30

   "ResFinder", "≥ 80%", "≥ 60%"
   "AMRFinderPlus", "Default (curated per gene, or 90%)", "Default (50%)"
   "VirulenceFinder", "≥ 90%", "≥ 60%"
   "PlasmidFinder", "≥ 80%", "≥ 60%"
   "MOB-suite (replicons)", "≥ 90%", "≥ 90%"
   "MLST", "100%", "100%"


References
##########

.. [ISO20397] ISO 20397-2:2021. Biotechnology — Massively parallel sequencing — Part 2: Quality evaluation of sequencing data. International Organization for Standardization, Geneva.
.. [ISO23418] ISO 23418:2022. Microbiology of the food chain — Whole genome sequencing for typing and genomic characterization of bacteria — General requirements and guidance. International Organization for Standardization, Geneva.
