# Replace multiple patterns in the selected text frame
#
# © mit, ale rimoldi, 2023

import sys
try:
    import scribus
except ImportError:
    print('This script must be run from inside Scribus')
    sys.exit(1)

if (not scribus.haveDoc() or
        scribus.selectionCount() != 1 or
        scribus.getObjectType() != "TextFrame"):
    scribus.messageBox('Warning', 'You need to select a text frame.')
    sys.exit(1)

replacements = (
    ("search", "replace"), # <- your list of search/replace tuples
)

content = scribus.getAllText()
for item in replacements:
    start = 0
    while start >= 0:
        start = content.find(item[0], start)
        if start == -1:
            continue
        count = len(item[0])
        # replace in the frame and try to keep the formattings
        scribus.selectText(start, count)
        scribus.deleteText()
        scribus.insertText(item[1], start)
        # replace in the extracted content
        content = content[0:start] + item[1] + content[start + count:]
        # prepare for the next find
        start += count

scribus.layoutText()
scribus.docChanged(True)
