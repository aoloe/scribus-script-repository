# -*- coding: utf-8 -*-
"""
ABOUT THIS SCRIPT:

Create the typographic grid and the baseline grid based on some parameters for the current page.

LICENSE:

This program is free software under the MIT license.

Find more details in the README file nearby or on:
http://github.com/aoloe/scribus-script-repository/typographic-grid/
"""

import sys
try:
   import scribus
except ImportError:
    print "This script only works from within Scribus"
    sys.exit(1)
    # mock of the scribus API for running the script with defaults values from the terminal
    # (for testing and developping)
    # uncomment the two lines above if you think this is what you want...
    class Scribus :
        UNIT_MILLIMETERS = 0
        ICON_WARNING = 0
        ICON_NONE = 0
        BUTTON_OK = 0
        BUTTON_YES = 0
        BUTTON_NO = 0

        def haveDoc(self) :
            return True
        def messageBox(self, title, description,  icon, button1 = 0, button2 = 0, button3 = 0) :
            return button1
        def valueDialog(self, title, description, default = '') :
            return default
        def setRedraw(self, activate) :
            return True
        def getUnit(self) :
            return True
        def setUnit(self, unit) :
            return True
        def currentPage(self) :
            return 1
        def getPageNMargins(self, n) :
            return (14.1111111111, 14.1111111111, 14.1111111111, 14.1111111111) 
        def getPageNSize(self, n) :
            return (210.0, 297.0)
        def setVGuides(self, guides) :
            return True
        def setHGuides(self, guides) :
            return True
        def setBaseLine(self, line_height_mm, margin_top) :
            return True
    scribus = Scribus()

def setGuidesColumn(n, gap):
    print "setGuidesColumn should be a scribus API function"

    (margin_top, margin_left, margin_right, margin_bottom) = scribus.getPageNMargins(scribus.currentPage())
    (width, height) = scribus.getPageNSize(scribus.currentPage())
    cell_width = (width - (margin_left + margin_right) - (gap * (n - 1))) / n

    guide = []
    previous_guide = margin_left
    for i in range(0, n - 1):
        guide.append(previous_guide + cell_width)
        guide.append(previous_guide + cell_width + gap)
        previous_guide = previous_guide + cell_width + gap
    scribus.setVGuides(guide)

def setGuidesRow(n, gap):
    print "setGuidesRow should be a scribus API function"
    (margin_top, margin_left, margin_right, margin_bottom) = scribus.getPageNMargins(scribus.currentPage())
    (width, height) = scribus.getPageNSize(scribus.currentPage())
    cell_height = (height - (margin_top + margin_bottom) - (gap * (n - 1))) / n
    guide = []
    previous_guide = margin_top
    for i in range(0, n - 1):
        guide.append(previous_guide + cell_height)
        guide.append(previous_guide + cell_height + gap)
        previous_guide = previous_guide + cell_height + gap
    scribus.setHGuides(guide)

def get_page_line_count(page_inner_height, line_height_mm) : 
    page_line_count = int(page_inner_height / line_height_mm)

    page_line_overflow = page_inner_height % line_height_mm

    if page_line_overflow > 0 :
        if page_line_overflow > line_height_mm / 2 :
            page_line_count = page_line_count + 1

    return page_line_count

def get_cell_width(page_inner_width, column_count, gap) :
    cell_width = (page_inner_width - (gap * (column_count - 1))) / column_count
    return  cell_width

def get_row_count(page_inner_height, row_height, gap) :
    row_count = int((page_inner_height + gap) / (row_height + gap))
    row_height_overflow = (page_inner_height + gap) % (row_height + gap)

    if row_height_overflow > row_height / 2 :
        row_count = row_count - 1
    return row_count

def get_int_from_dialog_value(value) :
    if value == '' :
        value = 0 
    else :
        value = int(value)
    if value <= 0 :
        sys.exit(1)
    return value

def debug(label, value = '') :
    if False :
        print label+' '+str(value)

debug("############")

# this script makes no sense without a document open
if not scribus.haveDoc():
    scribus.messageBox('Scribus - Script Error', "No document open", scribus.ICON_WARNING, scribus.BUTTON_OK)
    sys.exit(1)

# environment initialization

unit_current=scribus.getUnit() #get unit and change it to mm
scribus.setUnit(scribus.UNIT_MILLIMETERS)

# some ratios for calculations

pt_to_mm_ratio = 10.0/37
cell_ratio = 2.0/3 # or 3/2
    

# input values
column_count = scribus.valueDialog('Number of columns', 'Please set the number of columns\n(sane values are 6, 9, 12, 24)', '6')
column_count = get_int_from_dialog_value(column_count)

font_size_main_text = scribus.valueDialog('Text size', 'Please set the font size for the main text\n(this value will be used)', '12')
font_size_main_text = get_int_from_dialog_value(font_size_main_text)

horizontal_cells = scribus.messageBox('Cells orientation', 'Should the cells be wider than higer?', scribus.ICON_NONE, scribus.BUTTON_YES, scribus.BUTTON_NO,)
if horizontal_cells == scribus.BUTTON_YES : # doc of return value of messageBox is wrong: it returns the value of the button
    horizontal_cells = True
else :
    horizontal_cells = False

# get the measurements from the current page
(page_width, page_height) = scribus.getPageNSize(scribus.currentPage())
(margin_top, margin_left, margin_right, margin_bottom) = scribus.getPageNMargins(scribus.currentPage())

page_inner_width = page_width - margin_left - margin_right
page_inner_height = page_height - margin_top - margin_bottom

# calculate the basic values
line_height = font_size_main_text * 1.5 # real ratio 1.618
line_height_mm = line_height * pt_to_mm_ratio

debug("line_height", line_height)
debug("line_height_mm", line_height_mm)

gap = line_height_mm

# calculate number of lines fitting the page and the number of rows
page_line_count = get_page_line_count(page_inner_height, line_height_mm)

debug("page_line_count", page_line_count)

column_width = get_cell_width(page_inner_width, column_count, gap)

debug("column_width", column_width)

row_height = 0
if (horizontal_cells) :
    row_height = column_width * (2.0/3)
else :
    row_height = column_width * (3.0/2)

debug("row_height", row_height)

row_count = get_row_count(page_inner_height, row_height, gap)

debug("row_count", row_count)

# adjust the number of the lines to be "divisable" by the number of rows

row_lines_count = page_line_count - (row_count - 1) # in the rows we put all the lines but the gaps

lines_per_row_overflow = row_lines_count % row_count

debug("lines_per_row_overflow", lines_per_row_overflow)

if lines_per_row_overflow > 0 :
    if lines_per_row_overflow < (row_count / 2) :
        while row_lines_count % row_count > 0 :
            row_lines_count = row_lines_count - 1
    else :
        while row_lines_count % row_count > 0 :
            row_lines_count = row_lines_count + 1

debug("row_lines_count", row_lines_count)

page_line_count = row_lines_count  + (row_count - 1) # in the rows we put all the lines but the gaps

lines_per_row = page_line_count / row_count

debug("lines_per_row", lines_per_row)

# calculate the line height, the gap, create the typographic grid and define the baseline grid

line_height_mm = page_inner_height / page_line_count

debug("line_height_mm", line_height_mm)

row_height = line_height_mm * lines_per_row
gap = line_height_mm

setGuidesColumn(column_count, gap)
setGuidesRow(row_count, gap)

base_line_start = margin_bottom % line_height_mm

scribus.setBaseLine(line_height_mm, base_line_start)

# restore the user environment

scribus.setUnit(unit_current)
