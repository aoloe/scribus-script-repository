#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: replacetext.py
# © 2014.06.06 Gregory Pittman
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
"""
USAGE
 
You must have a document open, and a text frame selected.
If you have more than one object or a non-text frame selected,
there will be an error generated, and the script will exit.
 
 
"""
import scribus
import random
 
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
        continue
    alpha = random.randint(1,26)
    letter = chr(alpha + 96)
    LETTER = chr(alpha + 64)
    if ((ord(char)>96)and(ord(char)<123)):
	scribus.deleteText(textbox)
	scribus.insertText(letter, c, textbox)
    if ((ord(char)>64)and(ord(char)<91)):
	scribus.deleteText(textbox)
	scribus.insertText(LETTER, c, textbox)
 
 
    c += 1
    contents = scribus.getTextLength(textbox)
 
scribus.setRedraw(1)
scribus.docChanged(1)
scribus.messageBox("Finished", "That should do it!",icon=0,button1=1)
