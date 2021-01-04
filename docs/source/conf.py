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
import os
import sys
path_1 = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), "etldr")
path_2 = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())))
sys.path.insert(0, path_1)
sys.path.insert(0, path_2)

# -- use m2r to convert README to *.rst --------------------------------------
import m2r
path_to_readme = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), "README.md")
rst = m2r.parse_from_file(path_to_readme)

with open("README.rst", "a+") as file:
    file.seek(0)
    file.truncate()
    file.write(rst)

# -- Project information -----------------------------------------------------

project = 'ETL_data_reader'
copyright = '2021, CaptainDario'
author = 'CaptainDario'

# The full version, including alpha/beta/rc tags
release = '1.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.napoleon'
]

source_suffix = ['.rst', '.md']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'classic'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']