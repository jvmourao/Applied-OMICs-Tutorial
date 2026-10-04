.. _ngs-tools:

******************
Tools installation
******************

* Before you start this Tutorial, you need to have installed |conda| in your UNIX-based system.

* |conda| is an open-source package management system and environment management system that runs on Windows, macOS, and Linux, that can:

  * Quickly install, runs and update packages and their dependencies.

  * Easily create, save, load, and switch between environments on your local computer.

* |conda| was created for Python programs, but it can package and distribute software for any language.

To check if you already have |conda| installed open the Terminal and type:

.. code-block:: bash

   $ conda --version

.. figure:: ./images/Conda_version.png
   :figclass: align-left

*Figure 3. macOS Terminal showing the current version of conda.*

If you see the version number on the Terminal screen, you can skip the section "How to install conda". However, I suggest you update conda for the last version.
To do this you can run on the Terminal window:

.. code-block:: bash

   $ conda update conda


How to install conda
####################

Conda is included in all versions of |anaconda|, |miniconda| and |miniforge|. For this Tutorial, you will install |miniforge|.
Miniforge is a minimal installer that includes conda, mamba, Python and uses the **conda-forge** channel by default. You will use conda to install almost all the tools for this Tutorial easily.

.. attention::
   Contrarily to Miniforge, if you are interested in the hundreds of packages included with the Anaconda Distribution remember that this will require a lot of disk space in your computer (minimum 5 GB to download and install).
   Additionally, the ``defaults`` channel of Anaconda has `terms of service <https://www.anaconda.com/legal/terms/terms-of-service>`_ that may restrict its use in some institutions. This is why in this Tutorial the ``defaults`` channel is **not** used.

The example provided below is for a standard installation on a Linux-based system or macOS (both Intel and Apple Silicon). For Windows, install first the WSL (see :ref:`Before we begin <before-begin>`) and follow the Linux instructions. More details can be found in the |miniforge| official page.

1. Download the latest Miniforge installer by typing in the Terminal window:

.. code-block:: bash

   $ curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"

.. note::
   In alternative to Terminal, you can download the installer directly from the Miniforge `releases page <https://github.com/conda-forge/miniforge/releases/latest>`_.

2. To install conda, type in your Terminal window:

.. code-block:: bash

   $ bash Miniforge3-$(uname)-$(uname -m).sh

3. Follow the prompts that will appear on the installer screen and accept all the default settings.

.. attention::
   At the end of the installation when the installer prompts "Do you wish to update your shell profile to automatically initialize conda?" it is recommended to say "YES" to run conda correctly and smoothly.

4. Close and re-open your Terminal window to make the changes take effect.

5. To verify your installation type on Terminal window ``conda list``. If you see a list of installed packages, you are ready to go.

6. At the end of this Tutorial if you no longer want to have installed |miniforge| you can simply remove it by typing:

.. code-block:: bash

   # Remove Miniforge installation directory
   $ rm -rf ~/miniforge3

   # Remove additional hidden files and folders that you created
   $ rm -rf ~/.condarc ~/.conda

.. note::
   If you installed |miniconda| or |anaconda| instead, the installation directory is ``~/miniconda3`` or ``~/anaconda3``, respectively.

.. hint::
   The command ``mamba`` is a faster drop-in replacement of ``conda`` (e.g., ``mamba install fastqc``) and it is included in Miniforge. All ``conda install`` and ``conda create`` commands of this Tutorial can be run with ``mamba`` or with ``conda`` (recent conda versions use the same fast solver as mamba).


How to create environments
##########################

A `conda environment <https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/environments.html>`_ is a directory that can contain several installed conda packages for a specific project.
For example, you can have several conda environments, each one with different packages that required different Python versions.
You can quickly **activate** or **deactivate** environments, and because of that, they will work independently, thus minimizing the risk of incompatibilities between installed packages.

In this Tutorial, you will create several conda environments and install all the required packages to analyze and assemble bacterial genomes. All these steps will be performed in the Terminal window.

1. To create an environment with ``conda`` for Python development you can run:

.. code-block:: bash

   # This will create an environment with the same Python version as your current Shell Python interpreter
   $ conda create -n ENVNAME python

.. note::
   Replace **ENVNAME** by the name of your environment (e.g., omics).

.. code-block:: bash

   # This will create an environment with a different Python version (e.g., 3.11)
   $ conda create -n ENVNAME python=3.11

2. You can also install at the same time all the packages that you want to include in the environment.

.. code-block:: bash

   # This will create an environment with Python and NumPy
   $ conda create -n ENVNAME python=3.11 numpy

.. attention::
   It is recommended that you install all the packages at the same time to help avoid dependency conflicts.

3. To **activate** a specific environment run:

.. code-block:: bash

   $ conda activate ENVNAME

4. To **deactivate** a specific environment run:

.. code-block:: bash

   $ conda deactivate

.. figure:: ./images/Conda_environment.png
   :figclass: align-left

*Figure 4. macOS Terminal showing an activated environment named "assembly".*


How to install packages
#######################

1. Setting up conda channels

After creating your environment and before installing any packages, first you need to set up the conda channels.
A `channel <https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/channels.html>`_ is a location where the packages tools are stored and can be easily accessed.

In this Tutorial you will use two conda channels, **conda-forge** and **bioconda**, that should be added in this order by running (only once):

.. code-block:: bash

    $ conda config --add channels bioconda
    $ conda config --add channels conda-forge
    $ conda config --set channel_priority strict

.. attention::
   The channel added **last** has the **highest priority**; therefore, ``conda-forge`` must be added after ``bioconda``. Do not use the ``defaults`` channel. You can check the result with ``conda config --show channels``.

.. warning::
   Some bioconda packages are not yet available for **macOS with Apple Silicon (M1/M2/M3...)**. If a package is not found, create the environment using the Intel architecture, which runs through Rosetta 2:
   ``CONDA_SUBDIR=osx-64 conda create -n ENVNAME``, and then ``conda activate ENVNAME`` followed by ``conda config --env --set subdir osx-64``.

2. Install conda packages and tools

* To install new packages in your environment first activate your environment ``conda activate ENVNAME`` and second run:

.. code-block:: bash

    # Installing a new package
    # Replace PKGNAME by the name of your package
    $ conda install PKGNAME

    # For example, this will install two packages called abricate and bwa
    $ conda install abricate bwa

* You can also install packages without activating your environment although in this case, you need to specify the environment name in the command line as:

.. code-block:: bash

    # Install a package in an existing environment without activating it
    $ conda install -n ENVNAME PKGNAME

    # Create an environment and install a package at the same time
    $ conda create -n ENVNAME PKGNAME

    # In this case, it will install in the environment "annotation" the package "abricate"
    $ conda install -n annotation abricate

.. seealso::
   You can find in this `link <https://anaconda.org/bioconda/repo?access=all>`_ a full list of all available bioconda packages.
   All tools will be installed as you need them in the different sections of the tutorial.

Here is a list of all packages that you will install throughout the Tutorial. The versions shown are the latest ones at the time of writing; newer versions may be available when you run it (use ``conda search PKGNAME`` to check).

.. csv-table::
   Table with a full list of packages and tools needed for this Tutorial.
   :header: "Package name", "Version", "Tutorial section", "Environment", "Conda command"
   :widths: 20, 10, 20, 10, 20

   "sra-tools", "3.4.1", "Data acquisition", "data", "``conda install sra-tools``"
   "ncbi-genome-download", "0.3.3", "Data acquisition", "data", "``conda install ncbi-genome-download``"
   "ncbi-acc-download", "0.2.8", "Data acquisition", "data", "``conda install ncbi-acc-download``"
   "fastqc", "0.13.0", "Quality control", "qc", "``conda install fastqc``"
   "multiqc", "1.35", "Quality control", "multiqc", "``conda install multiqc``"
   "bbmap (BBTools)", "40.02", "Quality control", "qc", "``conda install bbmap``"
   "kraken2", "2.17.2", "Taxonomy", "taxonomy", "``conda install kraken2 bracken``"
   "bracken", "3.1", "Taxonomy", "taxonomy", "This package is installed together with Kraken2"
   "krona", "2.8.1", "Taxonomy", "taxonomy", "``conda install krona``"
   "unicycler", "0.5.1", "De novo genome assembly", "assembly", "``conda install unicycler``"
   "spades", "4.3.0", "De novo genome assembly", "assembly", "This package will be installed with Unicycler"
   "bandage", "0.9.0", "De novo genome assembly", "home directory", "https://rrwick.github.io/Bandage/"
   "quast", "5.3.0", "De novo genome assembly", "qc", "``conda install quast``"
   "bakta", "1.12.1", "Genome annotation", "bakta", "``conda install bakta``"
   "abricate", "1.4.0", "Genome annotation", "abricate", "``conda install abricate``"
   "busco", "6.1.0", "Genome annotation", "busco", "``conda install busco``"
   "resfinder", "4.7.2", "Antimicrobial resistance", "amr", "``conda install resfinder ncbi-amrfinderplus``"
   "ncbi-amrfinderplus", "4.2.7", "Antimicrobial resistance", "amr", "This package is installed together with ResFinder"
   "kma", "1.6.17", "Antimicrobial resistance and plasmids", "amr, plasmidfinder", "This package is installed together with ResFinder and PlasmidFinder"
   "plasmidfinder", "2.1.6", "Plasmids", "plasmidfinder", "``conda install plasmidfinder``"
   "mob_suite", "3.1.9", "Plasmids", "mobsuite", "``conda install mob_suite``"


Conda cheat sheet
#################

.. code-block:: bash

    # See a list of all created environments
    $ conda info -e

    # Print a list of all installed packages and version in the current environment
    $ conda list

    # Delete an entire environment
    $ conda remove --name ENVNAME --all

    # Remove unused cached files including unused packages
    $ conda clean --yes --all

    # Update all packages
    $ conda update --all --yes --name ENVNAME # Without activating the environment
    $ conda update --all --yes # With environment activated

    # Save the exact list of installed packages and versions to a file (reproducibility)
    $ conda list --name ENVNAME --export > ENVNAME_packages.txt

    # Export the environment to a YAML file and re-create it in another computer
    $ conda env export --name ENVNAME --from-history > ENVNAME.yml
    $ conda env create --file ENVNAME.yml

    # Update a specific package
    $ conda update -n ENVNAME PKGNAME # Without activating the environment
    $ conda update PKGNAME # With environment activated

    # Remove a specific package
    $ conda uninstall -n ENVNAME PKGNAME # Without activating the environment
    $ conda uninstall PKGNAME # With environment activated
