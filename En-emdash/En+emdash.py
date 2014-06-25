#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: en+emdash.py - convert hyphens to en and em dashes
# © 2014.04.27 Gregory Pittman
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
"""
USAGE
 
You must have a document open, and a text frame selected.
There are no dialogs. The presumption is that you have encoded a single
hyphen to mean a single hyphen, two hyphens to mean an en-dash, and three
hyphens to mean an em-dash.
 
"""
import scribus
 
if scribus.haveDoc():
    c = 0
 
else:
    scribus.messageBox('Usage Error', 'You need a Document open', icon=0, button1=1)
    sys.exit(2)
 
if scribus.selectionCount() == 0:
    scribus.messageBox('Scribus - Usage Error',
        "There is no object selected.\nPlease select a text frame and try again.",
        scribus.ICON_WARNING, scribus.BUTTON_OK)
    sys.exit(2)
if scribus.selectionCount() > 1:
    scribus.messageBox('Scribus - Usage Error',
        "You have more than one object selected.\nPlease select one text frame and try again.", scribus.ICON_WARNING, scribus.BUTTON_OK)
    sys.exit(2)
textbox = scribus.getSelectedObject()
pageitems = scribus.getPageItems()
boxcount = 1
for item in pageitems:
    if (item[0] == textbox):
        if (item[1] != 4):
            scribus.messageBox('Scribus - Usage Error', "This is not a textframe. Try again.", scribus.ICON_WARNING, scribus.BUTTON_OK)
            sys.exit(2)
contents = scribus.getTextLength(textbox)
 
ndash = u"\u2013"
mdash = u"\u2014"
prevchar = ''
 
while 1:
    if ((c == contents) or (c > contents)): break
    if ((c + 1) > contents - 1):
        nextchar = ' '
    else:
        scribus.selectText(c+1, 1, textbox)
        nextchar = scribus.getText(textbox)
    scribus.selectText(c, 1, textbox)
    char = scribus.getText(textbox)
    if (len(char) != 1):
        c += 1
 
    if (char == '-'):
 
      if (prevchar == '-'):
	if (nextchar == '-'):
	  scribus.selectText(c-1, 3, textbox)
	  scribus.deleteText(textbox)
	  scribus.insertText(mdash, c-1, textbox)
	  char = mdash
	else:
	  scribus.selectText(c-1, 2, textbox)
	  scribus.deleteText(textbox)
	  scribus.insertText(ndash, c-1, textbox)
	  char = ndash
      else:
	c += 1
 
    else:
	c += 1
 
    prevchar = char
    contents = scribus.getTextLength(textbox)
 
scribus.setRedraw(1)
scribus.docChanged(1)
scribus.messageBox("Finished", "That should do it!",icon=0,button1=1)
