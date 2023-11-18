"""Extract the text from a document, saving to a text file

Include the paths to the images in the document.

Based on work started by  Gregory Pittman (2006-03-04) and improved by Petr Vanek (2008-02-28)

© mit, ale rimoldi, 2023
"""

try:
    import scribus # pylint: disable=import-error
except ImportError:
    pass

def export_text(filename):
    """Store in the text file the content of the text frame and the paths to the images."""
    current_page = scribus.currentPage()
    with open(filename, 'w', encoding='utf-8') as f:
        for page in range(1, scribus.pageCount() + 1):
            scribus.gotoPage(page)
            f.write('Page '+ str(page) + '\n\n')
            for item in scribus.getPageItems():
                if item[1] == 4 and scribus.getPrevLinkedFrame(item[0]) is None:
                    f.write(item[0]+': '+ scribus.getAllText(item[0]) + '\n\n')
                elif item[1] == 2:
                    image = scribus.getImageFile(item[0])
                    if image == '':
                        continue
                    f.write(item[0]+': '+ image + '\n\n')
    scribus.gotoPage(current_page)

def main():
    try:
        scribus
    except NameError:
        print('This script must be run from inside Scribus')
        return

    if not scribus.haveDoc():
        scribus.messageBox('Export Error', 'You need an open document.', icon=scribus.ICON_CRITICAL)
        return

    filename = scribus.fileDialog('Target text file', \
        filter='Text Files (*.txt);;All Files (*)')

    export_text(filename)

if __name__ == '__main__':
    main()
