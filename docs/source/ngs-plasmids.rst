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
   * **Plasmid reconstruction**: identify which sequences (contigs) of an assembly belong to plasmids, group them into individual plasmids, and type them, using |mobsuite| [ROBERTSON2018]_ and |spades| plasmid mode (plasmidSPAdes) [ANTIPOV2016B]_.

4. Finally, you will connect the plasmids with the resistance genes that you found in the previous section.

.. attention::
   * The presence of a **replicon** does not mean that the complete plasmid is present or that you know its sequence. A plasmid can have more than one replicon (e.g., IncFIA + IncFII), and different plasmids can share the same replicon.
   * Plasmids are rich in **repeated sequences** (e.g., insertion sequences, transposons, integrons) and they also share regions with the chromosome and with other plasmids. Because of that, plasmids are frequently **fragmented in several contigs** in short-read assemblies. Complete plasmids are best obtained with **long reads** (e.g., the hybrid assemblies produced by |unicycler|).


Learning objectives
###################

After finishing this Tutorial section, you will be able to:

* Detect plasmid replicons in assembled genomes using PlasmidFinder.
* Reconstruct and type plasmids from complete or draft assemblies using MOB-suite.
* Extract plasmid-like contigs from raw short reads with plasmidSPAdes.
* Identify complete (circular) plasmids in a hybrid assembly.
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
   $ conda create -n plasmidfinder plasmidfinder

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

``Input``: A genome assembly in ``.fasta`` format (complete or draft), or raw reads in ``.fastq`` format. For this part of the Tutorial, we will use the assembled genomes in ``~/tutorial/genomes``.

``Output``: Several files are produced, but the most important are:

* ``results_tab.tsv``: a table with the replicons found.
* ``results.txt``: the same results in a text format, including the alignments of each hit.
* ``Hit_in_genome_seq.fsa`` and ``Plasmid_seqs.fsa``: sequences of the replicons in your genome and in the database (only produced with ``-x``).
* ``data.json``: all the results in a machine-readable format.

**2. Basic commands**

.. code-block:: bash

   # Let's first create new directories to store your plasmid analyses
   $ cd ~/tutorial
   $ mkdir -p plasmids/plasmidfinder plasmids/mobsuite plasmids/plasmidspades
   $ cd ~/tutorial/plasmids/plasmidfinder

   # The output directory must exist before running PlasmidFinder
   $ mkdir EC958

   # Run PlasmidFinder in the EC958 genome (BLAST is used for the assembled genomes)
   $ plasmidfinder.py -i ~/tutorial/genomes/EC958.fasta -o EC958 -p ~/databases/cge/plasmidfinder_db -x

   # See the results
   $ column -t -s $'\t' EC958/results_tab.tsv

   # Run PlasmidFinder with stricter thresholds (95% identity and 80% coverage), using only the Enterobacterales database
   $ plasmidfinder.py -i ~/tutorial/genomes/EC958.fasta -o EC958 -p ~/databases/cge/plasmidfinder_db -d enterobacteriales -t 0.95 -l 0.80 -x

.. csv-table:: Parameters explanation when using PlasmidFinder
   :header: "Parameter", "Description"
   :widths: 20, 60

   "``-i FILE``", "Input file(s) in fasta or fastq format"
   "``-o DIR``", "Output directory (it must already exist)"
   "``-p DIR``", "Directory of the PlasmidFinder database (if not provided, the database installed with conda is used)"
   "``-d NAME``", "Database(s) to search, e.g., ``enterobacteriales`` (default: all)"
   "``-t NUM``", "Minimum identity threshold, between 0 and 1 (default: 0.90)"
   "``-l NUM``", "Minimum coverage threshold, between 0 and 1 (default: 0.60)"
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
   A hit with identity below 100% (e.g., ``IncFII`` with 96%) means that your replicon is a **variant** of the one in the database. Replicons with lower identity or coverage than the thresholds are not reported, so a plasmid with a new replicon type can be missed. If you suspect it, run PlasmidFinder with lower thresholds (e.g., ``-t 0.80 -l 0.60``).

**3. Additional options**

.. code-block:: bash

   # To see a full list of available options in PlasmidFinder
   $ plasmidfinder.py --help

**4. Running PlasmidFinder in several genomes**

PlasmidFinder accepts several input files in the same command, but the results of all of them are mixed in the same output directory. It is better to run each genome in its own output directory using a loop.

.. code-block:: bash

   $ cd ~/tutorial
   $ mkdir -p logs
   $ for genome in genomes/*.fasta; do
   >    sample=$(basename $genome .fasta)
   >    echo "Running PlasmidFinder in ${sample}"
   >    mkdir -p plasmids/plasmidfinder/${sample}
   >    plasmidfinder.py -i $genome -o plasmids/plasmidfinder/${sample} -p ~/databases/cge/plasmidfinder_db -x > logs/${sample}_plasmidfinder.log 2>&1
   > done

   # Combine the replicons of all the genomes in a single table (the 1st column is the name of the genome)
   $ echo -e "genome\tdatabase\treplicon\tidentity\tquery_template_length\tcontig\tposition" > plasmids/plasmidfinder_all.tsv
   $ for dir in plasmids/plasmidfinder/*/; do
   >    sample=$(basename $dir)
   >    tail -n +2 $dir/results_tab.tsv | cut -f 1-6 | awk -F'\t' -v s=$sample '{print s"\t"$0}' >> plasmids/plasmidfinder_all.tsv
   > done

   # Visualise the table (without the 6th column, the name of the contig, which is very long)
   $ cut -f 1-5,7 plasmids/plasmidfinder_all.tsv | column -t -s $'\t'

   # Count the number of replicons found in each genome (genomes without any replicon, like K12, are not listed)
   $ tail -n +2 plasmids/plasmidfinder_all.tsv | cut -f 1 | sort | uniq -c

   # List the replicons found in each genome
   $ tail -n +2 plasmids/plasmidfinder_all.tsv | cut -f 1,3 | sort -u | awk -F'\t' '{r[$2]=1; g[$1]=g[$1]" "$2} END{for (i in g) print i":"g[i]}'

.. note::
   If you run PlasmidFinder in a **draft assembly**, a replicon may be found in a contig that is only a part of the plasmid. The same applies to the genomes with **more than one replicon**: PlasmidFinder does not tell you if the replicons belong to the same plasmid or to different ones (see the next sections).

.. note::
   |abricate| also has a ``plasmidfinder`` database (``abricate --db plasmidfinder``), that you already used in the previous section. It is a faster alternative that gives similar results, but it is not updated as frequently as the official PlasmidFinder.

.. todo::
   1. Run PlasmidFinder in strainA and strainB. Which replicons are present?
   2. Run the loop in all the genomes. Which genomes have more replicons? Which genome does not have any? Does it agree with the number of sequences that you saw in the ``.fasta`` files?
   3. In the Sakai genome, which replicon is in each of the two plasmids (pO157 and pOSAK1)? Hint: look at the contig names.
   4. In the EC958 genome, the replicons IncFIA and IncFII are in the same sequence. What does it mean?
   5. Compare the results with the ones that you obtained using |abricate|.


Plasmid reconstruction
######################

A **complete** genome (where each chromosome and plasmid is a single closed sequence) makes it easy to know which sequences are plasmids. But most of the genomes that you will work with are **drafts**, composed of tens to hundreds of contigs. The goal of plasmid reconstruction is to answer the following questions:

* Which contigs of the assembly are **plasmids** and which are chromosomal?
* How many **different plasmids** are present and which contigs belong to each of them?
* What is the **type** of each plasmid (replicon, mobility, host range, closest reference)?

There are several approaches, with different advantages and limitations.

.. csv-table:: Approaches and tools for plasmid reconstruction
   :header: "Approach", "Tools", "Input", "Comments"
   :widths: 20, 25, 20, 40

   "Contig classification using a plasmid database (**reference-based**)", "|mobsuite| (``mob_recon``)", "Assembly (draft or complete)", "Fast and works with any assembly; depends on the plasmids available in the database"
   "Contig classification using machine learning or marker genes (**reference-free**)", "`Platon <https://github.com/oschwengers/platon>`_, `PlasClass <https://github.com/Shamir-Lab/PlasClass>`_, `plasmidEC <https://github.com/ClaudiaMEC/plasmidEC>`_, `gplas2 <https://gitlab.com/sirarredondo/gplas2>`_", "Assembly (and assembly graph for gplas2)", "Can find new plasmids; may have more false positives/negatives; gplas2 also bins the contigs in plasmids using the assembly graph"
   "Assembly of plasmids from the **short reads** (graph-based)", "plasmidSPAdes (``spades.py --plasmid``)", "Short reads", "Assembles directly from reads using the copy number (coverage) of the plasmids; returns plasmid-like contigs, with false positives"
   "**Long-read** or **hybrid** assembly", "|unicycler|, `Plassembler <https://github.com/gbouras13/plassembler>`_, `Flye <https://github.com/mikolmogorov/Flye>`_, `Trycycler <https://github.com/rrwick/Trycycler/wiki>`_", "Long reads (and short reads)", "Best approach: complete and circular plasmids. Needs long-read sequencing"

.. attention::
   There is **no perfect tool**. The recommended approach is to combine the results of two or more complementary methods and check the results (e.g., PlasmidFinder replicons, size, coverage, circularity) before taking conclusions.


MOB-suite
*********

* |mobsuite| is a set of tools for the **clustering, reconstruction and typing of plasmids** from draft or complete assemblies [ROBERTSON2018]_.

* It has three main tools:

  1. ``mob_recon``: reconstructs plasmids from an assembly. It identifies which contigs are plasmids, groups them in individual plasmids, and types them.
  2. ``mob_typer``: types a plasmid (or a set of plasmid sequences): replicon (*rep*), relaxase (MOB), mating pair formation (MPF), *oriT*, predicted mobility, and closest plasmid in the database.
  3. ``mob_cluster``: clusters plasmids by similarity (to build or update a custom database).

* To do this, ``mob_recon`` compares the contigs with a database of **complete plasmids** (clusters of closely related plasmids), searches for replicons, relaxases, and other markers, and uses the contigs of **closed chromosomes** of the same species to remove the chromosomal ones. Contigs with a similar profile (e.g., the same plasmid cluster) are grouped in the same plasmid.


Installation
............

.. code-block:: bash

   # Deactivate all the current environments
   $ conda deactivate

   # Create a new environment named mobsuite
   $ conda create -n mobsuite mob_suite

   # Activate the new environment
   $ conda activate mobsuite

   # Check the installation
   $ mob_recon --version

   # Download and prepare the databases (about 3 GB of disk space, it takes a few minutes)
   $ mob_init

.. note::
   By default, ``mob_init`` saves the database inside the environment directory. You can choose another directory with ``mob_init -d <directory>``, but in that case you need to use ``-d <directory>`` in all the ``mob_recon`` and ``mob_typer`` commands.

.. warning::
   If the ``conda create`` command fails in macOS with Apple Silicon, create the environment using the Intel architecture: ``CONDA_SUBDIR=osx-64 conda create -n mobsuite mob_suite``.


Usage
.....

**1. Input/Output files**

``Input``: A genome assembly in ``.fasta`` format (complete or draft). For this part of the Tutorial, we will use the assembled genomes in ``~/tutorial/genomes``.

``Output``: A directory with several files. The most important ones are:

* ``contig_report.txt``: a table with one line for each contig, indicating if it is a ``chromosome`` or a ``plasmid``, and to which plasmid cluster it was assigned.
* ``plasmid_<cluster>.fasta``: the sequences of each reconstructed plasmid (when a plasmid is composed of several contigs, they are in the same file).
* ``chromosome.fasta``: the contigs classified as chromosomal.
* ``mobtyper_results.txt``: the typing of each reconstructed plasmid.
* ``mge.report.txt``: mobile genetic elements (e.g., insertion sequences) found in the contigs.
* ``biomarkers.blast.txt``: the BLAST results of the markers (replicons, relaxases, *oriT*, MPF).

**2. Basic commands**

.. code-block:: bash

   $ cd ~/tutorial/plasmids/mobsuite

   # Run MOB-recon in the EC958 genome
   # -s is the name that will appear in the reports, -n the number of threads and -f overwrites an existing directory
   $ mob_recon -i ~/tutorial/genomes/EC958.fasta -o EC958 -s EC958 -n 4 -f

   # See which sequences were classified as chromosome and plasmids
   $ cut -f 1,2,3,5,6 EC958/contig_report.txt | column -t -s $'\t'

   # See the typing results of each plasmid (replicon, relaxase, mobility...)
   $ cut -f 1,3,6,8,14 EC958/mobtyper_results.txt | column -t -s $'\t'

   # List the files of the reconstructed plasmids
   $ ls EC958/plasmid_*.fasta

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

   # Type a plasmid that you already have in a fasta file (e.g., one of the plasmids reconstructed before)
   $ mob_typer --infile EC958/plasmid_AA735.fasta --out_file EC958_AA735_typing.txt

**4. Running MOB-recon in several genomes**

.. code-block:: bash

   $ cd ~/tutorial
   $ for genome in genomes/*.fasta; do
   >    sample=$(basename $genome .fasta)
   >    echo "Running MOB-recon in ${sample}"
   >    mob_recon -i $genome -o plasmids/mobsuite/${sample} -s ${sample} -n 4 -f > logs/${sample}_mobrecon.log 2>&1
   > done

   # Combine the reconstructed plasmids of all the genomes in a single table
   # The header is taken from the first file (head -n 1) and then only the data lines of all the files are added
   $ head -n 1 plasmids/mobsuite/EC958/mobtyper_results.txt > plasmids/mobsuite_plasmids_all.tsv
   $ for dir in plasmids/mobsuite/*/; do
   >    if [ -s $dir/mobtyper_results.txt ]; then tail -n +2 $dir/mobtyper_results.txt >> plasmids/mobsuite_plasmids_all.tsv; fi
   > done

   # See the main columns: sample, number of contigs, size, replicons, mobility and closest organism
   $ cut -f 1,2,3,6,14,17 plasmids/mobsuite_plasmids_all.tsv | column -t -s $'\t'

   # Combine the contig reports of all the genomes
   $ head -n 1 plasmids/mobsuite/EC958/contig_report.txt > plasmids/mobsuite_contigs_all.tsv
   $ for dir in plasmids/mobsuite/*/; do tail -n +2 $dir/contig_report.txt >> plasmids/mobsuite_contigs_all.tsv; done

   # Count the number of contigs, and the total length (bp), classified as chromosome and as plasmid in each genome
   $ awk -F'\t' 'NR>1 {n[$1" "$2]++; l[$1" "$2]+=$6} END{for (k in n) print k"\t"n[k]"\t"l[k]}' plasmids/mobsuite_contigs_all.tsv | sort

.. note::
   The genomes without plasmids, like *E. coli* K-12, will not have any file ``mobtyper_results.txt`` (the ``if`` in the loop above skips them). Their ``contig_report.txt`` will only have the chromosome.

.. hint::
   |mobsuite| runs in about 40 seconds for a genome with ~1000 contigs. In very large datasets, you can run several genomes in parallel using ``xargs -P`` (see the Bash section).

**5. Reconstructing the plasmids of a draft assembly**

The previous genomes are complete, so they are easy cases. Run now |mobsuite| in the draft assembly that you obtained with |spades| and compare it with the hybrid assembly:

.. code-block:: bash

   # Draft assembly (short reads only): the plasmids are fragmented in several contigs
   $ mob_recon -i ~/tutorial/assembly/spades/strainA_spades_untrimmed.fasta -o plasmids/mobsuite/strainA_spades -s strainA_spades -n 4 -f

   # See which contigs were assigned to each plasmid cluster (the contigs with the same cluster id belong to the same plasmid)
   $ awk -F'\t' '$2=="plasmid" {print $3"\t"$5"\t"$6}' plasmids/mobsuite/strainA_spades/contig_report.txt | sort

   # See the typing of the reconstructed plasmids
   $ cut -f 1,2,3,6,14,17 plasmids/mobsuite/strainA_spades/mobtyper_results.txt | column -t -s $'\t'

For a typical O157:H7 genome, you should find, for example, the large virulence plasmid pO157 (IncFIB and IncFII replicons; ~90 kb) reconstructed from 3 to 4 contigs, and the small plasmid pOSAK1 (~3.3 kb) reconstructed from a single contig. Depending on the strain, other plasmids can be found (e.g., an IncI2 conjugative plasmid of ~57 kb). The sum of the sizes of the contigs of a plasmid will be close to the size of the complete plasmid in the hybrid assembly.

.. todo::
   6. Run |mobsuite| in strainA and strainB. How many plasmids does each strain have? What are their sizes and replicons?
   7. Run the loop in all the genomes. Which plasmids are predicted as **conjugative**? And **mobilizable**? Is it consistent with the presence of a relaxase (``relaxase_type(s)``)?
   8. Compare the replicons found by |mobsuite| (``rep_type(s)``) with the ones found by |plasmidfinder|. Are they the same?
   9. Run |mobsuite| in the SPAdes assembly of strainA. In how many contigs is each plasmid fragmented? How does the total size compare with the plasmids of the hybrid assembly (Unicycler)?
   10. What is the closest plasmid (``mash_nearest_neighbor``) of each reconstructed plasmid? Look for its accession number in `NCBI <https://www.ncbi.nlm.nih.gov/nuccore/>`_.


plasmidSPAdes
*************

* plasmidSPAdes is a mode of |spades| that assembles **plasmids directly from short reads** [ANTIPOV2016B]_.

* It is based on the fact that plasmids usually have a **higher copy number** than the chromosome, so the coverage of the plasmid sequences in the assembly graph is different from the coverage of the chromosomal ones. It searches the assembly graph for the components that have a coverage different from the chromosome and that are compatible with a plasmid.

* Contrary to |mobsuite|, it does not use plasmid databases, so it can find **new plasmids**. However, it does not separate the plasmids from each other and the output may contain **false positives**, i.e., contigs that are not plasmids (e.g., repeated regions of the chromosome, phages).

* It is already installed with |spades| (you installed it together with |unicycler|), so you only need to activate the ``assembly`` environment.


Usage
.....

**1. Input/Output files**

``Input``: Paired-end short reads (``.fastq`` or ``.fastq.gz``). For this part of the Tutorial, we will use the paired-end Illumina raw reads (or the trimmed reads, if you performed the trimming step).

``Output``: A directory with files similar to the standard |spades| output. The most important are ``contigs.fasta`` (the plasmid-like contigs), ``scaffolds.fasta`` and ``assembly_graph.fastg``. The contigs of the same plasmid component have the same ``component`` number in their name.

**2. Basic commands**

.. code-block:: bash

   # Activate the assembly environment
   $ conda activate assembly

   # Run plasmidSPAdes in the strainA short reads
   $ cd ~/tutorial/plasmids/plasmidspades
   $ spades.py --plasmid -1 ~/tutorial/raw_data/strainA_R1.fastq.gz -2 ~/tutorial/raw_data/strainA_R2.fastq.gz -t 4 -o strainA

   # See the number and the names of the contigs assembled
   $ grep '>' strainA/contigs.fasta | head

   # The name of each contig has its length and coverage (e.g., NODE_1_length_56623_cov_17.37_component_1)
   # Print the total number of contigs and the total length (bp)
   $ grep '>' strainA/contigs.fasta | awk -F'_' '{n++; l+=$4} END{print n" contigs, "l" bp"}'

   # Check which replicons are found in the plasmid contigs, using PlasmidFinder
   $ conda activate plasmidfinder
   $ mkdir -p strainA_plasmidfinder
   $ plasmidfinder.py -i strainA/contigs.fasta -o strainA_plasmidfinder -p ~/databases/cge/plasmidfinder_db -x
   $ column -t -s $'\t' strainA_plasmidfinder/results_tab.tsv | cut -c 1-120

.. csv-table:: Parameters explanation when using plasmidSPAdes
   :header: "Parameter", "Description"
   :widths: 20, 60

   "``--plasmid``", "Runs the plasmidSPAdes pipeline for plasmid detection"
   "``--metaplasmid``", "Runs the metaplasmidSPAdes pipeline for plasmids in metagenomic datasets"
   "``-1``, ``-2``", "Forward and reverse paired-end reads"
   "``-t NUM``", "Number of threads"
   "``-o DIR``", "Output directory"

**3. Running plasmidSPAdes in several samples**

.. code-block:: bash

   $ cd ~/tutorial/plasmids/plasmidspades
   $ while read -r sample; do
   >    echo "Running plasmidSPAdes in ${sample}"
   >    spades.py --plasmid -t 4 -1 ~/tutorial/raw_data/${sample}_R1.fastq.gz -2 ~/tutorial/raw_data/${sample}_R2.fastq.gz -o ${sample} > ${sample}.stdout 2>&1
   > done < ~/tutorial/samples.txt

   # Count the contigs and the total length for each sample
   $ for sample in $(cat ~/tutorial/samples.txt); do
   >    grep '>' ${sample}/contigs.fasta | awk -F'_' -v s=$sample '{n++; l+=$4} END{print s"\t"n" contigs\t"l" bp"}'
   > done

.. warning::
   plasmidSPAdes returns **plasmid-like** contigs, not confirmed plasmids. In the example of strainA, the output contains more than 300 contigs (~350 kb), although the real plasmids have, in total, ~150 kb. Always confirm the plasmid contigs with other evidence: replicons (PlasmidFinder), plasmid database hits (|mobsuite|), size, coverage, and circularity.

.. todo::
   11. Run plasmidSPAdes in strainA. How many contigs and total length did you obtain? How does it compare with the plasmids reconstructed by |mobsuite|?
   12. Run |plasmidfinder| in the plasmidSPAdes contigs. Are all the replicons that you found in the whole genome also in these contigs?
   13. Why do you think plasmidSPAdes returned more sequences than the real plasmids?


Complete plasmids in hybrid assemblies
**************************************

With **long reads**, plasmids are usually assembled as **single and circular** sequences. In the hybrid assemblies produced by |unicycler| you can identify them without any special tool, by looking at the sequence headers (as you saw in the assembly section):

.. code-block:: bash

   $ cd ~/tutorial/genomes

   # List the name, length, depth and circularity of all the sequences of the strainA assembly
   $ grep '>' strainA.fasta
   >1 length=5445618 depth=1.00x circular=true
   >2 length=92721 depth=1.13x circular=true
   >3 length=3365 depth=2.31x circular=true

   # Print only the sequences that are circular and that are smaller than 500 kb (plasmid candidates)
   $ grep '>' strainA.fasta | awk '{split($2,l,"="); if ($4=="circular=true" && l[2]<500000) print}'

* The largest sequence (``depth=1.00x``) is the chromosome. Plasmids have a depth **different from the chromosome**; a depth higher than 1 (e.g., ``2.31x``) means that the plasmid has more copies than the chromosome.

* ``circular=true`` means that Unicycler found a closed circular path in the assembly graph, i.e., the plasmid is **complete**. Plasmids without this flag are probably incomplete (or linear).

* You can visualise the assembly graph (``assembly.gfa``) with |bandage| and confirm that the plasmids are separate circular components (rings), disconnected from the chromosome.

* You can then split the assembly into one file for each sequence, to analyse the plasmids separately (e.g., with |plasmidfinder| or ``mob_typer``).

.. code-block:: bash

   # Split a multi-fasta file in one file for each sequence (the name of the file is the first word of the header)
   $ mkdir -p ~/tutorial/plasmids/strainA_sequences
   $ awk '/^>/ {id=substr($1,2); file="'$HOME'/tutorial/plasmids/strainA_sequences/strainA_" id ".fasta"} {print > file}' ~/tutorial/genomes/strainA.fasta
   $ ls ~/tutorial/plasmids/strainA_sequences

   # Type each plasmid sequence with MOB-typer (activate the mobsuite environment first)
   $ conda activate mobsuite
   $ for file in ~/tutorial/plasmids/strainA_sequences/*.fasta; do
   >    mob_typer --infile $file --out_file ${file%.fasta}_mobtyper.txt
   > done

.. note::
   The headers of the example above are only illustrative. Your results (number of plasmids, sizes, depths) will be different. If you were not able to run |unicycler|, you can use the complete genomes of the tutorial (Sakai, EC958 and LT2) to practise these steps, since each of their sequences is a complete and circular replicon.

.. seealso::
   * If you have long reads and you only want to reconstruct the plasmids, `Plassembler <https://github.com/gbouras13/plassembler>`_ is a tool specifically designed to assemble plasmids from hybrid or long-read data (e.g., ``plassembler run``), including small plasmids that are frequently lost by long-read assemblers.

   * For long-read assemblies that were not closed, `Trycycler <https://github.com/rrwick/Trycycler/wiki>`_ and `Flye <https://github.com/mikolmogorov/Flye>`_ followed by polishing are the recommended strategies.

.. todo::
   14. How many plasmids are circular in your hybrid assemblies of strainA and strainB? Are they the same plasmids that |mobsuite| found in the SPAdes draft assembly?
   15. Open the ``assembly.gfa`` of the Unicycler assemblies with |bandage|. Can you find the plasmids?
   16. Run |plasmidfinder| and |mobsuite| in each plasmid of the hybrid assembly. Are the replicons the same that were found in the draft?


Linking plasmids and resistance genes
#####################################

One of the main reasons to reconstruct plasmids is to know **where the resistance genes are**. A gene in a plasmid is more likely to be transferred to other bacteria than a gene in the chromosome.

You already have the two ingredients:

* The resistance genes, with the **contig** where each one was found (AMRFinderPlus: column ``Contig id``; ResFinder: column ``Contig``).
* The classification of each contig in chromosome/plasmid (MOB-suite: ``contig_report.txt``).

You only need to join them by the name of the contig:

.. code-block:: bash

   $ cd ~/tutorial

   # For each genome, list the AMR genes (core, type AMR) of AMRFinderPlus, the contig, and if the contig is a chromosome or a plasmid
   # In the MOB-suite report, the name of the contig is the full header, so we only use the first word (split)
   $ for genome in EC958 Sakai; do
   >    mobsuite_report=plasmids/mobsuite/${genome}/contig_report.txt
   >    awk -F'\t' -v g=$genome 'FNR==NR { if (FNR>1) { split($5,a," "); mol[a[1]]=$2; cl[a[1]]=$3 } next }
   >         FNR>1 && $9=="core" && $10=="AMR" { print g"\t"$7"\t"$12"\t"$3"\t"mol[$3]"\t"cl[$3] }' \
   >         $mobsuite_report amr/amrfinder/${genome}.tsv
   > done | column -t -s $'\t'

The output of this command has the following columns: **genome**, **gene**, **antibiotic class**, **contig**, **molecule** (chromosome or plasmid), and **plasmid cluster**. In EC958, you will find that the genes ``blaCTX-M-15``, ``blaTEM-1``, ``blaOXA-1``, ``aac(6')-Ib-cr``, ``aadA5``, ``sul1``, ``dfrA17``, ``tet(A)``, ``mph(A)`` and ``catB3`` are all in the same plasmid (cluster ``AA735``, IncFIA/IncFII, conjugative), while the ``blaCMY-23`` gene and the point mutations in *gyrA*, *parC* and *parE* are in the chromosome.

.. code-block:: bash

   # Do the same for all the genomes, saving the table in a file
   $ echo -e "genome\tgene\tclass\tcontig\tmolecule\tplasmid_cluster" > amr/amr_location_all.tsv
   $ for dir in plasmids/mobsuite/*/; do
   >    genome=$(basename $dir)
   >    [ -s amr/amrfinder/${genome}.tsv ] || continue
   >    awk -F'\t' -v g=$genome 'FNR==NR { if (FNR>1) { split($5,a," "); mol[a[1]]=$2; cl[a[1]]=$3 } next }
   >         FNR>1 && $9=="core" && $10=="AMR" { print g"\t"$7"\t"$12"\t"$3"\t"mol[$3]"\t"cl[$3] }' \
   >         $dir/contig_report.txt amr/amrfinder/${genome}.tsv >> amr/amr_location_all.tsv
   > done

   # Count the number of AMR genes/mutations in the chromosome and in plasmids of each genome
   $ tail -n +2 amr/amr_location_all.tsv | cut -f 1,5 | sort | uniq -c

.. attention::
   * In **draft assemblies**, the plasmid contigs are fragmented and, in many cases, an AMR gene is at the end of a contig. Check if the contig is classified as a plasmid by |mobsuite|, and if it also has other plasmid markers.
   * Resistance genes that are located in **repetitive elements** (e.g., transposons with several copies, integrons) can be assembled in a contig that is shared by the chromosome and the plasmids, and may be wrongly assigned to only one of them.
   * Genes in **chromosomal contigs** can also be mobile (e.g., in integrative conjugative elements or genomic islands), so the chromosome is not necessarily a stable location.

.. todo::
   17. In which molecule (chromosome or plasmid) are the AMR genes of strainA and strainB?
   18. Which resistance genes are in the plasmid of EC958 and which are in the chromosome? What does it mean for the potential of spreading the resistance?
   19. Do the plasmids of your strains (strainA and strainB) carry any resistance gene? And virulence genes (``--plus`` in AMRFinderPlus)?
   20. Write a short summary (table) of the AMR genes, mutations, replicons and plasmids of all the genomes.


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
    │   ├── amr_location_all.tsv
    ├── plasmids
    │   ├── plasmidfinder
    │   │   ├── <genome>
    │   │   │   ├── results_tab.tsv
    │   │   │   ├── results.txt
    │   │   │   ├── Hit_in_genome_seq.fsa
    │   │   │   ├── Plasmid_seqs.fsa
    │   ├── mobsuite
    │   │   ├── <genome>
    │   │   │   ├── contig_report.txt
    │   │   │   ├── mobtyper_results.txt
    │   │   │   ├── chromosome.fasta
    │   │   │   ├── plasmid_<cluster>.fasta
    │   ├── plasmidspades
    │   │   ├── <sample>
    │   │   │   ├── contigs.fasta
    │   ├── plasmidfinder_all.tsv
    │   ├── mobsuite_plasmids_all.tsv
    │   ├── mobsuite_contigs_all.tsv
    ├── logs


References
##########

.. [ROBERTSON2018] Robertson J, Nash JHE. 2018. MOB-suite: software tools for clustering, reconstruction and typing of plasmids from draft assemblies. Microb Genom. 4(8):e000206. `DOI: 10.1099/mgen.0.000206 <https://dx.doi.org/10.1099/mgen.0.000206>`_.
