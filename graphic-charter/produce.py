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

class chart_production:
    def __init__(self, target_display = 'console'):
        self.set_display(target_display)
        return


    def set_display(self, target):
        if (target == 'scribus'):
            self.output = inout.scribus_display()
        else:
            self.output = inout.console_display()
        return


    def display_colors(self, colors):
        self.output.display_text(inout.text("Colors used in chart",
                                            self.output.current_position
                                        )
                                 )
        for color in colors:
            self.output.display_figure('rect')
            text = "Color '%s': kind=%s, ref=%s" \
                   % (color.label, color.kind, color.ref)
            self.output.display_text(text)
        return
        

    def display_fonts(self, fonts):
        self.output.display_text("Fonts used in chart")
        for font in fonts:
            texte = "Font '%s', Style '%s'" \
                    % (font.name, font.style)
            self.output.display_text(texte)
        return


    def display_graphic_chart(self, graphic_chart):
        self.display_colors(graphic_chart.colors)
        self.display_fonts(graphic_chart.fonts)
        return


# Main executed if called out of script
if __name__ == "__main__":
    production = chart_production('scribus')
    production.display_graphic_chart(inout.test_chart)
