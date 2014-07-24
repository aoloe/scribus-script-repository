#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: paste2pagelist.py
# © 2012.03.22 Gregory Pittman
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
 
"""
USAGE
 
You must have a document open. Select a single object. Run the script, which asks for a list
 
of page numbers -- do not use commas to separate, just whitespace.
 
When pasted, the copies go to the same page coordinates of the original.
 
The script will work with a group. If you select more than one item without grouping, 
 
an error is generated.
 
"""
 
import scribus
 
if scribus.haveDoc():
    if scribus.selectionCount() == 0:
        scribus.messageBox('Scribus - Usage Error',
                           "There is no object selected.\nPlease try again.",
                           scribus.ICON_WARNING, scribus.BUTTON_OK)
        sys.exit(2)
    if scribus.selectionCount() > 1:
        scribus.messageBox('Scribus - Usage Error', "You have more than one object selected.
                                 \nPlease select one object and try again.", scribus.ICON_WARNING, scribus.BUTTON_OK)
        sys.exit(2)
    pagelist = scribus.valueDialog('Paste to...',"Paste to which pages?
                                 \n(page numbers, separated by white space)","1")
    pageslist = pagelist.split()
    selframe = scribus.getSelectedObject()
    pages = scribus.pageCount()
    for p in pageslist:
        p_no = int(p)
        if ((p_no > pages) or (p_no < 1)):
            scribus.messageBox('OOPS!', "You have a page number outside the range of pages in your document",
                      scribus.ICON_WARNING, scribus.BUTTON_OK)
            sys.exit(2)
    scribus.copyObject(selframe)
    for p in pageslist:
        p_no = int(p)
        scribus.gotoPage(p_no)
        scribus.pasteObject(selframe)
    scribus.setRedraw(1)
    scribus.docChanged(1)
    scribus.messageBox("Finished", "Done",icon=0,button1=1)
else:
    scribus.messageBox('Usage Error', 'You need a Document open', icon=0, button1=1)
    sys.exit(2)
