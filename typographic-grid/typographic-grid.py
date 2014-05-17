# Create the typographic grid and the baseline grid based on some parameters

import sys
try:
   import scribus
except ImportError:
   print "This script only works from within Scribus"
   sys.exit(1)

def setGuidesColumn(n, gap):
    print "setGuidesColumn should be a scribus API function"
    (margin_top, margin_left, margin_right, margin_bottom) = scribus.getPageNMargins(scribus.currentPage())
    print "left " + str(margin_left)
    print "right " + str(margin_right)
    (width, height) = scribus.getPageNSize(scribus.currentPage())
    print "width " + str(width)
    print "height " + str(height)
    cell_width = (width - (margin_left + margin_right) - (gap * (n - 1))) / n
    print cell_width
    guide = []
    previous_guide = margin_left
    for i in range(0, n - 1):
        guide.append(previous_guide + cell_width)
        guide.append(previous_guide + cell_width + gap)
        previous_guide = previous_guide + cell_width + gap
    scribus.setVGuides(guide)

def setGuidesRow(n, gap):
    print "TODO: implement setGuidesRow"

unit_current=scribus.getUnit() #get unit and change it to mm
scribus.setUnit(scribus.UNIT_MILLIMETERS)

page = scribus.getPageSize()
(margin_top, margin_left, margin_right, margin_bottom) = scribus.getPageNMargins(scribus.currentPage())

# scribus.setHGuides([10,20,30])

setGuidesColumn(6, 5)
# setGuidesRow(4, 5)

scribus.setBaseLine(20, margin_top)


scribus.setUnit(unit_current)
