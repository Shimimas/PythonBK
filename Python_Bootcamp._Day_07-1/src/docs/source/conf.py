import os
import sys

sys.path.insert(0, os.path.abspath('../../internal/'))

project = 'Day_7'
copyright = '2023, dagwynet'
author = 'dagwynet'
release = '2.28'

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'
