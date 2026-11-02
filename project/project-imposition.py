""" Impose a project's PDFs based on a impostion.yml file

For details see the README file.

(c) 2026 MIT ale rimoldi"""

import argparse
import yaml
from pypdf import PdfReader, PdfWriter, PaperSize, Transformation
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        prog='imposition-pdf',
        description='Impose a project\'s PDFs based on a impostion.yml file')
    parser.add_argument('filename', help='The .yml config file for the imposition')
    args = parser.parse_args()
    path = Path(args.filename).parent
    with open(args.filename, 'r') as file:
        config = yaml.safe_load(file)

    formats = {
        'a4': PaperSize.A4,
        'a5': PaperSize.A5,
    }
    if 'format' in config['target']:
        target_format = formats[config['target']['format']]
    else:
        target_format = PaperSize.A4
    if 'orientation' in config['target'] and config['target']['orientation'] == 'landscape':
        target_width = target_format.height
        target_height = target_format.width
    else:
        target_width = target_format.width
        target_height = target_format.height

    merger = PdfWriter()

    for source in config['source']:
        if 'layout' in source and source['layout'] == '2-n-up':
            reader = PdfReader(path / source['file'])
            number_of_pages = len(reader.pages)
            for page in range(number_of_pages):
                if page % 2 == 0:
                    destination_page = merger.add_blank_page(width=target_width, height=target_height)
                transformation = Transformation().translate(
                    (page % 2) * target_width / 2,
                    0
                )
                destination_page.merge_transformed_page(reader.pages[page], transformation)
        else:
            with open(path / source['file'], 'rb') as input_pdf:
                merger.append(input_pdf)

    merger.write(path / config['target']['file'])

if __name__ == '__main__':
    main()
