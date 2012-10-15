#!/usr/bin/python

"""
create "printable" guides and page margins for a draft
@author: ale rimoldi
@version: 1.0 / 20110901
@version: 1.1 / 20121015 (add baseline grid and fix height of vertical guides)
@copyright (c) 2011 ale rimoldi under the mit license
           http://www.opensource.org/licenses/mit-license.html
"""
from __future__ import division
from itertools import cycle
import sys
try:
   import scribus
except ImportError:
   print "This script only works from within Scribus"
   sys.exit(1)


unit_current=scribus.getUnit() #get unit and change it to mm
scribus.setUnit(scribus.UNIT_MILLIMETERS)

page = scribus.getPageSize()
margin = scribus.getPageMargins()

layer = scribus.getActiveLayer()

if ('guides' in scribus.getLayers()) :
    scribus.setActiveLayer('guides')
else:
    scribus.createLayer('guides')


# add the baseline grid (when it's not too close to a guide)
baseline_start = 0 # in mm
baseline = 14.4 # in pt

multiplicator = 10000
baseline = int(baseline * 0.352777 * multiplicator) # 14.4 pt in mm
#baseline = int(baseline * 0.351459 * multiplicator) # 14.4 pt in mm

if baseline > 0 :
  guide_i = 0
  guide_list = scribus.getHGuides()
  guide_list.append(page[1])
  guide = guide_list[guide_i]
  guide_n = len(guide_list)
  if not 'Gray' in scribus.getColorNames() :
      scribus.defineColor('Gray', 10, 10, 10, 10)
  for item in range(baseline + baseline_start*multiplicator, int(page[1] * multiplicator + baseline_start*multiplicator), baseline) :
    # print item/multiplicator
    while guide_i < guide_n - 1 and item/multiplicator > guide + 0.15 :
        guide_i = guide_i + 1
        guide = guide_list[guide_i]
    if item/multiplicator < guide - 0.15 :
        line = scribus.createLine(0, item/multiplicator , page[0], item/multiplicator)
        scribus.setLineColor('Gray', line)
        scribus.setLineWidth(0.6, line)
        # scribus.setLineStyle(scribus.LINE_DASHDOT, line)


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
    line = scribus.createLine(item, 0 , item, page[1])
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

scribus.setUnit(unit_current)
