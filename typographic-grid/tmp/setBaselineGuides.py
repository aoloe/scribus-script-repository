#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The script generates a grid and matching guides. 
# Set the baseline grid spacing and offset values
# Useful to snap/align objects to a baseline grid.

# Written using v1.5.4
# Not suitable for v1.4.7

# Author: ugajin@zoho.com
# Date: October 8, 2017

import sys

try:
    import scribus
except ImportError,err:
    print "This Python script is written for the Scribus scripting interface."
    print "It can only be run from within Scribus."
    sys.exit(1)

import math 

def main(argv):
    """A simple scripts to set baseline grid and matching guides."""

    CurrentUnit = scribus.getUnit() 
    
    scribus.setUnit(0) 
    H_Guides = [] 
    
    GuideHeight = float(scribus.valueDialog('Set BaseLine Grid & Guides', 'Enter value for Grid and Guide Height (pt).', '14.40') )
    GuideOffset = float(scribus.valueDialog('Set Grid & Guide Offsets', 'Enter value for Grid and Guide Offset (pt).', '0.0') )
    
    PageWidth, PageHeight = scribus.getPageSize() 
    
    NumLoops = math.floor(1 + (PageHeight - GuideOffset) / GuideHeight)
    
    for i in range(int(NumLoops)):
    	if i > 0:
    		H_Guides.append(GuideOffset + i * GuideHeight)
    
    scribus.setBaseLine(GuideHeight, GuideOffset)
    scribus.setHGuides(scribus.getHGuides() + H_Guides)
    
    scribus.setUnit(CurrentUnit)
    
    scribus.messageBox('Script', '<h3>Script by ugajin</h3><p>Thanks a bunch for using setBaselineGuides and Scribus!</p><p>ugajin@zoho.com</p>', scribus.ICON_INFORMATION, scribus.BUTTON_OK, scribus.BUTTON_CANCEL)
    
    

def main_wrapper(argv):
    try:
        scribus.statusMessage("Running script...")
        scribus.progressReset()
        main(argv)
    finally:
        if scribus.haveDoc():
            scribus.setRedraw(True)
        scribus.statusMessage("")
        scribus.progressReset()

if __name__ == '__main__':
    main_wrapper(sys.argv)