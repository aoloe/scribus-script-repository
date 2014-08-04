#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: paste2all.py
# © 2012.01.29 Gregory Pittman
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
 
"""
USAGE
 
You must have a document open. Select a single object. Run the script, which asks whether you want
 
all, odd, or even pages to get a copy of the selected object (no copy is made to the original
 
page of the object). Any other input is ignored. When pasted, the copies go to the same page
 
coordinates of the original.
 
The script will also work with a group, but if you select more than one item without grouping, 
 
an error is generated. This isn't completely necessary, but otherwise only one object would be 
 
copied and pasted.
 
"""
import scribus
if scribus.haveDoc():
    if scribus.selectionCount() == 0:
        scribus.messageBox('Scribus - Usage Error',
                           "There is no object selected.\nPlease try again.",
                           scribus.ICON_WARNING, scribus.BUTTON_OK)
        sys.exit(2)
    if scribus.selectionCount() > 1:
        scribus.messageBox('Scribus - Usage Error', "You have more than one object selected.\nPlease select only one object and try again.", scribus.ICON_WARNING, scribus.BUTTON_OK)
        sys.exit(2)
    paste2 = scribus.valueDialog('Paste to...',"Paste where?\n(all, odd, even)","all")
    selframe = scribus.getSelectedObject()
    pages = scribus.pageCount()
    currpage = scribus.currentPage()
    scribus.copyObject(selframe)
    if (paste2 == 'all'):
        i = 1
        while (i <= pages):
            if (i != currpage):
                scribus.gotoPage(i)
                scribus.pasteObject(selframe)
            i=i+1
    elif (paste2 == 'odd'):
        i = 1
        while (i <= pages):
            if (i != currpage):
                scribus.gotoPage(i)
                scribus.pasteObject(selframe)
            i=i+2
    elif (paste2 == 'even'):
        i = 2
        while (i <= pages):
            if (i != currpage):
                scribus.gotoPage(i)
                scribus.pasteObject(selframe)
            i=i+2
    scribus.setRedraw(1)
    scribus.docChanged(1)
    scribus.messageBox("Finished", "Done",icon=0,button1=1)
else:
    scribus.messageBox('Usage Error', 'You need a Document open', icon=0, button1=1)
    sys.exit(2)
