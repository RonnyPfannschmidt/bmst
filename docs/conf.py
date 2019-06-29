# -*- coding: utf-8 -*-
# sys.path.insert(0, os.path.abspath('.'))

# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ["sphinx.ext.autodoc", "sphinx.ext.doctest", "sphinx.ext.viewcode"]

templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"

project = "backup meta store"
copyright = "2010, Ronny Pfannschmidt"

version = "0.0"
release = "0.0"

exclude_patterns = ["_build"]

pygments_style = "sphinx"

html_theme = "default"
htmlhelp_basename = "backupmetastoredoc"
