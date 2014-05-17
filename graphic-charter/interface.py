#! /usr/bin/python
# -*- coding: utf-8-unix; -*- 
#
############################################################################### 
#
# Purpose:
#   Interface for Scribus tool "graphic-charter"
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

# List of color kinds used to identify colors within Scribus
color_kinds = ["rgb", "cmyk", "pantone"]

class color_def:
    """Class for color definition: 
  - kind: color kind (rgb, cmyk, pantone)
  - ref: reference (rgb code, cmyk code, or pantone reference)
  - label: label used to identify the color within Scribus
"""
    def __init__(kind, ref, label):
        self.kind = kind
        self.ref = ref
        self.label = label
        return

class font_def:
    """Class for font definition:
  - name: Font name, identifying the font (DejaVu, Libertine, ...)
  - style: Font style (italic, bold, condensed, ...)
"""
    def __init__(name, style):
        self.name = name
        self.style = style
        return

class graphic_chart_def:
    """Class for graphic chart definition:
  - colors (color_def): list of colors in graphic chart
  - fonts (font_def): list of fonts in graphic chart
"""
    def __init__():
        self.colors = []
        self.fonts = []

    def add_color(self, color):
        self.colors.append(color)

    def add_font(self, font):
        self.fonts.append(font)

