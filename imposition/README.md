# Impose a Scribus file

Python script that calls Scribus from the shell to produce a _normal_ Pdf of the file and an _imposed_ Pdf.

Only very simple imposition plans are supported:

- it has been created to allow the printing of A6 _cards_ as double sided or booklet on A4.
- it's been expanded to support A6 _cards_ and printing on single sided A4 paper.

## Notes

Since we're using pdfjam anyway, we can try to do _all_ the work in pdfjam:

`pdfjam --nup 2x1 --booklet true --frame false --landscape --a4paper --preamble '\usepackage{everyshi}\makeatletter\EveryShipout{\ifodd\c@page\pdfpageattr{/Rotate 180}\fi}\makeatother' --outfile test.pdf a5-8pages.pdf`
