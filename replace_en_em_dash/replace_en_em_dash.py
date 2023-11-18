"""
Replace double dashes (--) by en-dashes and triple dashes (---) by em-dashes.
If there is no selection, all the frames in the document are

© mit, ale rimoldi, 2023
Inspired by a similar script by Gregory Pittman
"""

try:
    import scribus # pylint: disable=import-error
except ImportError:
    pass

import re

N_DASH = '\u2013'
M_DASH = '\u2014'

def replace(frame):
    """
    find the position of all -- and --- and replace them starting from the end
    """
    text = scribus.getAllText(frame)
    pattern = re.compile("-{2,}") # we need to find all groups of - and then restrict the count to 3
    matches = [(m.start(), len(m.group())) for m in pattern.finditer(text) if len(m.group()) <= 3]
    for match in reversed(matches):
        scribus.selectText(match[0], match[1], frame)
        scribus.deleteText(frame)
        scribus.insertText(N_DASH if match[1] == 2 else M_DASH, match[0], frame)
    scribus.deselectAll()

def main():
    try:
        scribus
    except NameError:
        print('This script must be run from inside Scribus')
        return

    if not scribus.haveDoc():
        return

    if scribus.selectionCount() > 0:
        selection = [scribus.getSelectedObject(i) for i in range(scribus.selectionCount())]
        scribus.deselectAll()
        for item in [item for item in selection if scribus.getObjectType(item) == 'TextFrame']:
            replace(item)
        scribus.deselectAll()
        for item in selection:
            scribus.selectObject(item)
    else:
        for page in range(scribus.pageCount()):
            # get all text frame on the page that do not have a previsous linked frame
            for item in [item for item in scribus.getAllObjects(4, page)
                if scribus.getPrevLinkedFrame(item) is None]:
                    replace(item)

    scribus.setRedraw(True)
    scribus.docChanged(True)

if __name__ == '__main__':
    main()
