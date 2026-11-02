# Manage a Scribus project

Draft: this is an early draft.

Manage the files in a Scribus project through a project.yaml file and one or more scripts.

Currently, only the the imposition of multiple files into a single one is implemented.  
It runs from outside Scribus.

## Install and run

- `pip install -r requirements.txt`
- `python3 imposition-pdf.py samples/2-n-up-a5-to-a4/imposition.yml`
