.. _ngs-amr:

****************************************
Antimicrobial resistance genes/mutations
****************************************


Introduction
############

1. Antimicrobial resistance (AMR) is the ability of a microorganism to survive in the presence of an antimicrobial drug that would normally inhibit or kill it.

2. From a genomic point of view, resistance can be caused by two main types of genetic determinants:

   * **Acquired genes**: genes that are obtained by horizontal gene transfer, usually located in mobile genetic elements such as **plasmids**, transposons, or integrons (e.g., ``blaCTX-M-15``, ``tet(A)``, ``mcr-1``).
   * **Chromosomal point mutations**: single nucleotide changes, small insertions/deletions, or premature stop codons in genes that are intrinsically present in the genome, such as the genes that encode the antibiotic targets (e.g., *gyrA*, *parC*) or regulators of efflux pumps (e.g., *acrR*).

3. In the previous section, you used |abricate|, which detects the presence of genes using BLAST. However, specialised tools are needed to detect point mutations and to **predict the resistance phenotype** from the genotype.

4. In this section, you will use two complementary approaches:

   * |resfinder| and |pointfinder| (Center for Genomic Epidemiology, Technical University of Denmark), to detect **acquired genes** and **chromosomal mutations**, respectively [BORTOLAIA2020]_ [FLORENSA2022]_ [ZANKARI2017]_.
   * |amrfinder| (National Center for Biotechnology Information), to detect acquired genes, point mutations, and also stress (biocide, metal, heat) and virulence genes [FELDGARDEN2021]_.

5. You will run both tools in the **several genomes** that you prepared in the previous sections and compare the results.

.. attention::
   * The genotype does **not** always predict the phenotype. The presence of a gene does not mean that it is being expressed, and some resistance mechanisms are still unknown.
   * Always report the **versions of the tools and databases** that you used, since the databases are continually updated and the results may change.
   * Do not forget that the quality of the assembly influences the results: an AMR gene can be fragmented between two contigs in a draft assembly, or collapsed (appearing only once) when it is present in several copies.


Learning objectives
###################

After finishing this Tutorial section, you will be able to:

* Distinguish between acquired resistance genes and chromosomal resistance mutations.
* Detect acquired resistance genes and point mutations in assembled genomes using ResFinder/PointFinder and AMRFinderPlus.
* Choose the correct **species/organism** option for each genome.
* Run the same analysis in several genomes and **combine the results** into a single table.
* Interpret the identity and coverage values, and compare the results of different tools.


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

``Input``: A genome assembly in ``.fasta`` format (option ``-ifa``) or raw reads in ``.fastq`` format (option ``-ifq``). For this part of the Tutorial, we will use the assembled genomes in ``~/tutorial/genomes``.

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
   $ run_resfinder.py -ifa ~/tutorial/genomes/strainA.fasta -o strainA -s "Escherichia coli" --acquired --point

   # Run only ResFinder (acquired genes), i.e., without the species
   $ run_resfinder.py -ifa ~/tutorial/genomes/strainA.fasta -o strainA_acquired --acquired

   # Run ResFinder with different thresholds (minimum 90% identity and 80% coverage) and also DisinFinder
   $ run_resfinder.py -ifa ~/tutorial/genomes/strainA.fasta -o strainA_strict -s "Escherichia coli" --acquired --point --disinfectant -t 0.90 -l 0.80

   # Run ResFinder directly in the raw reads (it uses KMA)
   $ run_resfinder.py -ifq ~/tutorial/raw_data/strainA_R1.fastq.gz ~/tutorial/raw_data/strainA_R2.fastq.gz -o strainA_reads -s "Escherichia coli" --acquired --point

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
   "``-t NUM``", "Minimum identity threshold, between 0 and 1 (default: 0.8)"
   "``-l NUM``", "Minimum coverage (length of the hit / length of the gene) between 0 and 1 (default: 0.6)"
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
      run_resfinder.py -ifa genomes/${genome}.fasta -o amr/resfinder/${genome} -s "${species}" --acquired --point > logs/${genome}_resfinder.log 2>&1
   done < species.tsv

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
   5. Run ResFinder in the **raw reads** of strainA and compare the results with the ones obtained with the assembled genome.


AMRFinderPlus
*************

* |amrfinder| identifies **acquired antimicrobial resistance genes** and **point mutations** in assembled nucleotide or protein sequences, using the NCBI Pathogen Detection Reference Gene Catalog and Hidden Markov Models (HMMs) [FELDGARDEN2019]_ [FELDGARDEN2021]_.

* The point mutations are only searched when you specify the **organism** (``--organism``), for the groups of species available. They are listed with ``amrfinder --list_organisms``.

* With the option ``--plus``, |amrfinder| also reports genes related to **stress response** (biocides, metals, acid, heat) and **virulence**, and other genes not directly related to antibiotic resistance.

* It is also the AMR tool included in the Bakta annotation and the one used by NCBI in the Pathogen Detection browser.


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

Now that you have the results of |abricate|, |resfinder| and |amrfinder|, compare them.

.. csv-table:: Main differences between the tools used to detect AMR
   :header: "Feature", "ABRicate", "ResFinder/PointFinder", "AMRFinderPlus"
   :widths: 20, 20, 25, 25

   "Method", "BLAST (nucleotide)", "BLAST or KMA (nucleotide)", "BLAST (translated) and HMMs"
   "Input", "Assembled genomes", "Assembled genomes or reads", "Assembled genomes or proteins"
   "Acquired genes", "Yes", "Yes (ResFinder)", "Yes"
   "Point mutations", "No", "Yes (PointFinder; for 11 species)", "Yes (for some organisms)"
   "Phenotype prediction", "No", "Yes", "Class/subclass of the gene (not a phenotype)"
   "Database", "Several (including ResFinder and NCBI)", "ResFinder, PointFinder, DisinFinder", "NCBI Reference Gene Catalog"
   "Other genes", "Virulence, plasmids", "Disinfectants", "Stress (biocide, metal) and virulence (``--plus``)"

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
   10. Compare the results of |abricate| (``resfinder`` and ``ncbi`` databases), |resfinder| and |amrfinder| in the EC958 genome. Which genes are found by all the tools? Which genes are only found by one of them? Why?
   11. Which tools detected the mutations in *gyrA* and *parC*? Why did |abricate| not detect them?
   12. In your strains (strainA and strainB), are there any resistance genes located in plasmids? In the next section, you will learn how to confirm this.
   13. Why is the gene ``catB3`` found with only 70% coverage by ResFinder, but it is reported as ``PARTIALP`` by AMRFinderPlus when using the Bakta annotation?


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
    │   ├── amrfinder
    │   │   ├── <genome>.tsv
    │   ├── resfinder_acquired_all.tsv
    │   ├── pointfinder_all.tsv
    │   ├── amrfinder_all.tsv
    ├── logs


References
##########

.. [BORTOLAIA2020] Bortolaia V, et al. 2020. ResFinder 4.0 for predictions of phenotypes from genotypes. J Antimicrob Chemother. 75(12):3491-3500. `DOI: 10.1093/jac/dkaa345 <https://dx.doi.org/10.1093/jac/dkaa345>`_.
.. [FELDGARDEN2021] Feldgarden M, et al. 2021. AMRFinderPlus and the Reference Gene Catalog facilitate examination of the genomic links among antimicrobial resistance, stress response, and virulence. Sci Rep. 11:12728. `DOI: 10.1038/s41598-021-91456-0 <https://dx.doi.org/10.1038/s41598-021-91456-0>`_.
.. [FLORENSA2022] Florensa AF, Kaas RS, Clausen PTLC, Aytan-Aktug D, Aarestrup FM. 2022. ResFinder - an open online resource for identification of antimicrobial resistance genes in next-generation sequencing data and prediction of phenotypes from genotypes. Microb Genom. 8(1):000748. `DOI: 10.1099/mgen.0.000748 <https://dx.doi.org/10.1099/mgen.0.000748>`_.
.. [ZANKARI2017] Zankari E, et al. 2017. PointFinder: a novel web tool for WGS-based detection of antimicrobial resistance associated with chromosomal point mutations in bacterial pathogens. J Antimicrob Chemother. 72(10):2764-2768. `DOI: 10.1093/jac/dkx217 <https://dx.doi.org/10.1093/jac/dkx217>`_.
