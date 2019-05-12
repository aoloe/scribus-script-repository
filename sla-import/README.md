# SLA Import

Imports all pages of an SLA file into another one

Usage:
scribus -g -py sla-import.py base_file.sla import_file.sla --page PAGE

Optional arguments:
  --page PAGE  Pages are imported in relation to this page (required)
  --before     Imports pages *before* instead of *after* `--page`

:copyright: Martin Folkers

Licensed under [MIT](https://opensource.org/licenses/MIT)
