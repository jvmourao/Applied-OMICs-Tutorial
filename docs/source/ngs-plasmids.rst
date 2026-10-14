.. _ngs-plasmids:

************************************
Plasmid detection and reconstruction
************************************


Introduction
############

1. **Plasmids** are extrachromosomal DNA molecules that replicate independently of the chromosome. They are the main vehicles of horizontal gene transfer in bacteria and, very often, they carry antimicrobial resistance, virulence, and metal/biocide resistance genes.

2. Plasmids are usually classified by:

   * **Replicon type / incompatibility group (Inc)**: based on the replication initiation genes (*rep*), e.g., IncF, IncI, IncX, IncHI. Plasmids with the same replicon cannot be stably maintained in the same cell.
   * **Mobility**: **conjugative** plasmids encode all the machinery for self-transfer (a relaxase, MOB, and the mating pair formation system, MPF), **mobilizable** plasmids only encode a relaxase (or an *oriT*) and need the machinery of another plasmid, and **non-mobilizable** plasmids cannot be transferred by conjugation.

3. In this section, you will learn two different tasks:

   * **Plasmid detection**: identify which plasmid replicons are present in a genome using |plasmidfinder| [CARATTOLI2014]_.
   * **Plasmid typing and reconstruction**: type the plasmids of complete genomes (MOB-typer), and identify which contigs of a draft assembly belong to plasmids and group them into individual plasmids (MOB-recon), using |mobsuite| [ROBERTSON2018]_. You will also classify the contigs of a short-read assembly graph as plasmid or chromosome using |plasgraph2| [SIELEMANN2023]_.

4. Finally, you will connect the plasmids with the resistance genes that you found in the previous section.

.. attention::
   * The presence of a **replicon** does not mean that the complete plasmid is present or that you know its sequence. A plasmid can have more than one replicon (e.g., IncFIA + IncFII), and different plasmids can share the same replicon.
   * Plasmids are rich in **repeated sequences** (e.g., insertion sequences, transposons, integrons) and they also share regions with the chromosome and with other plasmids. Because of that, plasmids are frequently **fragmented in several contigs** in short-read assemblies. Complete plasmids are best obtained with **long reads** (e.g., the final assemblies that you obtained with |autocycler|).


Learning objectives
###################

After finishing this Tutorial section, you will be able to:

* Detect plasmid replicons in assembled genomes using PlasmidFinder.
* Type the plasmids of complete genomes (MOB-typer) and reconstruct the plasmids of draft assemblies (MOB-recon).
* Classify the contigs of a short-read assembly graph as plasmid or chromosome using plASgraph2.
* Identify the plasmids of a complete genome.
* Run all the analyses in several genomes and combine the results.
* Determine if a resistance gene is located in the chromosome or in a plasmid.


Plasmid detection
#################


PlasmidFinder
*************

* |plasmidfinder| identifies and types **plasmid replicons** in whole-genome sequences by comparing them with a curated database of replicon sequences (e.g., *Enterobacterales* replicons such as IncF, IncI, IncX, and Gram-positive replicons such as *rep* families) [CARATTOLI2014]_.

* It reports the **replicon name**, the **percentage of identity** and the **coverage** of the hit, and the contig where it was found.

* Besides the replicon database of *Enterobacterales* (``enterobacteriales``), it also has databases for Gram-positive bacteria (e.g., ``Rep1``, ``Rep2``, ``RepA_N``, ``Inc18``).

* The online version can be used at the `CGE website <https://cge.food.dtu.dk/services/PlasmidFinder/>`_. For many genomes it is better to use the command line.


Installation
............

.. code-block:: bash

   # Deactivate all the current environments
   $ conda deactivate

   # Create a new environment named plasmidfinder
   # BLAST and KMA are installed automatically as dependencies
   $ mamba create -n plasmidfinder plasmidfinder

   # Activate the new environment
   $ conda activate plasmidfinder

   # Check the installation
   $ plasmidfinder.py --version

The conda package already includes a copy of the database, but it may not be the most recent one. It is better to download the latest version from the CGE repository using ``git`` and index it with KMA.

.. code-block:: bash

   # Create a directory to keep the databases and go to it
   $ mkdir -p ~/databases/cge
   $ cd ~/databases/cge

   # Download the database
   $ git clone https://bitbucket.org/genomicepidemiology/plasmidfinder_db.git

   # Index the database with KMA (run INSTALL.py without any argument)
   $ cd plasmidfinder_db
   $ python INSTALL.py

   # Check the version of the database
   $ cat VERSION

.. note::
   To **update** the database in the future, go to the directory ``~/databases/cge/plasmidfinder_db``, run ``git pull`` and run ``python INSTALL.py`` again.


Usage
.....

**1. Input/Output files**

``Input``: A genome assembly in ``.fasta`` format (complete or draft), or raw reads in ``.fastq`` format. We will use the final assemblies in ``~/tutorial/genomes`` and also the Illumina-only assemblies (|shovill|).

.. attention::
   * In this Tutorial, |plasmidfinder| is run with a minimum of **80% identity** and **60% coverage** (``-t 0.80 -l 0.60``), as recommended by the authors to detect both the large plasmids and the small Col plasmids [CARATTOLI2014]_. The default of the command-line program is 90% identity (and the CGE web server may show other values, e.g., 95%), so always write the thresholds in the command and report them.
   * |plasmidfinder| is also run on the **Illumina-only assembly** (|shovill|). After the reorientation of the final assembly with |dnaapler|, the replicon (*rep*) sequence of a plasmid can be split between the end and the start of the sequence, and it may not be detected.

``Output``: Several files are produced, but the most important are:

* ``results_tab.tsv``: a table with the replicons found.
* ``results.txt``: the same results in a text format, including the alignments of each hit.
* ``Hit_in_genome_seq.fsa`` and ``Plasmid_seqs.fsa``: sequences of the replicons in your genome and in the database (only produced with ``-x``).
* ``data.json``: all the results in a machine-readable format.

**2. Basic commands**

.. code-block:: bash

   # Let's first create new directories to store your plasmid analyses
   $ cd ~/tutorial
   $ mkdir -p plasmids/plasmidfinder plasmids/plasmidfinder_shovill plasmids/mobsuite plasmids/plasgraph2
   $ cd ~/tutorial/plasmids/plasmidfinder

   # The output directory must exist before running PlasmidFinder
   $ mkdir EC958

   # Run PlasmidFinder in the EC958 genome (BLAST is used for the assembled genomes)
   $ plasmidfinder.py -i ~/tutorial/genomes/EC958.fasta -o EC958 -p ~/databases/cge/plasmidfinder_db -t 0.80 -l 0.60 -x

   # See the results
   $ column -t -s $'\t' EC958/results_tab.tsv

.. csv-table:: Parameters explanation when using PlasmidFinder
   :header: "Parameter", "Description"
   :widths: 20, 60

   "``-i FILE``", "Input file(s) in fasta or fastq format"
   "``-o DIR``", "Output directory (it must already exist)"
   "``-p DIR``", "Directory of the PlasmidFinder database (if not provided, the database installed with conda is used)"
   "``-d NAME``", "Database(s) to search, e.g., ``enterobacteriales`` (default: all)"
   "``-t NUM``", "Minimum identity threshold, between 0 and 1 (default: 0.90; used in this Tutorial: 0.80)"
   "``-l NUM``", "Minimum coverage threshold, between 0 and 1 (default: 0.60; used in this Tutorial: 0.60)"
   "``-x``", "Extended output: also saves the aligned sequences and the table ``results_tab.tsv``"
   "``-mp PATH``", "Path to the program that is used: ``blastn`` (assemblies) or ``kma`` (reads)"
   "``-tmp DIR``", "Directory for temporary files (it must exist; by default, a ``tmp`` directory is created in the output directory)"

The ``results_tab.tsv`` file has the following columns:

   1. **Database**: database where the replicon was found (e.g., ``enterobacteriales``).
   2. **Plasmid**: name of the replicon (e.g., ``IncFII``, ``IncFIB(AP001918)``). The text between brackets is the name of the plasmid that was used as reference of that replicon variant.
   3. **Identity**: percentage of identical nucleotides.
   4. **Query / Template length**: length of the hit in your genome / length of the replicon in the database. If they are similar, the full replicon was found.
   5. **Contig**: name of the sequence (chromosome, plasmid or contig) where the replicon was found.
   6. **Position in contig**: start and end of the replicon in the sequence.
   7. **Note**: additional comments.
   8. **Accession number**: accession number of the replicon in the database.

.. hint::
   A hit with identity below 100% (e.g., ``IncFII`` with 96%) means that your replicon is a **variant** of the one in the database. Replicons with lower identity or coverage than the thresholds are not reported, so a plasmid with a new replicon type can be missed. Hits between 80% and 90% identity should be checked carefully, and confirmed with |mobsuite| (see below).

**3. Additional options**

.. code-block:: bash

   # To see a full list of available options in PlasmidFinder
   $ plasmidfinder.py --help

**4. Running PlasmidFinder in several genomes**

PlasmidFinder accepts several input files in the same command, but the results of all of them are mixed in the same output directory. It is better to run each genome in its own output directory using a loop.

.. code-block:: bash

   $ cd ~/tutorial
   $ mkdir -p logs
   for genome in genomes/*.fasta; do
      sample=$(basename $genome .fasta)
      echo "Running PlasmidFinder in ${sample}"
      mkdir -p plasmids/plasmidfinder/${sample}
      plasmidfinder.py -i $genome -o plasmids/plasmidfinder/${sample} -p ~/databases/cge/plasmidfinder_db -t 0.80 -l 0.60 -x > logs/${sample}_plasmidfinder.log 2>&1
   done

   # Run PlasmidFinder also in the Illumina-only assemblies (Shovill) of your samples
   while read -r sample; do
      mkdir -p plasmids/plasmidfinder_shovill/${sample}
      plasmidfinder.py -i assembly/shovill/${sample}_shovill.fasta -o plasmids/plasmidfinder_shovill/${sample} -p ~/databases/cge/plasmidfinder_db -t 0.80 -l 0.60 -x > logs/${sample}_plasmidfinder_shovill.log 2>&1
   done < samples.txt

   # Combine the replicons of all the genomes in a single table (the 1st column is the name of the genome)
   $ echo -e "genome\tdatabase\treplicon\tidentity\tquery_template_length\tcontig\tposition" > plasmids/plasmidfinder_all.tsv
   for dir in plasmids/plasmidfinder/*/; do
      sample=$(basename $dir)
      tail -n +2 $dir/results_tab.tsv | cut -f 1-6 | awk -F'\t' -v s=$sample '{print s"\t"$0}' >> plasmids/plasmidfinder_all.tsv
   done

   # Visualise the table (without the 6th column, the name of the contig, which is very long)
   $ cut -f 1-5,7 plasmids/plasmidfinder_all.tsv | column -t -s $'\t'

   # Count the number of replicons found in each genome (genomes without any replicon, like K12, are not listed)
   $ tail -n +2 plasmids/plasmidfinder_all.tsv | cut -f 1 | sort | uniq -c

   # List the replicons found in each genome
   $ tail -n +2 plasmids/plasmidfinder_all.tsv | cut -f 1,3 | sort -u | awk -F'\t' '{r[$2]=1; g[$1]=g[$1]" "$2} END{for (i in g) print i":"g[i]}'

.. note::
   If you run PlasmidFinder in a **draft assembly**, a replicon may be found in a contig that is only a part of the plasmid. The same applies to the genomes with **more than one replicon**: PlasmidFinder does not tell you if the replicons belong to the same plasmid or to different ones (see the next sections).

.. todo::
   1. Run PlasmidFinder in strainA and strainB. Which replicons are present?
   2. Run the loop in all the genomes. Which genomes have more replicons? Which genome does not have any? Does it agree with the number of sequences that you saw in the ``.fasta`` files?
   3. In the Sakai genome, which replicon is in each of the two plasmids (pO157 and pOSAK1)? Hint: look at the contig names.
   4. In the EC958 genome, the replicons IncFIA and IncFII are in the same sequence. What does it mean?
   5. Compare the replicons found in the final assemblies and in the |shovill| assemblies of strainA and strainB. Is any replicon found only in the |shovill| assembly? Where is it located in the final assembly (start or end of a sequence)?


Plasmid reconstruction
######################

A **complete** genome (where each chromosome and plasmid is a single closed sequence) makes it easy to know which sequences are plasmids. But most of the genomes that you will work with are **drafts**, composed of tens to hundreds of contigs. The goal of plasmid reconstruction is to answer the following questions:

* Which contigs of the assembly are **plasmids** and which are chromosomal?
* How many **different plasmids** are present and which contigs belong to each of them?
* What is the **type** of each plasmid (replicon, mobility, host range, closest reference)?

There are several approaches, with different advantages and limitations.

.. csv-table:: Approaches and tools for plasmid reconstruction used in this Tutorial
   :header: "Approach", "Tools", "Input", "Comments"
   :widths: 20, 25, 20, 40

   "**Long-read** assembly", "|autocycler| (and |unicycler| for small plasmids)", "Long reads (and short reads)", "Best approach: complete and circular plasmids. Needs long-read sequencing. The plasmids are then typed with ``mob_typer``"
   "Contig classification using a plasmid database (**reference-based**)", "|mobsuite| (``mob_recon``)", "Draft assembly", "Fast and works with any assembly; depends on the plasmids available in the database"
   "Contig classification using the **assembly graph** and machine learning (**reference-free**)", "|plasgraph2|", "Short-read assembly graph (``.gfa``)", "Can find new plasmids, since it does not depend on a plasmid database; it classifies the contigs but does not separate the plasmids from each other"

.. attention::
   There is **no perfect tool**. The recommended approach is to combine the results of two or more complementary methods and check the results (e.g., PlasmidFinder replicons, size, coverage, circularity) before taking conclusions.


MOB-suite
*********

* |mobsuite| is a set of tools for the **clustering, reconstruction and typing of plasmids** from draft or complete assemblies [ROBERTSON2018]_.

* It has three main tools:

  1. ``mob_recon``: reconstructs plasmids from an assembly. It identifies which contigs are plasmids, groups them in individual plasmids, and types them.
  2. ``mob_typer``: types a plasmid (or a set of plasmid sequences): replicon (*rep*), relaxase (MOB), mating pair formation (MPF), *oriT*, predicted mobility, and closest plasmid in the database.
  3. ``mob_cluster``: clusters plasmids by similarity (to build or update a custom database).

* In this Tutorial, ``mob_typer`` is used for the **complete genomes** (each plasmid is already a single sequence) and ``mob_recon`` for the **draft assemblies**. The replicons are reported with a minimum of **90% identity** and **90% coverage**, and they are used to **validate** the replicons found by |plasmidfinder|.

* To do this, ``mob_recon`` compares the contigs with a database of **complete plasmids** (clusters of closely related plasmids), searches for replicons, relaxases, and other markers, and uses the contigs of **closed chromosomes** of the same species to remove the chromosomal ones. Contigs with a similar profile (e.g., the same plasmid cluster) are grouped in the same plasmid.


Installation
............

.. code-block:: bash

   # Deactivate all the current environments
   $ conda deactivate

   # Create a new environment named mobsuite
   $ mamba create -n mobsuite mob_suite

   # Activate the new environment
   $ conda activate mobsuite

   # Check the installation
   $ mob_recon --version

   # Download and prepare the databases (about 3 GB of disk space, it takes a few minutes)
   $ mob_init

.. note::
   By default, ``mob_init`` saves the database inside the environment directory. You can choose another directory with ``mob_init -d <directory>``, but in that case you need to use ``-d <directory>`` in all the ``mob_recon`` and ``mob_typer`` commands.

.. warning::
   If the ``mamba create`` command fails in macOS with Apple Silicon, create the environment using the Intel architecture: ``CONDA_SUBDIR=osx-64 mamba create -n mobsuite mob_suite``.


Usage
.....

**1. Input/Output files**

``Input``: A genome assembly in ``.fasta`` format (complete or draft). For this part of the Tutorial, we will use the complete genomes in ``~/tutorial/genomes`` (``mob_typer``) and the draft |shovill| assemblies (``mob_recon``).

``Output``: A directory with several files. The most important ones are:

* ``contig_report.txt``: a table with one line for each contig, indicating if it is a ``chromosome`` or a ``plasmid``, and to which plasmid cluster it was assigned.
* ``plasmid_<cluster>.fasta``: the sequences of each reconstructed plasmid (when a plasmid is composed of several contigs, they are in the same file).
* ``chromosome.fasta``: the contigs classified as chromosomal.
* ``mobtyper_results.txt``: the typing of each reconstructed plasmid.
* ``mge.report.txt``: mobile genetic elements (e.g., insertion sequences) found in the contigs.
* ``biomarkers.blast.txt``: the BLAST results of the markers (replicons, relaxases, *oriT*, MPF).

**2. Typing the plasmids of complete genomes (MOB-typer)**

In a complete genome, each plasmid is already a single sequence. Split the genome in one file for each sequence and type each of them with ``mob_typer``:

.. code-block:: bash

   $ cd ~/tutorial/plasmids/mobsuite

   # Split the EC958 genome in one file for each sequence (the name of the file is the first word of the header)
   $ mkdir -p EC958_sequences
   $ awk '/^>/ {id=substr($1,2); file="EC958_sequences/" id ".fasta"} {print > file}' ~/tutorial/genomes/EC958.fasta
   $ ls EC958_sequences

   # Type each sequence with MOB-typer (replicons with at least 90% identity and 90% coverage)
   for file in EC958_sequences/*.fasta; do
      mob_typer --infile $file --out_file ${file%.fasta}_mobtyper.txt --min_rep_ident 90 --min_rep_cov 90
   done

   # Combine the results of all the sequences (keeping only one header)
   $ awk 'FNR==1 && NR!=1 {next} {print}' EC958_sequences/*_mobtyper.txt > EC958_mobtyper.tsv
   $ cut -f 1,3,6,8,14 EC958_mobtyper.tsv | column -t -s $'\t'

.. csv-table:: Parameters explanation when using MOB-typer
   :header: "Parameter", "Description"
   :widths: 20, 60

   "``--infile FILE``", "Input plasmid sequence(s) in fasta format"
   "``--out_file FILE``", "Output file"
   "``--multi``", "Treat each sequence of the input file as an independent plasmid"
   "``--min_rep_ident NUM``", "Minimum identity (%) of the replicon hits (used in this Tutorial: 90)"
   "``--min_rep_cov NUM``", "Minimum coverage (%) of the replicon hits (used in this Tutorial: 90)"

.. note::
   The chromosome is also typed, but it will not have a plasmid replicon, relaxase or close plasmid neighbor. Compare the replicons of ``rep_type(s)`` with the ones found by |plasmidfinder|.

**3. Reconstructing the plasmids of draft assemblies (MOB-recon)**

In a draft assembly (e.g., the |shovill| assemblies), a plasmid is typically distributed in several contigs. ``mob_recon`` identifies the plasmid contigs and groups them in individual plasmids:

.. code-block:: bash

   $ cd ~/tutorial/plasmids/mobsuite

   # Run MOB-recon in the Shovill assembly of strainA
   # -s is the name that will appear in the reports, -n the number of threads and -f overwrites an existing directory
   $ mob_recon -i ~/tutorial/assembly/shovill/strainA_shovill.fasta -o strainA_shovill -s strainA_shovill -n 4 -f --min_rep_ident 90 --min_rep_cov 90

   # See which contigs were classified as chromosome and plasmids
   $ cut -f 1,2,3,5,6 strainA_shovill/contig_report.txt | column -t -s $'\t'

   # See the typing results of each plasmid (replicon, relaxase, mobility...)
   $ cut -f 1,2,3,6,8,14 strainA_shovill/mobtyper_results.txt | column -t -s $'\t'

   # List the files of the reconstructed plasmids
   $ ls strainA_shovill/plasmid_*.fasta

.. csv-table:: Parameters explanation when using MOB-recon
   :header: "Parameter", "Description"
   :widths: 20, 60

   "``-i FILE``", "Input assembly in fasta format"
   "``-o DIR``", "Output directory"
   "``-s NAME``", "Name of the sample that will be used in the reports (default: name of the file)"
   "``-n NUM``", "Number of threads (default: 1)"
   "``-f``", "Overwrite the output directory if it already exists"
   "``-p PREFIX``", "Prefix to add to the names of the result files"
   "``--max_contig_size NUM``", "Maximum size of a contig to be considered a plasmid (default: 450000 bp)"
   "``--max_plasmid_size NUM``", "Maximum size of a reconstructed plasmid (default: 450000 bp)"
   "``-d DIR``", "Directory of the databases (not needed if the default directory of ``mob_init`` was used)"
   "``-g PREFIX``", "Prefix of the databases of closed chromosomes (to filter the chromosomal contigs of a specific species)"
   "``--min_rep_ident NUM``", "Minimum identity (%) of the replicon hits (used in this Tutorial: 90)"
   "``--min_rep_cov NUM``", "Minimum coverage (%) of the replicon hits (used in this Tutorial: 90)"

The ``contig_report.txt`` has the following main columns:

   1. **sample_id**: name of the sample.
   2. **molecule_type**: ``chromosome`` or ``plasmid``.
   3. **primary_cluster_id** and **secondary_cluster_id**: plasmid cluster that was assigned (e.g., ``AA735``). Contigs with the same primary cluster belong to the same (or similar) plasmid.
   4. **contig_id**, **size**, **gc**: name, length, and GC content of the contig.
   5. **circularity_status**: indicates if the contig is circular (``circular``), incomplete (``incomplete``), or if it was not tested (``not tested``; e.g., in complete genomes).
   6. **rep_type(s)**, **relaxase_type(s)**, **mpf_type**, **orit_type(s)**: replicon, relaxase (MOB), MPF type and *oriT* found in the contig.
   7. **predicted_mobility**: ``conjugative``, ``mobilizable`` or ``non-mobilizable``.
   8. **mash_nearest_neighbor**, **mash_neighbor_distance**, **mash_neighbor_identification**: closest plasmid in the database (accession number and organism) and the distance to it (0 means identical).

The ``mobtyper_results.txt`` has the same type of information but **for each reconstructed plasmid** (one line per plasmid, with the contigs of the same plasmid together), including the total ``size`` and the number of contigs (``num_contigs``). It also includes the **predicted host range** of the plasmid.

.. note::
   When you run |mobsuite| in a **complete genome**, each sequence is already a replicon, so the main result is the classification of each one as chromosome or plasmid and the typing of the plasmids. In a **draft assembly**, a plasmid is typically distributed in several contigs, and the number of contigs (``num_contigs``) and the total size of the plasmid (``size``) of ``mobtyper_results.txt`` are important to know how complete the reconstruction is. Compare the size with the size of the closest reference plasmid (``mash_nearest_neighbor``).

**3. Additional options**

.. code-block:: bash

   # To see a full list of available options in MOB-recon
   $ mob_recon --help

   # To see a full list of available options in MOB-typer
   $ mob_typer --help

**5. Running MOB-suite in several genomes**

.. code-block:: bash

   $ cd ~/tutorial

   # MOB-typer in all the complete genomes (final assemblies and public genomes)
   for genome in genomes/*.fasta; do
      sample=$(basename $genome .fasta)
      echo "Running MOB-typer in ${sample}"
      mkdir -p plasmids/mobsuite/${sample}_sequences
      awk -v d=plasmids/mobsuite/${sample}_sequences '/^>/ {id=substr($1,2); file=d"/"id".fasta"} {print > file}' $genome
      for file in plasmids/mobsuite/${sample}_sequences/*.fasta; do
         mob_typer --infile $file --out_file ${file%.fasta}_mobtyper.txt --min_rep_ident 90 --min_rep_cov 90 >> logs/${sample}_mobtyper.log 2>&1
      done
      awk 'FNR==1 && NR!=1 {next} {print}' plasmids/mobsuite/${sample}_sequences/*_mobtyper.txt > plasmids/mobsuite/${sample}_mobtyper.tsv
   done

   # MOB-recon in the draft assemblies (Shovill) of your samples
   while read -r sample; do
      echo "Running MOB-recon in ${sample}"
      mob_recon -i assembly/shovill/${sample}_shovill.fasta -o plasmids/mobsuite/${sample}_shovill -s ${sample}_shovill -n 4 -f --min_rep_ident 90 --min_rep_cov 90 > logs/${sample}_mobrecon.log 2>&1
   done < samples.txt

   # Combine the MOB-typer results of all the complete genomes in a single table (keeping only one header)
   $ awk 'FNR==1 && NR!=1 {next} {print}' plasmids/mobsuite/*_mobtyper.tsv > plasmids/mobtyper_all.tsv

   # See the main columns: sequence, size, replicons, relaxases, mobility
   $ cut -f 1,2,6,8,14 plasmids/mobtyper_all.tsv | column -t -s $'\t'

.. hint::
   |mobsuite| runs in about 40 seconds for a genome with ~1000 contigs. In very large datasets, you can run several genomes in parallel using ``xargs -P`` (see the Bash section).

For a typical O157:H7 genome, you should find, for example, the large virulence plasmid pO157 (IncFIB and IncFII replicons; ~90 kb) and the small plasmid pOSAK1 (~3.3 kb). In a draft assembly, pO157 is usually reconstructed from 3 to 4 contigs, while pOSAK1 is in a single contig. The sum of the sizes of the contigs of a plasmid will be close to the size of the complete plasmid in the final assembly.

.. todo::
   6. Run ``mob_typer`` in the final assemblies of strainA and strainB. How many plasmids does each strain have? What are their sizes and replicons?
   7. Run the loop in all the genomes. Which plasmids are predicted as **conjugative**? And **mobilizable**? Is it consistent with the presence of a relaxase (``relaxase_type(s)``)?
   8. Compare the replicons found by |mobsuite| (``rep_type(s)``) with the ones found by |plasmidfinder|. Are they the same? Which replicons of |plasmidfinder| are validated by |mobsuite|?
   9. Run ``mob_recon`` in the |shovill| assembly of strainA. In how many contigs is each plasmid fragmented? How does the total size compare with the plasmids of the final assembly?
   10. What is the closest plasmid (``mash_nearest_neighbor``) of each reconstructed plasmid? Look for its accession number in `NCBI <https://www.ncbi.nlm.nih.gov/nuccore/>`_.


plASgraph2
**********

* |plasgraph2| classifies the contigs of a **short-read assembly graph** as **plasmid** or **chromosome**, using a graph neural network [SIELEMANN2023]_.

* Besides the sequence of each contig (e.g., GC content, k-mers), it uses the **assembly graph**: the coverage of the contigs and their connections with the neighbouring contigs. This helps to classify short contigs, that are difficult to classify by their sequence alone.

* Contrary to |mobsuite|, it does not use a plasmid database, so it can find **new plasmids**. However, it does not separate the plasmids from each other, and a contig can be labelled as ``ambiguous`` (e.g., a repeat shared by a plasmid and the chromosome).

* |plasgraph2| was trained with assembly graphs produced by |unicycler| and SKESA from **short reads only**. It includes a model trained on the ESKAPEE pathogens (*Enterococcus faecium*, *Staphylococcus aureus*, *Klebsiella pneumoniae*, *Acinetobacter baumannii*, *Pseudomonas aeruginosa*, *Enterobacter* spp. and *E. coli*), that can also be applied to other species.


Installation
............

|plasgraph2| is not available in conda. It is installed from its GitHub repository, in a conda environment with Python 3.8.

.. code-block:: bash

   # Deactivate all the current environments
   $ conda deactivate

   # Download plASgraph2 to a directory with your software
   $ mkdir -p ~/software
   $ cd ~/software
   $ git clone https://github.com/cchauve/plASgraph2.git

   # Create an environment with Python 3.8 and install the required packages (including TensorFlow)
   $ mamba create -n plasgraph2 python=3.8
   $ conda activate plasgraph2
   $ pip install -r ~/software/plASgraph2/requirements.txt

   # Check the installation
   $ python ~/software/plASgraph2/src/plASgraph2_classify.py --help


Usage
.....

**1. Input/Output files**

``Input``: A short-read assembly graph in **compressed** GFA format (``.gfa.gz``), produced by |unicycler| (with short reads only) or SKESA.

.. note::
   In this Tutorial we use the graph of |unicycler| with **short reads only**, since it is one of the two types of graphs used to train and test |plasgraph2|, and |unicycler| is already installed. Do not use the |unicycler| hybrid assembly (with long reads) or the graph of |shovill|: the model was not trained with them, so the results may not be reliable.

``Output``: A ``.csv`` file with one line per contig (longer than 100 bp): the contig name, its length, the **plasmid score** and the **chromosome score** (between 0 and 1), and the final **label** (``plasmid``, ``chromosome``, ``ambiguous`` or ``unlabeled``).

**2. Basic commands**

.. code-block:: bash

   # Assemble the clean Illumina reads with Unicycler (short reads only) to obtain the assembly graph
   $ conda activate unicycler
   $ mkdir -p ~/tutorial/plasmids/plasgraph2
   $ cd ~/tutorial/plasmids/plasgraph2
   $ unicycler -1 ~/tutorial/qc_improvement/strainA_clean_R1.fastq.gz -2 ~/tutorial/qc_improvement/strainA_clean_R2.fastq.gz -o strainA_unicycler_short -t 4

   # Compress the assembly graph
   $ gzip -c strainA_unicycler_short/assembly.gfa > strainA.gfa.gz

   # Classify the contigs with plASgraph2, using the ESKAPEE model
   $ conda activate plasgraph2
   $ python ~/software/plASgraph2/src/plASgraph2_classify.py gfa strainA.gfa.gz ~/software/plASgraph2/model/ESKAPEE_model/ strainA_plasgraph2.csv

   # See the results
   $ column -t -s, strainA_plasgraph2.csv | head -n 20

   # Count the number of contigs of each label (last column)
   $ awk -F, 'NR>1 {print $NF}' strainA_plasgraph2.csv | sort | uniq -c

.. csv-table:: Arguments of plASgraph2_classify.py
   :header: "Argument", "Description"
   :widths: 20, 60

   "``gfa``", "Classify the contigs of a single assembly graph"
   "``set``", "Classify the contigs of several assembly graphs listed in a ``.csv`` file (see below)"
   "``FILE.gfa.gz``", "Compressed assembly graph"
   "``MODEL_DIR``", "Directory of the trained model (``model/ESKAPEE_model/``)"
   "``OUTPUT.csv``", "Output file"

.. note::
   |plasgraph2| uses TensorFlow, which can use a GPU if available. If you have problems with the GPU, force the use of the CPU with ``export CUDA_VISIBLE_DEVICES=""``.

**3. Running plASgraph2 in several samples**

In the ``set`` mode, |plasgraph2| classifies several graphs at the same time. It needs a ``.csv`` file with one line per sample: the name of the ``.gfa.gz`` file, a second field that is not used, and the name of the sample. All the graphs must be in the same directory.

.. code-block:: bash

   $ cd ~/tutorial/plasmids/plasgraph2

   # Assemble the reads of all the samples and compress the graphs
   $ conda activate unicycler
   while read -r sample; do
      unicycler -1 ~/tutorial/qc_improvement/${sample}_clean_R1.fastq.gz -2 ~/tutorial/qc_improvement/${sample}_clean_R2.fastq.gz -o ${sample}_unicycler_short -t 4 > ${sample}_unicycler_short.stdout 2>&1
      gzip -c ${sample}_unicycler_short/assembly.gfa > ${sample}.gfa.gz
   done < ~/tutorial/samples.txt

   # Create the input file (file name, unused field, sample name)
   $ awk '{print $1".gfa.gz,-,"$1}' ~/tutorial/samples.txt > input.csv

   # Classify all the samples
   $ conda activate plasgraph2
   $ python ~/software/plASgraph2/src/plASgraph2_classify.py set input.csv . ~/software/plASgraph2/model/ESKAPEE_model/ all_samples_plasgraph2.csv

   # Total length (bp) of the contigs of each label in each sample (columns: sample, contig, length, ..., label)
   $ awk -F, 'NR>1 {l[$1" "$NF]+=$3} END{for (k in l) print k"\t"l[k]}' all_samples_plasgraph2.csv | sort

.. todo::
   10. Run |plasgraph2| in strainA and strainB. How many contigs were classified as plasmid? What is their total length?
   11. Compare the total length of the plasmid contigs with the size of the plasmids of the final assembly, and with the plasmids reconstructed by ``mob_recon``.
   12. How many contigs were labelled as ``ambiguous``? Why do you think it is difficult to classify them?


Plasmids in complete genomes
****************************

With **long reads**, plasmids are usually assembled as **single and circular** sequences. In the final assemblies (|autocycler| + |dnaapler| + |polypolish|) you can identify them by their **size**: the chromosome is the largest sequence (~5 Mb in *E. coli*), and the plasmids are the smaller ones.

.. code-block:: bash

   $ cd ~/tutorial/genomes

   # Print the name and the length of all the sequences of the strainA assembly
   $ awk '/^>/{if(id) print id"\t"len; id=substr($1,2); len=0; next} {len+=length($0)} END{print id"\t"len}' strainA.fasta

   # Compare with the sequences of the Unicycler assembly: is any small plasmid missing in the final assembly?
   $ awk '/^>/{if(id) print id"\t"len; id=$0; len=0; next} {len+=length($0)} END{print id"\t"len}' ~/tutorial/assembly/unicycler/strainA_unicycler.fasta

* The ``depth`` of the |unicycler| headers (relative to the chromosome) is also informative: a plasmid with a depth higher than 1 (e.g., ``2.31x``) has more copies than the chromosome, which is common in **small plasmids**.

* After identifying the plasmids, type each of them with ``mob_typer`` (see above).

.. todo::
   13. How many plasmids do your final assemblies of strainA and strainB have? Are they the same plasmids that ``mob_recon`` found in the |shovill| draft assembly?
   14. Is any small plasmid present in the |unicycler| assembly but missing in the final assembly?


Linking plasmids with resistance and virulence genes
####################################################

One of the main reasons to reconstruct plasmids is to know **where the resistance and virulence genes are**. A gene in a plasmid is more likely to be transferred to other bacteria than a gene in the chromosome.

You already have the two ingredients:

* The resistance genes, with the **contig** where each one was found (AMRFinderPlus: column ``Contig id``; ResFinder: column ``Contig``).
* The classification of each sequence in chromosome or plasmid. In complete genomes, the chromosome is the largest sequence (here, longer than 1 Mb), and the plasmids are the smaller ones, typed with ``mob_typer``.

You only need to join them by the name of the sequence:

.. code-block:: bash

   $ cd ~/tutorial

   # For each genome, list the AMR genes (core, type AMR) of AMRFinderPlus, the sequence, and if it is the chromosome or a plasmid
   for genome in EC958 Sakai; do
      awk '/^>/{if(id) print id"\t"len; id=substr($1,2); len=0; next} {len+=length($0)} END{print id"\t"len}' genomes/${genome}.fasta > /tmp/${genome}_lengths.tsv
      awk -F'\t' -v g=$genome 'FNR==NR { mol[$1]=($2>1000000 ? "chromosome" : "plasmid"); size[$1]=$2; next }
           FNR>1 && $9=="core" && $10=="AMR" { print g"\t"$7"\t"$12"\t"$3"\t"mol[$3]"\t"size[$3] }' \
           /tmp/${genome}_lengths.tsv amr/amrfinder/${genome}.tsv
   done | column -t -s $'\t'

The output of this command has the following columns: **genome**, **gene**, **antibiotic class**, **sequence**, **molecule** (chromosome or plasmid), and **size** of the sequence. In EC958, you will find that the genes ``blaCTX-M-15``, ``blaTEM-1``, ``blaOXA-1``, ``aac(6')-Ib-cr``, ``aadA5``, ``sul1``, ``dfrA17``, ``tet(A)``, ``mph(A)`` and ``catB3`` are all in the same plasmid (pEC958, IncFIA/IncFII, conjugative), while the ``blaCMY-23`` gene and the point mutations in *gyrA*, *parC* and *parE* are in the chromosome.

.. code-block:: bash

   # Do the same for all the genomes, saving the table in a file
   $ echo -e "genome\tgene\tclass\tsequence\tmolecule\tsize" > amr/amr_location_all.tsv
   for genome in genomes/*.fasta; do
      name=$(basename $genome .fasta)
      [ -s amr/amrfinder/${name}.tsv ] || continue
      awk '/^>/{if(id) print id"\t"len; id=substr($1,2); len=0; next} {len+=length($0)} END{print id"\t"len}' $genome > /tmp/${name}_lengths.tsv
      awk -F'\t' -v g=$name 'FNR==NR { mol[$1]=($2>1000000 ? "chromosome" : "plasmid"); size[$1]=$2; next }
           FNR>1 && $9=="core" && $10=="AMR" { print g"\t"$7"\t"$12"\t"$3"\t"mol[$3]"\t"size[$3] }' \
           /tmp/${name}_lengths.tsv amr/amrfinder/${name}.tsv >> amr/amr_location_all.tsv
   done

   # Count the number of AMR genes/mutations in the chromosome and in plasmids of each genome
   $ tail -n +2 amr/amr_location_all.tsv | cut -f 1,5 | sort | uniq -c

The same can be done for the **virulence genes** found by |virulencefinder|. In its ``results_tab.tsv`` file, the gene is in the 2nd column and the sequence in the 5th column (only the first word of the header is used):

.. code-block:: bash

   # Link the virulence genes of all the genomes to the chromosome or to a plasmid
   $ echo -e "genome\tgene\tprotein_function\tsequence\tmolecule\tsize" > amr/virulence_location_all.tsv
   for genome in genomes/*.fasta; do
      name=$(basename $genome .fasta)
      [ -s amr/virulencefinder/${name}/results_tab.tsv ] || continue
      awk '/^>/{if(id) print id"\t"len; id=substr($1,2); len=0; next} {len+=length($0)} END{print id"\t"len}' $genome > /tmp/${name}_lengths.tsv
      awk -F'\t' -v g=$name 'FNR==NR { mol[$1]=($2>1000000 ? "chromosome" : "plasmid"); size[$1]=$2; next }
           FNR>1 { split($5,a," "); print g"\t"$2"\t"$7"\t"a[1]"\t"mol[a[1]]"\t"size[a[1]] }' \
           /tmp/${name}_lengths.tsv amr/virulencefinder/${name}/results_tab.tsv >> amr/virulence_location_all.tsv
   done

   # Visualise the table and count the virulence genes in the chromosome and in plasmids of each genome
   $ column -t -s $'\t' amr/virulence_location_all.tsv | cut -c 1-150
   $ tail -n +2 amr/virulence_location_all.tsv | cut -f 1,5 | sort | uniq -c

.. note::
   In the Sakai genome (STEC O157:H7), you should find the Shiga toxin genes (*stx1*, *stx2*) in the **chromosome** (they are carried by prophages), and genes such as the enterohaemolysin (*ehxA*) in the large virulence plasmid **pO157**.

.. attention::
   * In **draft assemblies**, the plasmid contigs are fragmented and, in many cases, an AMR gene is at the end of a contig. Check if the contig is classified as a plasmid by ``mob_recon`` and |plasgraph2|, and if it also has other plasmid markers.
   * Resistance genes that are located in **repetitive elements** (e.g., transposons with several copies, integrons) can be assembled in a contig that is shared by the chromosome and the plasmids, and may be wrongly assigned to only one of them.
   * Genes in **chromosomal contigs** can also be mobile (e.g., in integrative conjugative elements or genomic islands), so the chromosome is not necessarily a stable location.

.. todo::
   15. In which molecule (chromosome or plasmid) are the AMR genes of strainA and strainB?
   16. Which resistance genes are in the plasmid of EC958 and which are in the chromosome? What does it mean for the potential of spreading the resistance?
   17. Do the plasmids of your strains (strainA and strainB) carry any resistance gene? And virulence genes (|virulencefinder|)? Are the *stx* genes in the chromosome or in a plasmid?
   18. Write a short summary (table) of the AMR genes, mutations, virulence genes, replicons and plasmids of all the genomes, indicating if each gene is in the chromosome or in a plasmid.


Folder structure
################

At the end of this section, you will have the following folder structure (only the new folders are detailed).

::

    tutorial
    ├── samples.txt
    ├── raw_data
    ├── genomes
    ├── qc_visualisation
    ├── qc_improvement
    ├── taxonomy
    ├── assembly
    ├── annotation
    ├── amr
    │   ├── resfinder
    │   ├── amrfinder
    │   ├── virulencefinder
    │   ├── amr_location_all.tsv
    │   ├── virulence_location_all.tsv
    ├── plasmids
    │   ├── plasmidfinder
    │   │   ├── <genome>
    │   │   │   ├── results_tab.tsv
    │   │   │   ├── results.txt
    │   │   │   ├── Hit_in_genome_seq.fsa
    │   │   │   ├── Plasmid_seqs.fsa
    │   ├── plasmidfinder_shovill
    │   │   ├── <sample>
    │   ├── mobsuite
    │   │   ├── <genome>_sequences
    │   │   ├── <genome>_mobtyper.tsv
    │   │   ├── <sample>_shovill
    │   │   │   ├── contig_report.txt
    │   │   │   ├── mobtyper_results.txt
    │   │   │   ├── chromosome.fasta
    │   │   │   ├── plasmid_<cluster>.fasta
    │   ├── plasgraph2
    │   │   ├── <sample>.gfa.gz
    │   │   ├── input.csv
    │   │   ├── all_samples_plasgraph2.csv
    │   ├── plasmidfinder_all.tsv
    │   ├── mobtyper_all.tsv
    ├── logs


References
##########

.. [CARATTOLI2014] Carattoli A, et al. 2014. In Silico Detection and Typing of Plasmids using PlasmidFinder and Plasmid Multilocus Sequence Typing. Antimicrob Agents Chemother. 58(7):3895–3903. `DOI: 10.1128/AAC.02412-14 <https://dx.doi.org/10.1128/AAC.02412-14>`_.
.. [ROBERTSON2018] Robertson J, Nash JHE. 2018. MOB-suite: software tools for clustering, reconstruction and typing of plasmids from draft assemblies. Microb Genom. 4(8):e000206. `DOI: 10.1099/mgen.0.000206 <https://dx.doi.org/10.1099/mgen.0.000206>`_.
.. [SIELEMANN2023] Sielemann J, Sielemann K, Brejová B, Vinař T, Chauve C. 2023. plASgraph2: using graph neural networks to detect plasmid contigs from an assembly graph. Front Microbiol. 14:1267695. `DOI: 10.3389/fmicb.2023.1267695 <https://dx.doi.org/10.3389/fmicb.2023.1267695>`_.
