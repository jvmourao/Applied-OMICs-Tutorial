**************************************************
Welcome to Applied OMICs Tutorial's documentation!
**************************************************

Welcome to the introductory tutorial for the curricular unit of Applied OMICs where you will learn fundamental bioinformatics analysis using mainly Linux command-line.

During this tutorial, we will use real next-generation sequencing (NGS) data retrieved from the Sequence Read Archive (SRA). In the end, you will be able to assemble and analyze bacterial genomes, to detect antimicrobial resistance genes and mutations, and to detect and reconstruct plasmids, running all the analyses in several genomes.

If you have any doubts about this tutorial, you can contact me through my email **joam@food.dtu.dk** or **GitHub** account `@jvmourao <https://github.com/jvmourao>`_.


Prerequisites
#############

Almost none. This course is an introduction, so the only thing that you need to know is where to find your Terminal. You will need a computer with Linux, macOS, or Windows with WSL, ~16 GB of RAM and ~100 GB of free disk space for the full analysis (less if you use the lighter databases or the provided data).
If you are not used to using the terminal you can find a small tutorial in the :ref:`Before we begin <before-begin>` section


.. only:: builder_html

   Contents
   --------

.. toctree::
   :maxdepth: 4

   objectives

.. toctree::
   :maxdepth: 4
   :caption: Beginners

   before-begin

.. toctree::
   :numbered:
   :maxdepth: 8
   :caption: Advanced

   ngs-tools
   ngs-data
   ngs-qc
   ngs-taxonomy
   ngs-assembly
   ngs-annotations
   ngs-amr
   ngs-plasmids

.. toctree::
   :maxdepth: 4
   :caption: Resources

   downloads

.. only:: latex

   .. raw:: latex

      \listoffigures
      \listoftables
