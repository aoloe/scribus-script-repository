"""
create "printable" guides, page margins and placeholders for empty image frames.
@author: ale rimoldi
@version: 2.1 / 20231227
@copyright (c) MIT license  2016, ale rimoldi
http://www.opensource.org/licenses/mit-license.html
"""

try:
    import scribus # pylint: disable=import-error
except ImportError:
    pass

def drawImagePlaceholder(item):
    pos = scribus.getPosition(item)
    size = scribus.getSize(item)
    rectangle = scribus.createRect(pos[0], pos[1], size[0], size[1])
    scribus.setFillColor('none', rectangle)
    scribus.setLineColor('Black', rectangle)
    scribus.setLineWidth(0.4, rectangle)
    line = scribus.createLine(pos[0], pos[1] , pos[0] + size[0], pos[1] + size[1])
    scribus.setLineColor('Black', line)
    scribus.setLineWidth(0.4, line)
    line = scribus.createLine(pos[0], pos[1] + size[1], pos[0] + size[0], pos[1])
    scribus.setLineColor('Black', line)
    scribus.setLineWidth(0.4, line)

def drawVerticalGuide(x, height):
    line = scribus.createLine(x, 0 , x, height)
    scribus.setLineColor('Black', line)
    scribus.setLineWidth(0.6, line)
    scribus.setLineStyle(scribus.LINE_DASHDOT, line)

def drawHorizontalGuide(y, width):
    line = scribus.createLine(0, y , width, y)
    scribus.setLineColor('Black', line)
    scribus.setLineWidth(0.6, line)
    scribus.setLineStyle(scribus.LINE_DASHDOT, line)

def drawPlaceholders():
    page = scribus.getPageSize()
    margin = scribus.getPageMargins()

    # add the page margins
    rectangle = scribus.createRect(margin[1],
        margin[0], (page[0] - margin[1] - margin[2]),
        (page[1] - margin[0] - margin[3]))
    scribus.setFillColor('none', rectangle)
    scribus.setLineColor('Blue', rectangle)
    scribus.setLineWidth(0.4, rectangle)

    # add horizontal and vertical guides
    for item in scribus.getHGuides():
        drawHorizontalGuide(item, page[0])

    for item in scribus.getVGuides():
        drawVerticalGuide(item, page[1])

    # add column and row guides
    for item in scribus.getRowGuides()['guides']:
        drawHorizontalGuide(item, page[0])

    for item in scribus.getColumnGuides()['guides']:
        drawVerticalGuide(item, page[1])

    # add a "crossed frame" for missing images
    for item in scribus.getAllObjects():
        if scribus.getObjectType(item) == 'ImageFrame':
            image = scribus.getImageFile(item)
            if image == '':
                drawImagePlaceholder(item)

def main():
    try:
        scribus
    except NameError:
        print('This script must be run from inside Scribus.')
        return

    if scribus.selectionCount() > 0:
        for i in range(scribus.selectionCount):
            item = scribus.getSelectedObject(i)
            item_type = scribus.getObjectType()
            if item_type == 'ImageFrame':
                drawImagePlaceholder(item)
        return

    layer = scribus.getActiveLayer()

    if ('placeholder' in scribus.getLayers()) :
        scribus.setActiveLayer('placeholder')
    else:
        scribus.createLayer('placeholder')

    for page in range(1, scribus.pageCount() + 1):
        scribus.gotoPage(page)
        drawPlaceholders()

    scribus.setActiveLayer(layer)

if __name__ == '__main__':
    main()
