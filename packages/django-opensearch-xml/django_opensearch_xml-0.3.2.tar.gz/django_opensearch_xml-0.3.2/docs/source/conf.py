# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import pprint

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys
from pathlib import Path

project = "django-opensearch-xml"
copyright = "2025, François GUÉRIN <fguerin@ville-tourcoing.fr>"  # noqa: A001
author = "François GUÉRIN <fguerin@ville-tourcoing.fr>"
version = "0.3"
release = "0.3.2"
SRC_PATH = (Path(__file__).parents[2] / "src").resolve()
sys.path.append(str(SRC_PATH))
print(f"DEV::sys.path = {pprint.pformat(sys.path)}", file=sys.stderr)  # noqa

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
