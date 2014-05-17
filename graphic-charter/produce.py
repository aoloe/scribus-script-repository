# -*- coding: utf-8-unix; -*- 
#
############################################################################### 
#
# Purpose:
#   Produce part for Scribus tool "graphic-charter"
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

import scribus
import interface
import inout

print "Produce content of graphic chart"

# Display content to active destination output
def display(content):
    #destination = inout.scribus()
#    destination = inout.console_display
#    destination.display(content)
    destination_display = inout.console_display
    destination_display(content)

def display_graphic_chart(graphic_chart):
    display_colors(graphic_chart.colors)
    display_fonts(graphic_chart.fonts)
    return

def display_colors(colors):
    for color in colors:
        texte = "Color '%s': kind=%s, ref=%s" \
                % (color.label, color.kind, color.ref)
        display(texte)
    return


def display_fonts(fonts):
    for font in fonts:
        texte = "Font '%s', Style '%s'" \
                % (font.name, font.style)
        display(texte)
    return


display_graphic_chart(inout.test_chart)
