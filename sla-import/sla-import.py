##
# Imports all pages of an `.sla` file into another one
#
# For more information, see https://wiki.scribus.net/canvas/Automatic_Scripter_Commands_list
#
# Usage:
# scribus -g -py import-pages.py base_file.sla import_file.sla
#
# License: MIT
# (c) Martin Folkers
##

import scribus
import argparse

parser = argparse.ArgumentParser(
    description='Imports all pages of an `.sla` file into another one'
)

parser.add_argument(
    'files',
    nargs='*',
    default=None,
    help='SLA files to be processed',
)

parser.add_argument(
    '--page',
    type=int,
    help='Pages are imported before / after this page'
)

parser.add_argument(
    '--before',
    action='store_true',
    help='Imports pages before instead of after'
)

parser.add_argument(
    '--output',
    help='Creates new SLA file under specified path'
)

def get_pages_range(sla_file):
    scribus.openDoc(sla_file)
    l = range(1, scribus.pageCount() + 1)
    scribus.closeDoc()

    return tuple(l)

args = parser.parse_args()

base_file = args.files[0]
import_file = args.files[1]
page_number = args.page - 1
insert_position = 0 if args.before == True else 1 # 0 = before; 1 = after

# Importing `import_file`
scribus.openDoc(base_file)
scribus.importPage(import_file, get_pages_range(import_file), 1, insert_position, page_number)

# Either overwriting `import_file` ..
if args.output == None:
    scribus.saveDoc()
# .. or creating new `output` file (requires `--output`)
else:
    scribus.saveDocAs(args.output)

scribus.closeDoc()

