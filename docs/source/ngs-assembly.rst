.. _ngs-assembly:

*************************
*De novo* genome assembly
*************************


Introduction
############

[MILLER2010]_

An assembly is a hierarchical data structure that maps the sequence data to a putative reconstruction of the target.
It groups reads into contigs and contigs into scaffolds. Contigs provide a multiple sequence alignment of reads plus the consensus sequence.
The scaffolds, sometimes called supercontigs or metacontigs, define the contig order and orientation and the sizes of the gaps between contigs.
Scaffold topology may be a simple path or a network. Most assemblers output, in addition, a set of unassembled or partially assembled reads.
The most widely accepted data file format for an assembly is FASTA, wherein contig consensus sequence can be represented by strings of the characters A, C, G, T, plus possibly other characters with special meaning.
Dashes, for instance, can represent extra bases omitted from the consensus but present in a minority of the underlying reads. Scaffold consensus sequence may have N's in the gaps between contigs. The number of consecutive N's may indicate the gap length estimate based on spanning paired ends.

Assemblies are measured by the size and accuracy of their contigs and scaffolds.
Assembly size is usually given by statistics including maximum length, average length, combined total length, and N50.
The contig N50 is the length of the smallest contig in the set that contains the fewest (largest) contigs whose combined length represents at least 50% of the assembly.
The N50 statistics for different assemblies are not comparable unless each is calculated using the same combined length value.
Assembly accuracy is difficult to measure. Some inherent measure of accuracy is provided by the degrees of mate-constraint satisfaction and violation [17].
Alignment to reference sequences is useful whenever trusted references exist.



1. xxxx.

2. xxxx.

3. xxxx.

4. In this section we will be using |spades| for assembling Illumina-only raw reads and |unicycler| for an hybrid assembly, i.e. when we have sequenced our isolates with Illumina and PacBio or Nanopore platforms.


Learning objectives
###################

After completing this Tutorial, you will be able to:

* Perform a *de novo* assembly using raw sequence reads from different platforms.
* Visualize and analyze *de novo* assembly graphs.
* Evaluate the quality of a genome assembly.


Short-read assembly
###################


SPAdes
******

* |spades| - SPAdes – St. Petersburg genome assembler – is an assembly toolkit containing various assembly pipelines [BANKEVICH2012]_.

* Besides the typical |spades| module for short-read genome assembly other additional pipelines are also available such as:

  1. ``metaSPAdes`` for **metagenomic** data sets [NURK2017]_.
  2. ``plasmidSPAdes`` for extracting and assembling **plasmids** from metagenomic data sets [ANTIPOV2016]_.
  3. ``metaplasmidSPAdes`` – a pipeline for extracting and assembling **plasmids from metagenomic** data sets [ANTIPOV2019]_.
  4. ``rnaSPAdes`` – a de novo transcriptome assembler from **RNA-Seq** data [BUSHMANOVA2019]_.
  5. ``truSPAdes`` – a module for **TruSeq** barcode assembly [BANKEVICH2016]_.
  6. ``biosyntheticSPAdes`` – a module for **biosynthetic** gene cluster assembly with paired-end reads [MELESHKO2019]_.


Installation
............

.. code-block:: bash

   # Create a new environment named assembly
   $ conda create -n assembly python=3

   # Activate the new environment
   $ conda activate assembly

   # Install SPAdes
   $ conda install spades

   # Check SPAdes installation
   $ spades.py --version
   $ spades.py --test

.. note::

   If the installation is successful, you will find the following information at the end of the Bash shell ``TEST PASSED CORRECTLY``.

Usage
.....

**1. Input/Output files**

``Input``: Accept compress or uncompress files such as ``.fastq`` or ``.fastq.gz``. For this part of the Tutorial, we will use the paired-end Illumina raw reads.

``Output``: Several files are produced by |spades|. However, particular attention will be given to ``contigs.fasta`` (xxxx), ``assembly_graph.gfa`` (xxxx), and ``warnings.log`` (xxxx).

**2. Basic commands**

.. code-block:: bash

   # Run SPAdes in your trimmed and untrimmed paired-end Illumina reads
   $ spades.py -1 strainA_R1_paired_trimmed.fastq.gz -2 strainA_R2_paired_trimmed.fastq.gz --careful -k 21,33,55,77 -t 8 -o strainA_SPAdes
   $ spades.py -1 strainA_R1_paired_untrimmed.fastq.gz -2 strainA_R2_paired_untrimmed.fastq.gz --careful -k 21,33,55,77 -t 8 -o strainA_SPAdes

   # Move your result files to the spades directory
   $ mv <path_results_spades> ~/tutorial/assembly/spades/

.. csv-table:: Parameters explanation when using Unicycler
   :header: "Parameter", "Description"
   :widths: 20, 60

   "``-1 <filename>``", "File with forward paired-end reads"
   "``-2 <filename>``", "File with reverse paired-end reads"
   "``--careful``", "Tries to reduce number of mismatches and short indels"
   "``-k <int>``", "list of k-mer sizes (must be odd and less than 128) [default: 'auto']"
   "``-t <int>``", "Number of threads [default: 16]"
   "``-o <output_dir>``", "Directory to store all the resulting files (required)"
   "``--isolate``", "Improves the assembly quality and running time"

.. seealso::

   If you have high-coverage data for bacterial isolate, |spades| developers highly recommend to use the ``--isolate`` option that is not compatible with ``--careful`` option; thus, you must disable the last one.


**3. Parameters**

.. code-block:: bash

   # To see a full list of available options in SPAdes
   $ spades.py --help

















Hybrid assembly
###############


Unicycler
*********

When assembling just Illumina reads, Unicycler functions mainly as a SPAdes optimiser. It offers a few benefits over using SPAdes alone:

    Tries a wide range of k-mer sizes and automatically selects the best.
    Filters out low-depth parts of the assembly to remove contamination.
    Applies SPAdes repeat resolution to the graph (as opposed to disconnected contigs in a FASTA file).
    Rejects low-confidence repeat resolution to reduce the rate of misassembly.
    Trims off graph overlaps so sequences aren't repeated where contigs join.


Installation
............

.. code-block:: bash

   # Activate the assembly environment
   $ conda activate assembly

   # Install Unicycler
   $ conda install unicycler

   # Check Unicycler installation
   $ unicycler --version


Usage
.....

**1. Input/Output files**

``Input``: Accept compress or uncompress files such as ``.fastq`` or ``.fastq.gz``. For this part of the Tutorial, we will use the paired-end Illumina raw reads.

``Output``: Several files are produced by |spades|. However, particular attention will be given to ``contigs.fasta`` (xxx), ``assembly_graph.gfa`` (xxx), and ``warnings.log`` (xxx).

**2. Basic commands**

.. code-block:: bash

   # Run SPAdes in your trimmed and untrimmed paired-end Illumina reads
   $ spades.py -1 strainA_R1_paired_trimmed.fastq.gz -2 strainA_R2_paired_trimmed.fastq.gz --careful -k 21,33,55,77 -t 8 -o strainA_SPAdes
   $ spades.py -1 strainA_R1_paired_untrimmed.fastq.gz -2 strainA_R2_paired_untrimmed.fastq.gz --careful -k 21,33,55,77 -t 8 -o strainA_SPAdes

   # Move your result files to the spades directory
   $ mv <path_results_spades> ~/tutorial/assembly/spades/

.. csv-table:: Parameters explanation when using Unicycler
   :header: "Parameter", "Description"
   :widths: 20, 60

   "``-1 <filename>``", "File with forward paired-end reads"
   "``-2 <filename>``", "File with reverse paired-end reads"
   "``--careful``", "Tries to reduce number of mismatches and short indels"
   "``-k <int>``", "list of k-mer sizes (must be odd and less than 128) [default: 'auto']"
   "``-t <int>``", "Number of threads [default: 16]"
   "``-o <output_dir>``", "Directory to store all the resulting files (required)"
   "``--isolate``", "Improves the assembly quality and running time"

.. seealso::

   If you have high-coverage data for bacterial isolate, |spades| developers highly recommend to use the ``--isolate`` option that is not compatible with ``--careful`` option; thus, you must disable the last one.

**3. Parameters**

.. code-block:: bash

   # To see a full list of available options in SPAdes
   $ unicycler --help






Assembly visualization
######################


Bandage
.......


Assembly quality control
########################


QUAST
.....




.. todo::

   1. Run |spades| assembler in your trimmed and untrimmed paired-end Illumina reads.
   2. Assess the quality of both |spades| assemblies quality using |quast|.
   3. How many contigs in total did the assembly produced?
   4. What is the N50 of the assembly? What does this mean?
   5. Did you noticied any difference in the assembly using trimmed and untrimmed reads? What is the main different in terms of quality parameters?
   6. Run |unicycler| for an hybrid assembly using the short-read paired-end Illumina and the long-read Nanopore.
   7. Compare |spades| and |unicycler| assemblies. What are the main differences? Did you noticed any kind of improvement in genome assembly?
   8. Run |kraken|, |bracken| and |krona| also in your assembled genomes.
   9. Is there any contaminations in your assembled genomes? What kind of contamination?


Folder structure
################

At the end of this section, you will have the following folder structure.

::

    tutorial
    ├── raw_data
    │   ├── files_fastq.gz
    │   ├── files.fa
    │   ├── files.fna
    │   ├── files.gbff
    ├── qc_visualization
    │   ├── trimmed
    │   │   ├── files_clean_fastqc.html
    │   │   ├── files_clean_fastqc.zip
    │   │   ├── multiqc_clean_report.html
    │   │   ├── multiqc_clean_data
    │   ├── untrimmed
    │   │   ├── files_fastqc.html
    │   │   ├── files_fastqc.zip
    │   │   ├── multiqc_report.html
    │   │   ├── multiqc_data
    ├── qc_improvement
    │   ├── files_clean.fastq.gz
    ├── taxonomy
    │   ├── kraken_bracken
    │   │   ├── files_cseqs_1.fastq
    │   │   ├── files_cseqs_2.fastq
    │   │   ├── output.kraken
    │   │   ├── report.kreport
    │   │   ├── output.bracken
    │   ├── krona
    │   │   ├── output_krona.html
    ├── assembly
    │   ├── spades
    │   │   ├── assembly_spades_trimmed.fasta
    │   │   ├── assembly_spades_trimmed.gfa
    │   │   ├── assembly_spades_trimmed.log
    │   │   ├── assembly_spades_untrimmed.fasta
    │   │   ├── assembly_spades_untrimmed.gfa
    │   │   ├── assembly_spades_untrimmed.log
    │   ├── unicycler
    │   │   ├── assembly_unicycler.fasta


References
##########

.. [MILLER2010] Miller JR, Koren S, Sutton G. 2010. Assembly algorithms for next-generation sequencing data. Genomics. 95(6):315-27. `DOI: 10.1016/j.ygeno.2010.03.001 <https://dx.doi.org/10.1016/j.ygeno.2010.03.001>`_.
.. [BANKEVICH2012] Bankevich A, et al. 2012. SPAdes: A New Genome Assembly Algorithm and Its Applications to Single-Cell Sequencing. J Comput Biol. 19(5):455–477. `DOI: 10.1089/cmb.2012.0021 <https://dx.doi.org/10.1089/cmb.2012.0021>`_.
.. [NURK2017] Nurk S, Meleshko D, Korobeynikov A, Pevzner PA. 2017. metaSPAdes: a new versatile metagenomic assembler. Genome Res. 27(5):824–834. `DOI: 10.1101/gr.213959.116 <https://dx.doi.org/10.1101/gr.213959.116>`_.
.. [ANTIPOV2016] Antipov D, et al. 2016. plasmidSPAdes: assembling plasmids from whole genome sequencing data. Bioinformatics. 32(22):3380-3387. `DOI: 10.1093/bioinformatics/btw493 <https://dx.doi.org/10.1093/bioinformatics/btw493>`_.
.. [ANTIPOV2019] Antipov D, Raiko M, Lapidus A, Pevzner PA. 2019. Plasmid detection and assembly in genomic and metagenomic data sets. Genome Res. 29(6):961-968. `DOI: 10.1101/gr.241299.118 <https://dx.doi.org/10.1101/gr.241299.118>`_.
.. [BUSHMANOVA2019] Bushmanova E, Antipov D, Lapidus A, Prjibelski AD. 2019. rnaSPAdes: a de novo transcriptome assembler and its application to RNA-Seq data. Gigascience. 8(9):giz100. `DOI: 10.1093/gigascience/giz100 <https://dx.doi.org/10.1093/gigascience/giz100>`_.
.. [BANKEVICH2016] Bankevich A, Pevzner PA. 2016. TruSPAdes: barcode assembly of TruSeq synthetic long reads. Nat Methods. 13(3):248-50. `DOI: 10.1038/nmeth.3737 <https://dx.doi.org/10.1038/nmeth.3737>`_.
.. [MELESHKO2019] Meleshko D, et al. 2019. BiosyntheticSPAdes: reconstructing biosynthetic gene clusters from assembly graphs. Genome Res. 29(8):1352–1362. `DOI: 10.1101/gr.243477.118 <https://dx.doi.org/10.1101/gr.243477.118>`_.


List of Assembly tools
######################

.. seealso::

   * The tools used in this Tutorial section are not the only ones available for the purpose of *de novo* genome assembly.

   * Other tools can also be used to perform this task (**some examples are provided in table below**).

   * Nowadays most of these tools accept both short- (e.g., **Illumina**) and long-read sequence data (e.g., **PacBio**, **Nanopore**). Therefore, the best approach is to test more than one tool and choose those results that best help to answer your initial research question while presenting the best quality.

.. csv-table::
   Table with other available assembly Software installed by conda.
   :header: "Package name", "Version", "Algorithm used"
   :widths: 20, 20, 40

   "`ABySS <https://github.com/bcgsc/abyss>`_", "2.2.5", "de Bruijn Graph"
   "`Flye <https://github.com/fenderglass/Flye>`_", "2.8.1", "Repeat graph - long-read assembly"
   "`MaSuRCA <https://github.com/alekseyzimin/masurca>`_", "3.4.2", "*super read* with Overlap–layout–consensus"
   "`SOAPdenovo2 <https://github.com/aquaskyline/SOAPdenovo2>`_", "2.40", "de Bruijn Graph"
   "`SPAdes <https://github.com/ablab/spades>`_", "3.14.1", "paired de Bruijn Graph - short- and long-read assembly"
   "`Trycycler <https://github.com/rrwick/Trycycler/wiki>`_", "0.3.1", "Multiple sequence alignment - long-read assembly"
   "`Unicycler <https://github.com/rrwick/Unicycler>`_", "0.4.8", "de Bruijn Graph with greedy approach - long-read assembly"
   "`Velvet <https://github.com/dzerbino/velvet>`_", "1.2.10", "de Bruijn Graph"
