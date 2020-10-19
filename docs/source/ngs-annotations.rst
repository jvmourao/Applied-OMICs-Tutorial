.. _ngs-annotations:

*****************
Genome annotation
*****************


Introduction
############

1. After you performed de novo assembled using raw sequence reads, it is useful to know what **relevant genomic features** are on the produced contigs.

2. Genome annotation is the process that allows us to **identify** features of interest in those contigs and to **label** them with useful information.

3. In this section, you will use |prokka| for whole-genome annotation, |abricate| for a more specific one and `IGV <http://software.broadinstitute.org/software/igv/>`_ for its interactive visualization. At the end we will evaluate assembly completeness using |busco|.

4. When it comes to annotation process there are two key concepts, **Sequence Ontology** and **Gene Ontology**, that you should understand before you move forward.


Sequence Ontology (SO)
**********************

* SO is a **structured controlled vocabulary** of sequence features that are part of the genomic annotation.

* This vocabulary definition is vital for the exchange, analysis and management of genomic data [EILBECK2005]_.

* You will see for example SO terms used in **GenBank annotation files** (e.g., CDS, ORF, tRNA_gene).

.. seealso::

   To understand the **definition of all terms** used you can go to the `Sequence Ontology Browser <http://www.sequenceontology.org/browser/obob.cgi>`_ and search for it.


Gene Ontology (GO)
******************

* |go| is a controlled vocabulary that correlates each gene to one or more functions [ALBERT2019]_.

* The |go| ontology structure can be represented as a graph where nodes are the GO terms and the edges are the associations between these terms.

* Each child node is more “specific” than its parent, and function is “inherited” down the line

* |go| has three structured, independent sub-ontologies that describe our knowledge of the gene products:

  1. **Molecular Function** - The molecular-level activities performed by the gene product.
  2. **Cellular Component** - The locations relative to cellular structures where the gene product performs a function.
  3. **Biological Process** - The larger processes accomplished by multiple molecular activities.

.. seealso::

   You can search for GO terms or Gene products in `The Gene Ontology Resource <http://geneontology.org/>`_ official webpage.


Learning objectives
###################

After finishing this Tutorial section, you will be able to:

* Make gene predictions of assembled genomes.
* Evaluate the presence of specific genes conferring adaptative features.
* Evaluate assembly completeness through the search of orthologues presence or absence.
* Use specific Software to visualize and edit genome annotations.


Whole-genome annotation
#######################


Prokka
******

* |prokka| - Prokaryotic Annotation - is a software tool that finds and annotate bacterial, archaeal and viral features from genome sequences quickly and produce standards-compliant output files (e.g., GenBank, EMBL and GFF formats) [SEEMANN2014]_.

* The annotation process of protein coding genes by |prokka| relies on several external feature prediction tools and has two main steps:

  1. First, it uses Prodigal to identify the coordinates of candidate genes on the assembled genome.

  2. Second, the putative gene product is predicted by similarity against a large database of known sequences.

* You will use |prokka| to annotate all your bacterial assemblies from |spades| and |unicycler|.


Installation
............

.. code-block:: bash

   # Create a new environment named annotation
   $ conda create -n annotation python=3

   # Activate the new environment
   $ conda activate annotation

   # Install Prokka
   $ conda install prokka

   # Check Prokka installation
   $ prokka --version


Usage
.....

**1. Input/Output files**

``Input``: Single or multiple ``.fasta`` files from assembly tools.

``Output``: Several output files are generated. A particular attention should be given to ``.gff`` and ``.gbk`` (information about the annotated features), ``.txt`` (number of annotated features), ``.faa`` (protein sequences of annotated genes), and ``.ffn`` (nucleotide sequences of annotated genes).

**2. Basic commands**

.. code-block:: bash

   # Let's first create new directories to store your annotations
   $ cd ~/tutorial
   $ mkdir annotation
   $ cd ~/tutorial/annotation/
   $ mkdir prokka abricate

   # Run Prokka in your assembled genomes (FASTA format)
   $ prokka --centre strainA --compliant --locustag mystrain --prefix mygenome --outdir mydir ~/tutorial/assembly/*.fasta

   # Move your result files to the Prokka directory
   $ mv <path_results_prokka> ~/tutorial/annotation/prokka/

.. csv-table:: Parameters explanation when using Prokka
   :header: "Parameter", "Description"
   :widths: 20, 60

   "``--centre [X]``", "Sequencing centre ID (default '')"
   "``--compliant``", "Force Genbank/ENA/DDJB compliance: --addgenes --mincontiglen 200 --centre XXX (default OFF)"
   "``--locustag [X]``", "Locus tag prefix [auto] (default '')"
   "``--prefix [X]``", "Filename output prefix [auto] (default '')"
   "``--outdir [X]``", "Output folder [auto] (default '')"
   "``--isolate``", "Improves the assembly quality and running time"

.. attention::

   When running |prokka| the header ID in your ``.fasta`` file must be **less than 38 characters** to avoid conflicts with GenBank annotations. To withdraw this issue use the ``--centre [X]`` and ``--compliant`` options.

.. seealso::

   `RAST <https://rast.nmpdr.org/>`_ web tool is an excellent alternative if you want a more **detailed annotation** and **pathway analysis** of your genome that is not provided with |prokka|. However, you need to upload the assemblies one by one, and usually, it can take a **few hours** to run a genome.

**3. Additional options**

.. code-block:: bash

   # To see a full list of available options in SPAdes
   $ prokka --help


Specific annotations
####################


ABRicate
********

* If you prefer to look for specific adaptative features in your genome, you can use |abricate|.

* This tool allows the mass screening of contigs for antimicrobial resistance or virulence genes.

* One of its main assets is that it comes with important **pre-downloaded databases** such as:

  1. `NCBI <https://www.ncbi.nlm.nih.gov/bioproject/PRJNA313047>`_ - includes the AMRFinderPlus tool and resistance gene database [FELDGARDEN2019]_.
  2. `CARD <https://card.mcmaster.ca/>`_ - Comprehensive Antibiotic Resistance Database [ALCOCK2020]_.
  3. `ARG-ANNOT <http://en.mediterranee-infection.com/article.php?laref=283%26titre=arg-annot>`_ - Antibiotic Resistance Gene-ANNOTation [GUPTA2014]_.
  4. `Resfinder <https://cge.cbs.dtu.dk/services/ResFinder/>`_ - identification of acquired antimicrobial resistance genes [ZANKARI2012]_.
  5. `MEGARes <https://megares.meglab.org/>`_ - identification of antimicrobial resistance genes from metagenomic datasets [DOSTER2020]_.
  6. `EcOH <https://github.com/katholt/srst2/tree/master/data>`_ - accurate serotype of *E. coli* isolates from raw WGS data [INGLE2016]_.
  7. `PlasmidFinder <https://cge.cbs.dtu.dk/services/PlasmidFinder/>`_ - in silico detection of whole-plasmid sequence data [CARATTOLI2014]_.
  8. `Ecoli_VF <https://github.com/phac-nml/ecoli_vf>`_ - database of *E. coli* virulence factors from VFDB plus additional factors from the literature.
  9. `VFDB <http://www.mgc.ac.cn/VFs/>`_ - Virulence Factor DataBase [CHEN2016]_.

* In this section you will annotate you draft genomes in ``.fasta`` format using |abricate| and look for the presence of specific genes.


Installation
............

.. code-block:: bash

   # Activate the annotation environment
   $ conda activate annotation

   # Install ABRicate
   $ conda install abricate

   # Check ABRicate installation
   $ abricate --version


Usage
.....

**1. Input/Output files**

``Input``: It accepts any compressed or uncompressed sequence file that can be converted to ``FASTA`` format by ``any2fasta`` (e.g., GenBank, EMBL).

``Output``: A tab-separated file containing the following columns:

.. figure:: ./Images/Abricate_report.png
   :figclass: align-left

*Figure 18. Example of an ABRicate report using the ARG-ANNOT database. From left to right you can see the following columns: the filename, the sequence in the filename, start and end coordinates in the sequence, strand, gene name, what proportion of the gene is in your sequence, a visual representation of the hit, gaps in subject and query, the proportion of gene covered, the proportion of exact nucleotide matches, database name, accession number of the sequence source, and gene product (if available).*

**2. Basic commands**

.. code-block:: bash

   # General ABRicate usage
   $ abricate [options] <contigs.{fasta,gbk,embl}[.gz] ...> > out.tab

   # Run ABRicate in your assembled genomes (FASTA format)
   $ abricate --db argannot --quiet --csv ~/tutorial/assembly/*.fasta > strainA.csv

   # Move your result files to the ABRicate directory
   $ mv <path_results_abricate> ~/tutorial/annotation/abricate/

.. csv-table:: Parameters explanation when using Prokka
   :header: "Parameter", "Description"
   :widths: 20, 60

   "``--db [X]``", "Database to use (default 'ncbi')"
   "``--quiet``", "Quiet mode, no stderr output"
   "``--csv``", "Output CSV instead of TSV"

**3. Additional options**

.. code-block:: bash

   # To see a full list of available options in ABRicate
   $ abricate --help

   # Check the list of installed databases in ABRicate
   $ abricate --list

.. todo::

   1. Run |prokka| and |abricate| in your assembled draft genomes using the ``.fasta`` files.
   2. Did your isolates carry putative antimicrobial resistance or virulence genes? Which ones are present?
   3. How many coding sequences (CDS) were predicted?
   4. Visualize your genome annotations using Integrative Genomics Viewer - `IGV <http://software.broadinstitute.org/software/igv/>`_ explained in the section below.

.. seealso::

   * Although you use draft assembled genomes for this specific annotation process, it is also viable to use the initial **raw sequence reads** using for example `ARIBA <https://github.com/sanger-pathogens/ariba>`_.

   * Yet, it is essential to highlight that assembled sequences facilitate an understanding of the genetic context of the resistance mechanism by assessing, for example, gene synteny, mutations on regulatory regions or co-localization with other genes [KWONG2017]_.


Interactive visualization
#########################


IGV
***

* The Integrative Genomics Viewer - `IGV <http://software.broadinstitute.org/software/igv/>`_ is a freely-available and interactive high-performance desktop tool for visualization of diverse genomic data [THORVALDSDOTTIR2013]_.

* There are a panaply of other desktop application for visulaization of genomic data that you can also explore such as `Geneious <https://www.geneious.com/>`_, `UGENE <http://ugene.net/>`_, `Tablet <https://ics.hutton.ac.uk/tablet/>`_, or `Artemis <https://sanger-pathogens.github.io/Artemis/>`_.


Installation
............

1. Download the latest IGV with Java included for Mac, Linux or Windows using the link provided `here <http://software.broadinstitute.org/software/igv/download>`_.

2. Unzip the content on your computer.

.. figure:: ./Images/IGV_window.png
   :figclass: align-left

*Figure 19. Visualization of the main window of IGV showing data from The Cancer Genome Atlas. 1 - IGV toolbar to access commonly used features; 2 - red box indicates the portion of the chromosome that is displayed; 3 - the ruler reflects the visible part of the chromosome; 4 - data is shown in horizontal rows called tracks; 5 - gene features; 6 - track names; 7 - optional attribute panel represented as coloured blocks.*


Usage
.....

1. Open IGV in your computer.

2. Go to ``Genomes`` -> ``Load Genome from File``.

3. Choose a genome assembly to load from your computer in ``.fasta`` format.

4. To load tracks go to ``File`` -> ``Load from File``.

5. Choose the annotations files from your computer in ``.gff`` format.

6. Move your cursor to right and left to see the predicted genes.

7. Try to find the **bla** gene using the ``Go`` search box.

8. Zoom in the **bla** gene to see their sequence (DNA and protein).

9. What is the correct reading frame for this gene?

.. seealso::

   For detailed information about IGV please see the full `manual <http://software.broadinstitute.org/software/igv/UserGuide>`_.


Assembly completeness
#####################


Busco
*****

* In the previous section you performed a *de novo* assembled and evaluated its completeness and quality using |quast|. However, most of these quality metrics, although informative, can also be misleading.

* In this section you will use |busco| - Benchmarking Universal Single-Copy Orthologs - to assess the completeness of genomes, using their **gene content** as a complementary method to other technical metrics [SEPPEY2019]_.

* For this, |busco| will find in your genome assembly, **marker genes** that are conserved across a range of species; being their presence a good indication of quality.


Installation
............

.. code-block:: bash

   # Create a new environment named busco
   $ conda create -n busco python=3

   # Activate the busco environment
   $ conda activate busco

   # Install BUSCO
   $ conda install busco

   # Check BUSCO installation
   $ busco --version


Usage
.....

**1. Input/Output files**

``Input``: Accepts a genome assembly, an annotated gene set, or a transcriptome assembly.

``Output``: Several files are produced, although particular attention should be paid to ``short_summary.txt`` (a short summary of BUSCO report), ``full_table.tsv``(list of all BUSCO genes), and ``missing_buscos_list.tsv`` (list of missing BUSCO gene).

**2. Basic commands**

.. code-block:: bash

   # Let's first create new directories to store your annotations
   $ cd ~/tutorial/annotation/
   $ mkdir busco

   # Check BUSCO databases that will be used to assess orthologue presence absence the genome
   $ busco --list-datasets

   # Move the configuration file to a location with "write" privileges
   $ cp -r ~/miniconda3/envs/annotation/config/ .

   # Run BUSCO in your assembled genomes (.fasta format)
   $ busco -i ~/tutorial/assembly/*.fasta -o OUTPUT_NAME -l bacteria_odb10 -m geno --config config/config.ini

   # Or run BUSCO in you annotated genomes (.faa format)
   $ busco -i ~/tutorial/annotation/prokka/*.faa -o OUTPUT_NAME -l bacteria_odb10 -m prot --config config/config.ini

   # Move your result files to the BUSCO directory
   $ mv <path_results_busco> ~/tutorial/annotation/busco/

   # Plot the results obtained by BUSCO
   $ generate_plot -wd PATH

.. csv-table:: Parameters explanation when using BUSCO
   :header: "Parameter", "Description"
   :widths: 20, 60

   "``-i [X]``", "Input file to analyse which is either a nucleotide fasta (``.fasta``) file or a protein fasta file (``.gff``)"
   "``-o [X]``", "Name of the folder that will contain all results, logs, and intermediate data"
   "``-l [X]``", "Lineage database name that BUSCO will use to assess orthologue presence absence"
   "``-m [X]``", "Sets the assessment mode, e.g., genome, proteins, transcriptome"


**3. Additional options**

.. code-block:: bash

   # To see a full list of available options in BUSCO
   $ busco --help

.. todo::

   1. How many marker genes have BUSCO found? How many are absent?
   2. Do you think that your results are good in terms of genome annotation completeness? Why?


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
    │   ├── bandage
    │   │   ├── graphs.svg
    │   ├── quast
    │   │   ├── report.html
    ├── annotation
    │   ├── prokka
    │   │   │   ├── annotations.gff
    │   │   │   ├── annotations.gbk
    │   │   │   ├── annotations.faa
    │   ├── abricate
    │   │   │   ├── annotations.csv
    │   │   │   ├── annotations.tab
    │   ├── busco


References
##########

.. [EILBECK2005] Eilbeck K, et al. 2005. The Sequence Ontology: a tool for the unification of genome annotations. Genome Biol. 6(5):R44. `DOI: 10.1186/gb-2005-6-5-r44 <https://dx.doi.org/10.1186/gb-2005-6-5-r44>`_.
.. [SEEMANN2014] Seemann T. 2014. Prokka: rapid prokaryotic genome annotation. Bioinformatics. 30(14):2068-9. `DOI: 10.1093/bioinformatics/btu153 <https://dx.doi.org/10.1093/bioinformatics/btu153>`_.
.. [FELDGARDEN2019] Feldgarden M, et al. 2019. Validating the AMRFinder Tool and Resistance Gene Database by Using Antimicrobial Resistance Genotype-Phenotype Correlations in a Collection of Isolates. Antimicrob Agents Chemother. 63(11):e00483-19. `DOI: 10.1128/AAC.00483-19 <https://dx.doi.org/10.1128/AAC.00483-19>`_.
.. [ALCOCK2020] Alcock BP, et al. 2020. CARD 2020: antibiotic resistome surveillance with the comprehensive antibiotic resistance database. Nucleic Acids Res. 48(D1):D517–D525. `DOI: 10.1093/nar/gkz935 <https://dx.doi.org/10.1093/nar/gkz935>`_.
.. [GUPTA2014] Gupta AK, et al. 2014. ARG-ANNOT, a new bioinformatic tool to discover antibiotic resistance genes in bacterial genomes. Antimicrob Agents Chemother. 58(1):212-20. `DOI: 10.1128/AAC.01310-13 <https://dx.doi.org/10.1128/AAC.01310-13>`_.
.. [ZANKARI2012] Zankari E, et al. 2012. Identification of acquired antimicrobial resistance genes. J Antimicrob Chemother. 67(11):2640-4. `DOI: 10.1093/jac/dks261 <https://dx.doi.org/10.1093/jac/dks261>`_.
.. [DOSTER2020] Doster E, et al. 2020. MEGARes 2.0: a database for classification of antimicrobial drug, biocide and metal resistance determinants in metagenomic sequence data. Nucleic Acids Res. 48(D1):D561–D569. `DOI: 10.1093/nar/gkz1010 <https://dx.doi.org/10.1093/nar/gkz1010>`_.
.. [INGLE2016] Ingle DJ, et al. 2016. In silico serotyping of E. coli from short read data identifies limited novel O-loci but extensive diversity of O:H serotype combinations within and between pathogenic lineages. Microb Genom. 2(7):e000064. `DOI: 10.1099/mgen.0.000064 <https://dx.doi.org/10.1099/mgen.0.000064>`_.
.. [CARATTOLI2014] Carattoli A, et al. 2014. In Silico Detection and Typing of Plasmids using PlasmidFinder and Plasmid Multilocus Sequence Typing. Antimicrob Agents Chemother. 58(7):3895–3903. `DOI: 10.1128/AAC.02412-14 <https://dx.doi.org/10.1128/AAC.02412-14>`_.
.. [CHEN2016] Chen L, et al. 2016. VFDB 2016: hierarchical and refined dataset for big data analysis—10 years on. Nucleic Acids Res. 44(DI):D694–D697. `DOI: 10.1093/nar/gkv1239 <https://dx.doi.org/10.1093/nar/gkv1239>`_.
.. [KWONG2017] Kwong JC, et al. 2017. Comment on: Benchmarking of methods for identification of antimicrobial resistance genes in bacterial whole genome data. J Antimicrob Chemother. 72(2):635-636. `DOI: 10.1093/jac/dkw473 <https://dx.doi.org/10.1093/jac/dkw473>`_.
.. [THORVALDSDOTTIR2013] Thorvaldsdóttir H, Robinson JT, Mesirov JP. Integrative Genomics Viewer (IGV): high-performance genomics data visualization and exploration. Brief Bioinform. 14(2):178-92. `DOI: 10.1093/bib/bbs017 <https://dx.doi.org/10.1093/bib/bbs017>`_.
.. [SEPPEY2019] Seppey M, Manni M, Zdobnov EM. 2019. BUSCO: Assessing Genome Assembly and Annotation Completeness. In: Kollmar M. (eds) Gene Prediction. Methods in Molecular Biology, vol 1962. Humana, New York, NY. 2019. `DOI: 10.1007/978-1-4939-9173-0_14 <https://dx.doi.org/10.1007/978-1-4939-9173-0_14>`_.
