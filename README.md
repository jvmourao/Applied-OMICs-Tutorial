# Applied-OMICs-Tutorial

Introductory tutorial for the Applied OMICs curricular unit of the Master in Computational Biology.

Using the Linux/macOS command line, you will go from raw sequencing reads to a characterised bacterial genome, always showing how to run each command in **one genome** and in **several genomes** (Bash loops).

## Contents

- **Before we begin**: Bash commands (files, pipes, tables, variables, loops, scripts)
- **Tools installation**: Miniforge3 (mamba), environments, channels
- **Data acquisition**: SRA reads and NCBI genomes (SRA Toolkit, ncbi-genome-download)
- **Quality control**: coverage, FastQC, MultiQC, fastp (Illumina); NanoPlot, Chopper, Porechop, Filtlong (Nanopore)
- **Taxonomy and contamination**: Kraken2, Bracken, Krona, ConFindr
- **De novo assembly**: Shovill, Autocycler, Dnaapler, Polypolish, Unicycler, QUAST, CheckM2
- **Genome annotation**: Bakta, MLST
- **Antimicrobial resistance and virulence**: ResFinder/PointFinder, AMRFinderPlus, VirulenceFinder
- **Plasmid detection and reconstruction**: PlasmidFinder, MOB-suite, plASgraph2

## Building the documentation

The tutorial is written in reStructuredText and built with [Sphinx](https://www.sphinx-doc.org/).

```bash
mamba create -n sphinx -c conda-forge sphinx sphinx_rtd_theme
conda activate sphinx
cd docs
make html        # output in docs/build/html
```

## Contact

joam@food.dtu.dk or [@jvmourao](https://github.com/jvmourao)
