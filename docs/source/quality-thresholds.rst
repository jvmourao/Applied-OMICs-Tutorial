.. _quality-thresholds:

******************
Quality thresholds
******************

Before you interpret the results of a genome (e.g., AMR genes, typing, plasmids), you must check that the data and the assembly have enough quality. This page summarises all the thresholds used in this Tutorial. Each section of the Tutorial has a **"Does your sample pass?"** step, with the commands to check them.

* **Fail**: the sample (or the assembly) should not be used; e.g., it should be sequenced again.
* **Warning**: the sample can be used, but look at its results more carefully.

.. note::
   These thresholds are for **Illumina** reads and for bacterial isolates. They are commonly used in routine whole-genome sequencing, but they are a guidance: always check the requirements of your study, and the most recent values for your species.


Reads (quality control)
#######################

.. csv-table::
   :header: "Metric", "Threshold", "Type", "Tool"
   :widths: 30, 40, 10, 20

   "Bases with quality ≥ Q30 (after cleaning)", "≥ 80% (reads ≤ 150 bp); ≥ 75% (≤ 250 bp); ≥ 70% (> 250 bp)", "Fail", "fastp"
   "GC content of the reads (ΔGC)", "Deviation from the expected GC content of the species < 4% (e.g., *E. coli* 50.6%: 46.6–54.6%)", "Fail", "fastp"
   "Bases with quality ≥ Q20", "≥ 95%", "Warning", "fastp"
   "Per base sequence quality", "> 20 in all positions", "Warning", "FastQC"


Coverage
########

.. csv-table::
   :header: "Metric", "Threshold", "Type", "Tool"
   :widths: 30, 40, 10, 20

   "Depth of coverage", "≥ 30x (routine analyses); ≥ 50x (SNP-based analyses); ≥ 80x (*Campylobacter* sequenced with Nextera XT)", "Fail", "BWA + SAMtools"
   "Breadth of coverage (10x)", "≥ 95% of the reference genome", "Fail", "BWA + SAMtools"
   "Coverage uniformity (coefficient of variation)", "< 0.25", "Warning", "BWA + SAMtools"


Species and contamination
#########################

.. csv-table::
   :header: "Metric", "Threshold", "Type", "Tool"
   :widths: 30, 40, 10, 20

   "Inter-species contamination (Illumina reads)", "Most abundant species ≥ 90% of the classified reads, **or** its genus ≥ 90% and the species ≥ 75% (*Escherichia* and *Shigella* counted as one genus)", "Fail", "Kraken2 + Bracken"
   "Species detected", "The same as the expected species", "Fail", "Bracken, ConFindr"
   "Intraspecies contamination", "Not detected (``ContamStatus = False``)", "Warning", "ConFindr"
   "Contamination of the assembly", "≤ 5%", "Fail", "CheckM2"


Assembly
########

.. csv-table::
   :header: "Metric", "Threshold", "Type", "Tool"
   :widths: 30, 40, 10, 20

   "Completeness", "≥ 90%", "Fail", "CheckM2"
   "Contamination", "≤ 5%", "Fail", "CheckM2"
   "Genome size, GC content, N50, number of contigs, coding sequences", "Within the species-specific range of `QualiBact <https://qualibact.org/>`_ (see below)", "Fail / Warning", "QUAST, Bakta"

.. note::
   The completeness and contamination of the assembly are always evaluated with |checkm2| (≥ 90% and ≤ 5%). QualiBact also gives completeness and contamination ranges, but they were calculated with CheckM, so they are not used in this Tutorial.

.. csv-table:: Species-specific thresholds of QualiBact (version qualibact-v1.0) for the species of this Tutorial (FAIL range / WARNING range)
   :header: "Metric", "*Escherichia coli*", "*Salmonella enterica*"
   :widths: 30, 35, 35

   "Genome size (bp)", "4,100,000–6,300,000 / 4,400,000–5,700,000", "4,400,000–5,900,000 / 4,500,000–5,100,000"
   "GC content (%)", "50.0–51.2 / 50.2–50.9", "51.1–52.4 / 51.9–52.3"
   "N50 (bp)", "≥ 20,000 / ≥ 23,000", "≥ 64,000 / ≥ 90,000"
   "Number of contigs", "≤ 670 / ≤ 600", "≤ 190 / ≤ 160"
   "Coding sequences (CDS)", "3,900–6,500 / 4,200–5,800", "4,100–6,000 / 4,200–4,900"

The thresholds of other species are available on the `QualiBact <https://qualibact.org/species/>`_ website.


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
