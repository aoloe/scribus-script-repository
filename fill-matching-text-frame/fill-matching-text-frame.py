# Look for all text frames with a name that start with pattern and
# set the content to content.
#
# - Create an original document.
# - Name all the fields that have to be synchronized with the same
#   starting string (Month01, Month02, ...)
# - Make a copy of the document for each actual document.
# - Do not run this script on the original document.
# - Set the "master" field to the correct value.
# - Run the script.
# - In 1.5.x use the frame patterns, instead.
#
# TODO:
# - Get the pattern by stripping the numbers from the name
#   of the current frame
# - Find a way to rename the created frames.
#
# 2016-09-13 Ale Rimoldi
#
#
# Copyright (c) 2016, Ale Rimoldi
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import scribus

def fileMatchingTextFrame(sampleFrameName, pattern):
    pagenum = scribus.pageCount()
    T = []
    # duplicateName = duplicate current frame
    for page in range(1, pagenum):
        scribus.gotoPage(page)
        d = scribus.getPageItems()
        strpage = str(page)
        T.append('Page '+ strpage + '\n\n')
        for item in d:
            # print(item)
            frameName = item[0]
            if (item[1] == 4):
                if (frameName.startswith(pattern)):
                    # print(frameName)
                    position = scribus.getPosition(frameName)
                    scribus.selectObject(sampleFrameName)
                    scribus.duplicateObject()
                    #duplicateFrameName = scribus.getSelectedObject()
                    scribus.moveObjectAbs(position[0], position[1])
                    scribus.deleteObject(frameName)
                    # TODO: rename the duplicate to the old frameName
    # scribus.messageBox("Finished", "String replaced" ,icon=0,button1=1)

if not scribus.haveDoc():
    scribus.messageBox('Usage Error', 'You need a Document open', icon=0, button1=1)
    sys.exit(2)
 
if scribus.selectionCount() == 0:
    scribus.messageBox('Scribus - Usage Error',
        "There is no frame selected.\nPlease select a text frame and try again.",
        scribus.ICON_WARNING, scribus.BUTTON_OK)
    sys.exit(2)

if scribus.selectionCount() > 1:
    scribus.messageBox('Scribus - Usage Error',
        "You have more than one frame selected.\nPlease select one text frame and try again.", scribus.ICON_WARNING, scribus.BUTTON_OK)
    sys.exit(2)
 
currentFrameName = scribus.getSelectedObject()
print(currentFrameName)

if (scribus.getObjectType(currentFrameName) == 4):
    scribus.messageBox('Scribus - Usage Error', "You did not select a textframe. Try again.", scribus.ICON_WARNING, scribus.BUTTON_OK)
    sys.exit(2)

scribus.duplicateObject()
duplicateFrameName = scribus.getSelectedObject()

print(duplicateFrameName)

# valueDialog(caption, message [,defaultvalue])
fileMatchingTextFrame(duplicateFrameName, "Monat")

scribus.deleteObject(duplicateFrameName)
# scribus.selectObject(currentFrameName) // we will be able to this if we can set the frame's name
