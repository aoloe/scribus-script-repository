# © 2014.07.06 Gregory Pittman
# © 2023 ale riomldi
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
"""
This script moves all images in the current layer to a specific layer.
The idea being that you can show/hide, print-export/not as desired.

You must have a document open.
"""
 
def main():
    try:
        import scribus

        if not scribus.haveDoc():
            return
    except ImportError:
        print('This script must be run from inside Scribus')
        # return

    current_layer = scribus.getActiveLayer()

    layers = scribus.getLayers()
    try:
        target_layer = scribus.itemDialog('Choose a layer', 'Choose one of the layers or type the name of the layer to be created:', layers, True)
    except:
        # scribus.itemDialog() has been crated for this script and might not yet be in your scribus
        target_layer = scribus.valueDialog('Choose a layer', 'Choose one of the layers or type the name of the layer to be created:')
    if target_layer == '':
        return
    if not target_layer in layers:
        scribus.createLayer(target_layer)
        scribus.setActiveLayer(current_layer)

    for page in range(scribus.pageCount()):
        scribus.gotoPage(page + 1)
        for item in scribus.getPageItems():
            if item[1] != 2:
                continue
            scribus.sendToLayer(target_layer, item[0])
            imagebox = item[0]

    scribus.setRedraw(True)
    scribus.docChanged(True)
     
if __name__ == '__main__':
   main()
