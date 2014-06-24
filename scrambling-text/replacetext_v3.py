# -*- coding: utf-8 -*-
# © 2014.06.06 Gregory Pittman
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
"""
USAGE
 
You must have a document open.
WARNING: this script irreversibly scrambles your text on all pages.
You would be wise to work on a copy of the original to avoid 
accidentally saving this scrambled version only to lose the original.
"""

import scribus
import random
 
if scribus.haveDoc():
    c = 0
 
else:
    scribus.messageBox('Usage Error', 'You need a Document open', icon=0, button1=1)
    sys.exit(2)
scribus.messagebarText("Getting ready to process Page 1")  # a bit kludgey maybe, but gives an initial message about Page 1
scribus.redrawAll()
 
warnresult = scribus.valueDialog('Warning!', 'This script is going to irreversibly alter the text in your document.\nChange this default value to abort', 'Ok!')
 
if (warnresult != 'Ok!'):
    sys.exit(2)
 
page = 1
pagenum = scribus.pageCount()
while (page <= pagenum):
  scribus.gotoPage(page)
  scribus.messagebarText("Processing Page "+str(page)) # New Feature! - sends a message to message bar 
  scribus.redrawAll()                                  # this allows the message to show
 
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
	  if (len(char) != 1):   # here is where you skip over any nonprinting characters
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
  page += 1
 
scribus.setRedraw(1)
scribus.docChanged(1)
scribus.messageBox("Finished", "That should do it!",icon=0,button1=1)
