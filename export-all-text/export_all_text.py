# Extracts the text from a document, saving to a text file
# also lists image files with pathnames
# 2006-03-04 Gregory Pittman
# 2008-02-28 Petr Vanek - fileDialog replaces valueDialog
# 2019-09-16 Ale Rimoldi - modernize the code
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import scribus

def exportText(filename):
    file_content = []
    content = []
    for page in range(1, scribus.pageCount() + 1):
        scribus.gotoPage(page)
        file_content.append('Page '+ str(page) + '\n\n')
        for item in scribus.getPageItems():
            if item[1] == 4:
                contents = scribus.getAllText(item[0])
                if contents in content:
                    contents = 'Duplication, perhaps linked-to frame'
                file_content.append(item[0]+': '+ contents + '\n\n')
                content.append(contents)
            elif item[1] == 2:
                imgname = scribus.getImageFile(item[0])
                file_content.append(item[0]+': ' + imgname + '\n')
        file_content.append('\n')
    output_file = open(filename, 'w')
    output_file.writelines(file_content)
    output_file.close()
    # scribus.messageBox("Finished", filename + ' was created', icon=0, button1=1)


if scribus.haveDoc():
    filename = scribus.fileDialog('Enter name of file to save to', \
                                  filter='Text Files (*.txt);;All Files (*)')
    try:
        if filename == '':
            raise Exception
        exportText(filename)
    except Exception, e:
        print e

else:
    scribus.messageBox('Export Error', 'You need a Document open, and a frame selected.', \
                       icon=0, button1=1)
