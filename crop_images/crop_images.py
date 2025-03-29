""" Crop the images in the selection

TODO:
- take the maximum resolution from the preflight verifier maximum resolution
  (add a function to read the preflight verifier settings and one for the results)

© mit, ale rimoldi, 2023
"""

try:
    import scribus # pylint: disable=import-error
except ImportError:
    pass

try:
    # if PIL / Pillow is installed in non standard location (and not recognized):
    #sys.path.append('C:\\Users\\Python37\\Lib\\site-packages')  # Windows
    #sys.path.append('/usr/lib/python3/dist-packages')   # Linux
    from pillow import Image # pylint: disable=import-error
except ImportError:
    pass

import logging

# TODO: read it from a json file. if it does not exists, create it and fill it with the defaults: sla-filename-crop.json
IMAGE_RESOLUTION = 300 # TODO: we should read it from the maximum in the preflight verifier

def crop_image(item):
    image_filename = scribus.getImageFile(item)
    if image_filename == "":
        return

    try:
        image = Image.open(image_filename)
    except:
        scribus.messageBox('Warning:', f'Failed to open {image_filename} for {item}',
            scribus.ICON_WARNING)
        return

    document_unit = scribus.getUnit()

    scribus.setUnit(scribus.UNIT_INCHES)
    frame_width_in, frame_height_in = scribus.getSize(item)
    # TODO: what is it doing here?
    # TODO: do not scale if resolution is smaller than the target
    target_image_width = int(frame_width_in * IMAGE_RESOLUTION)
    target_image_height = int(frame_height_in * IMAGE_RESOLUTION)

    scribus.setUnit(scribus.UNIT_POINTS)

    frame_width, frame_height = scribus.getSize(item)
    image_x_offset = int(scribus.getProperty(item, 'imageXOffset'))
    image_y_offset = int(scribus.getProperty(item, 'imageYOffset'))
    image_x_scale = int(scribus.getProperty(item,'imageXScale'))
    image_y_scale = int(scribus.getProperty(item,'imageYScale'))
    image_width, image_height = image.size

    crop_box_left = - image_x_offset
    crop_box_top = - image_y_offset
    crop_box_right = crop_box_left + frame_width // image_x_scale
    crop_box_bottom = crop_box_top + frame_height // image_y_scale

    # do not crop if the image does not fill the frame
    if image_x_offset > 0 or image_y_offset > 0 or \
            crop_box_right > image_width or crop_box_bottom > image_height:
        scribus.messageBox('Warning:', f'The image does not fill the frame {item}.',
            scribus.ICON_WARNING)
        return

    # TODO: if the filename for the cropped image exists, add an index

def main():
    try:
        scribus
    except NameError:
        print('This script must be run from inside Scribus.')
        return

    try:
        image
    except NameError:
        print('Could not find the Pillow / PIL Python package.')
        return

    if not scribus.haveDoc():
        scribus.messageBox('Export Error', 'You need an open document.', icon=scribus.ICON_CRITICAL)
        return

    # TODO: use logging instead of messageBox
    # logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    # logging.debug('This message should go to the log file')
    # logging.warning('And this, too')
    # logging.error('And non-ASCII stuff, too, like Øresund and Malmö')
    # logging.warning('%s before you %s', 'Look', 'leap!') # f-strings are not necessary
    # if 40 in logger._cache and logger._cache[40]... to check if something has been logged
    # log to sla-filename-crop.log

    for i in range(scribus.selectionCount()):
        item = scribus.getSelectedObject(i)
        item_type = scribus.getObjectType(item)
        if item_type == 'ImageFrame':
            crop_image(item)
        elif item_type == 'Group':
            if hasattr(scribus, 'getGroupItems'):
                for item in scribus.getGroupItems(item,
                        recursive=True, type=scribus.ITEMTYPE_IMAGEFRAME):
                    crop_image(item['name'])
            else:
                scribus.messageBox('Warning', f'The group {item} will be skipped.', scribus.ICON_WARNING)

if __name__ == '__main__':
    main()
