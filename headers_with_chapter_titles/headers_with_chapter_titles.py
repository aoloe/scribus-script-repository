"""create running titles, based on master pages and text styles

For more details see the README.md

(c) MIT 2024, ale rimoldi <ale@graphicslab.org>
"""

try:
    import scribus
except ImportError:
    pass


HEADING_STYLE = 'h1'
HEADING_ITEM_PREFIX = 'running_title_'

def get_master_pages_with_running_titles():
    """get the names of the master page with a running title
       and the name of the text frame for it"""
    master_pages = {}
    for master_page in scribus.masterPageNames():
        scribus.editMasterPage(master_page)
        for item in (item[0] for item in scribus.getPageItems() if item[1] == 4):
            if item.startswith(HEADING_ITEM_PREFIX):
                master_pages[master_page] = item
                break
    scribus.closeMasterPage()
    return master_pages

def delete_all_heading_frames():
    for page in range(1, scribus.pageCount() + 1):
        scribus.gotoPage(page)
        for item in (item[0] for item in scribus.getPageItems() if item[1] == 4):
            if item.startswith(HEADING_ITEM_PREFIX):
                scribus.deleteObject(item)


def get_first_h1_in_page(page):
    """go through all paragraphs in all frames in page
        and if there is an h1 paragraph style return its text."""
    scribus.gotoPage(page)

    # get the text and linked frames, sorted by the position on the page
    page_text_frames = [(item[0], scribus.getPosition(item[0])) for item in scribus.getPageItems()
        if item[1] == 4]
    page_text_frames.sort(key= lambda item: (item[1][1], item[1][0]))

    for item, _ in page_text_frames:
        scribus.deselectAll()
        scribus.selectObject(item)

        paragraphs = scribus.getFrameText().split('\r')

        start = 0
        for p in paragraphs:
            scribus.selectFrameText(start, len(p))
            p_style = scribus.getParagraphStyle()
            if p_style == HEADING_STYLE:
                return p
            start += len(p) + 1
    return None

def main():
    try:
        scribus # pylint: disable=pointless-statement
    except NameError:
        return

    scribus.setRedraw(False)

    scribus.closeMasterPage()
    current_page = scribus.currentPage()

    master_pages = get_master_pages_with_running_titles()
    if len(master_pages) == 0:
        scribus.messageBox(
            'Error',
            f'No master page found, with a text item starting with {HEADING_ITEM_PREFIX}',
            icon=scribus.ICON_CRITICAL)
        return

    delete_all_heading_frames()

    current_h1 = None
    for page in range(1, scribus.pageCount() + 1):
        # TODO: it might be better to get both the first and last h1 on the page.
        # the first for this page, the last (if different) for the following ones
        h1 = get_first_h1_in_page(page)
        if h1 is not None:
            current_h1 = h1
        if current_h1 is None:
            continue
        master_page = scribus.getMasterPage(page)
        if master_page not in master_pages:
            continue
        scribus.editMasterPage(master_page)
        scribus.copyObjects([master_pages[master_page]])
        scribus.closeMasterPage()
        scribus.gotoPage(page)
        new_frame = scribus.pasteObjects()[0]
        scribus.setText(current_h1, new_frame)
        scribus.setProperty(new_frame, 'printEnabled', True)
        scribus.setItemName(HEADING_ITEM_PREFIX + str(page), new_frame)
    scribus.deselectAll()
    scribus.gotoPage(current_page)
    scribus.setRedraw(True)

if __name__ == '__main__':
    main()
