#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from PyPDF2 import PdfFileReader, PdfFileWriter, PageObject
#import papersize

try:
    import scribus as s
except ImportError(err):
    print("This Python script is written for the Scribus scripting interface.")
    print("It can only be run from within Scribus.")
    sys.exit(1)


def makeZine(nome_pdf):
    pdf = PdfFileReader(nome_pdf)
    outputPDF = os.path.splitext(nome_pdf)[0]+"-zine.pdf"

    #target_size = papersize.parse_papersize("a3")
    target_size = (pdf.getPage(0).mediabox.getHeight()*2, pdf.getPage(0).mediabox.getWidth()*4)
    newPage = PageObject.create_blank_page(None, target_size[1], target_size[0])

    #riordina pagine e le aggiunge alla pagina bianca
    for i in range(5,8):
        p = pdf.getPage(i)
        newPage.mergeRotatedScaledTranslatedPage(p , 0, 1, float(p.mediabox.getWidth())*(i-5), 0)
    p = pdf.getPage(0)
    newPage.mergeRotatedScaledTranslatedPage(p, 0, 1, float(p.mediabox.getWidth())*3, 0)
    for i in range(4,0,-1):
        p = pdf.getPage(i)
        newPage.mergeRotatedScaledTranslatedPage(p , 180, 1, float(p.mediabox.getWidth())*(5-i) , float(p.mediabox.getHeight())*2)

    pdf_writer = PdfFileWriter()
    pdf_writer.add_page(newPage)

    with open(outputPDF, "wb") as out:
        pdf_writer.write(out)

def main(argv):
    """This script run on Scribus with a 8 pages document open, creates a 1-page
    folding mini-zine, correctly re-arranging and rotating the pages. It is a pure-python
    soluiton, and depends only on PyPDF2"""

    if (s.haveDoc() and s.pageCount() == 8):
        pdf = s.PDFfile()
        pdf.file = s.fileDialog("export zine in pdf", ".pdf", "zine.pdf", 0, 1, 0)
        os.chdir(os.path.dirname(pdf.file))
        pdf.save()
        makeZine(pdf.file)
        s.messageBox("zine created", "successfully created zine in " + os.path.dirname(pdf.file))

def main_wrapper(argv):
    """The main_wrapper() function disables redrawing, sets a sensible generic
    status bar message, and optionally sets up the progress bar. It then runs
    the main() function. Once everything finishes it cleans up after the main()
    function, making sure everything is sane before the script terminates."""
    try:
        s.statusMessage("Running script...")
        s.progressReset()
        main(argv)
    finally:
        # Exit neatly even if the script terminated with an exception,
        # so we leave the progress bar and status bar blank and make sure
        # drawing is enabled.
        if s.haveDoc():
            s.setRedraw(True)
        s.statusMessage("")
        s.progressReset()

# This code detects if the script is being run as a script, or imported as a module.
# It only runs main() if being run as a script. This permits you to import your script
# and control it manually for debugging.
if __name__ == '__main__':
    main_wrapper(sys.argv)