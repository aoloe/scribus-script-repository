#!/usr/bin/env python3

import sys
import argparse
import subprocess
# from mockAPI import Scribus

# scribus = Scribus()

from pathlib import Path
import json

def main() :
    try:
        import scribus
        run_script()
    except ImportError:
        run_scribus()

def run_scribus() :
    global debug

    args = get_args_terminal()

    # todo: remove the -1.5
    call_args = ['scribus-1.5', '-g', '-py', str(Path(__file__).parent / sys.argv[0])]
    # https://stackoverflow.com/questions/51114248/qt-application-running-with-platform-offscreen-argument-cannot-establish-webs
    # call_args += ['-platform', 'offscreen']
    if args.config:
        config_file = Path(args.config)
        if config_file.is_file():
            call_args += ['-config']
            call_args += [args.config]
        else:
            print(f'Ingoring -config {args.config}: file not found.')

    if args.file:
        if args.files:
            print(f'Ingoring -files {args.files}: conflicting with the files list.')
        for file in args.file:
            # print(call_args + ['--', str(Path(__file__).parent / file.name)])
            subprocess.call(call_args + ['--', str(Path(__file__).parent / file.name)])
    elif args.files:
        files_file = Path(args.files)
        if files_file.is_file():
            call_args += ['-files']
            call_args += [args.files]

            print(call_args);
            subprocess.call(call_args)
            # fake_scribus_call(call_args)
        else:
            print(f'Error in -files {args.files}: file not found.')

def run_script() :
    args = get_args_scribus()

    config = {}
    if args.config:
        try:
            with open(args.config) as f:
                config = json.load(f)
        except (json.JSONDecodeError):
            print(f'Error in config: invalid json file.')
            return

    # print(args)
    if scribus.haveDoc():
        with open(str(Path(__file__).parent / 'test.txt'), 'w') as f:
           f.write(scribus.getDocName()) 
        pdf_file = str(Path(scribus.getDocName()).with_suffix('.pdf'))
        export(pdf_file, config)
    elif args.files:
        try:
            with open(args.files) as f:
                files = json.load(f)
        except (json.JSONDecodeError):
            print(f'Error in -files {args.files}: invalid json file.')
            return
        for file in files:
            if not 'sla' in file:
                print(f'Missing sla in {args.files} entry: {file}')
                continue
            if 'pdf' in file:
                pdf_file = file['pdf']
            else:
                pdf_file = Path(file['sla']).with_suffix('.pdf')
            print(f'opening {file["sla"]}')
            scribus.openDoc(file['sla'])
            export(pdf_file, config)
            scribus.closeDoc()
    else:
        if not scribus.haveDoc():
            print("No file open");
            return

        filename = os.path.splitext(scribus.getDocName())[0]

def fake_scribus_call(args):
    print(args)
    files = []
    try:
        i = args.index('-files');
        try:
            with open(args[i + 1]) as f:
                files = json.load(f)
        except (json.JSONDecodeError):
            print(f'Error in -files: invalid json file.')
            return
    except (ValueError):
        pass

    config = {}
    try:
        i = args.index('-config');
        try:
            with open(args[i + 1]) as f:
                config = json.load(f)
        except (json.JSONDecodeError):
            print(f'Error in config: invalid json file.')
            return
    except (ValueError):
        pass

    for file in files:
        scribus.openDoc(file['sla'])
        export(config)
        scribus.closeDoc()

def export(pdf_filename, config):
    pdf = scribus.PDFfile()
    # TODO: should we make sure that the values are valid?
    for key, value in config.items():
        if value is not None:
            setattr(pdf, key, value)
    pdf.file = pdf_filename
    pdf.save()

def get_args_terminal():
    parser = argparse.ArgumentParser(description='Creates a pdf at the original size and one imposed on A4.')

    parser.add_argument('-config', action='store',
        help='json file with pdf options')

    parser.add_argument('-files', action='store',
        help='json file with a list of .sla to convert')

    parser.add_argument('file', type=argparse.FileType('r'), nargs='*',
        default=None,
        help='.sla files to be processed')

    return parser.parse_args()

def get_args_scribus():
    parser = argparse.ArgumentParser(description='Creates a pdf at the original size and one imposed on A4.')

    parser.add_argument('-config', action='store',
        help='json file with pdf options')

    parser.add_argument('-files', action='store',
        help='json file with a list of .sla to convert')

    parser.add_argument('file', type=argparse.FileType('r'), nargs='*',
        default=None,
        help='.sla files to be processed')

    return parser.parse_args()

if __name__ == "__main__":
    main()
