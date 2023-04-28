# Replace multiple patterns in the selected text frame
#
# © mit, ale rimoldi, 2023

import sys
try:
    from scribus import *
except ImportError:
    print('Ce script est écrit en Python. Il ne peut être lancé que depuis Scribus.')
    sys.exit(1)

if (not scribus.haveDoc() or
        scribus.selectionCount() != 1 or
        scribus.getObjectType() != "TextFrame"):
    scribus.messageBox('Warning', 'Vous devez sélectionner un cadre de texte.')
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
        scribus.selectText(start, count)
        scribus.deleteText()
        scribus.insertText(item[1], start)
        content = content[0:start] + item[1] + content[start + count:]
        start += count

scribus.layoutText()
scribus.docChanged(True)
