#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: invisibleImages.py
# © 2014.07.06 Gregory Pittman
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
"""
USAGE
 
You must have a document open.
 
This script moves all images to a new layer called "Ghostlayer",
the idea being that you can show/hide, print-export/not as desired.
 
"""
import scribus
 
if scribus.haveDoc():
 
  fantome = "Ghostlayer"
  scribus.createLayer(fantome)
  working = scribus.getActiveLayer()
  page = 1
  pagenum = scribus.pageCount()
  while (page <= pagenum):
    scribus.gotoPage(page)
    scribus.setActiveLayer(working)  # maybe not necessary?  
    pageitems = scribus.getPageItems()
 
    for item in pageitems:
      if (item[1] == 2):
	imagebox = item[0]
	scribus.selectObject(imagebox)
	scribus.copyObject(imagebox)
	scribus.setActiveLayer(fantome)
	scribus.pasteObject(imagebox)
	scribus.deleteObject(imagebox)
	scribus.setActiveLayer(working)
    page += 1
  scribus.setLayerPrintable(fantome, 0)  # comment this out to do manually later
  scribus.setLayerVisible(fantome, 0)    # comment this out to do manually later
  scribus.setRedraw(1)
  scribus.docChanged(1)
  scribus.messageBox("Finished", "That should do it!",icon=0,button1=1)
 
else:
    scribus.messageBox('Usage Error', 'You need a Document open', icon=0, button1=1)
    sys.exit(2)
