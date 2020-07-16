# encoding: utf-8
# (c) MIT ale rimoldi
# Simple Table of Content script for Scribus
# For details see the README file.

try:
    import scribus
except ImportError:
    print('This script must be run from inside Scribus')

import sys

if not scribus.haveDoc():
    scribus.messageBox('Error', 'You need a Document open.', icon=0, button1=1)
    sys.exit(2)

if scribus.selectionCount() != 1:
    scribus.messageBox('Error',
                       "Please select the target text frame.",
                       scribus.ICON_WARNING, scribus.BUTTON_OK)
    sys.exit(2)

toc_frame = scribus.getSelectedObject()

if scribus.getObjectType(toc_frame) != 'TextFrame':
    scribus.messageBox('Error',
                       "Please select the target text frame.",
                       scribus.ICON_WARNING, scribus.BUTTON_OK)
    sys.exit(2)

toc_styles = {'h1': 'toc1', 'h2': 'toc2', 'h3': 'toc3'}
toc_content = []

for page in range(1, scribus.pageCount() + 1):
    scribus.gotoPage(page)
    for item in scribus.getPageItems():
        if item[1] == 4:
            scribus.deselectAll()
            scribus.selectObject(item[0])
            content = scribus.getFrameText()
            next_line_feed = content.find('\r')
            start_selection = 0
            while next_line_feed >= 0:
                line = content[start_selection:next_line_feed]
                if len(line) > 0:
                    scribus.selectFrameText(start_selection, 1)
                    style = scribus.getParagraphStyle()
                    if style in toc_styles:
                        toc_content.append((content[start_selection:next_line_feed], page, toc_styles[style]))
                start_selection = next_line_feed + 1
                next_line_feed = content.find('\r', next_line_feed + 1)

scribus.deselectAll()
scribus.selectObject(toc_frame)

# print(toc_content)
scribus.deleteText()
position = 0
for toc_item in toc_content:
    toc_item_content = toc_item[0] + '\t' + str(toc_item[1])
    scribus.insertText(toc_item_content, -1)
    scribus.selectText(position, 1)
    scribus.setParagraphStyle(toc_item[2])
    scribus.insertText('\r', -1)
    position += len(toc_item_content) + 1
