"""Write the list of all images in the document into a JSON file.

The JSON file contains a dictionary with the page number (or rather the index,
starting with 1) as a key  and a list of paths as the value.

© 2014, MIT license, Ale Rimoldi <a.l.e@graphicslab.org>
"""

import json

try:
    import scribus # pylint: disable=import-error
except ImportError:
    pass

def get_images():
    """return a dict of pages and image paths from the current document"""
    images = {}

    for page in range(scribus.pageCount()):
        items = scribus.getAllObjects(2, page)
        if len(items) == 0:
            continue
        images[page + 1] = []
        for item in items:
            path = scribus.getImageFile(item)
            if path == '':
                continue
            images[page + 1].append(path)
    return images

def main():
    try:
        scribus
    except NameError:
        print('This script must be run from inside Scribus')
        return

    if not scribus.haveDoc():
        scribus.messageBox('Export Error', 'You need an open document.', icon=scribus.ICON_CRITICAL)
        return

    images = get_images()

    filename = scribus.fileDialog('Enter name of file to save to', \
        filter='JSON Files (*.json);;All Files (*)')
    if filename == '':
        return

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(images, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()
