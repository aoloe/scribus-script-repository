# -*- coding: utf-8-unix; -*- 
#
############################################################################### 
#
# Purpose:
#   Input/Output handler for Scribus tool "graphic-charter"
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


# Handle display to the console
#class console():
#    def __init__(self):
#        return
#
#    def display(self, content):
#        print content
#        return 
#
# Handle display to Scribus
#class scribus():
#    def __init__(self):
#        return
#
#    def display(self, content):
#        # scribus.print_message(content)
#        print content
#        return 

def console_display(content):
    print content


def scribus_display(content):
    # scribus.print_message(content)
    print content
    return 


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
    
