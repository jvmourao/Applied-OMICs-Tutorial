.. _ngs-annotations:

*****************
Genome annotation
*****************


Introduction
############

1. After you performed de novo assembled using raw sequence reads, it is useful to know what **relevant genomic features** are on the produced contigs.

2. Genome annotation is the process that allows us to **identify** features of interest in those contigs and to **label** them with useful information.

3. In this section, you will use |bakta| for whole-genome annotation and |mlst| for the Multilocus Sequence Typing (MLST) of the genomes. The detection of antimicrobial resistance genes and mutations, virulence genes, and plasmids will be covered in more detail in the next two sections.

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
* Interpret the annotation files and summaries.
* Determine the sequence type (ST) of a genome and interpret the allele profile.


Preparing the genomes
#####################

From now on, you will analyse **several genomes** with the same commands. For that, put all the final assemblies in the same directory, ``~/tutorial/genomes``, using the same naming convention (``<sample>.fasta``). Besides your own final assemblies (strainA and strainB), this directory already contains the public genomes that you downloaded in the :ref:`Data acquisition <ngs-data>` section (Sakai, EC958, K12 and LT2).

.. attention::
   Only copy the genomes that passed the |checkm2| thresholds (at least 90% completeness and at most 5% contamination), see the :ref:`assembly <ngs-assembly>` section.

.. code-block:: bash

   # Copy the final assemblies (Autocycler + Dnaapler + Polypolish) of your samples to the genomes directory
   while read -r sample; do
      cp ~/tutorial/assembly/final/${sample}.fasta ~/tutorial/genomes/${sample}.fasta
   done < ~/tutorial/samples.txt

   # Check all the genomes that you will analyse
   $ ls -lh ~/tutorial/genomes/
   $ grep -c '>' ~/tutorial/genomes/*.fasta

.. note::
   If you were not able to run |autocycler|, you can also use the |shovill| assemblies (``~/tutorial/assembly/shovill/<sample>_shovill.fasta``), or download the final assemblies from the :ref:`Downloads <ngs-downloads>` section. Keep in mind that the plasmids will be more fragmented in the short-read assemblies.


Whole-genome annotation
#######################


Bakta
*****

* |bakta| - is a tool for the rapid & standardised annotation of bacterial genomes and plasmids from both isolates and MAGs [SCHWENGERS2021]_.

* The annotation process of |bakta| relies on several external feature prediction tools and has many advantages:

  1. It provides a comprehensive annotation workflow including the detection of small proteins taking into account replicon metadata.

  2. The annotation of coding sequences is accelerated via an alignment-free sequence identification approach that in addition facilitates the precise assignment of public database cross-references.

  3. Annotation results are exported in GFF3 and International Nucleotide Sequence Database Collaboration (INSDC)-compliant flat files, as well as comprehensive JSON files, facilitating automated downstream analysis.

* You will use |bakta| to annotate all the genomes of the ``~/tutorial/genomes`` directory.


Installation
............

.. code-block:: bash

   # Create a new environment named bakta
   $ mamba create -n bakta

   # Activate the Bakta environment
   $ conda activate bakta

   # Install Bakta with conda
   $ mamba install bakta

   # Check Bakta installation
   $ bakta --version


Usage
.....

.. warning::

   * You will need at least 8-12 Gb of RAM to be able to run |bakta| with the full database, and ~85 Gb of free disk space (the download has ~30 Gb).

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
   $ mkdir bakta mlst
   $ cd bakta/

   # List the available versions of the Bakta database
   $ bakta_db list

   # Download the mandatory database for Bakta
   # The "light" database (~1.3 Gb download, ~4 Gb on disk) is enough for this Tutorial
   $ bakta_db download --output ~/databases/bakta --type light

   # Or download the "full" database (~30 Gb download, ~85 Gb on disk) to get the most detailed annotation
   $ bakta_db download --output ~/databases/bakta --type full

   # Run Bakta in your assembled genomes using the .fasta file
   # With the light database use ~/databases/bakta/db-light; with the full database use ~/databases/bakta/db
   $ bakta --db ~/databases/bakta/db-light --threads 4 --verbose --output ~/tutorial/annotation/bakta/strainA --prefix strainA ~/tutorial/genomes/strainA.fasta

.. warning::
   Do not delete the downloaded ``.tar.xz`` archive while ``bakta_db`` is still running; it removes it by itself at the end.

.. note::
   If Bakta stops with the error ``amrfinder error! error code: 1``, the AMRFinderPlus database included in the Bakta database is older than your AMRFinderPlus software. Update it with:
   ``amrfinder_update --force_update --database ~/databases/bakta/db-light/amrfinderplus-db``

.. csv-table:: Parameters explanation when using Bakta
   :header: "Parameter", "Description"
   :widths: 20, 60

   "``--db DB``", "Database path (default = <bakta_path>/db)"
   "``--complete``", "All the sequences are complete replicons (e.g., a complete long-read assembly); it must not be used with draft assemblies"
   "``--locus-tag TAG``", "Locus tag prefix of the annotated features (e.g., ``STRAINA``)"
   "``--force``", "Overwrite an existing output directory"
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

**3. Running Bakta in several genomes**

.. code-block:: bash

   $ cd ~/tutorial
   $ mkdir -p logs
   for genome in genomes/*.fasta; do
      sample=$(basename $genome .fasta)
      echo "Annotating ${sample}"
      bakta --db ~/databases/bakta/db-light --threads 4 \
         --output annotation/bakta/${sample} --prefix ${sample} --locus-tag ${sample} \
         $genome > logs/${sample}_bakta.log 2>&1
   done

   # Check the summary of the annotation of all the genomes (number of CDS, tRNAs, etc.)
   $ grep -H "^CDSs" annotation/bakta/*/*.txt

.. hint::
   Add ``--complete`` to the command for genomes that are closed (e.g., your final assemblies if all the replicons are circular, and the public genomes Sakai, EC958, K12 and LT2). For the draft assemblies (e.g., Shovill), do not use it.

**4. Additional options**

.. code-block:: bash

   # To see a full list of available options in Bakta
   $ bakta --help

.. todo::
   1. Run |bakta| in your final assemblies and in the public genomes using the ``.fasta`` files.
   2. How many coding sequences (CDS) were predicted in each genome? And how many tRNAs and rRNAs?
   3. Open the ``.tsv`` (or ``.gff3``) file of strainA. Which gene is at the start of the chromosome? Why? (Remember the reorientation with |dnaapler|.)

.. note::
   The number of **coding sequences (CDS)** is also a quality metric of the assembly: an assembly with too few CDS may be incomplete, and one with too many may be contaminated or have many errors (e.g., frameshifts that split the genes). Compare the number of CDS with the expected values of the species in the :ref:`Quality thresholds <quality-thresholds>` page (e.g., *E. coli*: 3,900–6,500).

   .. code-block:: bash

      # Number of CDS of each genome, and check against the FAIL range of E. coli
      $ grep -H "^CDSs" ~/tutorial/annotation/bakta/*/*.txt | awk -F'[/:]' '{n=$NF+0; print $(NF-3)"\t"n"\t"((n>=3900 && n<=6500) ? "PASS" : "FAIL")}' | column -t


Multilocus Sequence Typing
##########################


MLST
****

* **Multilocus Sequence Typing (MLST)** characterises bacterial isolates using the sequences of internal fragments of several (usually 7) **housekeeping genes**.

* Each different sequence of a gene is an **allele**, and each combination of alleles (allelic profile) is a **sequence type (ST)**. Isolates with the same ST are closely related.

* |mlst| scans the genomes against the MLST schemes of `PubMLST <https://pubmlst.org/>`_ [JOLLEY2018]_. It detects automatically which scheme to use (e.g., ``ecoli_achtman_4`` for *E. coli*, and ``senterica_achtman_2`` for *Salmonella*).

* In this Tutorial, only the alleles with **100% identity** and **100% coverage** are accepted.


Installation
............

.. code-block:: bash

   # Deactivate all the current environments
   $ conda deactivate

   # Create a new environment named mlst and install mlst
   $ mamba create -n mlst mlst

   # Activate the mlst environment and check the installation
   $ conda activate mlst
   $ mlst --version

   # See the list of available schemes
   $ mlst --list


Usage
.....

**1. Input/Output files**

``Input``: Genome assemblies in ``.fasta`` (or GenBank) format. You can provide several files at the same time.

``Output``: A tab-separated table with one line per genome: the file name, the scheme, the **ST** and the allele of each gene.

**2. Basic commands**

.. code-block:: bash

   $ cd ~/tutorial/annotation/mlst

   # Run mlst in all your genomes at the same time (100% identity and 100% coverage)
   $ mlst --minid 100 --mincov 100 --threads 4 ~/tutorial/genomes/*.fasta > mlst.tsv

   # See the results
   $ column -t mlst.tsv

   # Force the use of a specific scheme
   $ mlst --scheme ecoli_achtman_4 --minid 100 --mincov 100 ~/tutorial/genomes/strainA.fasta

.. csv-table:: Parameters explanation when using mlst
   :header: "Parameter", "Description"
   :widths: 20, 60

   "``--minid NUM``", "Minimum DNA % identity of the allele (default: 95)"
   "``--mincov NUM``", "Minimum DNA % coverage of the allele (default: 10)"
   "``--scheme NAME``", "Use only this scheme (default: automatic)"
   "``--threads NUM``", "Number of threads"
   "``--csv``", "Output in CSV format instead of tab-separated"
   "``--label NAME``", "Replace the file name by this label in the output (only for one genome)"
   "``--list``", "List the available schemes"

The symbols in the allele columns mean:

.. csv-table::
   :header: "Symbol", "Meaning"
   :widths: 20, 60

   "``n``", "Exact match to the allele number n"
   "``~n``", "Novel full-length allele, similar to allele n"
   "``n?``", "Partial match to allele n"
   "``-``", "Allele missing"
   "``n,m``", "Multiple alleles (e.g., more than one copy of the gene, or contamination)"

.. note::
   If an ST cannot be assigned (``-`` in the ST column), check the alleles: a novel or partial allele, or a missing gene, can indicate a new ST, a problem in the assembly, or contamination.

**3. Additional options**

.. code-block:: bash

   # To see a full list of available options in mlst
   $ mlst --help

.. todo::
   4. Run |mlst| in your final assemblies and in the public genomes.
   5. What is the ST of each genome? Do strainA and strainB belong to the same ST?
   6. Which genome is the *E. coli* ST131 (a pandemic multidrug-resistant clone)? Which scheme was used for LT2? Why?


Folder structure
################

At the end of this section, you will have the following folder structure.

::

    tutorial
    ├── samples.txt
    ├── public_genomes.tsv
    ├── raw_data
    │   ├── <sample>_R1.fastq.gz
    │   ├── <sample>_R2.fastq.gz
    │   ├── <sample>_nanopore.fastq.gz
    │   ├── files.fasta
    │   ├── files.gbk
    │   ├── files.gff
    ├── genomes
    │   ├── <sample>.fasta
    │   ├── Sakai.fasta
    │   ├── EC958.fasta
    │   ├── K12.fasta
    │   ├── LT2.fasta
    ├── qc_visualisation
    ├── qc_improvement
    ├── taxonomy
    ├── assembly
    │   ├── shovill
    │   ├── autocycler
    │   ├── polish
    │   ├── final
    │   ├── unicycler
    │   ├── quast
    │   ├── checkm2
    ├── annotation
    │   ├── bakta
    │   │   ├── <genome>
    │   │   │   ├── <genome>.gff3
    │   │   │   ├── <genome>.gbff
    │   │   │   ├── <genome>.txt
    │   │   │   ├── <genome>.faa
    │   │   │   ├── <genome>.ffn
    │   ├── mlst
    │   │   ├── mlst.tsv
    ├── logs


References
##########

.. [EILBECK2005] Eilbeck K, et al. 2005. The Sequence Ontology: a tool for the unification of genome annotations. Genome Biol. 6(5):R44. `DOI: 10.1186/gb-2005-6-5-r44 <https://dx.doi.org/10.1186/gb-2005-6-5-r44>`_.
.. [JOLLEY2018] Jolley KA, Bray JE, Maiden MCJ. 2018. Open-access bacterial population genomics: BIGSdb software, the PubMLST.org website and their applications. Wellcome Open Res. 3:124. `DOI: 10.12688/wellcomeopenres.14826.1 <https://dx.doi.org/10.12688/wellcomeopenres.14826.1>`_.
.. [SCHWENGERS2021] Schwengers O, et al. 2021. Bakta: rapid and standardized annotation of bacterial genomes via alignment-free sequence identification. Microbial Genomics. 7(11):000685. `DOI: 10.1099/mgen.0.000685 <https://dx.doi.org/10.1099/mgen.0.000685>`_.
