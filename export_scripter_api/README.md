# Export the API documentation

Exports the list of all Scripter commands and their docstrings to a set of Markdown files.

## Requirements

- This scripts runs from inside Scribus
- It needs a Scribus 1.5.6svn newer than mid August 2020 (and `__file__` being correctly set)

## Usage

You can run `export-scripter-api.py` from inside of Scribus or run `run-export-scripter-api.py` from a terminal (it will launch Scribus with `export-scripter-api.py`).

This will create the scripter API documentation by reading the _docstrings_ defind in the Scribus source code.

The markdown files are written into an `out` directory next to the script itself.

The script also writes `out/mkdocs.yml`, a configuration file that can be used with `mkdocs` to generate Html files.

Finally, `out/logs.txt` contains the list of the functions and constants that have not be processed by the rules defined in the `run-export-script-api.json` config.  
You can use it to check that all commands are included in the documentation.

## Exporting with mkdocs

`mkdocs` can use the Markdown files created by this script to create a directory of static HTML files:

- The script creates a `out/mkdocs.yml` config file for mkdocs.
- in the `out/` directory, run `mkdocs build && cp ../in/README.md site/`
- View or upload your files.
- The result can be seen here: <http://impagina.org/scribus-scripter-api/>

## Implementation details

### The configuration file

The behavior of the script is configured with the file `export-api.json` next to the script itself.

- `files`: List of files that should be copied to the `out/` directory.
- `output`: List of sections with their titles, in the order used in the table of contents.
- `source`: List of sections with the functions, variables constants and classes to be included.

  The items can be assigned to a section through:

  - regular expressions,
  - explicit listing.

  For each section, functions will first be checked by list and thenby regular expresion.  
  Each set of constants can only be defined by list _or_ by regular expressions.  
  The order of the entries relates to the order of the regular expressions (as an example `masterpage` is defined before `page`).

## Todo

- [ ] Merge the two script and make it self calling if Scribus is not running.
- [ ] improve the `scribus.__doc__` text
- [ ] add the default values to the class members (most of all PDFExport)
- [ ] optionally import markdown files for single commands (by checking if a file by the same name as the command exists)
- [ ] allow commenting on single commands (inline comments or as link to github / gilab)
- [ ] some function might be useful in multiple places. as an example, "getCustomLineStyle" and "setCustomLineStyle" are captured by "other styles" but might also need to be referenced in "Lines"
- [ ] evaluate <https://github.com/egoist/docute> to create a vue.js site with on the fly reading of md files.
  - [ ] it should have some search functionalities (<https://docute.org/plugin-api#apienablesearchoptions>)
- [ ] improve the signature of the functions in the code by using the typing and explicit default values
 - [ ] `setInfo(author: str, info: str, description:str) -> bool
 - [ ] `getAllObjects(page: int = None) -> list
 - [ ] (This new convention has been retained by the team and will be implemented step by step)

## Notes

- It seems to be impossible to get the signature of functions defined in Cython. we will need to parse the first line of the docstring
- Search:
  - [MiniSearch, a client-side full-text search engine](https://lucaongaro.eu/blog/2019/01/30/minisearch-client-side-fulltext-search-engine.html)
  - <https://github.com/bvaughn/js-search>
  - <https://www.oreilly.com/library/view/javascript-application-cookbook/1565925777/ch01.html>
  - <https://lunrjs.com/>
