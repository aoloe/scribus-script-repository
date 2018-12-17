# - get the directory with all images
# - on the first page where you want the image create an image frame of the right size
# - select the empty image frame
# - run the script
# - the script copies the frame, then loads the first image in the exiting frame
# - then on other following pages paste the emtpy frame and load the next image
# - if there are not enough pages, create them to put all the images in the directory
#
# 1.5 only, since it uses copy/paste of objects
# it's untested.
import os
import sys
import scribus

if not scribus.haveDoc():
    scribus.messagebarText("No .") 
    sys.exit()

path = "/tmp/t/lot_forum"
extensions = ['jpg', 'png', 'tif']
filenames = [f for f in os.listdir(path)
              if any(f.endswith(ext) for ext in extensions)]
if not filenames:
    scribus.messagebarText("No image found.") 
    sys.exit()

page = 1
n_pages = scribus.pageCount()

scribus.copyObject()

scribus.loadImage(filenames[0])
filenames = filenames[1:]

for filename in filenames:
    if page <= n_pages:
        scribus.gotoPage(page)
    else:
        scribus.newPage(-1)
        scribus.gotoPage(scribus.pageCount())
        page_item = scribus.pasteObject()
        scribus.loadImage(filename, page_item)
