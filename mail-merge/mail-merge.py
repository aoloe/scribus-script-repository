# encoding: utf-8
# (c) MIT ale rimoldi
# Simple Mail Merge script for Scribus.
# For details see the README file.

try:
    import scribus
except ImportError:
    print('This script must be run from inside Scribus')

import sys
import csv
import os.path

from pathlib import Path

PLACEHOLDER_START = '{'
PLACEHOLDER_END = '}'

if not scribus.haveDoc():
    scribus.messageBox('Script failed', 'You need an open template document.')
    sys.exit(2)

def get_placeholders(text):
    """ return a list of keys and placeholders indexes in the inverse order """
    placeholders = []

    i = text.find(PLACEHOLDER_START)
    while i != -1:
        j = text.find(PLACEHOLDER_END, i)
        if j == -1:
            break

        key = text[i + 1:j]
        placeholders.insert(0, {'key': key, 'start': i, 'end': j})
        i = text.find(PLACEHOLDER_START, j)

    return placeholders

def get_text_placeholders(frame):

    scribus.selectText(0, 0, frame)
    text = scribus.getText(frame)
    return get_placeholders(text)

def get_image_placeholders(frame):
    filename = scribus.getImageFile(frame)
    return get_placeholders(filename)

def fill_text_placeholders(frame, fields, row):
    for field in fields:
        # TODO: what happens if the field is not defined? delete it? log it as an error?
        if field['key'] in row:
            scribus.insertText(row[field['key']], field['start'] + 1, frame)
            # delete key}
            scribus.selectText(field['start'] + len(row[field['key']]) + 1, field['end'] - field['start'], frame)
            scribus.deleteText(frame)
            # delete {
            scribus.selectText(field['start'], 1, frame)
            scribus.deleteText(frame)

def fill_image_placeholders(frame, fields, row):
    filename = scribus.getImageFile(frame)
    for field in fields:
        print(field)
        new_filename = filename[0:field['start']] + \
            row[field['key']] + \
            filename[field['end'] + 1:]
        # print(new_filename)
        scribus.loadImage(new_filename, frame)

# TODO: define, while reading the config file
len_start = len(PLACEHOLDER_START)
len_end = len(PLACEHOLDER_END)

def main():
    text_frames = []
    image_frames = []

    for page in range(1, scribus.pageCount() + 1):
        scribus.gotoPage(page)
        for item in scribus.getPageItems():
            if item[1] == 2:
                placeholders = get_image_placeholders(item[0])
                if placeholders:
                    image_frames.append((item[0], placeholders))
            if item[1] == 4:
                placeholders = get_text_placeholders(item[0])
                if placeholders:
                    text_frames.append((item[0], placeholders))

    sla_template_path = Path(scribus.getDocName())

    csv_path = sla_template_path.with_suffix('.csv')
    json_path = sla_template_path.with_suffix('.json')

    if os.path.isfile(csv_path):
        csv_file = open(csv_path, 'rt')
        reader = csv.DictReader(csv_file)
    elif os.path.isfile(json_path):
        # print(json_path)
        pass

    pdf = scribus.PDFfile()
    pdf.quality = 0
    pdf.fontEmbedding = 0
    pdf.version = 14

    pdf_base_filename = sla_template_path.stem
    pdf_path = Path(sla_template_path.parent)

    scribus.setRedraw(False)
    for row in reader:
        for frame, placeholders in text_frames:
            fill_text_placeholders(frame, placeholders, row)
        for frame, placeholders in image_frames:
            fill_image_placeholders(frame, placeholders, row)

        pdf.file = str(pdf_path.joinpath(pdf_base_filename + '-' + next(iter(row.items()))[1].lower() + '.pdf'))
        pdf.save()

        scribus.docChanged(True)
        scribus.revertDoc()
    scribus.setRedraw(True)

main()
