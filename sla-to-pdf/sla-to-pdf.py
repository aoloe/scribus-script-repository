#!/usr/bin/env python3
# -booklet: only available from 4 pages up

import sys
import os
import argparse
import subprocess

debug = False

def main() :
    try:
        import scribus
        run_script()
    except ImportError:
        run_scribus()

def run_scribus() :
    global debug
    args = get_args_terminal()
    # print(args)

    if args.file:
        for file in args.file:
            # TODO: how to pass arguments to the python script?
            # os.system('scribus -g -py ' + sys.argv[0] + ' -- ' + '-o test ' + file.name)
            # os.system('scribus -g -py ' + sys.argv[0] + ' -pa -booklet ' + ' -- ' + file.name)
            call_args = ['scribus', '-g', '-py', sys.argv[0]]
            if args.booklet:
                call_args += ['-booklet']
                # call_args += ['-pa', '-booklet']
            call_args += ['--', file.name]
            subprocess.call(call_args)
    else:
        pass

def run_script() :
    args = get_args_scribus()
    print('booooklet ' + str(args.booklet))

    if not scribus.haveDoc():
        print("No file open");
        return

    filename = os.path.splitext(scribus.getDocName())[0]

    # scribus.getPageSize()
    # create a PDF with the original size
    pdf = scribus.PDFfile()
    pdf.file = filename + ".pdf"
    pdf.save()

    # create a pdf with the page reordered
    # get it to be steared by facing pages and first page left / right
    # it's booklet if it has facing pages and first page right
    # (the function are probably not in the API yet)
    n = scribus.pageCount()
    pdf = scribus.PDFfile()
    pdf.file = filename + "-reordered.pdf"
    if (n == 1) :
        pdf.pages = [1,1,1,1]
    elif (n == 2) :
        pdf.pages = [1,1,1,1,2,2,2,2]
    elif (n == 4) :
        if args.booklet:
            pdf.pages = [4,1,4,1,2,3,2,3]
        else:
            pdf.pages = [1,3,1,3,4,2,4,2]
    elif (n == 8) :
        if args.booklet:
            pdf.pages = [8,1,6,3,2,7,4,5]
        else:
            pdf.pages = [1,3,5,7,4,2,8,6]
    elif (n == 12) :
        if args.booklet:
            pdf.pages = [12, 1, 2, 11, 10, 3, 4, 9, 8, 5, 6, 7]
        else :
            pass
    elif (n == 16) :
        if args.booklet:
            pdf.pages = [16, 1, 14 , 3, 2, 15, 4, 13, 12, 5, 10, 7, 6, 11, 8, 9] # <- first join top/down , then staple 1/2
        else:
            pass
    elif (n == 24) :
        if args.booklet:
            pass
        else:
            pdf.pages = [1,3,5,7,4,2,8,6,9,11,13,15,12,10,16,14,17,19,21,23,20,18,24,22] # mit starter cards
    else:
        print('{} are not yet supported'.format(n))
    pdf.save()

    call_args = ['pdfnup', '--nup', '2x2', '--frame', 'false', '--no-landscape']
    call_args += ['--', 'outfile', filename.replace("a6", "a4") + ".pdf"]
    call_args += [filename + '-reordered.pdf']
    subprocess.call(call_args)

    os.system("pdfnup --nup 2x2 --frame false --no-landscape " + filename + "-reordered.pdf --outfile " + filename.replace("a6", "a4") + ".pdf")
    os.remove(pdf.file)


def get_args_terminal():
    parser = argparse.ArgumentParser(description='Creates a pdf at the original size and one imposed on A4.')

    parser.add_argument('-booklet', action='store_true',
        help='impose as a booklet')

    parser.add_argument('file', type=argparse.FileType('r'), nargs='*',
        default=None,
        help='.sla files to be processed')

    parser.add_argument('-debug', action='store_true',
        help='output debug information')

    return parser.parse_args()

def get_args_scribus():
    parser = argparse.ArgumentParser(description='Creates a pdf at the original size and one imposed on A4.')

    parser.add_argument('-booklet', action='store_true',
        help='impose as a booklet')

    parser.add_argument('-debug', action='store_true',
        help='output debug information')

    return parser.parse_args()

if __name__ == "__main__":
    main()
