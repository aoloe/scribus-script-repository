# replace fonts in the whole document
#
# © mit, ale rimoldi, 2023

try:
    import scribus
except ImportError:
    print('This script must be run from inside Scribus')

def main():
    if not scribus.haveDoc():
        scribus.messagebarText("No document open.") 
        return

    if scribus.selectionCount() == 0:
        scribus.messagebarText("No frame selected.") 
        return

    if scribus.selectionCount() > 1:
        scribus.messagebarText("Please select one single frame.") 
        return

    image_frame = scribus.getSelectedObject()

    image = scribus.fileDialog('Open image file', '*.jpg *.jpeg *.png *.tif')
    if image == '':
        return

    offset = scribus.getImageOffset()
    scale = scribus.getImageScale()
    scribus.loadImage(image)
    scribus.setImageScale(scale[0], scale[1])
    scribus.setImageOffset(offset[0], offset[1])

if __name__ == '__main__':
    main()
