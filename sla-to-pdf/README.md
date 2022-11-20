# Impose a .sla as Pdf

`sla-to-pdf.py` reads a A5 or A6 portrait Scribus document and produces:

- a PDF with the current settings in the Scribus file;
- with the `-booklet` option, it also produces an A4 Pdf that can be printed both sides to create a simple booklet;
- with the `-impose` option, it also produces an A4 Pdf to be printed single sided (contact print);

> Please, hae a look at the _Imposition_ script in this repository. It's probably a better solution.

## Introduction

The script should be started from the command line, and it will launch Scribus before running the script with the given options.

You can run it with the `-h` option to get more information about its usage.

In order to run the script you need Scribus (1.5+) and pdfjam installed (on Debian it's part of `texlive-extra-utils`).

## Page count

You can only create booklets if the number of pages is a multiple of 4.  
The only exceptions are 2 pages document, where the `-booklet` produces and imposed duplex A4 Pdf

## Notes

### Adding a full page cover

In order to create a full page cover and all other pages imposed from an A5/A6 created for booklet printing:

- Create the Pdf with the cover:
  - Save your document as `document-cover.sla`
  - Change the document page size to A4 (landscape for A5)
  - Modify the layout of the cover to match the new size.
  - Create the `document-cover.pdf`
- Create a new Pdf with all the pages but the cover (and possibly another page to get an even number of pages).  
  You can use `pdfjam` to extract the pages:  
  `pdfjam document.pdf 2- document.pdf -o document-nocover.pdf`
- Create the nup Pdf:  
  `pdfjam --nup 2x1 --landscape --a4paer --outfile document-a4-nocover.pdf document-nocover.pdf`
- Join the A4 cover with the A4 pdf:  
  `pdfjam document-cover.pdf document-a4-nocover.pdf --nup 1x1 --landscape --a4paper --outfile document-a4.pdf`
