# -*- coding: utf-8 -*-
# © 2014, MIT license, Ale Rimoldi <a.l.e@graphicslab.org>
"""
USAGE
 
You must have a document open, and at least one text frame selected.
 
"""
import scribus
import random
import os
import distutils.spawn
 
if not scribus.haveDoc():
    scribus.messageBox('Usage Error', 'You need a Document open', icon=0, button1=1)
    sys.exit(2)

charsIgnore = ["-", "–", "­", " ", ".", ":", ";", ";", "?", "!", "\n", "'", "‘", "’", "," "\"", "“", "”", "\r"]

button = scribus.messageBox('Confirmation', 'You should only scramble a copy of your document', scribus.ICON_WARNING, scribus.BUTTON_OK, scribus.BUTTON_CANCEL)
print button
if button == scribus.BUTTON_CANCEL :
    sys.exit(2)

selectedFrame = []
textFrame = []
imageFrame = []
if scribus.selectionCount() == 0:
    for page in range(scribus.pageCount()) :
        scribus.gotoPage(page + 1)
        scribus.messagebarText("Processing Page "+str(page))
        scribus.redrawAll()
        for item in scribus.getPageItems() :
            if (item[1] == 4):
                textFrame.append(item[0])
            elif (item[1] == 2) :
                imageFrame.append(item[0])
else :
    for i in range(scribus.selectionCount()) :
        item = scribus.getSelectedObject(i)
        selectedFrame.append(item)
        if scribus.getObjectType(item) == "TextFrame" :
            textFrame.append(item)
        if scribus.getObjectType(item) == "ImageFrame" :
            imageFrame.append(item[0])

# print textFrame
# print imageFrame

scribus.deselectAll()
chars = []
for item in textFrame :
    scribus.deselectAll()
    scribus.selectObject(item)
    n = scribus.getTextLength()
    for i in range(n) :
        scribus.selectText(i, 1)
        char = scribus.getText()
        if (char not in charsIgnore and len(char) > 0) :
            chars.append(char.lower())

random.shuffle(chars)

for item in textFrame :
    scribus.messagebarText("Processing text frame "+item)
    scribus.redrawAll()
    print item
    scribus.deselectAll()
    scribus.selectObject(item)
    n = scribus.getTextLength()
    print n
    for i in range(n) :
        scribus.selectText(i, 1)
        original = scribus.getText()
        if original not in charsIgnore and len(original) > 0:
            shuffled = chars.pop(0)
            if original.isupper() :
                shuffled = shuffled.upper()
            scribus.insertText(shuffled, i)
            scribus.selectText(i + 1, 1)
            scribus.deleteText()

for item in imageFrame :
    print item
    scribus.messagebarText("Processing image frame "+item)
    scribus.redrawAll()
    imageFile = scribus.getImageFile(item)
    fileName, fileExtension = os.path.splitext(imageFile)
    imageFileBlurred = fileName+"_blurred"+fileExtension
    # TODO: instead of using image magick we should expos scribus' own blur to the scripter
    if distutils.spawn.find_executable("convert") != "" :
        command = "identify "+imageFile
        result = os.popen(command).read();
        if result != "" :
            size = max(result.split(" ")[2].split("x")) # extract max(width, height)
            command = "convert "+imageFile+" -blur 0x"+str(int(size)/50)+" "+imageFileBlurred
            # print  command
            os.system(command)
            scribus.loadImage(imageFileBlurred, item)

scribus.deselectAll()
for item in selectedFrame :
    scribus.selectObject(item)
 
scribus.messagebarText("Finished, The text has been shuffled")
scribus.setRedraw(1)
scribus.docChanged(1)

