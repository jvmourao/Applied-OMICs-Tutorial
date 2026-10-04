.. _ngs-qc:

***************
Quality control
***************


Introduction
############

1. We know that none of the described sequencing technologies is perfect; thus, they will generate different **types** and **amounts** of **errors**.

2. Therefore, it is of utmost importance to **identify** the errors that may influence further data analysis and interpretation.

3. In this section, you will first learn how to visualize the quality of the data using |fastqc| and |multiqc|.

4. After that, we will **trim** and **filter** low quality or uninformative reads/bases through |bbduk|.

5. You will be working only with the paired-end raw data acquired through the **Illumina HiSeq 2500** Platform [GREIG2019]_.


Learning objectives
###################

After finishing this Tutorial section, you will be able to:

* Calculate the sequencing coverage.
* Generate a full combined quality report.
* Assess and interpret the general quality of raw reads.
* Improve the quality of raw reads by trimming, masking and filtering.


Coverage
########

1. As you already saw in the theoretical classes, a sequencing platform needs to sequence every base in a given sample several times.

2. The number of ``x`` times a genome has been sequenced (depth of sequencing) is expressed by a **coverage metric**.

3. There are no strict recommendations for ideal sequencing coverage. Most researchers determine the necessary coverage based on the type of study and available literature.

4. Ideal coverage for a genome assembly should be **50x or above** [ALBERT2019]_. It means that each base on average is sequenced 50 times.

.. hint::
   The coverage can be calculated using the following equations.

   **A. For an instrument with fixed read length:**

   ``C = LN / G``

   C: Coverage

   L: is the read length in bp (e.g., 150 bp)

   N: is the total number of sequenced reads (for paired-end data, count the reads of both files, R1 and R2)

   G: is the haploid genome length in bp

   **B. For an instrument with variable read length:**

   ``C = SUM(Li) / G``

   C: Coverage

   Li: is the length of read *i* in bp

   G: is the haploid genome length in bp

Let's try to do some basic analysis and calculate the coverage using the **paired-end Illumina raw reads** (files SRR6052929 and SRR7184397).

You can easily count the reads and the sequenced bases in the command line. Remember that each read has 4 lines in a fastq file.

.. code-block:: bash

   # Go to the raw_data directory
   $ cd ~/tutorial/raw_data

   # Display the first read (4 lines) of a compressed fastq file
   $ gunzip -c strainA_R1.fastq.gz | head -n 4

   # Count the number of reads of a sample
   $ gunzip -c strainA_R1.fastq.gz | awk 'END{print NR/4}'

   # Calculate the number of reads, bases and coverage (genome size = 5500000 bp)
   # of the forward and reverse reads together
   $ gunzip -c strainA_R1.fastq.gz strainA_R2.fastq.gz | awk -v G=5500000 'NR%4==2{n++; b+=length($0)} END{printf "reads=%d bases=%d coverage=%.1fx\n", n, b, b/G}'

Now, repeat the same calculation for **all the samples** using a loop and save the results in a table (the sample names are listed in the file ``samples.txt`` that you created in the data acquisition section):

.. code-block:: bash

   $ cd ~/tutorial
   $ echo -e "sample\treads\tbases\tcoverage" > coverage.tsv
   while read -r sample; do
      gunzip -c raw_data/${sample}_R1.fastq.gz raw_data/${sample}_R2.fastq.gz | awk -v s=$sample -v G=5500000 'NR%4==2{n++; b+=length($0)} END{printf "%s\t%d\t%d\t%.1f\n", s, n, b, b/G}' >> coverage.tsv
   done < samples.txt
   $ column -t coverage.tsv

.. todo::
   1. Open the file with the command line or with the text editor to get an idea about the structure.
   2. What is the unique identifier of each read in the fastq files? What is the read length?
   3. How many raw sequence reads are in the files?
   4. Calculate the coverage of strainA and strainB, assuming a genome size of ~5.5 Mb. Is it higher than 50x?
   5. Calculate the coverage of the Nanopore reads of both strains using the same equation and the second one (variable read length).


Visualisation of data quality
#############################

1. The first step after receiving the sequencing data is to perform some simple quality control evaluations.

2. This step will be important to ensure that your raw data looks good and there are no problems or biases.

2. For that, you’ll first use two programs called |fastqc| and |multiqc|, to visualize the quality of the raw reads.


FastQC
******

* We already saw in the :ref:`data acquisition <ngs-data>` section that to each base is assigned a |phred| quality score.

* In this section, we will see how to visualize all these scores collectively using |fastqc|.

* Also, |fastqc| will allow you to:

  1. Create user-friendly **plots** and **tables** to assess the general quality and composition of raw sequence data.
  2. Identify any **problems** originated either in the sequencer or in the starting library material.
  3. Export the results to an **HTML** based reports.

.. note::
   Don't forget that fastq errors are not entirely accurate measures, hence use them as **warnings** for further analysis.


Installation
............

.. code-block:: bash

    # Create a new conda environment named qc
    $ conda create -n qc python=3.11

    # Activate the new environment
    $ conda activate qc

    # Install FastQC as a command-line utility
    $ conda install fastqc

    # Check if FastQC is installed
    $ fastqc --version


Usage
.....

**1. Input/Output files**

``Input``: Accept compress or uncompress Illumina files such as ``.fastq`` or ``.fastq.gz``. For this part of the Tutorial, we will use the paired-end Illumina raw reads.

``Output``: Two files are produced, a ``.zip`` archive containing all the plots, and a ``.html`` report. You can open the HTML files with your web browser.

**2. Basic commands**

.. code-block:: bash

    # Let's first create three new directories to keep your reports
    $ cd ~/tutorial/
    $ mkdir qc_visualisation
    $ cd qc_visualisation/
    $ mkdir trimmed untrimmed
    $ cd

    # Run FastQC on multiple fastq.gz files at the same time
    # Specify the directory where your Illumina fastq.gz files are located
    # The wildcard *_R?.fastq.gz selects all the _R1 and _R2 files but not the Nanopore ones
    $ fastqc -t 4 ~/tutorial/raw_data/*_R?.fastq.gz -o ~/tutorial/qc_visualisation/untrimmed/

.. csv-table:: Parameters explanation when using FastQC
   :header: "Parameter", "Description"
   :widths: 20, 60

   "``-t NUM``", "Specifies the number of files which can be processed simultaneously (1 thread = 250 Mb memory)"
   "``-o NAME``", "Create all output files in the specified and already created output directory"
   "``--memory NUM``", "Sets the base amount of memory, in Megabytes, used to process each file (default: 512 Mb)"
   "``--nano``", "Files come from nanopore sequences and are in fast5 format"
   "``-q``", "Suppress all progress messages on stdout and only report errors"
   "``*_R?.fastq.gz``", "Full path to paired-end Illumina raw sequence reads (the ``?`` wildcard matches one character: 1 or 2)"

.. code-block:: bash

    # See the files that FastQC created
    $ cd ~/tutorial/qc_visualisation/untrimmed/
    $ ls

    # Open FastQC html report in Ubuntu/WSL
    $ sensible-browser <filename>_fastqc.html
    $ cd

    # Or open FastQC html report in macOS
    $ open <filename>_fastqc.html
    $ cd

**3. Additional options**

.. code-block:: bash

    # To see all the parameters available on FastQC
    $ fastqc --help

**4. Running FastQC in several samples**

FastQC accepts many files in the same command, so a loop is not mandatory. However, if you prefer to run each sample separately (e.g., to keep a log file per sample), you can use a loop:

.. code-block:: bash

   $ cd ~/tutorial
   $ mkdir -p logs
   while read -r sample; do
      fastqc -t 2 raw_data/${sample}_R1.fastq.gz raw_data/${sample}_R2.fastq.gz -o qc_visualisation/untrimmed/ &> logs/${sample}_fastqc.log
   done < samples.txt

.. hint::
   To run more than one sample **at the same time** you can use ``xargs``: ``cat samples.txt | xargs -P 2 -I {} sh -c 'fastqc -t 1 raw_data/{}_R1.fastq.gz raw_data/{}_R2.fastq.gz -o qc_visualisation/untrimmed/'``. Here ``-P 2`` means two samples in parallel. Do not use more processes than the CPUs of your computer.

.. todo::
   6. Run |fastqc| on all the downloaded paired-end Illumina raw reads and save a copy of the report in your computer.
   7. Explore the Fastqc `website <https://www.bioinformatics.babraham.ac.uk/projects/fastqc/Help/3%20Analysis%20Modules/>`_ and try to interpret your results according to the various quality modules.
      Pay special attention to the **Basic Statistics**, **Per base Sequence Quality** and **Sequence Length Distribution**.
   8. Do your sequences have any kind of adapters?
   9. Do you think these Illumina sequencing runs gave good quality sequences? Why?
   10. Based on the FastQC report, do you think your data will need further trimming and filtering? Why?

.. figure:: ./images/Fastqc_report.png
   :figclass: align-left

*Figure 9. Example of a FastQC report using paired-end Illumina raw reads on a macOS.*


MultiQC
*******

The |multiqc| tool is designed to combine different quality reports, such as the ones produced by |fastqc| into a single one, thus allowing multiple comparisons at the same time.


Installation
............

.. code-block:: bash

    # Deactivate all current environments
    $ conda deactivate

    # Create a new conda environment named multiqc
    $ conda create -n multiqc

    # Activate the multiqc environment
    $ conda activate multiqc

    # Install MultiQC with conda
    $ conda install multiqc

    # Check if MultiQC is installed
    $ multiqc --version


Usage
.....

**1. Input/Output files**

``Input``: In this tutorial you will use the ``fastqc.*`` quality visualisation reports.

``Output``: The MultiQC will generate an ``.html`` file containing the full report and a folder that contains easily machine readable data analysis.

**2. Basic commands**

.. code-block:: bash

    # Run MultiQC to combine the reports of all FastQC runs
    # Specify the directory where your FastQC reports are located (MultiQC searches it recursively)
    $ multiqc ~/tutorial/qc_visualisation/untrimmed/ -o ~/tutorial/qc_visualisation/untrimmed/

.. csv-table:: Parameters explanation when using MultiQC
   :header: "Parameter", "Description"
   :widths: 20, 60

   "``-o NAME``", "Create report in the specified and already created output directory"
   "``-q``", "Only show log warnings"
   "``<directory>``", "Full path to the directory with the FastQC quality visualisation reports"
   "``-n NAME``", "Name of the output report (e.g., ``-n multiqc_clean_report`` for the trimmed data)"
   "``-f``", "Overwrite existing reports"

.. code-block:: bash

    # Navigate to the directory containing the MultiQC .html report
    $ cd ~/tutorial/qc_visualisation/untrimmed/

    # Open MultiQC html report in Ubuntu/WSL
    $ sensible-browser multiqc_report.html
    $ cd

    # Or open MultiQC html report in macOS
    $ open multiqc_report.html
    $ cd

**3. Additional options**

.. code-block:: bash

   # To see all the parameters available on MultiQC
   $ multiqc --help

.. todo::
   11. Run |multiqc| on all the reports generated by FastQC.
   12. What are the paired-end Illumina raw reads that present the best quality? Why?

.. figure:: ./images/Multiqc_report.png
   :figclass: align-left

*Figure 10. Example of a MultiQC report using a combination of FastQC reports.*


Quality control
###############

1. In the previous section, we have **evaluated** and **visualised** the quality of our raw sequence reads using |fastqc|.

2. Now you have to decide if your data should be subject to **Quality Control (QC)**, i.e. the process of improving data by removing identifiable errors from it.

3. You must remember that by performing QC we can also introduce **errors** (we want the same data but with better quality). Thus, we should not perform QC if the quality appears to be satisfactory.

.. attention::
   Only perform QC if your data need it. Whether you should quality-trim, and what the threshold should be, depends on your **data quality** and their **intended use**. Often a threshold of **~10** is pretty good for most of the cases.


BBDuk
*****

If your data needs QC you can use |bbduk| to trim adapters and filter other low-quality data. |bbduk| can run in trimming mode or filtering mode.


Installation
............

.. note::
   |bbtools| is written in Java, but conda will install the required Java version automatically together with the package ``bbmap``. In previous versions of this Tutorial, BBTools was manually downloaded from SourceForge; this is no longer necessary.

.. code-block:: bash

    # Activate the qc environment
    $ conda activate qc

    # Install BBTools (BBMap package) through conda
    $ conda install bbmap

    # Let's also create a new directory to keep the clean raw sequence reads
    $ mkdir ~/tutorial/qc_improvement

    # To test the installation, run stats.sh against the PhiX reference genome that is included in BBTools
    # At the end you should see some statistics in your shell
    $ stats.sh in=$(ls $CONDA_PREFIX/opt/bbmap-*/resources/phix174_ill.ref.fa.gz)


Usage
.....

**1. Input/Output files**

``Input``: You will use the Illumina raw sequence data contained in the ``.fastq.gz`` files.

``Output``: BBDuk will generate ``.fastq`` files containing your sequence data trimmed and filtered according to the input parameters.

**2. Basic commands**

.. note::

   * When you have the **paired-end reads** in 2 files you should **always processed them together**, not one at a time.

   * In the commands provided below don't forget to add the full path of your ``fastq.gz`` files.

   * With the conda installation, the BBTools scripts are available directly in the command line (e.g., ``bbduk.sh``), without any path.

.. code-block:: bash

    # Go to the directory where you want to keep the trimmed data
    $ cd ~/tutorial/qc_improvement/

    # Trim adapters when present in the raw sequence reads
    # ref=adapters uses the file with all the adapters (adapters.fa) that is included in BBTools
    $ bbduk.sh -Xmx1g in1=read1.fastq.gz in2=read2.fastq.gz out1=clean1.fastq.gz out2=clean2.fastq.gz ref=adapters ktrim=r k=23 mink=11 hdist=1 tpe tbo

    # Trim regions with an average quality below 10 in both ends of the reads
    $ bbduk.sh -Xmx1g in1=read1.fastq.gz in2=read2.fastq.gz out1=clean1.fastq.gz out2=clean2.fastq.gz qtrim=rl trimq=10

    # Discard raw sequence reads with average quality below 10
    $ bbduk.sh -Xmx1g in1=read1.fastq.gz in2=read2.fastq.gz out1=clean1.fastq.gz out2=clean2.fastq.gz maq=10

    # Trim regions with an average quality below 10 and discard reads with average quality below 5 after trimming
    # (trimq only works if you also say which side of the reads must be trimmed, using qtrim)
    $ bbduk.sh -Xmx1g in1=read1.fastq.gz in2=read2.fastq.gz out1=clean1.fastq.gz out2=clean2.fastq.gz qtrim=rl trimq=10 maq=5

    # Optionally you can also evaluate all raw reads length and display basic statistics
    $ readlength.sh in=reads.fastq.gz out=histogram.txt

.. csv-table:: Parameters explanation when using BBDuk
   :header: "Parameter", "Description"
   :widths: 20, 60

   "``hdist``", "Hamming distance (e.g., hdist=1, this allows one mismatch)"
   "``ktrim=r``", "Once a reference kmer is matched in a read, that kmer and all the bases to the right will be trimmed (3' adapters)"
   "``ktrim=l``", "Once a reference kmer is matched in a read, that kmer and all the bases to the left will be trimmed (5' adapters)"
   "``ktrim=N``", "Rather than trimming, it masks all bases covered by reference kmers to *N*"
   "``k``", "Kmer size to use. It can have a length between 1-31. Usually the longer a kmer, the greater the specificity"
   "``maq``", "Discard reads with average quality below a specified value (e.g., maq=10, means average quality BELOW 10)"
   "``mink``", "Allows to use shorter kmers at the ends of the read (e.g., k=11 for the last 11 bases)"
   "``out``", "Catch reads that don't match a reference kmers (the cleaned reads); ``out1``/``out2`` for paired-end reads"
   "``outm``", "Catch reads that match a reference kmers"
   "``qtrim=rl``", "It will trim the left and right sides"
   "``qtrim=l``", "It will trim the left side"
   "``qtrim=r``", "It will trim the right side"
   "``ref=file.fa``", "Fasta file containing adapters sequence or other contamination"
   "``stats``", "Produce a report with the contaminant sequences and how many reads of them were seen"
   "``tbo``", "Also trim adapters based on pair overlap detection using BBMerge"
   "``tpe``", "Trim both reads to the same length"
   "``trimq``", "Quality-trim using the Phred algorithm (e.g., trimq=10, it will trim regions with an average quality BELOW 10). Requires ``qtrim``"
   "``-Xmx1g``", "It forces BBDuk to use 1 GB of memory (use more for large files)"
   "``in1/in2``", "Input forward and reverse reads. For interleaved or single-end reads use ``in=``"
   "``minlength=50``", "Reads shorter than this after trimming will be discarded (default: 10)"
   "``stats=FILE``", "Write a report of the contaminants/adapters found to this file"


**3. Running BBDuk in several samples**

In practice, you need to run BBDuk in all the samples of your project with the **same parameters**. Use a loop with the sample names (``samples.txt``) and keep one log file per sample:

.. code-block:: bash

   $ cd ~/tutorial
   $ mkdir -p logs
   while read -r sample; do
      echo "Trimming ${sample}"
      bbduk.sh -Xmx2g \
         in1=raw_data/${sample}_R1.fastq.gz in2=raw_data/${sample}_R2.fastq.gz \
         out1=qc_improvement/${sample}_clean_R1.fastq.gz out2=qc_improvement/${sample}_clean_R2.fastq.gz \
         ref=adapters ktrim=r k=23 mink=11 hdist=1 tpe tbo \
         qtrim=rl trimq=10 minlength=50 \
         stats=qc_improvement/${sample}_bbduk_stats.txt 2> logs/${sample}_bbduk.log
   done < samples.txt

   # Check how many reads were kept in each sample
   $ grep -H "Result:" logs/*_bbduk.log

.. note::
   Compare the number of reads before and after the trimming. If more than ~10% of the reads were removed, check your quality reports, since something may be wrong with your data.

**4. Additional options**

.. code-block:: bash

   # To see all the parameters available on BBDuk
   $ bbduk.sh --help

.. todo::
   13. Run |bbduk| on all the downloaded raw paired-end Illumina reads if needed.
   14. Run |fastqc| in the trimmed files, saving the reports in ``~/tutorial/qc_visualisation/trimmed``.
   15. Aggregate all the reports of trimmed and untrimmed files with |multiqc|.
   16. Did you notice any kind of improvement in quality after the trimming and filtering process? Which parameters are now better?
   17. Compare the number of reads and the coverage before and after trimming.

.. hint::
   If you want to use less disk space in your computer, you can compress all the previous ``.fastq`` files by using the ``gzip`` command (BBDuk can already write compressed ``.fastq.gz`` files if the output name ends with ``.gz``).

.. seealso::
   `fastp <https://github.com/OpenGene/fastp>`_ is a fast all-in-one alternative to perform adapter trimming, quality filtering and reporting in a single command (e.g., ``fastp -i R1.fastq.gz -I R2.fastq.gz -o clean_R1.fastq.gz -O clean_R2.fastq.gz --detect_adapter_for_pe``).

Folder structure
################

At the end of this section, you will have the following folder structure.

::

    tutorial
    ├── raw_data
    │   ├── <sample>_R1.fastq.gz
    │   ├── <sample>_R2.fastq.gz
    │   ├── <sample>_nanopore.fastq.gz
    │   ├── files.fasta
    │   ├── files.gff
    │   ├── files.gbk
    ├── genomes
    ├── qc_visualisation
    │   ├── trimmed
    │   │   ├── <sample>_clean_R1_fastqc.html
    │   │   ├── <sample>_clean_R1_fastqc.zip
    │   │   ├── multiqc_clean_report.html
    │   │   ├── multiqc_clean_data
    │   ├── untrimmed
    │   │   ├── <sample>_R1_fastqc.html
    │   │   ├── <sample>_R1_fastqc.zip
    │   │   ├── multiqc_report.html
    │   │   ├── multiqc_data
    ├── qc_improvement
    │   ├── <sample>_clean_R1.fastq.gz
    │   ├── <sample>_clean_R2.fastq.gz
    │   ├── <sample>_bbduk_stats.txt
    ├── logs


References
##########

.. [ALBERT2019] Albert I. 2019. The Biostar Handbook. 2nd Edition. `<https://www.biostarhandbook.com/>`_


List of QC tools
################

.. seealso::

   * The tools used in this Tutorial section are not the only ones available for the purpose of quality control.

   * Other tools can also be used to perform this task (**some examples are provided in table below**).

.. csv-table::
   Table with other available Software installed by conda.
   :header: "Package name", "Version", "Main objective"
   :widths: 20, 20, 40

   "`BBTools <https://jgi.doe.gov/data-and-tools/software-tools/bbtools/>`_", "40.02", "Quality control tools (contains BBMap, BBDuk)"
   "`Cutadapt <https://cutadapt.readthedocs.io/en/stable/>`_", "5.2", "Quality control tool"
   "`FastQC <https://www.bioinformatics.babraham.ac.uk/projects/fastqc/>`_", "0.13.0", "Quality control visualisation"
   "`MultiQC <https://multiqc.info/>`_", "1.35", "Quality control visualisation"
   "`fastp <https://github.com/OpenGene/fastp>`_", "1.3.7", "Quality control visualisation and improvement (all-in-one)"
   "`PRINSEQ <http://prinseq.sourceforge.net>`_", "0.20.4", "Quality control visualisation and improvement"
   "`Trimmomatic <http://www.usadellab.org/cms/?page=trimmomatic>`_", "0.36", "Quality control tool"
   "`Trim Galore <http://www.bioinformatics.babraham.ac.uk/projects/trim_galore/>`_", "0.6.2", "Quality control tool"
   "`NanoPlot <https://github.com/wdecoster/NanoPlot>`_", "1.20.0", "Quality control visualisation for Oxford Nanopore reads"
   "`Porechop <https://github.com/rrwick/Porechop>`_", "0.2.4", "Quality control improvement for Oxford Nanopore reads"
   "`Nanofilt <https://github.com/wdecoster/nanofilt>`_", "2.3.0", "Quality control visualisation and improvement for Oxford Nanopore reads"
