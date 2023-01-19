# go through all text items in the document, check for heading styles and create matching attributes for the table of contents
#
# © mit, ale rimoldi, 2023

import scribus

headings = ['h1', 'h2', 'h3']
attribute_name = 'Table of Contents'

# go through all paragraphs in the currently selected frame,
# and if the style is h1, set the corresponding attribute for the table of contents
def add_attributes_for_heading_styles():
    scribus.selectText(0, 0)
    paragraphs = scribus.getFrameText().split('\r')
    # print(paragraphs)

    toc_attributes = []
    start = 0
    for p in paragraphs:
        scribus.selectText(start, len(p))
        p_style = scribus.getParagraphStyle()
        if p_style in headings:
            toc_attributes.append({
                'Name': attribute_name,
                'Type': 'none',
                'Value': scribus.getFrameText(),
                'Parameter': str(headings.index(p_style) + 1),
                'Relationship': 'none',
                'RelationshipTo': '',
                'AutoAddTo': 'none'
            })
        start += len(p) + 1

    if toc_attributes:
        attributes = [a for a in scribus.getObjectAttributes() if a['Name'] != attribute_name]
        scribus.setObjectAttributes(attributes + toc_attributes)

def main():
    if not scribus.haveDoc():
        return

    for page in range(1, scribus.pageCount() + 1):
        scribus.gotoPage(page)
        for item in scribus.getPageItems():
            if item[1] == 4:
                scribus.deselectAll()
                scribus.selectObject(item[0])
                add_attributes_for_heading_styles()

    scribus.deselectAll()

main()
