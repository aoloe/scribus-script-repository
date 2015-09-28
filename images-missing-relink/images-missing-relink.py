# -*- coding: utf-8 -*-
# © 2015.09.22 ale rimoldi <ale@graphicslab.org>
# This program is free software under the MIT license.
"""
USAGE
 
You must have a document open.
This script checks if the document contains image frames with a broken link.
If any is found, it will ask if you want to look for the correct image and then
prompt for the new location of the first image.
It will then check all other image frames with a broken link, and look for an image
of the same name in the new location. It the image is there, the link will be
replaced.

You would be wise to work on a copy of the original to avoid accidentally include
the wrong images.
"""

import scribus
import os.path

page_n = scribus.pageCount()
item_missing = []

# create a list of items with a brokein link
for page_i in range(0, page_n) :
    scribus.gotoPage(page_i + 1)
    item_list = scribus.getPageItems()
    #print(item_list)
    for item in item_list :
        if item[1] == 2 :
            image_filepath = ""
            image_filepath = scribus.getImageFile(item[0])
            print(image_filepath)
            if image_filepath != "" and not os.path.isfile(image_filepath) :
                item_missing.append((item[0], image_filepath))
# print(item_missing)

# read the link for the first image with a broken link and try to apply the path
# to each other image with a broken link
if item_missing :
    if scribus.messageBox("Missing images", "There are missing images. Do you want to look for them?", scribus.ICON_WARNING, scribus.BUTTON_YES, scribus.BUTTON_NO) == scribus.BUTTON_YES:
        filename_found = scribus.fileDialog("Find "+os.path.basename(item_missing[0][1]), "Image files (*."+os.path.splitext(item_missing[0][1])[1][1:]+")")
        # print(filename_found)

        if filename_found:
            path_found = os.path.dirname(filename_found)
            # print("path_found "+path_found)
            for item in item_missing:
                item_filename = os.path.join(path_found, os.path.basename(item[1]))
                # print(item_filename)
                if os.path.isfile(item_filename) :
                    scribus.loadImage(item_filename, item[0])
