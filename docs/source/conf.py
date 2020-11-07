# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'Applied OMICs Tutorial'
copyright = '2020, Joana Mourão'
author = 'Joana Mourão'

# The short X.Y version.
version = "1.0"

# The full version, including alpha/beta/rc tags
release = '2020.1.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.todo",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
import sphinx_rtd_theme

html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []
# rtd
html_context = {
    "display_github": True,
    "github_user": "jvmourao",
    "github_repo": "Applied-OMICs-Tutorial",
    "github_version": "master/docs/source/",
}

# -- Options for HTMLHelp output ---------------------------------------------

# Language to be used for generating the HTML full-text search index.
# Output file base name for HTML help builder.
htmlhelp_basename = "AppliedOMICsDoc"

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#
html_logo = "./Images/Logo.png"

# -- Options for LaTeX output ---------------------------------------------

latex_engine = 'pdflatex'
latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    "papersize": "a4paper",
    # The font size ('10pt', '11pt' or '12pt').
    #
    "pointsize": "10pt",
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    "preamble": r"""
        \usepackage{charter}
        \usepackage[defaultsans]{lato}
        \usepackage{inconsolata}
    	""",
    # Latex figure (float) alignment
    #
    #'figure_align': 'htbp',
}

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#
latex_use_parts = False

# If true, show page references after internal links.
#
latex_show_pagerefs = True

# If true, show URL addresses after external links.
# one of:
# 'no' – do not display URLs (default)
# 'footnote' – display URLs in footnotes
# 'inline' – display URLs inline in parentheses

latex_show_urls = "footnote"

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)

rst_epilog = """
.. |abricate| replace:: `ABRicate <https://github.com/tseemann/abricate>`__
.. |anaconda| replace:: `Anaconda <https://docs.anaconda.com/anaconda/install/>`__
.. |bandage| replace:: `Bandage <https://rrwick.github.io/Bandage/>`__
.. |bbduk| replace:: `BBDuk <https://jgi.doe.gov/data-and-tools/bbtools/bb-tools-user-guide/bbduk-guide/>`__
.. |bbtools| replace:: `BBTools <https://jgi.doe.gov/data-and-tools/bbtools/bb-tools-user-guide/>`__
.. |bracken| replace:: `Bracken <https://ccb.jhu.edu/software/bracken/>`__
.. |busco| replace:: `BUSCO <https://busco.ezlab.org/>`__
.. |conda| replace:: `conda <https://conda.io/projects/conda/en/latest/index.html>`__
.. |fastqc| replace:: `FastQC <http://www.bioinformatics.babraham.ac.uk/projects/fastqc/>`__
.. |go| replace:: `GO <http://geneontology.org/>`__
.. |multiqc| replace:: `MultiQC <https://multiqc.info/>`__
.. |kraken| replace:: `Kraken2 <https://github.com/DerrickWood/kraken2/blob/master/docs/MANUAL.markdown>`__
.. |krona| replace:: `Krona <https://github.com/marbl/Krona/wiki>`__
.. |miniconda| replace:: `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`__
.. |ncbi| replace:: `NCBI <https://www.ncbi.nlm.nih.gov/>`__
.. |phred| replace:: `Phred <https://en.wikipedia.org/wiki/Phred_quality_score>`__
.. |prokka| replace:: `Prokka <https://github.com/tseemann/prokka>`__
.. |quast| replace:: `Quast <http://quast.sourceforge.net/quast>`__
.. |rast| replace:: `RAST <https://rast.nmpdr.org/>`__
.. |spades| replace:: `SPAdes <https://github.com/ablab/spades/blob/spades_3.14.1/README.md>`__
.. |sra| replace:: `SRA <https://www.ncbi.nlm.nih.gov/sra>`__
.. |unicycler| replace:: `Unicycler <https://github.com/rrwick/Unicycler>`__
"""
