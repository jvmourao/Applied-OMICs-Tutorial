# Applied-OMICs-Tutorial

Introductory tutorial for the Applied OMICs curricular unit of the Master in Computational Biology.

Using the Linux/macOS command line, you will go from raw sequencing reads to a characterised bacterial genome, always showing how to run each command in **one genome** and in **several genomes** (Bash loops).

## Contents

- **Before we begin**: Bash commands (files, pipes, tables, variables, loops, scripts)
- **Tools installation**: Miniforge/conda, environments, channels
- **Data acquisition**: SRA reads and NCBI genomes (SRA Toolkit, ncbi-genome-download)
- **Quality control**: coverage, FastQC, MultiQC, BBDuk
- **Taxonomy**: Kraken2, Bracken, Krona
- **De novo assembly**: SPAdes, Unicycler, Bandage, QUAST
- **Genome annotation**: Bakta, ABRicate, IGV, BUSCO
- **Antimicrobial resistance genes/mutations**: ResFinder/PointFinder, AMRFinderPlus
- **Plasmid detection and reconstruction**: PlasmidFinder, MOB-suite, plasmidSPAdes

## Building the documentation

The tutorial is written in reStructuredText and built with [Sphinx](https://www.sphinx-doc.org/).

```bash
python3 -m venv tutorialenv
source tutorialenv/bin/activate
pip install sphinx sphinx_rtd_theme
cd docs
make html        # output in docs/build/html
```

## Contact

joana.mourao@uc.pt or [@jvmourao](https://github.com/jvmourao)
