# -*- coding: utf-8 -*-
# © 2014, MIT license, Ale Rimoldi <a.l.e@graphicslab.org>
#
# List all images in a document into a text file
#
# USAGE
#  
# Run this script from the Scribus Scripter.
# You must have a document open.

import scribus

def listImages(filename):

    file_content = []
    for page in range(1, scribus.pageCount() + 1):
        scribus.gotoPage(page)
        file_content.append('Page ' + str(page) + '\n\n')
        for item in scribus.getPageItems():
            if item[1] == 2:
                file_content.append(scribus.getImageFile(item[0]) + '\n')

        file_content.append('\n')
    output_file = open(filename, 'w')
    output_file.writelines(file_content)
    output_file.close()

if scribus.haveDoc():
    filename = scribus.fileDialog('Enter name of file to save to', \
        filter='Text Files (*.txt);;All Files (*)')
    try:
        if filename == '':
            raise Exception
        listImages(filename)
    except Exception, e:
        print(e)

else:
    scribus.messageBox('Export Error', 'You need a Document open, and a frame selected.', \
        icon=0, button1=1)
