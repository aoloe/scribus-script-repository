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
color_kinds = ["rgb", "cmyb", "pantone"]

class color_def:
    """Class for color definition: 
  - kind: color kind (rgb, cmyb, pantone)
  - ref: reference (rgb code, cmyb code, or pantone reference)
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

