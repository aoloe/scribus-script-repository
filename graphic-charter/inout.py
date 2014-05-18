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

class unit(object):
    available_units = ['cm', 'mm', 'in', 'pt', 'char'] # 'char' is for console
    scale = { 
        'cm': {'cm': 1, 'mm': 10, 'in': 1/2.54, 'pt': 28.45274},
        'mm': {'cm': 0.1, 'mm': 1, 'in': 0.1/2.54, 'pt': 2.84527},
        'in': {'cm': 2.54, 'mm': 254, 'in': 1, 'pt': 72.2699},
        'pt': {'cm': 0.35146, 'mm': 0.03514, 'in': 0.001384, 'pt': 1} 
    }
    scribus_constants = {
        'mm': scribus.UNIT_MILLIMETERS,
        'in': scribus.UNIT_INCHES,
        'pt': scribus.UNIT_POINTS
}

    def __init__(self, unit):
        if unit in self.available_units:
            self.unit = unit
        else:
            self.unit = None

    def to(self, unit):
        print "Converting from %s to %s" % (self.unit, unit)
        return self.scale[self.unit][unit.unit]


    def scribus_repr(self):
        if self.unit in self.scribus_constants.keys():
            return self.scribus_constants[self.unit]
        else:
            return None


class measure(object):
    def __init__(self, measure_value, measure_unit):
        self.unit = unit(measure_unit)
        if self.unit:
            self.measure = measure_value
        else:
            self.measure = None
        return

    def to(self, unit):
        """Convert measure to other unit"""
        self.measure = self.measure * self.unit.to(unit)
        return

    def dup_to(self, unit):
        """Return a new measure converted to other unit"""
        return measure(self.measure * self.unit.to(unit), unit)

    def scribus_repr(self, scribus_units):
        return self.dup_to(scribus_units).measure


    def __str__(self):
        return "%f %s" % (self.measure, self.unit)


class hv_position(object):
    """Horizontal and Vertical position, expressed as a 'measure' instance"""
    def __init__(self, hpos, vpos):
        self.hpos = hpos
        self.vpos = vpos
        return

    def move(hmove, vmove):
        self.hpos = self.hpos + hmove
        self.vpos = self.vpos + vmove
        return


class text(object):
    def __init__(self, text, style = None, fg_color = None, 
                 bg_color = None, font = None):
        self.text = text
        self.style = style
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.font = font
        return

class figure(object):
    available_figures = ['rect', 'circle']
    def __init__(self, figure, figure_spec):
        if figure in figure.available_figures:
            self.figure = figure
        else:
            self.figure = None
        return


class figure_rect(figure):
    def __init__(self):
        return


# Handle display to the console
class console_display(object):
    def __init__(self):
        self.current_position = hv_position(measure(0, 'char'),
                                            measure(0, 'char'))
        return

    def display_text(self, text):
        # In console, only "text" is supported, other features are ignored
        print text
        return 

    def display_figure(self, figure):
        # In console, figure are not displayed
        return


    def move(self, hmove, vmove, unit):
        
        return

# Handle display to Scribus
class scribus_display(object):
    # Scribus document features
    page_size = scribus.PAPER_A4
    # Units for document details (as available in Scribus)
    units = unit("mm")
    # Margins: left, right, top, bottom
    margins = { 
        "left": measure(1.4111, 'cm'),
        "right": measure(1.4111, 'cm'),
        "top": measure(1.4111, 'cm'),
        "bottom": measure(1.4111, 'cm')
    }
    # Orientation: "PORTRAIT" or "LANDSCAPE"
    orientation = scribus.PORTRAIT

    def __init__(self):
        self.doc = scribus.newDocument(
            self.page_size,
            (self.margins["left"].scribus_repr(self.units),
             self.margins["right"].scribus_repr(self.units),
             self.margins["top"].scribus_repr(self.units),
             self.margins["bottom"].scribus_repr(self.units)),
            self.orientation,
            1, # Number of first page
            self.units.scribus_repr(),
            scribus.FACINGPAGES,
            scribus.FIRSTPAGELEFT,
            1 # Number of pages in document
        )
        self.current_position = hv_position(
            self.margins["left"],
            self.margins["top"]
        )
        return

    def display_text(self, text):
        # scribus.print_message(content)
        print text
        return 

    def display_figure(self, figure):
        return


