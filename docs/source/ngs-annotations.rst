.. _ngs-annotations:

*****************
Genome annotation
*****************


Introduction
############

1. After you performed de novo assembled using raw sequence reads, it is useful to know what **relevant genomic features** are on the produced contigs.

2. Genome annotation is the process that allows us to **identify** features of interest in those contigs and to **label** them with useful information.

3. In this section, you will use |bakta| for whole-genome annotation, |abricate| for a more specific one and `IGV <http://software.broadinstitute.org/software/igv/>`_ for its interactive visualisation. In the end, you will evaluate assembly completeness using |busco|.

4. When it comes to annotation process there are two key concepts, **Sequence Ontology** and **Gene Ontology**, that you should understand before you move forward.


Sequence Ontology (SO)
**********************

* SO is a **structured controlled vocabulary** of terms and the relationships between them useful to describe features of a genomic annotation [EILBECK2005]_.

* This vocabulary definition is vital for the exchange, analysis and management of genomic data.

* If you open a **GenBank annotation file**, you will see several demonstrations of SO terms (e.g., the term `CDS <http://sequenceontology.org/browser/current_svn/term/SO:0000316>`_ is defined as a contiguous sequence which begins with, and includes, a start codon and ends with, and includes a stop codon).

.. seealso::
   To understand the **definition of all SO terms** available you can go to the `Sequence Ontology Browser <http://www.sequenceontology.org/browser/obob.cgi>`_ and search for each one.


Gene Ontology (GO)
******************

* |go| is a controlled vocabulary that correlates each gene to one or more functions [ALBERT2019]_.

* The |go| structure can be represented as a graph where nodes are the GO terms, and the edges are the associations between these terms.

* Each child node is more “specific” than its parent, and function is “inherited” down the line.

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
* Evaluate the presence of specific genes conferring adaptive features.
* Evaluate assembly completeness through the search of orthologues presence or absence.
* Use specific software to visualise and edit genome annotations.


Whole-genome annotation
#######################


Bakta
*****

* |bakta| - is a tool for the rapid & standardised annotation of bacterial genomes and plasmids from both isolates and MAGs [SCHWENGERS2021]_.

* The annotation process of |bakta| relies on several external feature prediction tools and has many advantages:

  1. It provides a comprehensive annotation workflow including the detection of small proteins taking into account replicon metadata.

  2. The annotation of coding sequences is accelerated via an alignment-free sequence identification approach that in addition facilitates the precise assignment of public database cross-references.

  3. Annotation results are exported in GFF3 and International Nucleotide Sequence Database Collaboration (INSDC)-compliant flat files, as well as comprehensive JSON files, facilitating automated downstream analysis.

* You will use |bakta| to annotate all your bacterial assemblies from |spades| and |unicycler|.


Installation
............

.. code-block:: bash

   # Create a new environment named Bakta
   $ conda create -n bakta python=3.8

   # Activate the Bakta environment
   $ conda activate bakta

   # Install Bakta with conda
   $ conda install -c conda-forge -c bioconda bakta

   # Check Bakta installation
   $ bakta --version


Usage
.....

.. warning::

   * You will need at least 8-12 Gb of RAM to be able to run |bakta|.

   * If you are unable to run |bakta| please download the final hybrid annotations using this `link <https://mega.nz/folder/4uZymaKb#xL9gxvv7gDFqMXMTu5J63g>`_.

**1. Input/Output files**

``Input``: Bacterial genomes and plasmids (complete/draft assemblies) in (zipped) ``.fasta`` format.

``Output``: Annotation results are provided in standard bioinformatics file formats. A particular attention should be given to ``.gff3`` and ``.gbff`` (information about the annotated features), ``.txt`` (summary of annotated features), ``.faa`` (protein sequences of annotated genes), and ``.ffn`` (nucleotide sequences of annotated genes).

**2. Basic commands**

.. code-block:: bash

   # Let's first create new directories to store your annotations
   $ cd ~/tutorial
   $ mkdir annotation
   $ cd ~/tutorial/annotation/
   $ mkdir bakta abricate
   $ cd bakta/

   # Download the mandatory database for Bakta (~30 Gb)
   $ bakta_db list
   $ bakta_db download --output ~/tutorial/annotation/bakta

   # Run Bakta in your assembled genomes using the .fasta file
   $ bakta --db ~/tutorial/annotation/bakta/db --verbose --output ~/tutorial/annotation/bakta/strainX --prefix strainX ~/tutorial/assembly/unicycler/<genome>.fasta

.. csv-table:: Parameters explanation when using Bakta
   :header: "Parameter", "Description"
   :widths: 20, 60

   "``--db DB``", "Database path (default = <bakta_path>/db)"
   "``--verbose``", "Print verbose information"
   "``--output OUTPUT``", "Output directory (default = current working directory)"
   "``--prefix PREFIX``", "Prefix for output files"
   "``--threads THREADS``", "Number of threads to use (default = number of available CPUs)"
   "``<genome>``", "Genome sequences in (zipped) fasta format"
   "``--genus GENUS``", "Genus name"
   "``--species SPECIES``", "Species name"
   "``--strain STRAIN``", "Strain name"
   "``--plasmid PLASMID``", "Plasmid name"
   "``--compliant``", "Force Genbank/ENA/DDJB compliance"

.. seealso::

   * `RAST <https://rast.nmpdr.org/>`_ web tool is an excellent alternative if you want a more **detailed annotation** and **pathway analysis** of your genome that is not provided with other tools.

   * However, you need to upload the assemblies one by one, and usually, it can take **several minutes** to run a genome.

**3. Additional options**

.. code-block:: bash

   # To see a full list of available options in Bakta
   $ bakta --help


Specific annotations
####################


ABRicate
********

* If you prefer to look for genes encoding for specific adaptive features in your genome, you can use |abricate|.

* This tool allows the mass screening of contigs for antimicrobial resistance or virulence genes.

* One of its main assets is that it comes with important **pre-downloaded databases** such as:

  1. `NCBI <https://www.ncbi.nlm.nih.gov/bioproject/PRJNA313047>`_ - includes the AMRFinderPlus tool and resistance gene database [FELDGARDEN2019]_.
  2. `CARD <https://card.mcmaster.ca/>`_ - Comprehensive Antibiotic Resistance Database [ALCOCK2020]_.
  3. `ARG-ANNOT <http://en.mediterranee-infection.com/article.php?laref=283%26titre=arg-annot>`_ - Antibiotic Resistance Gene-ANNOTation [GUPTA2014]_.
  4. `Resfinder <https://cge.cbs.dtu.dk/services/ResFinder/>`_ - identification of acquired antimicrobial resistance genes [ZANKARI2012]_.
  5. `MEGARes <https://megares.meglab.org/>`_ - identification of antimicrobial resistance genes from metagenomic datasets [DOSTER2020]_.
  6. `EcOH <https://github.com/katholt/srst2/tree/master/data>`_ - accurate serotype of *E. coli* isolates from raw WGS data [INGLE2016]_.
  7. `PlasmidFinder <https://cge.cbs.dtu.dk/services/PlasmidFinder/>`_ - *in-silico* detection of whole-plasmid sequence data [CARATTOLI2014]_.
  8. `Ecoli_VF <https://github.com/phac-nml/ecoli_vf>`_ - database of *E. coli* virulence factors from VFDB plus additional factors from the literature.
  9. `VFDB <http://www.mgc.ac.cn/VFs/>`_ - Virulence Factor DataBase [CHEN2016]_.

* In this section you will annotate you draft genomes in ``.fasta`` format using |abricate| and look for the presence of specific genes.


Installation
............

.. code-block:: bash

   # Create the abricate environment and install ABRicate
   $ conda create -n abricate -c conda-forge -c bioconda -c defaults abricate

   # Activate the abricate environment
   $ conda activate abricate

   # Check ABRicate installation
   $ abricate --version
   $ abricate --check

   # See the list of installed databases in ABRicate
   $ abricate --list

Usage
.....

**1. Input/Output files**

``Input``: It accepts any compressed or uncompressed sequence file that can be converted to ``FASTA`` format by ``any2fasta`` (e.g., GenBank, EMBL).

``Output``: A tab-separated file containing the following columns:

.. figure:: ./images/Abricate_report.png
   :figclass: align-left

*Figure 18. Example of an ABRicate report using the ARG-ANNOT database. From left to right you can see the following columns: the filename, the sequence in the filename, start and end coordinates in the sequence, strand, gene name, what proportion of the gene is in your sequence, a visual representation of the hit, gaps in subject and query, the proportion of gene covered, the proportion of exact nucleotide matches, database name, accession number of the sequence source, and gene product (if available).*

**2. Basic commands**

.. code-block:: bash

   # Let's first go to the directory where we want to store ABRicate results
   $ cd ~/tutorial/annotation/abricate/

   # Run ABRicate database ResFinder in your assembled genomes (FASTA format)
   $ abricate --db resfinder --quiet ~/tutorial/assembly/*.fasta > resfinder_ann.tab

   # Run ABRicate database PlasmidFinder in your assembled genomes (FASTA format)
   $ abricate --db plasmidfinder --quiet ~/tutorial/assembly/*.fasta > plasmidfinder_ann.tab

   # Run ABRicate database Ecoli_VF in your assembled genomes (FASTA format)
   $ abricate --db ecoli_vf --quiet ~/tutorial/assembly/*.fasta > ecoli_vf_ann.tab

   # Run ABRicate database EcOH in your assembled genomes (FASTA format)
   $ abricate --db ecoh --quiet ~/tutorial/assembly/*.fasta > ecoh_ann.tab

   # Generate a summary report for each analysis
   $ abricate --summary resfinder_ann.tab > resfinder_ann_summary.tab
   $ abricate --summary plasmidfinder_ann.tab > plasmidfinder_ann_summary.tab
   $ abricate --summary ecoli_vf_ann.tab > ecoli_vf_summary.tab
   $ abricate --summary ecoh_ann.tab > ecoh_summary.tab

.. csv-table:: Parameters explanation when using ABRicate
   :header: "Parameter", "Description"
   :widths: 20, 60

   "``--db [X]``", "Database to use (default 'ncbi')"
   "``--quiet``", "Quiet mode, no stderr output"
   "``abricate-get_db --db NAME``", "Re-use existing download and just regenerate the database"
   "``abricate-get_db --db NAME --force``", "Force download of latest version"

**3. Additional options**

.. code-block:: bash

   # To see a full list of available options in ABRicate
   $ abricate --help

.. todo::
   1. Run |bakta| and |abricate| in your hybrid assembled draft genomes using the ``.fasta`` files.
   2. Did your isolates carry putative antimicrobial resistance or virulence genes? Which ones are present?
   3. How many coding sequences (CDS) were predicted?

.. seealso::
   * Although you use draft assembled genomes for this specific annotation process, it is also viable to use the initial **raw sequence reads** using for example `ARIBA <https://github.com/sanger-pathogens/ariba>`_.

   * Yet, it is essential to highlight that assembled sequences facilitate an understanding of the genetic context of the resistance mechanism by assessing, for example, gene synteny, mutations on regulatory regions or co-localisation with other genes [KWONG2017]_.


Interactive visualisation
#########################


IGV
***

* The Integrative Genomics Viewer - `IGV <http://software.broadinstitute.org/software/igv/>`_ is a freely-available and interactive high-performance desktop tool for visualisation of diverse genomic data [THORVALDSDOTTIR2013]_.

* In this section we will use IGV to explore our previous genome annotations.

* There are a panoply of other desktop applications for visualisation of genomic data that you can also explore such as `Geneious <https://www.geneious.com/>`_, `UGENE <http://ugene.net/>`_, `Tablet <https://ics.hutton.ac.uk/tablet/>`_, or `Artemis <https://sanger-pathogens.github.io/Artemis/>`_.


Installation
............

1. Download the latest IGV with Java included for Mac, Linux or Windows using the link provided `here <http://software.broadinstitute.org/software/igv/download>`_.

2. Unzip the content on your computer.

.. figure:: ./images/IGV_window.png
   :figclass: align-left

*Figure 19. Visualisation of the main window of IGV showing data from The Cancer Genome Atlas. 1 - IGV toolbar to access commonly used features; 2 - red box indicates the portion of the chromosome that is displayed; 3 - the ruler reflects the visible part of the chromosome; 4 - data is shown in horizontal rows called tracks; 5 - gene features; 6 - track names; 7 - optional attribute panel represented as coloured blocks.*


Usage
.....

1. Open IGV in your computer by running ``igv.sh`` (Linux and macOS) or ``igv-launcher.bat`` (Windows).

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

.. todo::
   4. Visualize your genome annotations using Integrative Genomics Viewer - `IGV <http://software.broadinstitute.org/software/igv/>`_ explained in the section below. Try to identify the *mdf(A)* gene.


Assembly completeness
#####################


Busco
*****

* In the previous section you performed a *de novo* assembled and evaluated its quality using |quast|. However, most of these quality metrics, although informative, can also be misleading.

* In this section you will use |busco| - Benchmarking Universal Single-Copy Orthologs - to assess the completeness of genomes, using their **gene content** as a complementary method to other technical metrics [SEPPEY2019]_.

* For this, |busco| will find in your genome assembly, **marker genes** that are conserved across a range of species; being their presence a good indication of quality.


Installation
............

.. code-block:: bash

   # Create a new environment and install busco at the same time 
   $ conda create -n busco -c conda-forge -c bioconda busco=5.4.4

   # Activate the busco environment
   $ conda activate busco

   # Check BUSCO installation
   $ busco --version

   # See a list of all available datasets in BUSCO
   $ busco --list-datasets # When running an analysis BUSCO will download the dataset

   # Place the configuration file BUSCO in a location where you have “write” privileges
   $ cp -r ~/miniconda3/envs/busco/config/ .


Usage
.....

**1. Input/Output files**

``Input``: Accepts a genome assembly, an annotated gene set, or a transcriptome assembly.

``Output``: Several files are produced, although particular attention should be paid to ``short_summary.txt`` (a short summary of BUSCO report), ``full_table.tsv`` (list of all BUSCO genes), and ``missing_buscos_list.tsv`` (list of missing BUSCO genes).

**2. Basic commands**

.. code-block:: bash

   # Let's first create new directories to store your annotations
   $ cd ~/tutorial/annotation/
   $ mkdir busco
   $ cd busco/

   # Run BUSCO in your assembled genomes (.fasta format)
   $ busco -i ~/tutorial/assembly/*.fasta -o OUTPUT_NAME -l bacteria_odb10 -m geno

   # Or run BUSCO in your annotated genomes (.faa format)
   $ busco -i ~/tutorial/annotation/bakta/*.faa -o OUTPUT_NAME -l bacteria_odb10 -m prot

   # Plot the results obtained by BUSCO
   $ ~/miniconda3/env/busco/bin/generate_plot.py -wd <path_results_busco>

   # Open BUSCO .png image in Ubuntu/WSL
   $ sensible-browser busco_figure.png
   $ cd

   # Or open BUSCO .png image in macOS
   $ open busco_figure.png
   $ cd

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
   5. Run |busco| in the hybrid assemblies from Unicycler.
   6. How many marker genes have BUSCO found? How many are absent?
   7. Do you think that your results are good in terms of genome annotation completeness? Why?


Folder structure
################

At the end of this section, you will have the following folder structure.

::

    tutorial
    ├── raw_data
    │   ├── files_fastq.gz
    │   ├── files.fasta
    │   ├── files.gbk
    │   ├── files.gff
    ├── qc_visualisation
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
    │   │   ├── assembly_unicycler.gfa
    │   │   ├── assembly_unicycler.log
    │   ├── bandage
    │   │   ├── graphs.png
    │   ├── quast
    │   │   ├── report_without_reference.html
    │   │   ├── report_with_reference.html
    ├── annotation
    │   ├── bakta
    │   │   │   ├── annotations.gff3
    │   │   │   ├── annotations.gbff
    │   │   │   ├── annotations.txt
    │   │   │   ├── annotations.faa
    │   │   │   ├── annotations.ffn
    │   ├── abricate
    │   │   │   ├── annotations.csv
    │   │   │   ├── annotations.tab
    │   ├── busco


References
##########

.. [ALCOCK2020] Alcock BP, et al. 2020. CARD 2020: antibiotic resistome surveillance with the comprehensive antibiotic resistance database. Nucleic Acids Res. 48(D1):D517–D525. `DOI: 10.1093/nar/gkz935 <https://dx.doi.org/10.1093/nar/gkz935>`_.
.. [CARATTOLI2014] Carattoli A, et al. 2014. In Silico Detection and Typing of Plasmids using PlasmidFinder and Plasmid Multilocus Sequence Typing. Antimicrob Agents Chemother. 58(7):3895–3903. `DOI: 10.1128/AAC.02412-14 <https://dx.doi.org/10.1128/AAC.02412-14>`_.
.. [CHEN2016] Chen L, et al. 2016. VFDB 2016: hierarchical and refined dataset for big data analysis—10 years on. Nucleic Acids Res. 44(DI):D694–D697. `DOI: 10.1093/nar/gkv1239 <https://dx.doi.org/10.1093/nar/gkv1239>`_.
.. [DOSTER2020] Doster E, et al. 2020. MEGARes 2.0: a database for classification of antimicrobial drug, biocide and metal resistance determinants in metagenomic sequence data. Nucleic Acids Res. 48(D1):D561–D569. `DOI: 10.1093/nar/gkz1010 <https://dx.doi.org/10.1093/nar/gkz1010>`_.
.. [EILBECK2005] Eilbeck K, et al. 2005. The Sequence Ontology: a tool for the unification of genome annotations. Genome Biol. 6(5):R44. `DOI: 10.1186/gb-2005-6-5-r44 <https://dx.doi.org/10.1186/gb-2005-6-5-r44>`_.
.. [FELDGARDEN2019] Feldgarden M, et al. 2019. Validating the AMRFinder Tool and Resistance Gene Database by Using Antimicrobial Resistance Genotype-Phenotype Correlations in a Collection of Isolates. Antimicrob Agents Chemother. 63(11):e00483-19. `DOI: 10.1128/AAC.00483-19 <https://dx.doi.org/10.1128/AAC.00483-19>`_.
.. [GUPTA2014] Gupta AK, et al. 2014. ARG-ANNOT, a new bioinformatic tool to discover antibiotic resistance genes in bacterial genomes. Antimicrob Agents Chemother. 58(1):212-20. `DOI: 10.1128/AAC.01310-13 <https://dx.doi.org/10.1128/AAC.01310-13>`_.
.. [INGLE2016] Ingle DJ, et al. 2016. In silico serotyping of E. coli from short read data identifies limited novel O-loci but extensive diversity of O:H serotype combinations within and between pathogenic lineages. Microb Genom. 2(7):e000064. `DOI: 10.1099/mgen.0.000064 <https://dx.doi.org/10.1099/mgen.0.000064>`_.
.. [KWONG2017] Kwong JC, et al. 2017. Comment on: Benchmarking of methods for identification of antimicrobial resistance genes in bacterial whole genome data. J Antimicrob Chemother. 72(2):635-636. `DOI: 10.1093/jac/dkw473 <https://dx.doi.org/10.1093/jac/dkw473>`_.
.. [SCHWENGERS2021] Schwengers O, et al. 2021. Bakta: rapid and standardized annotation of bacterial genomes via alignment-free sequence identification. Microbial Genomics. 7(11):000685. `DOI: 10.1099/mgen.0.000685 <https://dx.doi.org/10.1099/mgen.0.000685>`_.
.. [SEPPEY2019] Seppey M, Manni M, Zdobnov EM. 2019. BUSCO: Assessing Genome Assembly and Annotation Completeness. In: Kollmar M. (eds) Gene Prediction. Methods in Molecular Biology, vol 1962. Humana, New York, NY. 2019. `DOI: 10.1007/978-1-4939-9173-0_14 <https://dx.doi.org/10.1007/978-1-4939-9173-0_14>`_.
.. [THORVALDSDOTTIR2013] Thorvaldsdóttir H, Robinson JT, Mesirov JP. Integrative Genomics Viewer (IGV): high-performance genomics data visualization and exploration. Brief Bioinform. 14(2):178-92. `DOI: 10.1093/bib/bbs017 <https://dx.doi.org/10.1093/bib/bbs017>`_.
.. [ZANKARI2012] Zankari E, et al. 2012. Identification of acquired antimicrobial resistance genes. J Antimicrob Chemother. 67(11):2640-4. `DOI: 10.1093/jac/dks261 <https://dx.doi.org/10.1093/jac/dks261>`_.
