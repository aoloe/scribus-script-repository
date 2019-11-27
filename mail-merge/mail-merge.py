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
import json
import os.path

from pathlib import Path

if not scribus.haveDoc():
    scribus.messageBox('Script failed', 'You need an open template document.')
    sys.exit(2)

# TODO: read from a conf.json file
CONFIGURATION_DEFAULT = {
    'placeholder': {
        'start': '{',
        'end': '}'
    },
    'data': {
        'file': None,
        'format': 'csv'
    },
    'output': {
        'pdf': True,
        'single-sla': False,
    }
}

def merge_configuration(default, local):
    """ merge the local dict into the default one
        (https://stackoverflow.com/a/7205107/5239250)"""
    for key in local:
        if key in default:
            if isinstance(default[key], dict) and isinstance(local[key], dict):
                merge_configuration(default[key], local[key])
            elif default[key] == local[key]:
                pass # same leaf value
            else:
                default[key] = local[key]
        else:
            default[key] = local[key]

def get_configuration(scribus_doc):
    """ return the project configuration merged with the default one"""
    configuration = CONFIGURATION_DEFAULT
    path = Path(scribus_doc)
    config_filename = path.with_suffix('.conf.json')
    if os.path.isfile(config_filename):
        if config_filename:
            with open(config_filename, 'r') as json_file:
                json_data = json.load(json_file)
                merge_configuration(configuration, json_data)
    return configuration

def duplicate_content(pages, named_items):
    """ duplicate the content of pages at the end of the document
        and track the new item names for the items in named_items
    return the list of created item names from named_items """
    result = {}
    page_n = scribus.pageCount()
    for page in pages:
        scribus.gotoPage(page)
        items = [item[0] for item in scribus.getPageItems()]
        scribus.newPage(-1, scribus.getMasterPage(page))
        page_n += 1

        for item in items:
            scribus.gotoPage(page)
            scribus.copyObject(item)
            scribus.gotoPage(page_n)
            scribus.pasteObject()
            if item in named_items:
                result[item] = scribus.getSelectedObject()
    return result

def get_placeholders_from_string(text):
    """ return a list of keys and placeholders indexes in the inverse order """
    placeholders = []

    i = text.find(CONFIGURATION['placeholder']['start'])
    while i != -1:
        j = text.find(CONFIGURATION['placeholder']['end'], i)
        if j == -1:
            break

        key = text[i + 1:j]
        placeholders.insert(0, {'key': key, 'start': i, 'end': j})
        i = text.find(CONFIGURATION['placeholder']['start'], j)

    return placeholders

def get_text_placeholders(frame):
    scribus.selectText(0, 0, frame)
    text = scribus.getText(frame)
    return get_placeholders_from_string(text)

def get_image_placeholders(frame):
    filename = scribus.getImageFile(frame)
    return get_placeholders_from_string(filename)

def fill_text_placeholders(frame, fields, row):
    for field in fields:
        # TODO: currently, if the fields is not found it's left as is, with no warning
        if field['key'] in row:
            scribus.insertText(row[field['key']], field['start'] + 1, frame)
            # delete "key}"
            scribus.selectText(field['start'] + len(row[field['key']]) + 1, field['end'] - field['start'], frame)
            scribus.deleteText(frame)
            # delete "{"
            scribus.selectText(field['start'], 1, frame)
            scribus.deleteText(frame)

def fill_image_placeholders(frame, fields, row):
    filename = scribus.getImageFile(frame)
    for field in fields:
        print(field)
        new_filename = filename[0:field['start']] + \
            row[field['key']] + \
            filename[field['end'] + 1:]
        scribus.loadImage(new_filename, frame)

def get_placeholders():
    text_frames = []
    image_frames = []

    page_n = scribus.pageCount()
    for page in range(1, page_n + 1):
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
    return text_frames, image_frames

def main():
    text_frames, image_frames = get_placeholders()

    sla_template_filename = scribus.getDocName()
    sla_template_path = Path(sla_template_filename)

    if 'file' in CONFIGURATION['data'] and CONFIGURATION['data']['file']:
        data_path = str(sla_template_path.parent.joinpath(CONFIGURATION['data']['file']))
    elif CONFIGURATION['data']['format'] == 'json':
        data_path = sla_template_path.with_suffix('.json')
    else:
        data_path = sla_template_path.with_suffix('.csv')

    if not os.path.isfile(data_path):
        sys.exit()

    if CONFIGURATION['data']['format'] == 'json':
        pass
    else:
        data_file = open(data_path, 'rt')
        reader = csv.DictReader(data_file)

    pdf_base_filename = sla_template_path.stem
    pdf_path = Path(sla_template_path.parent)

    if CONFIGURATION['output']['pdf']:
        pdf = scribus.PDFfile()
        pdf.quality = 0
        pdf.fontEmbedding = 0
        pdf.version = 14

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
    elif CONFIGURATION['output']['single-sla']:
        original_pages = list(range(1, scribus.pageCount() + 1))
        for row in reader:
            new_frames = duplicate_content(original_pages, [i[0] for i in text_frames + image_frames])

            for frame, placeholders in text_frames:
                fill_text_placeholders(new_frames[frame], placeholders, row)
            for frame, placeholders in image_frames:
                fill_image_placeholders(new_frames[frame], placeholders, row)
        for page in original_pages:
            scribus.deletePage(page)

if __name__ == "__main__":
    CONFIGURATION = get_configuration(scribus.getDocName())
    main()
