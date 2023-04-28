# Replace a list of patterns

Replace a list of patterns in the current text frame.

## Usage

You need to set the replacements you need in the `replacements` list:

```py

replacements = (
    ("search", "replace"), # <- your list of search/replace tuples
)
```

The script can easily be extended to do the replacements in all text frames of a page or a document:

```py

for page in range(1, scribus.pageCount() + 1):
    scribus.gotoPage(page)
    for text_frame in [item[0] for item in scribus.getPageItems() if item[1] == 4]:
        scribus.selectObject(text_frame)
        # ...
```
