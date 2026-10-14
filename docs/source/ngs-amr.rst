.. _ngs-amr:

**************************************
Antimicrobial resistance and virulence
**************************************


Introduction
############

1. Antimicrobial resistance (AMR) is the ability of a microorganism to survive in the presence of an antimicrobial drug that would normally inhibit or kill it.

2. From a genomic point of view, resistance can be caused by two main types of genetic determinants:

   * **Acquired genes**: genes that are obtained by horizontal gene transfer, usually located in mobile genetic elements such as **plasmids**, transposons, or integrons (e.g., ``blaCTX-M-15``, ``tet(A)``, ``mcr-1``).
   * **Chromosomal point mutations**: single nucleotide changes, small insertions/deletions, or premature stop codons in genes that are intrinsically present in the genome, such as the genes that encode the antibiotic targets (e.g., *gyrA*, *parC*) or regulators of efflux pumps (e.g., *acrR*).

3. Specialised tools are needed to detect point mutations and to **predict the resistance phenotype** from the genotype.

4. In this section, you will use two complementary approaches to detect AMR:

   * |resfinder| and |pointfinder| (Center for Genomic Epidemiology, Technical University of Denmark), to detect **acquired genes** and **chromosomal mutations**, respectively [BORTOLAIA2020]_ [FLORENSA2022]_ [ZANKARI2017]_.
   * |amrfinder| (National Center for Biotechnology Information), to detect acquired genes, point mutations, and also stress (biocide, metal, heat) and virulence genes [FELDGARDEN2021]_.

5. You will run both tools in the **several genomes** that you prepared in the previous sections and compare the results. |resfinder| will also be run in the **Illumina reads**, while |pointfinder| and |amrfinder| are only run in the assemblies.

6. Finally, you will use |virulencefinder| (Center for Genomic Epidemiology) to detect **virulence genes** [JOENSEN2014]_.

.. attention::
   * The genotype does **not** always predict the phenotype. The presence of a gene does not mean that it is being expressed, and some resistance mechanisms are still unknown.
   * Always report the **versions of the tools and databases** that you used, since the databases are continually updated and the results may change.
   * Do not forget that the quality of the assembly influences the results: an AMR gene can be fragmented between two contigs in a draft assembly, or collapsed (appearing only once) when it is present in several copies.


Learning objectives
###################

After finishing this Tutorial section, you will be able to:

* Distinguish between acquired resistance genes and chromosomal resistance mutations.
* Detect acquired resistance genes and point mutations in assembled genomes using ResFinder/PointFinder and AMRFinderPlus.
* Detect acquired resistance genes directly in the Illumina reads using ResFinder.
* Detect virulence genes using VirulenceFinder.
* Choose the correct **species/organism** option for each genome.
* Run the same analysis in several genomes and **combine the results** into a single table.
* Interpret the identity and coverage values, and compare the results of different tools.
* Evaluate the results of several tools and inputs together, and decide which AMR genes and mutations are confirmed.


Detection of AMR genes and mutations
####################################


ResFinder and PointFinder
*************************

* |resfinder| identifies **acquired antimicrobial resistance genes** by comparing the genome with the ResFinder database, which contains acquired genes curated by the Center for Genomic Epidemiology (CGE). Since version 4, it also predicts the **phenotype** (the antibiotics to which the isolate is predicted to be resistant).

* |pointfinder| identifies **chromosomal point mutations** associated with resistance, using the PointFinder database. These mutations are only available for some species: *Campylobacter*, *Enterococcus faecalis*, *Enterococcus faecium*, *Escherichia coli*, *Helicobacter pylori*, *Klebsiella*, *Mycobacterium tuberculosis*, *Neisseria gonorrhoeae*, *Plasmodium falciparum*, *Salmonella*, and *Staphylococcus aureus*.

* Both are run together by the same program, ``run_resfinder.py`` (ResFinder 4.x), which can use as input **assembled genomes** (``.fasta``, using BLAST) or **raw reads** (``.fastq``, using |kma|).

* You can also run them online on the `CGE website <https://genepi.food.dtu.dk/resfinder>`_, but this is not practical for many genomes.


Installation
............

.. code-block:: bash

   # Deactivate all the current environments
   $ conda deactivate

   # Create a new environment named amr and install ResFinder and AMRFinderPlus (installed in the next section)
   # KMA and BLAST are installed automatically as dependencies
   $ mamba create -n amr resfinder ncbi-amrfinderplus

   # Activate the new environment
   $ conda activate amr

   # Check the installation
   $ run_resfinder.py --version
   $ kma -v
   $ blastn -version

The conda package installs only the program. The **databases** must be downloaded separately from the CGE repositories using ``git`` and indexed with KMA.

.. code-block:: bash

   # Create a directory to keep the databases and go to it
   $ mkdir -p ~/databases/cge
   $ cd ~/databases/cge

   # Download the three databases (acquired resistance genes, point mutations and disinfectant resistance genes)
   $ git clone https://bitbucket.org/genomicepidemiology/resfinder_db.git
   $ git clone https://bitbucket.org/genomicepidemiology/pointfinder_db.git
   $ git clone https://bitbucket.org/genomicepidemiology/disinfinder_db.git

   # Index each database with KMA (run INSTALL.py without any argument, with the amr environment activated)
   $ for db in resfinder_db pointfinder_db disinfinder_db; do (cd $db && python INSTALL.py); done

   # Check the version of the downloaded databases
   $ cat resfinder_db/VERSION pointfinder_db/VERSION disinfinder_db/VERSION

   # Tell ResFinder where the databases are (add these lines to your ~/.bashrc or ~/.zshrc to keep them permanently)
   $ export CGE_RESFINDER_RESGENE_DB=~/databases/cge/resfinder_db
   $ export CGE_RESFINDER_RESPOINT_DB=~/databases/cge/pointfinder_db
   $ export CGE_DISINFINDER_DB=~/databases/cge/disinfinder_db

.. note::
   * If you do not use the ``export`` commands, you must provide the database directories in each run with ``-db_res``, ``-db_point`` and ``-db_disinf``.
   * To **update** the databases in the future, go to each directory, run ``git pull`` and run ``python INSTALL.py`` again.
   * Do not give an argument to ``INSTALL.py`` (e.g., ``non_interactive``), since it will be interpreted as the path of a program and the script will try to compile KMA by itself.

.. warning::
   If the ``mamba create`` command fails in macOS with Apple Silicon, create the environment using the Intel architecture: ``CONDA_SUBDIR=osx-64 mamba create -n amr resfinder ncbi-amrfinderplus``.


Usage
.....

**1. Input/Output files**

``Input``: A genome assembly in ``.fasta`` format (option ``-ifa``) or raw reads in ``.fastq`` format (option ``-ifq``). We will use the Illumina raw reads (acquired genes only) and the assembled genomes in ``~/tutorial/genomes`` (acquired genes and point mutations).

.. note::
   In this Tutorial, |resfinder| is run with a minimum of **80% identity** (``-t 0.80``) and **60% coverage** (``-l 0.60``). These are also the default values, but it is good practice to write them in the command, so that the thresholds are always reported.

``Output``: A directory with several files. The most important ones are:

* ``ResFinder_results_tab.txt``: table with the acquired resistance genes found (one gene per line).
* ``PointFinder_results.txt``: table with the point mutations found.
* ``pheno_table.txt``: predicted phenotype for each antimicrobial (resistant or not, and which genes/mutations explain it).
* ``ResFinder_Hit_in_genome_seq.fsa`` and ``ResFinder_Resistance_gene_seq.fsa``: sequences of the genes in your genome and in the database.
* ``<sample>.json``: all the results in a machine-readable format.

**2. Basic commands**

.. code-block:: bash

   # Let's first create new directories to store the results of all the AMR analyses
   $ cd ~/tutorial
   $ mkdir -p amr/resfinder amr/amrfinder
   $ cd ~/tutorial/amr/resfinder

   # Run ResFinder (acquired genes) and PointFinder (point mutations) in the strainA genome
   # The species of the genome must be provided to run PointFinder
   $ run_resfinder.py -ifa ~/tutorial/genomes/strainA.fasta -o strainA -s "Escherichia coli" --acquired --point -t 0.80 -l 0.60

   # Run ResFinder (acquired genes only) directly in the Illumina raw reads (it uses KMA)
   $ run_resfinder.py -ifq ~/tutorial/raw_data/strainA_R1.fastq.gz ~/tutorial/raw_data/strainA_R2.fastq.gz -o strainA_reads --acquired -t 0.80 -l 0.60

.. csv-table:: Parameters explanation when using ResFinder/PointFinder
   :header: "Parameter", "Description"
   :widths: 20, 60

   "``-ifa FILE``", "Input genome in fasta format (assembled genome)"
   "``-ifq FILE [FILE]``", "Input raw reads in fastq format (one file, or two files for paired-end reads)"
   "``--nanopore``", "Use it if the input reads are Nanopore reads"
   "``-o DIR``", "Output directory (it is created by the program)"
   "``-s SPECIES``", "Species of the sample between quotation marks (e.g., ``""Escherichia coli""``, ``Salmonella``). Required by ``--point``. Use ``other`` if the species is not available in PointFinder"
   "``-acq`` or ``--acquired``", "Run ResFinder for acquired resistance genes"
   "``-c`` or ``--point``", "Run PointFinder for chromosomal mutations"
   "``-d`` or ``--disinfectant``", "Run DisinFinder for disinfectant resistance genes"
   "``-t NUM``", "Minimum identity threshold, between 0 and 1 (default: 0.8; used in this Tutorial: 0.80)"
   "``-l NUM``", "Minimum coverage (length of the hit / length of the gene) between 0 and 1 (default: 0.6; used in this Tutorial: 0.60)"
   "``--ignore_missing_species``", "Do not stop with an error if PointFinder does not have a database for the species provided in ``-s``"
   "``-db_res``, ``-db_point``, ``-db_disinf``", "Directories of the databases (not needed if the environment variables were exported)"

If you open the ``ResFinder_results_tab.txt`` file, you will see the following columns:

   1. **Resistance gene**: name of the gene in the database.
   2. **Identity**: percentage of identical nucleotides between your genome and the database gene.
   3. **Alignment Length/Gene Length**: length of the alignment and length of the gene in the database.
   4. **Coverage**: percentage of the gene that is present in your genome.
   5. **Position in reference**: positions of the gene that are aligned.
   6. **Contig**: name of the sequence (chromosome, plasmid or contig) where the gene was found.
   7. **Position in contig**: start and end of the gene in the sequence.
   8. **Phenotype**: antibiotics to which the gene confers resistance.
   9. **Accession no.**: accession number of the gene in GenBank.

.. note::
   If a gene appears in more than one line (with different accession numbers), it was found with a similar sequence in more than one entry of the database. If the **coverage is lower than 100%** (e.g., ``catB3`` with ~70% in the example genome EC958), the gene may be truncated or interrupted by the end of a contig. Always check these cases.

If you open the ``PointFinder_results.txt`` file, you will see the following columns: the **mutation** (e.g., ``gyrA p.S83L``, serine 83 changed to leucine in the protein), the **nucleotide change** (``TCG -> TTG``), the **amino acid change** (``S -> L``), the **resistance** conferred by the mutation, and the **PMID** of the article that describes it.

**3. Additional options**

.. code-block:: bash

   # To see a full list of available options in ResFinder
   $ run_resfinder.py --help

**4. Running ResFinder/PointFinder in several genomes**

Each genome may belong to a **different species**, so the species must be adjusted for each genome. The easiest way is to create a small tab-separated table with the genome name and the species, and use it in a loop.

.. code-block:: bash

   $ cd ~/tutorial

   # Create a table with the name of the genome and the species
   $ printf "strainA\tEscherichia coli\nstrainB\tEscherichia coli\nSakai\tEscherichia coli\nEC958\tEscherichia coli\nK12\tEscherichia coli\nLT2\tSalmonella\n" > species.tsv

   # Run ResFinder and PointFinder in all the genomes
   $ mkdir -p logs
   while IFS=$'\t' read -r genome species; do
      echo "Running ResFinder in ${genome} (${species})"
      run_resfinder.py -ifa genomes/${genome}.fasta -o amr/resfinder/${genome} -s "${species}" --acquired --point -t 0.80 -l 0.60 > logs/${genome}_resfinder.log 2>&1
   done < species.tsv

   # Run ResFinder (acquired genes only) in the Illumina raw reads of your samples
   $ mkdir -p amr/resfinder_reads
   while read -r sample; do
      echo "Running ResFinder in the reads of ${sample}"
      run_resfinder.py -ifq raw_data/${sample}_R1.fastq.gz raw_data/${sample}_R2.fastq.gz -o amr/resfinder_reads/${sample} --acquired -t 0.80 -l 0.60 > logs/${sample}_resfinder_reads.log 2>&1
   done < samples.txt

.. warning::
   The species must be correct! PointFinder looks for mutations in the genes of the species that you provide. If you run a *Salmonella* genome as if it was *E. coli*, it may find false mutations because the reference sequences are different.

Now you have one directory for each genome. To compare them it is useful to **combine all the results into a single table**:

.. code-block:: bash

   # Combine the acquired genes of all the genomes in a single table (the 1st column is the name of the genome)
   $ echo -e "genome\tgene\tidentity\tcoverage\tphenotype" > amr/resfinder_acquired_all.tsv
   for dir in amr/resfinder/*/; do
      genome=$(basename $dir)
      tail -n +2 $dir/ResFinder_results_tab.txt | awk -F'\t' -v g=$genome '{print g"\t"$1"\t"$2"\t"$4"\t"$8}' >> amr/resfinder_acquired_all.tsv
   done

   # Combine the point mutations of all the genomes in a single table
   $ echo -e "genome\tmutation\tamino_acid_change\tresistance" > amr/pointfinder_all.tsv
   for dir in amr/resfinder/*/; do
      genome=$(basename $dir)
      tail -n +2 $dir/PointFinder_results.txt | awk -F'\t' -v g=$genome '{print g"\t"$1"\t"$3"\t"$4}' >> amr/pointfinder_all.tsv
   done

   # Visualise the tables
   $ column -t -s $'\t' amr/resfinder_acquired_all.tsv | cut -c 1-120
   $ column -t -s $'\t' amr/pointfinder_all.tsv

   # Count the number of different acquired genes in each genome
   $ tail -n +2 amr/resfinder_acquired_all.tsv | cut -f 1,2 | sort -u | cut -f 1 | uniq -c

   # See in which genomes a specific gene was found (e.g., the ESBL gene blaCTX-M-15)
   $ grep -w "blaCTX-M-15" amr/resfinder_acquired_all.tsv

.. todo::
   1. Run ResFinder and PointFinder in strainA and strainB. Which genes and mutations were found? What is the predicted phenotype (``pheno_table.txt``)?
   2. Run the loop in all the genomes. Which genome has more resistance genes? Which genomes do not have any acquired gene?
   3. Is the *Salmonella* LT2 genome truly free of resistance mutations? What happens if you run it with ``-s "Escherichia coli"``?
   4. In which sequence (chromosome or plasmid) are the acquired genes of EC958 located? What does it mean?
   5. Run ResFinder in the **raw reads** of strainA and strainB and compare the results with the ones obtained with the assembled genomes. Are there genes found only in the reads? Why can this happen (e.g., low copy genes that were not assembled)?


AMRFinderPlus
*************

* |amrfinder| identifies **acquired antimicrobial resistance genes** and **point mutations** in assembled nucleotide or protein sequences, using the NCBI Pathogen Detection Reference Gene Catalog and Hidden Markov Models (HMMs) [FELDGARDEN2019]_ [FELDGARDEN2021]_.

* The point mutations are only searched when you specify the **organism** (``--organism``), for the groups of species available. They are listed with ``amrfinder --list_organisms``.

* With the option ``--plus``, |amrfinder| also reports genes related to **stress response** (biocides, metals, acid, heat) and **virulence**, and other genes not directly related to antibiotic resistance.

* It is also the AMR tool included in the Bakta annotation and the one used by NCBI in the Pathogen Detection browser.

* In this Tutorial, |amrfinder| is run in the **assemblies** with its **default thresholds**: the curated identity threshold of each gene (or **90%** identity when there is none) and **50%** coverage of the reference protein.


Installation
............

|amrfinder| was already installed in the ``amr`` environment together with ResFinder. If you want to install it in a separate environment, run ``mamba create -n amrfinder ncbi-amrfinderplus``.

.. code-block:: bash

   # Activate the amr environment
   $ conda activate amr

   # Check the version of the software
   $ amrfinder --version

   # Download (or update) the AMRFinderPlus database
   $ amrfinder --update

   # Check the version of the database that you are using
   $ amrfinder --database_version

   # See the list of organisms for which point mutations are available
   $ amrfinder --list_organisms

.. note::
   The database is saved inside the environment directory (``$CONDA_PREFIX/share/amrfinderplus/data``), and each version has its own directory (named by date). If you use the Bakta database, remember that it contains its own copy of the AMRFinderPlus database (``amrfinder_update --force_update --database <bakta_db>/amrfinderplus-db``).


Usage
.....

**1. Input/Output files**

``Input``: A nucleotide fasta file with the genome (``-n``), and/or a protein fasta file (``-p``) with a GFF file (``-g``) describing the location of the proteins. For this part of the Tutorial, we will use the assembled genomes in ``~/tutorial/genomes``.

``Output``: A tab-separated table, one line for each gene or mutation found.

**2. Basic commands**

.. code-block:: bash

   # Go to the directory where you will keep the results
   $ cd ~/tutorial/amr/amrfinder

   # Run AMRFinderPlus in a genome (nucleotide sequences) and do not search for mutations (no organism provided)
   $ amrfinder -n ~/tutorial/genomes/strainA.fasta -o strainA_no_organism.tsv

   # Run AMRFinderPlus indicating the organism (it adds the point mutations) and adding the name of the genome in the first column
   $ amrfinder -n ~/tutorial/genomes/strainA.fasta -O Escherichia --name strainA --threads 4 -o strainA.tsv

   # Add the "plus" genes: stress response and virulence
   $ amrfinder -n ~/tutorial/genomes/strainA.fasta -O Escherichia --plus --name strainA --threads 4 -o strainA_plus.tsv

   # Use the proteins and the annotation produced by Bakta (it is faster, and gives the protein identifiers of Bakta)
   $ amrfinder -n ~/tutorial/annotation/bakta/strainA/strainA.fna -p ~/tutorial/annotation/bakta/strainA/strainA.faa -g ~/tutorial/annotation/bakta/strainA/strainA.gff3 -a bakta -O Escherichia --plus --name strainA -o strainA_bakta.tsv

.. csv-table:: Parameters explanation when using AMRFinderPlus
   :header: "Parameter", "Description"
   :widths: 20, 60

   "``-n FILE``", "Input nucleotide fasta file (genome or contigs)"
   "``-p FILE``", "Input protein fasta file"
   "``-g FILE``", "GFF file with the location of the proteins (it must be used with ``-n`` and ``-p``)"
   "``-a FORMAT``", "Type of GFF file: ``bakta``, ``genbank``, ``prokka``, ``pgap``, ``prodigal``, ``standard``, etc. (default: genbank)"
   "``-O ORGANISM``", "Organism, to search for point mutations and to remove intrinsic genes (e.g., ``Escherichia``, ``Salmonella``, ``Klebsiella_pneumoniae``). See ``--list_organisms``"
   "``--plus``", "Add the stress response, virulence, and other genes to the report"
   "``--name NAME``", "Text to add as the first column of the report (e.g., the name of the genome)"
   "``-o FILE``", "Output file (default: print in the terminal)"
   "``--threads N``", "Maximum number of threads (default: 4)"
   "``-i NUM``", "Minimum proportion of identity (0 to 1). By default, it uses curated thresholds of each gene (and 0.9 otherwise)"
   "``-c NUM``", "Minimum coverage of the reference protein (0 to 1) (default: 0.5)"
   "``--mutation_all FILE``", "Save in a file all the positions checked for mutations, including the susceptible (wild-type) ones"
   "``--nucleotide_output FILE``", "Save the nucleotide sequences of the elements found"
   "``-u`` or ``--update``", "Update the database"
   "``-q``", "Quiet mode: suppress messages in the terminal"

The AMRFinderPlus output has the following main columns:

   1. **Name**: name that you gave with ``--name`` (only if used).
   2. **Protein id**, **Contig id**, **Start**, **Stop**, **Strand**: identifier and location of the element found.
   3. **Element symbol** and **Element name**: name of the gene (e.g., ``blaCTX-M-15``) or of the mutation (e.g., ``gyrA_S83L``) and its description.
   4. **Scope**: ``core`` (the main AMR elements) or ``plus`` (extra elements reported with ``--plus``).
   5. **Type** and **Subtype**: type of element (``AMR``, ``STRESS``, ``VIRULENCE``) and its subtype (e.g., ``AMR`` for a gene, ``POINT`` for a mutation, ``POINT_DISRUPT`` for a gene disrupted by a mutation like a frameshift, ``BIOCIDE``, ``METAL``).
   6. **Class** and **Subclass**: antibiotic class and, when known, the specific antibiotics (e.g., ``BETA-LACTAM`` / ``CEPHALOSPORIN``).
   7. **Method**: how the element was found (e.g., ``EXACTX``/``EXACTP``: 100% identical to a reference sequence; ``ALLELEX``/``ALLELEP``: identical to a known allele; ``BLASTX``/``BLASTP``: similar to a reference; ``PARTIALX``/``PARTIALP``: partial hit; ``POINTX``/``POINTP``: point mutation; ``HMM``: found with an HMM). The ``X`` means that the search was done in nucleotide (translated) sequences and the ``P`` in protein sequences.
   8. **Target length**, **Reference sequence length**, **% Coverage of reference**, **% Identity to reference**, **Alignment length**: details of the alignment with the closest reference.
   9. **Closest reference accession** and **Closest reference name**: reference of the database that was most similar.

**3. Additional options**

.. code-block:: bash

   # To see a full list of available options in AMRFinderPlus
   $ amrfinder --help

**4. Running AMRFinderPlus in several genomes**

As in ResFinder, each genome may need a different organism option. Note that the organism names are **not** the same as in ResFinder (e.g., ``Escherichia`` for AMRFinderPlus vs. ``"Escherichia coli"`` for ResFinder; ``Salmonella`` is the same). Use ``amrfinder --list_organisms`` to see the available ones. For genomes of species that do not have an organism available, run the command without ``-O``.

.. code-block:: bash

   $ cd ~/tutorial

   # Create a table with the name of the genome and the organism
   $ printf "strainA\tEscherichia\nstrainB\tEscherichia\nSakai\tEscherichia\nEC958\tEscherichia\nK12\tEscherichia\nLT2\tSalmonella\n" > organisms.tsv

   # Run AMRFinderPlus in all the genomes
   while IFS=$'\t' read -r genome organism; do
      echo "Running AMRFinderPlus in ${genome} (${organism})"
      amrfinder -n genomes/${genome}.fasta -O ${organism} --plus --name ${genome} --threads 4 -o amr/amrfinder/${genome}.tsv -q
   done < organisms.tsv

   # Combine all the results in a single table (keeping only one header)
   $ awk 'FNR==1 && NR!=1 {next} {print}' amr/amrfinder/*.tsv > amr/amrfinder_all.tsv

   # Number of elements found in each genome, by scope (core/plus) and type (AMR/STRESS/VIRULENCE)
   $ awk -F'\t' 'NR>1 {print $1"\t"$9"\t"$10}' amr/amrfinder_all.tsv | sort | uniq -c

   # Print only the main AMR genes and mutations (scope = core, type = AMR) of all the genomes
   $ awk -F'\t' 'NR==1 || ($9=="core" && $10=="AMR")' amr/amrfinder_all.tsv | cut -f 1,7,11,12 | column -t -s $'\t'

   # Count the number of AMR genes/mutations of each antibiotic class in each genome
   $ awk -F'\t' 'NR>1 && $9=="core" && $10=="AMR" {print $1"\t"$12}' amr/amrfinder_all.tsv | sort | uniq -c

   # Separate the acquired genes (subtype AMR) from the point mutations (subtype POINT)
   $ awk -F'\t' 'NR==1 || ($10=="AMR" && $11=="AMR")' amr/amrfinder_all.tsv > amr/amrfinder_genes.tsv
   $ awk -F'\t' 'NR==1 || ($10=="AMR" && $11 ~ /^POINT/)' amr/amrfinder_all.tsv > amr/amrfinder_mutations.tsv

.. note::
   If the number of genomes is very high, you can run several genomes in parallel with ``xargs -P`` (see the Bash section), using ``--threads 1`` in each run.

.. warning::
   Provide the **correct organism**. For example, if you run the *Salmonella* LT2 genome with ``-O Escherichia``, AMRFinderPlus reports point mutations (e.g., ``parC_S57T``) that are not real, since they are only differences between the two species. With ``-O Salmonella`` no resistance elements are found in this laboratory strain.

.. todo::
   6. Run |amrfinder| in strainA and strainB. How many AMR genes and mutations were found (``Scope = core`` and ``Type = AMR``)?
   7. Run the loop in all the genomes. Which genomes have point mutations? Which antibiotic classes are affected in EC958?
   8. Run |amrfinder| with and without ``--plus``. What type of extra elements are reported?
   9. Run |amrfinder| using the proteins annotated by |bakta| (``-p``, ``-g`` and ``-a bakta``). Are the results the same as using only the genome?


Comparing the tools
###################

Now that you have the results of |resfinder| and |amrfinder|, compare them.

.. csv-table:: Main differences between the tools used to detect AMR
   :header: "Feature", "ResFinder/PointFinder", "AMRFinderPlus"
   :widths: 20, 30, 30

   "Method", "BLAST or KMA (nucleotide)", "BLAST (translated) and HMMs"
   "Input", "Assembled genomes or reads", "Assembled genomes or proteins"
   "Acquired genes", "Yes (ResFinder)", "Yes"
   "Point mutations", "Yes (PointFinder; for 11 species)", "Yes (for some organisms)"
   "Phenotype prediction", "Yes", "Class/subclass of the gene (not a phenotype)"
   "Database", "ResFinder, PointFinder, DisinFinder", "NCBI Reference Gene Catalog"
   "Thresholds used in this Tutorial", "80% identity, 60% coverage", "Default: curated per gene (or 90% identity), 50% coverage"
   "Other genes", "Disinfectants", "Stress (biocide, metal) and virulence (``--plus``)"

For example, in the EC958 genome (*E. coli* ST131 with an extended-spectrum β-lactamase plasmid) you should find, among others:

.. csv-table:: Main resistance determinants expected in the EC958 genome
   :header: "Class", "Gene/mutation", "Location"
   :widths: 25, 40, 25

   "β-lactams (including 3rd generation cephalosporins)", "``blaCTX-M-15``, ``blaTEM-1``, ``blaOXA-1``, ``blaCMY-23``", "Plasmid pEC958 (``blaCMY-23``: chromosome)"
   "Aminoglycosides", "``aadA5``, ``aac(6')-Ib-cr``", "Plasmid pEC958"
   "Fluoroquinolones", "``aac(6')-Ib-cr``; mutations ``gyrA`` S83L and D87N, ``parC`` S80I and E84V, and ``parE`` I529L", "Plasmid / chromosome"
   "Sulfonamides, trimethoprim", "``sul1``, ``dfrA17``", "Plasmid pEC958"
   "Tetracyclines, macrolides, phenicols", "``tet(A)``, ``mph(A)``, ``catB3``", "Plasmid pEC958"

The strains Sakai and K-12 do not have any acquired resistance gene, and the *Salmonella* LT2 only has the cryptic aminoglycoside acetyltransferase ``aac(6')-Iaa``.

.. todo::
   10. Compare the results of |resfinder| and |amrfinder| in the EC958 genome. Which genes are found by both tools? Which genes are only found by one of them? Why?
   11. Do both tools detect the same mutations in *gyrA* and *parC*?
   12. In your strains (strainA and strainB), are there any resistance genes located in plasmids? In the next section, you will learn how to confirm this.
   13. Why is the gene ``catB3`` found with only 70% coverage by ResFinder, but it is reported as ``PARTIALP`` by AMRFinderPlus when using the Bakta annotation?


Evaluating the AMR results together
###################################

You now have **three** AMR results for each of your samples: |resfinder| in the reads, |resfinder| in the assembly, and |amrfinder| in the assembly (and two for the point mutations: |pointfinder| and |amrfinder|). They will not always agree. Instead of choosing one tool, the results are **evaluated together**, following a few simple rules:

1. **Primary result**: |amrfinder| in the assembly (it compares proteins, and reports if a gene is complete, partial or interrupted).
2. **Validation**: the gene is also found by |resfinder| in the assembly.
3. **Rescue**: a gene that is partial in the assembly (e.g., split at the end of a contig) is accepted if |resfinder| finds it complete in the **reads**.
4. **Mutations**: the point mutations of |pointfinder| and |amrfinder| are combined.

**1. Combining the results of the three methods**

The following commands create a table with one line per gene and genome, and one column per method. For |amrfinder| the column shows the **method** (e.g., ``EXACTX``, ``PARTIALX``), and for |resfinder| the **coverage** (%) of the gene; ``-`` means that the gene was not found.

.. code-block:: bash

   $ cd ~/tutorial
   $ echo -e "genome\tgene\tAMRFinderPlus_assembly\tResFinder_assembly\tResFinder_reads" > amr/amr_evaluation_all.tsv
   for genome in genomes/*.fasta; do
      g=$(basename $genome .fasta)
      {
         # AMRFinderPlus: acquired AMR genes (scope core, type AMR, subtype AMR) and the method
         awk -F'\t' 'NR>1 && $9=="core" && $10=="AMR" && $11=="AMR" {print $7"\tamrfinder\t"$14}' amr/amrfinder/${g}.tsv
         # ResFinder in the assembly: gene and coverage
         tail -n +2 amr/resfinder/${g}/ResFinder_results_tab.txt | awk -F'\t' '{print $1"\tres_assembly\t"$4}'
         # ResFinder in the reads (only for your samples)
         [ -s amr/resfinder_reads/${g}/ResFinder_results_tab.txt ] && \
            tail -n +2 amr/resfinder_reads/${g}/ResFinder_results_tab.txt | awk -F'\t' '{print $1"\tres_reads\t"$4}'
      } | awk -F'\t' -v g=$g '{gene[$1]=1; hit[$1 SUBSEP $2]=$3}
            END {for (x in gene) {
                    a = ((x SUBSEP "amrfinder") in hit) ? hit[x SUBSEP "amrfinder"] : "-"
                    r = ((x SUBSEP "res_assembly") in hit) ? hit[x SUBSEP "res_assembly"] : "-"
                    q = ((x SUBSEP "res_reads") in hit) ? hit[x SUBSEP "res_reads"] : "-"
                    print g"\t"x"\t"a"\t"r"\t"q}}' | sort >> amr/amr_evaluation_all.tsv
   done

   # Visualise the table
   $ column -t -s $'\t' amr/amr_evaluation_all.tsv

   # Point mutations: PointFinder ("gyrA p.S83L") is converted to the AMRFinderPlus format ("gyrA_S83L")
   $ echo -e "genome\tmutation\tAMRFinderPlus\tPointFinder" > amr/mutations_evaluation_all.tsv
   for genome in genomes/*.fasta; do
      g=$(basename $genome .fasta)
      {
         awk -F'\t' 'NR>1 && $10=="AMR" && $11 ~ /^POINT/ {print $7"\tamrfinder"}' amr/amrfinder/${g}.tsv
         tail -n +2 amr/resfinder/${g}/PointFinder_results.txt | awk -F'\t' '{m=$1; sub(/ p\./, "_", m); print m"\tpointfinder"}'
      } | awk -F'\t' -v g=$g '{mut[$1]=1; hit[$1 SUBSEP $2]=1}
            END {for (x in mut) print g"\t"x"\t"(((x SUBSEP "amrfinder") in hit) ? "yes" : "-")"\t"(((x SUBSEP "pointfinder") in hit) ? "yes" : "-")}' | sort >> amr/mutations_evaluation_all.tsv
   done
   $ column -t -s $'\t' amr/mutations_evaluation_all.tsv

.. attention::
   The same gene can have **different names** in the two databases (e.g., ``aac(6')-Ib-cr`` in |resfinder| and ``aac(6')-Ib-cr5`` in |amrfinder|), and |resfinder| can report the same gene in several lines (similar entries of the database). In these cases the gene appears in two lines of the table, each one found by only one tool. Before deciding that the tools disagree, check if they are the **same gene** (e.g., the same contig and position).

**2. Decision table**

Use the following table to classify each gene of ``amr_evaluation_all.tsv``. A **complete** hit by |amrfinder| is one found with the methods ``EXACT``, ``ALLELE`` or ``BLAST``; a **partial or interrupted** hit is one found with ``PARTIAL``, ``PARTIAL_CONTIG_END``, ``INTERNAL_STOP`` or only by ``HMM``. A hit of |resfinder| is accepted with at least **60% coverage** (and 80% identity).

.. csv-table:: Decision table for the AMR genes
   :header: "AMRFinderPlus (assembly)", "ResFinder (assembly)", "ResFinder (reads)", "Decision", "Interpretation"
   :widths: 18, 15, 15, 12, 40

   "Complete", "Found", "Any", "**Confirmed**", "Both tools agree in the assembly."
   "Complete", "Not found", "Any", "**Confirmed**", "The primary tool found a complete gene. Check if |resfinder| reports it with another name, or if the gene is not in the ResFinder database."
   "Partial or interrupted", "Any", "Found (complete)", "**Confirmed** (rescued)", "The gene is complete in the reads, so it was probably split at the end of a contig or has an assembly error."
   "Partial or interrupted", "Any", "Not found or not run", "**Check**", "The gene may be truncated, interrupted (frameshift, internal stop) or at the end of a contig. Look at its position and coverage; it may not be functional."
   "Not found", "Found", "Any", "**Check**", "Only |resfinder| found it: check the name, the identity and the coverage, and if it is the same gene as another hit of |amrfinder|."
   "Not found", "Not found", "Found", "**Reads only**", "The gene is in the reads but not in the assembly: low copy number (e.g., a small plasmid that was not assembled), a contamination, or a false positive. Check the assembly and the contamination results."

.. attention::
   **None ≠ absent**: if a gene is not detected, it does not mean that it is absent. Genes can be missed because of a poor sequence or assembly quality, a low coverage (e.g., GC/AT bias), the limitations of the detection method, or gaps and errors in the database. The **reads only** category is an example: the gene is in the sample, but not in the assembly. If the result is critical, try another assembly, tool or database, or sequence the sample again.

.. csv-table:: Decision table for the point mutations
   :header: "AMRFinderPlus", "PointFinder", "Decision"
   :widths: 20, 20, 60

   "Found", "Found", "**Confirmed**"
   "Found", "Not found", "**Check**: the mutation may not be in the PointFinder database, or the species option (``-s``/``-O``) may be wrong"
   "Not found", "Found", "**Check**: the mutation may not be in the AMRFinderPlus database, or the species option may be wrong"

**3. How confident are we about a gene?**

The decision table tells you if a gene is detected. To know how confident you can be that the gene is present **and functional**, look at both the **% identity** of the alignment and the **% coverage** of the reference gene:

.. csv-table:: Confidence in the presence of a gene
   :header: "Identity", "Coverage", "Interpretation"
   :widths: 20, 20, 60

   "High (> 98%)", "Full or close to full", "**High confidence** in the presence of a functional gene."
   "High", "Partial", "The gene may be **truncated**, or split at the end of a contig (contig break): its function may be reduced. Check it in the reads (rescue)."
   "Low", "Any, or very short", "A **novel variant** or a **false positive**. Needs a careful interpretation."

Always interpret the hits in the context of the read depth, the assembly quality, the species and, when available, the phenotypic data (antimicrobial susceptibility testing).

.. note::
   Some genes need a special interpretation, even when they are **confirmed**:

   * **Intrinsic genes**: genes that are naturally present in all the isolates of a species and do not confer acquired resistance (e.g., ``blaEC`` in *E. coli*). |amrfinder| removes most of them when you use the ``-O`` option.
   * **Low-level resistance**: genes that only increase the MIC a little, so the isolate may still be classified as susceptible (e.g., ``qnrS1`` for fluoroquinolones).
   * **Variants that are not ESBL**: some β-lactamase variants are not extended-spectrum β-lactamases, although they belong to a family with ESBL variants (e.g., ``blaTEM-135``). Always check the exact variant.
   * **Context-dependent genes**: the effect of some genes depends on their genetic context (expression level, regulatory region, other genes). For example, ``mph(A)`` (macrolides) is part of the operon *mph(A)*-*mrx*-*mphR(A)*. Isolates of *E. coli* and *Salmonella* with ``mph(A)`` can be **susceptible** to azithromycin when the operon or its regulatory region is disrupted (e.g., by the insertion of an IS\ *Ecp1*-*bla*\ :sub:`CTX-M-1` transposition unit) [MIRENA2024]_.

   **Detection ≠ resistance**: the detection of a gene or mutation suggests resistance, but it does not guarantee it. Phenotypic antimicrobial susceptibility testing remains the reference for clinical decisions.

.. todo::
   14. Build the tables ``amr_evaluation_all.tsv`` and ``mutations_evaluation_all.tsv``. Classify each gene and mutation of strainA, strainB and EC958 using the decision tables.
   15. Is there any gene found only in the reads of strainA or strainB? What could be the reason?
   16. Which genes of EC958 need to be checked (e.g., ``catB3``)? Why can the public genomes not be rescued with the reads?
   17. Write the final list of confirmed AMR genes and mutations of each genome.


Detection of virulence genes
############################


VirulenceFinder
***************

* |virulencefinder| identifies **virulence genes** by comparing the genome (or the reads) with the VirulenceFinder database of the Center for Genomic Epidemiology [JOENSEN2014]_ [MALBERGTETZSCHNER2020]_.

* The database is divided by species groups (e.g., *E. coli*, *Enterococcus*, *Listeria*, *Staphylococcus aureus*). For *E. coli*, it includes the **Shiga toxin** genes (*stx*), used for the subtyping of Shiga toxin-producing *E. coli* (STEC), such as strainA and strainB.

* In this Tutorial, |virulencefinder| (version 2.0.4) is used for the detection of virulence genes (instead of the ``--plus`` option of |amrfinder|), with a minimum of **90% identity** and **60% coverage**.


Installation
............

.. code-block:: bash

   # Deactivate all the current environments
   $ conda deactivate

   # Create a new environment named virulencefinder and install VirulenceFinder
   $ mamba create -n virulencefinder virulencefinder=2.0.4

   # Activate the new environment
   $ conda activate virulencefinder

   # Download the database and index it with KMA (as for ResFinder)
   $ cd ~/databases/cge
   $ git clone https://bitbucket.org/genomicepidemiology/virulencefinder_db.git
   $ cd virulencefinder_db
   $ python INSTALL.py

   # Check the version of the database
   $ cat VERSION

   # See the databases available (one per species group)
   $ cat config


Usage
.....

**1. Input/Output files**

``Input``: A genome assembly in ``.fasta`` format, or the raw reads in ``.fastq`` format.

``Output``: A directory with several files. The most important ones are ``results_tab.tsv`` (table with the virulence genes found), ``results.txt`` (results and alignments) and ``data.json`` (all the results in a machine-readable format).

**2. Basic commands**

.. code-block:: bash

   $ mkdir -p ~/tutorial/amr/virulencefinder/strainA
   $ cd ~/tutorial/amr/virulencefinder

   # Run VirulenceFinder in the strainA genome, using all the databases
   $ virulencefinder.py -i ~/tutorial/genomes/strainA.fasta -o strainA -p ~/databases/cge/virulencefinder_db -t 0.90 -l 0.60 -x

   # See the results
   $ column -t -s $'\t' strainA/results_tab.tsv | cut -c 1-150

.. csv-table:: Parameters explanation when using VirulenceFinder
   :header: "Parameter", "Description"
   :widths: 20, 60

   "``-i FILE``", "Input genome (``.fasta``) or reads (``.fastq``)"
   "``-o DIR``", "Output directory (it must already exist)"
   "``-p DIR``", "Path to the VirulenceFinder database"
   "``-d NAMES``", "Databases to use, separated by commas (see the ``config`` file of the database; default: all)"
   "``-t NUM``", "Minimum identity, between 0 and 1 (default: 0.90; used in this Tutorial: 0.90)"
   "``-l NUM``", "Minimum coverage, between 0 and 1 (default: 0.60; used in this Tutorial: 0.60)"
   "``-x``", "Extended output: also write the tables and the alignments"

The ``results_tab.tsv`` file has the following main columns: the **database**, the **virulence factor** (gene), the **identity**, the **query/template length** (coverage), the **contig** and **position** where the gene was found, the **protein function** and the **accession number**.

**3. Running VirulenceFinder in several genomes**

.. code-block:: bash

   $ cd ~/tutorial
   for genome in genomes/*.fasta; do
      name=$(basename $genome .fasta)
      mkdir -p amr/virulencefinder/${name}
      virulencefinder.py -i $genome -o amr/virulencefinder/${name} -p ~/databases/cge/virulencefinder_db -t 0.90 -l 0.60 -x > logs/${name}_virulencefinder.log 2>&1
   done

   # Combine the results of all the genomes in a single table
   $ echo -e "genome\tdatabase\tgene\tidentity\tcontig" > amr/virulencefinder_all.tsv
   for dir in amr/virulencefinder/*/; do
      genome=$(basename $dir)
      tail -n +2 $dir/results_tab.tsv | awk -F'\t' -v g=$genome '{print g"\t"$1"\t"$2"\t"$3"\t"$5}' >> amr/virulencefinder_all.tsv
   done
   $ column -t -s $'\t' amr/virulencefinder_all.tsv

.. todo::
   18. Run |virulencefinder| in all the genomes. Which genomes carry Shiga toxin genes (*stx*)? Which subtypes?
   19. Compare the virulence genes of strainA and strainB with the ones of Sakai (STEC O157:H7) and K12 (laboratory strain). What do you notice?
   20. In which sequences (chromosome or plasmids) are the virulence genes located?


Folder structure
################

At the end of this section, you will have the following folder structure (only the new folders are detailed).

::

    tutorial
    ├── samples.txt
    ├── species.tsv
    ├── organisms.tsv
    ├── raw_data
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
    ├── annotation
    ├── amr
    │   ├── resfinder
    │   │   ├── <genome>
    │   │   │   ├── ResFinder_results_tab.txt
    │   │   │   ├── PointFinder_results.txt
    │   │   │   ├── pheno_table.txt
    │   │   │   ├── <genome>.json
    │   ├── resfinder_reads
    │   │   ├── <sample>
    │   ├── amrfinder
    │   │   ├── <genome>.tsv
    │   ├── virulencefinder
    │   │   ├── <genome>
    │   │   │   ├── results_tab.tsv
    │   ├── resfinder_acquired_all.tsv
    │   ├── pointfinder_all.tsv
    │   ├── amrfinder_all.tsv
    │   ├── amr_evaluation_all.tsv
    │   ├── mutations_evaluation_all.tsv
    │   ├── virulencefinder_all.tsv
    ├── logs


References
##########

.. [BORTOLAIA2020] Bortolaia V, et al. 2020. ResFinder 4.0 for predictions of phenotypes from genotypes. J Antimicrob Chemother. 75(12):3491-3500. `DOI: 10.1093/jac/dkaa345 <https://dx.doi.org/10.1093/jac/dkaa345>`_.
.. [FELDGARDEN2019] Feldgarden M, et al. 2019. Validating the AMRFinder Tool and Resistance Gene Database by Using Antimicrobial Resistance Genotype-Phenotype Correlations in a Collection of Isolates. Antimicrob Agents Chemother. 63(11):e00483-19. `DOI: 10.1128/AAC.00483-19 <https://dx.doi.org/10.1128/AAC.00483-19>`_.
.. [FELDGARDEN2021] Feldgarden M, et al. 2021. AMRFinderPlus and the Reference Gene Catalog facilitate examination of the genomic links among antimicrobial resistance, stress response, and virulence. Sci Rep. 11:12728. `DOI: 10.1038/s41598-021-91456-0 <https://dx.doi.org/10.1038/s41598-021-91456-0>`_.
.. [FLORENSA2022] Florensa AF, Kaas RS, Clausen PTLC, Aytan-Aktug D, Aarestrup FM. 2022. ResFinder - an open online resource for identification of antimicrobial resistance genes in next-generation sequencing data and prediction of phenotypes from genotypes. Microb Genom. 8(1):000748. `DOI: 10.1099/mgen.0.000748 <https://dx.doi.org/10.1099/mgen.0.000748>`_.
.. [JOENSEN2014] Joensen KG, Scheutz F, Lund O, Hasman H, Kaas RS, Nielsen EM, Aarestrup FM. 2014. Real-time whole-genome sequencing for routine typing, surveillance, and outbreak detection of verotoxigenic Escherichia coli. J Clin Microbiol. 52(5):1501-1510. `DOI: 10.1128/JCM.03617-13 <https://dx.doi.org/10.1128/JCM.03617-13>`_.
.. [MALBERGTETZSCHNER2020] Malberg Tetzschner AM, Johnson JR, Johnston BD, Lund O, Scheutz F. 2020. In Silico Genotyping of Escherichia coli Isolates for Extraintestinal Virulence Genes by Use of Whole-Genome Sequencing Data. J Clin Microbiol. 58(10):e01269-20. `DOI: 10.1128/JCM.01269-20 <https://dx.doi.org/10.1128/JCM.01269-20>`_.
.. [MIRENA2024] Azithromycin resistance in Escherichia coli and Salmonella from food-producing animals and meat in Europe. 2024. J Antimicrob Chemother. 79:1657–1667. `DOI: 10.1093/jac/dkae161 <https://dx.doi.org/10.1093/jac/dkae161>`_.
.. [ZANKARI2017] Zankari E, et al. 2017. PointFinder: a novel web tool for WGS-based detection of antimicrobial resistance associated with chromosomal point mutations in bacterial pathogens. J Antimicrob Chemother. 72(10):2764-2768. `DOI: 10.1093/jac/dkx217 <https://dx.doi.org/10.1093/jac/dkx217>`_.
