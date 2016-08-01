# Produces a PDF for the SLA passed as a parameter.
# Uses the same file name and replaces the .sla extension with .pdf
#
# usage:
# scribus -g -py to-pdf.py -- file.sla
#
# license:
# (c) MIT Ale Rimoldi

import os
import scribus

if scribus.haveDoc() :
    filename = os.path.splitext(scribus.getDocName())[0]
    pdf = scribus.PDFfile()
    pdf.file = filename+".pdf"
    pdf.save()
else :
    print("No file open")
