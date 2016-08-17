"""
create "printable" guides and page margins for a draft
@author: ale rimoldi
@version: 1.0 / 20110901
@copyright (c) 2011 alessandro rimoldi under the mit license
http://www.opensource.org/licenses/mit-license.html
"""

import sys
try:
    import scribus
except ImportError:
    print "This script only works from within Scribus"
    sys.exit(1)

page = scribus.getPageSize()
margin = scribus.getPageMargins()

layer = scribus.getActiveLayer()

if ('guides' in scribus.getLayers()) :
    scribus.setActiveLayer('guides')
else:
    scribus.createLayer('guides')

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

scribus.setActiveLayer(layer)
