# go through all text items in the document, check for heading styles and create a table of contents in the current text frame
#
# © mit, ale rimoldi, 2023

import sys

try:
    import scribus
except ImportError:
    print('This script must be run from inside Scribus')
    sys.exit()

heading_styles = ['h1', 'h2', 'h3']
toc_styles = ['toc1', 'toc2', 'toc3']
toc_new_lines = None # strip | truncate
# you can use the item attributes to set the heading and toc styles
heading_attribute = 'heading_styles'
toc_attribute = 'toc_styles'
new_lines_attribute = 'toc_new_lines'

# go through all paragraphs in the currently selected frame,
# and if the style is h1 add the paragraph to the list of headings
def get_frame_headings_by_style():
    headings = []
    paragraphs = scribus.getFrameText().split('\r')

    start = 0
    for p in paragraphs:
        scribus.selectFrameText(start, len(p))
        p_style = scribus.getParagraphStyle()
        start += len(p) + 1
        if p_style == None:
            continue
        if hasattr(scribus, 'currentPageNumberForSection'):
            # introduced in 1.5.9svn on 2023-01-25
            page_number = scribus.currentPageNumberForSection()
        else:
            page_number = scribus.currentPageNumber()

        if p_style in heading_styles:
            # remove frame (26) and column (27) breaks
            p = ''.join([c for c in p if ord(c) not in [26, 27]])
            # ignore empty lines (most of all if they only contain a frame break)
            if p == '':
                continue

            if toc_new_lines is not None:
                parts = p.split(chr(8232))
                if toc_new_lines == 'strip':
                    p = ' '.join(parts)
                elif toc_new_lines == 'truncate':
                    p = parts[0]
            headings.append({
                'title': p,
                'page': page_number,
                'level': heading_styles.index(p_style),
            })

    return headings

def main():
    global heading_styles, toc_styles, toc_new_lines
    if not scribus.haveDoc():
        return

    if scribus.selectionCount() == 0:
        return

    if scribus.getObjectType() != 'TextFrame':
        return

    toc_item = scribus.getSelectedObject()

    # read the heading and toc styles from the toc frame attributes
    for attribute in scribus.getObjectAttributes():
        if attribute['Name'] == heading_attribute:
            heading_styles = [style.strip() for style in attribute['Value'].split(',')]
        elif attribute['Name'] == toc_attribute:
            toc_styles = [style.strip() for style in attribute['Value'].split(',')]
        elif attribute['Name'] == new_lines_attribute:
            toc_new_lines = attribute['Value'].strip()
    # ensure that the styles exist
    for style in set(heading_styles + toc_styles).difference(scribus.getParagraphStyles()):
        scribus.createParagraphStyle(style)

    headings = []

    scribus.setRedraw(False)
    for page in range(1, scribus.pageCount() + 1):
        scribus.gotoPage(page)
        # get the text and linked frames, sorted by the position on the page
        page_text_frames = [(item[0], scribus.getPosition(item[0])) for item in scribus.getPageItems()
            if item[1] == 4]
        page_text_frames.sort(key= lambda item: (item[1][1], item[1][0]))

        for item, _ in page_text_frames:
            scribus.deselectAll()
            scribus.selectObject(item)
            headings += get_frame_headings_by_style()
    scribus.deselectAll()
    scribus.setRedraw(True)

    scribus.selectObject(toc_item)
    scribus.deleteText()
    start = 0
    for heading in headings:
        if start > 0:
            scribus.insertText('\r', -1)
        scribus.insertText(heading['title'] + '\t' + str(heading['page']), -1)
        scribus.selectText(start, len(heading['title']))
        scribus.setParagraphStyle(toc_styles[heading['level']])
        start += len(heading['title']) + 1 + len(str(heading['page'])) + 1
    scribus.layoutText()

if __name__ == "__main__":
    main()
