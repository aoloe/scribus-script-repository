# - get the directory with all images
# - on the first page where you want the image create an image frame of the right size
# - select the empty image frame
# - run the script
# - the script copies the frame, then loads the first image in the exiting frame
# - then on other following pages paste the emtpy frame and load the next image
# - if there are not enough pages, create them to put all the images in the directory
import os
import sys
import scribus

if not scribus.haveDoc():
    scribus.messagebarText("No .") 
    sys.exit()

if scribus.selectionCount() == 0:
    scribus.messagebarText("No frame selected.") 
    sys.exit()

if scribus.selectionCount() > 1:
    scribus.messagebarText("Please select one single frame.") 
    sys.exit()

master_frame = scribus.getSelectedObject()

x,y = scribus.getPosition()
width, height = scribus.getSize()


path = scribus.fileDialog("Pick a directory", scribus.getDocName(), isdir = True)
if path == '':
    scribus.messagebarText("No directory selected.") 
    

extensions = ['jpg', 'png', 'tif']
filenames = [f for f in os.listdir(path)
              if any(f.endswith(ext) for ext in extensions)]

if not filenames:
    scribus.messagebarText("No image found.") 
    sys.exit()

# sorted(filenames)
filenames.sort()

scribus.loadImage(filenames[0])
filenames = filenames[1:]

page = scribus.currentPage() + 1
n_pages = scribus.pageCount()

for filename in filenames:
    print(filename)
    if page <= n_pages:
        scribus.gotoPage(page)
    else:
        # TODO: currently this does not work if there are multiple master pages
        # (facing pages). you need to create all pages before loading the images.
        scribus.newPage(-1)
        scribus.gotoPage(scribus.pageCount())
    new_image = scribus.createImage(x, y, width, height)
    scribus.setScaleImageToFrame(True, True, new_image)
    scribus.loadImage(filename, new_image)
    page += 1
