# go through all text items in the document, check for heading styles and create a table of contents in the current text frame
#
# © mit, ale rimoldi, 2023

import sys

test = len(sys.argv) == 2 and sys.argv[1] == 'test'

try:
    import scribus
except ImportError:
    # we only test functions that do not depend on scribus being loaded
    if not test:
        print('This script must be run from inside Scribus')
        sys.exit()

heading_styles = ['h1', 'h2', 'h3']
toc_styles = ['toc1', 'toc2', 'toc3']
# you can use the item attributes to set the heading and toc styles
heading_attribute = 'heading_styles'
toc_attribute = 'toc_styles'
# TODO:  as soon the API supports reading the sections, read the the values from the real sections
sections = [
    {
        'end': 0, # last page index in this section (0 = to the end)
        'format': '1', # one of '1', 'i', 'I', 'a', 'A' # TODO: scribus has even more  formats we could support
        'start_number': 1,
    },
]

def get_current_section(sections, page):
    for section in sections:
        if section['end'] == 0:
            return section
        if section['end'] <= page:
            return section
    return sections[-1] # should never get here

ROMAN_DIVISORS = {1000: 'M', 900: 'CM', 500: 'D', 400: 'CD', 100: 'C', 90: 'XC', 50: 'L', 40: 'XL', 10: 'X', 9: 'IX', 5: 'V', 4: 'IV', 1: 'I'}

def int_to_roman(number):
    roman = ''
    for divisor, symbol in ROMAN_DIVISORS.items():
        quotient = divmod(number, divisor)[0]
        roman += symbol * quotient
        number -= divisor * quotient
        if number < 1:
            break
    return roman

# https://codereview.stackexchange.com/a/182756
# num >= 0
def int_to_alpha(num):
    if num == 0:
        return ""
    else:
        q, r = divmod(num - 1, 26)
        return int_to_alpha(q) + chr(ord('a') + r)

def get_formatted_page_number(page, section):
    page_number = section['start_number'] + page - 1
    # TODO: wait for match being available in the python distribute with scribus (3.10)
    # match section['format']:
    #"""     case 'i':
    if section['format'] == 'i':
            page_number = int_to_roman(page_number).lower()
    #     case 'I':
    elif section['format'] == 'I':
            page_number = int_to_roman(page_number)
    #     case 'a':
    elif section['format'] == 'a':
            page_number = int_to_alpha(page_number)
    #     case 'A':
    elif section['format'] == 'A':
            page_number = int_to_alpha(page_number).to_upper()
    return page_number

# go through all paragraphs in the currently selected frame,
# and if the style is h1 add the paragraph to the list of headings
def get_frame_headings_by_style(page_number):
    headings = []
    paragraphs = scribus.getFrameText().split('\r')

    start = 0
    for p in paragraphs:
        scribus.selectFrameText(start, len(p))
        p_style = scribus.getParagraphStyle()
        if p_style == None:
            start += len(p) + 1
            continue
        if p_style in heading_styles:
            headings.append({
                'title': p,
                'page': page_number,
                'level': heading_styles.index(p_style),
            })
        start += len(p) + 1

    return headings

def main():
    global heading_styles, toc_styles
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
    # ensure that the styles exist
    for style in set(heading_styles + toc_styles).difference(scribus.getParagraphStyles()):
        scribus.createParagraphStyle(style)

    headings = []

    scribus.setRedraw(False)
    for page in range(1, scribus.pageCount() + 1):
        section = get_current_section(sections, page)
        page_number = get_formatted_page_number(page, section)
        scribus.gotoPage(page)
        # get the text and linked frames, sorted by the position on the page
        page_text_frames = [(item[0], scribus.getPosition(item[0])) for item in scribus.getPageItems()
            if item[1] == 4 or item[1] == 5]
        page_text_frames.sort(key= lambda item: (item[1][1], item[1][0]))

        for item, _ in page_text_frames:
            scribus.deselectAll()
            scribus.selectObject(item)
            headings += get_frame_headings_by_style(page_number)
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

def main_test():
    assert(int_to_alpha(1) == 'a')
    assert(int_to_alpha(27) == 'aa')

if __name__ == "__main__":
    if test:
        main_test()
    else:
        main()
