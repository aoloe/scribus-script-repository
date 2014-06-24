#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: replacetext_v2.py
# © 2014.06.06 Gregory Pittman
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
"""
USAGE
 
You must have a document open.
WARNING: this script irreversibly scrambles your text
 
 
"""
import scribus
import random
 
if scribus.haveDoc():
    c = 0
 
else:
    scribus.messageBox('Usage Error', 'You need a Document open', icon=0, button1=1)
    sys.exit(2)
 
warnresult = scribus.valueDialog('Warning!', 'This script is going to irreveribly alter the text in your document.\nChange this default value to abort', 'Ok!')
 
if (warnresult != 'Ok!'):
    sys.exit(2)
 
pageitems = scribus.getPageItems()
 
for item in pageitems:
    if (item[1] == 4):
      c = 0
      textbox = item[0]
      scribus.selectObject(textbox)
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
