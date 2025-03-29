# Search and replace fonts in the whole document

Search a font variant in the whole document and replace it with a different font variant.

## Implementation details

Shows a Tkinter dialog with two lists of fonts.

The script words that start with the searched font: changes of font in the middle of a word are not supported.

It's very likely that RTL languages are not correctly supported, but it might be easy to add (I can't test it since I don't have any test documents for it).

## Notes

- [Tkinter list box with a search filter](http://deneb.click/tkinter-list-box-with-a-search-filter/)
