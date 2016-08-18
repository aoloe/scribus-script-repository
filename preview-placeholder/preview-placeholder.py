"""
create "printable" guides, page margins and placeholders for empty image frames.
@author: ale rimoldi
@version: 2.0 / 20160817
@copyright (c) MIT license  2016, ale rimoldi
http://www.opensource.org/licenses/mit-license.html
"""

import sys
try:
    import scribus
except ImportError:
    print "This script only works from within Scribus"
    sys.exit(1)

def drawPlaceholders():
    page = scribus.getPageSize()
    margin = scribus.getPageMargins()

    # add the page margins
    rectangle = scribus.createRect(margin[1], margin[0], (page[0] - margin[1] - margin[2]), (page[1] - margin[0] - margin[3]))
    scribus.setFillColor('none', rectangle)
    scribus.setLineColor('Blue', rectangle)
    scribus.setLineWidth(0.4, rectangle)

    # add horizontal and vertical guides
    for item in scribus.getHGuides():
        line = scribus.createLine(0, item , page[0], item)
        scribus.setLineColor('Black', line)
        scribus.setLineWidth(0.6, line)
        scribus.setLineStyle(scribus.LINE_DASHDOT, line)

    for item in scribus.getVGuides():
        line = scribus.createLine(item, 0 , item, page[0])
        scribus.setLineColor('Black', line)
        scribus.setLineWidth(0.6, line)
        scribus.setLineStyle(scribus.LINE_DASHDOT, line)

    # add a "crossed frame" for missing images
    for item in scribus.getAllObjects():
        if scribus.getObjectType(item) == 'ImageFrame':
            image = scribus.getImageFile(item)
            if image == '':
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

layer = scribus.getActiveLayer()

if ('placeholder' in scribus.getLayers()) :
    scribus.setActiveLayer('placeholder')
else:
    scribus.createLayer('placeholder')

for page in range(1, scribus.pageCount() + 1):
    scribus.gotoPage(page)
    drawPlaceholders()

scribus.setActiveLayer(layer)
