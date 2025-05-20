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

def drawBaselineGrid(page_width, page_height):
    try:
        scribus.getColorAsRGB('Grey')
    except scribus.NotFoundError:
        scribus.defineColorRGB('Grey', 192, 192, 192)
        
    baseline, offset = scribus.getBaseLine()

    # range only works with ints: we multiply by 100 to increase the precision
    for y in range(int(offset * 100), int(page_height * 100), int(baseline * 100)):
        line = scribus.createLine(0, y / 100 , page_width, y / 100)
        scribus.setLineColor('Grey', line)
        scribus.setLineWidth(0.6, line)

def drawPlaceholders():
    page_width, page_height = scribus.getPageSize()
    margin = scribus.getPageMargins()

    # add the page margins
    rectangle = scribus.createRect(margin[1],
        margin[0], (page_width - margin[1] - margin[2]),
        (page_height - margin[0] - margin[3]))
    scribus.setFillColor('none', rectangle)
    scribus.setLineColor('Blue', rectangle)
    scribus.setLineWidth(0.4, rectangle)

    # add horizontal and vertical guides
    for item in scribus.getHGuides():
        drawHorizontalGuide(item, page_width)

    for item in scribus.getVGuides():
        drawVerticalGuide(item, page_height)

    # add column and row guides
    for item in scribus.getRowGuides()['guides']:
        drawHorizontalGuide(item, page_width)

    for item in scribus.getColumnGuides()['guides']:
        drawVerticalGuide(item, page_height)

    # add a "crossed frame" for missing images
    for item in scribus.getAllObjects():
        if scribus.getObjectType(item) == 'ImageFrame':
            image = scribus.getImageFile(item)
            if image == '':
                drawImagePlaceholder(item)

    # TODO: disabled by default until we can check if the baseline is visible
    # drawBaselineGrid(page_width, page_height)

def main():
    try:
        scribus
    except NameError:
        print('This script must be run from inside Scribus.')
        return

    if scribus.selectionCount() > 0:
        for i in range(scribus.selectionCount()):
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
