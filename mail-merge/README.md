# Mail merge

This is a small Mail merge solution for Scribus.

By default the script looks for a CSV (`.csv`) file with the same name as the current Scribus file (`sla`) and creates one Pdf for each row in the CSV.

The behavior can be configured through a `json` file with the same name as the `.sla` file but the extension `conf.json`.  
A dialog is planned.

This script has been inspired by the [Scribus Generator](https://github.com/berteh/ScribusGenerator).

## Features

- Replace placeholders with data from a `csv` file
- Create one Pdf per row in the data.
- Data can be in Json or CSV format.
- Images can also depend on the data..
- The behavior can be configured with a Json file.

The main differences with the ScribusGenerator are:

- This script parses the document inside of Scribus, instead of using XML to replace the placeholders.
- This script uses configuration files instead of command line options (the planned dialog will also create a configuration file).

## Usage

The most simple usage:

- Create a Scribus document.
- Define the placeholders with the `{` and `}` _markers_ and save the document.
- The formatting of the placeholders will be respected (the first character after the start marker will be decisive).
- Put a `csv` with the same name as the Scribus document close to it (if your document is named `letter.sla` the data source will be `letter.csv`).
- In the first line of the `csv` file put the name of the placeholders, separated by commas.
- The other rows of the `csv` files will contain the values, also separated by commas.
- The CSV file must be valid: you will probably want to generate it with a spreadsheet and avoid filling it by hand.
- For images use names like `images/portrait-{name}.jpg`, where `{name}` will be replaced by the name of the person. The images will be at the _calculated_ path.

With a configuration file (with the `conf.json` extension: for `letter.sla` you will use `letter.conf.json` you can set:

  - Set alternative markers for the placeholders.
  - Define a data source.
  - Use Json instead of CSV data sources.
  - Output to a single Scribus file (instead of multiple Pdf files).

An example of configuration file:

```json
{
    "placeholder": {
        "start": "<",
        "end": ">"
    },
    "data": {
        "file": "data.json",
        "format": "json"
    },
    "output": {
        "pdf": false,
        "single-sla": true
    }
}
```

## Status

This script is not feature complete, but is already usable for a few use cases.

- The script can be partially (for now) configured with a file that has the same name as the template, but the suffix `.conf.json`
- It goes through the whole document and looks for placeholders (_labels_ between `{` and `}`) in all text frames and stores the list of frame names and placeholder positions.
- It reads a data source as CSV or Json
- For CSV files the first row is a header with the name of the fields.
- You need to save the _template_ document before running the script (unsaved changes will be used for the first row and then discarded for the other rows).
- The script replaces all occurrences of the placeholders with the matching values in the current row of the `csv` file.
- It can create one Pdf for each row in the CSV
  - The Pdf is saved it next to the Scribus file, with the value of each first field added to the file name.
  - After each row, the document is reverted to the saved state and the replacements are discarded.
- As an alternative, it can add pages to the Scribus document, one page per row in the CSV.

## Todo

Some planned improvements:

- read data from json files
- improve the configuration:
  - use a variable length for the placeholders
  - custom separator for csv files
  - pdf settings
    - version
    - target directory
    - variable file name field
    - base name
- log errors
  - unmatched fields
- read the default settings from a json file stores next to `mail-merge.py`
  - how to get the current script path? (when the script runs in Scribus)

## Future plans

- Allow the creation of a single Pdf with all the created content.
- Fill one single page with multiple records:
  - the scribus Generator is doing many records on a page by using a special command to be put in a text frame (supposing that the order of the frames is _right_)
  - we should group items and set a specific attribute (in that case we should inspect groups while scanning the document for fields)
  - it should duplicate the page before starting the replacement and automatically create new pages when there are no fillable records (we will need to rescan the page to discover the new frame names)
  - this might be a separate script (we can merge them later if it's easier)
  - see the tickets 15889 and 15888 for the missing features in the scripter.
  - for this we will probably need to inspect the content of groups: <https://bugs.scribus.net/view.php?id=15889>
- Variable colors (cf. the scribus generator)


## Notes

### Import pages

A try to get the original pages through `importPage` (fails, because Scribus renames the items in non predictable way: <https://bugs.scribus.net/view.php?id=15960>)

```py
scribus.saveDocAs(str(pdf_path.joinpath(pdf_base_filename + '-' + 'merged'+'.sla')))
page_count = scribus.pageCount()
for row in reader:
    n = scribus.pageCount()
    for frame, placeholders in text_frames:
        fill_text_placeholders(frame, placeholders, row)
        scribus.setItemName(frame + '-' + str(n), frame)
    for frame, placeholders in image_frames:
        fill_image_placeholders(frame, placeholders, row)
        scribus.setItemName(frame + '-' + str(n), frame)
    scribus.importPage(sla_template_filename, tuple(range(1, page_count + 1)))
for i in range(0, page_count):
    scribus.deletePage(scribus.pageCount())
```
