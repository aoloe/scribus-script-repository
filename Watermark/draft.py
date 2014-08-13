#!/usr/bin/env python
 
'''
A script to place a light grey watermark 'DRAFT' on a new layer. 
Requires an existing document, but can be modified to 
create a new document if it does not exist
 
uses (See the API in Help->Scribus Manual->For Developers->Scripter API;
 haveDoc
 createLayer
 getActiveLayer
 setActiveLayer
 createText
 setUnit
 setText
 setTextColor
 setFontSize
 rotateObject
Tested on 1.4.3 and A2, A4, A5, Letter. 
'''
 
from scribus import *
 
# Could be expanded to include localization here
draft  = "DRAFT"
#draft = "ENTWURF"
#draft = "BROUILLON"
 
L = len(draft)                                	# The length of the word 
                                              	# will determine the font size
defineColor("gray", 11, 11, 11, 11)           	# Set your own color here
 
if haveDoc():
    u  = getUnit()                            	# Get the units of the document
    al = getActiveLayer()                     	# Identify the working layer
    setUnit(UNIT_MILLIMETERS)                 	# Set the document units to mm,                                            
    (w,h) = getPageSize()                     	# needed to set the text box size
 
    createLayer("c")
    setActiveLayer("c")
 
    T = createText(w/6, 6*h/10 , h, w/2)  # Create the text box
    setText(draft, T)                         	# Insert the text
    setTextColor("gray", T)                  	# Set the color of the text
    setFontSize((w/210)*(180 - 10*L), T)     	# Set the font size according to length and width
 
    rotateObject(45, T)                      	# Turn it round antclockwise 45 degrees
    setUnit(u)                               	# return to original document units
    setActiveLayer(al)                       	# return to the original active layer
