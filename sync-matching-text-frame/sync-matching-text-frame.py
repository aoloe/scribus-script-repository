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
# - It will work also if you don't make a copy first, but you'd better avoid it.
# - In 1.5.x use the frame patterns, instead.
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
import re

def remove_copy_prefix(text):
    for prefix in ("Copy of ", "Kopie von "):
        if text.startswith(prefix):
            text = text[len(prefix):]
    return text

def checkForOneFrameSelected() :
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

def fileMatchingTextFrame(sampleFrameName, pattern):
    pagenum = scribus.pageCount()
    for page in range(1, pagenum + 1):
        scribus.gotoPage(page)
        d = scribus.getPageItems()
        for item in d:
            # print(item)
            frameName = item[0]
            if (item[1] == 4):
                if frameName != sampleFrameName and remove_copy_prefix(frameName).startswith(pattern):
                    print(frameName + " found")
                    position = scribus.getPosition(frameName)
                    scribus.selectObject(sampleFrameName)
                    scribus.duplicateObject()
                    #duplicateFrameName = scribus.getSelectedObject()
                    scribus.moveObjectAbs(position[0], position[1])
                    scribus.deleteObject(frameName)
                    # TODO: rename the duplicate to the old frameName

checkForOneFrameSelected()
 
currentFrameName = scribus.getSelectedObject()
print(currentFrameName)

if (scribus.getObjectType(currentFrameName) == 4):
    scribus.messageBox('Scribus - Usage Error', "You did not select a textframe. Try again.", scribus.ICON_WARNING, scribus.BUTTON_OK)
    sys.exit(2)

# the pattern is the name of the current frame up to the first digit
# and with the "Copy of " at the beginning stripped away.
matchNonDigit = re.compile(r'(^\D+)')
matchResult = matchNonDigit.search(currentFrameName)
pattern = matchResult.group(1)
pattern = remove_copy_prefix(pattern)
pattern = remove_copy_prefix(pattern)
print("pattern: " + pattern)

scribus.duplicateObject()
duplicateFrameName = scribus.getSelectedObject()

print(duplicateFrameName)

fileMatchingTextFrame(duplicateFrameName, pattern)

scribus.deleteObject(duplicateFrameName)
