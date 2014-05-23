# -*- coding: utf-8-unix; -*- 
#
############################################################################### 
#
# Purpose:
#   Test interface for Scribus tool "graphic-charter"
#    
#============================================================================== 
#
# Auteurs et Licence: 
#  (C) 2014 AGPLv3
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation; version 3.
#
###############################################################################

import extract
import produce
import interface

# Test production routine
## Definition of tests data for production

test_chart = interface.graphic_chart_def()
colors = [
    ("rgb", (255, 255, 255), "color1"),
    ("rgb", (127, 127, 127), "color2"),
    ("rgb", (0, 0, 0), "color3"),
]

fonts = [
    ("MyFirstFont", "Normal"),
    ("MySecondFont", "Italic"),
    ("MyThirdFont", "Bold")
]

for color in colors:
    (kind, ref, label) = color
    test_chart.add_color(interface.color_def(kind, ref, label))

for font in fonts:
    (name, style) = font
    test_chart.add_font(interface.font_def(name, style))

## Start tests for production
print "Test for production"
production = produce.chart_production('scribus')
production.display_graphic_chart(test_chart)


print "\n\n"
print "Test for extract, then production"
test_chart = interface.graphic_chart_def()
extract.extract(test_chart)
production.display_graphic_chart(test_chart)
