#!/usr/bin/env python3
"""Export all Scribus Scripter API commands into a set of Markdown files.

For more details see the README.md

(c) MIT 2023, ale rimoldi <ale@graphicslab.org>
"""
import subprocess

import os
import sys
import inspect

import logging

from dataclasses import dataclass

import copy
import json
import re
from pathlib import Path

import shutil

import datetime

@dataclass
class DocModule:
    """Collecting the inspected values."""
    name: str
    classes: dict
    functions: dict
    constants: dict
    members: dict
    others: dict

def get_inspection(item):
    """ Get the module's inspected data aggregated by type """
    functions = {}
    constants = {}
    members = {}
    classes = {}
    others = {}

    module = item.__name__

    for i in dir(item):
        if i.startswith('__'):
            continue

        attr = getattr(item, i)
        if inspect.isclass(attr):
            # print('class', i)
            classes[i] = attr
        elif inspect.ismethod(attr):
            print('method', i)
        elif inspect.isfunction(attr):
            print('function', i)
        elif inspect.isroutine(attr):
            # print('routine', i)
            functions[i] = attr.__doc__
        elif inspect.ismemberdescriptor(attr):
            # print('member descriptor', i)
            if not 'Deprecated' in attr.__doc__:
                members[i] = attr.__doc__
        elif i.isupper():
            # print('constant', i)
            constants[i] = ''
        else:
            # print('else', i)
            others[i] = attr.__doc__
    return DocModule(module, classes, functions, constants, members, others)

class DocApi:
    """ Collect the data in sections that are ready for the output """
    def __init__(self, scribus_doc):
        # make a deep copy: the items in the local scribus_doc are removed
        # as soon as they have been added to the internal structures
        self.scribus_doc = copy.deepcopy(scribus_doc)
        self.sections = {}

    def add_section(self, section_id):
        """ Initialise a section dictionary entry """
        self.sections[section_id] = {
            'doc': '',
            'functions': {},
            'classes': [], # {'name': '', 'doc': '', functions: [], 'members': []}
            'constants': [], # {'doc': '', 'list': []}
            'members': {}
        }

    def add_function_by_regex(self, section_id, regexes):
        """ Find the functions that match a regex """
        if not isinstance(regexes, list):
            regexes = [regexes]
        for regex in regexes:
            r = re.compile(regex)
            functions = list(filter(r.match, self.scribus_doc.functions.keys()))
            for f in functions:
                self.add_function(section_id, f)

    def add_function(self, section_id, command, doc=None):
        """ Add a function to the list of the section's functions """
        if command not in self.scribus_doc.functions:
            logging.warning('%s is not a function', command)
            return
        if doc is None:
            if command in self.scribus_doc.functions:
                doc = self.scribus_doc.functions[command]
        del self.scribus_doc.functions[command]
        if not section_id in self.sections:
            self.add_section(section_id)
        self.sections[section_id]['functions'][command] = doc

    def add_constants_by_regex(self, section_id, regexes, doc):
        """ Find the constants that match a regex """
        if type(regexes) != list:
            regexes = [regexes]
        for regex in regexes:
            r = re.compile(regex)
            constants = list(filter(r.match, self.scribus_doc.constants))
            self.add_constants(section_id, constants, doc)

    def add_constants(self, section_id, constants, doc):
        """ Add constants to the section's list """
        constants_set = {'doc': doc, 'list': []}
        for constant in constants:
            if constant in self.scribus_doc.constants:
                constants_set['list'].append(constant)
                del self.scribus_doc.constants[constant]
            elif constant in self.scribus_doc.others: # m, mm, ...
                constants_set['list'].append(constant)
                del self.scribus_doc.others[constant]
            else:
                logging.warning('%s is not a constant', constant)
        if not section_id in self.sections:
            self.add_section(section_id)
        self.sections[section_id]['constants'].append(constants_set)

    def add_class(self, section_id, attr):
        """ Inspect a class and add it to the list of the section's classes """
        if not section_id in self.sections:
            self.add_section(section_id)

        del self.scribus_doc.classes[attr.__name__]

        class_item = {'name': '', 'doc': '', 'functions': {}, 'members': {}}
        class_item['name'] = attr.__name__

        class_doc = get_inspection(attr)

        class_item['doc'] = attr.__doc__

        for f, doc in class_doc.functions.items():
            class_item['functions'][f] = doc
        for f, doc in class_doc.members.items():
            class_item['members'][f] = doc
        for f, doc in class_doc.others.items():
            class_item['members'][f] = doc

        self.sections[section_id]['classes'].append(class_item)

def function_doc_to_md(doc):
    """ Extract the function name from the first line of a function doc
        and make it a title """
    lines = doc.split('\n')
    function_name = lines[0].partition('(')[0]
    lines[0] = f'`{lines[0]}`'
    lines.insert(0, f'## {function_name}\n')

    return '\n'.join(lines)

def run_script():

    SCRIPT_PATH = Path(__file__).parent

    CONFIG_FILE = SCRIPT_PATH.joinpath('export_scripter_api.json')
    OUTPUT_PATH = SCRIPT_PATH.joinpath('out/')
    INPUT_PATH = SCRIPT_PATH.joinpath('in/')
    CONTENT_PATH = 'docs/'
    OUTPUT_DOCS_PATH = OUTPUT_PATH.joinpath(CONTENT_PATH)

    # sys.stdout = open(SCRIPT_PATH.joinpath('output.txt'), 'w')

    if not os.path.exists(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)

    logging.basicConfig(
        filename=OUTPUT_PATH.joinpath('logs.txt'),
        level=logging.DEBUG, filemode='w')

    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)

    # read all the available commands
    scribus_doc = get_inspection(scribus)

    # categorize the commands into sections
    api_doc = DocApi(scribus_doc)

    for section_id, section in config['sources'].items():
        if section_id == 'document':
            print('>>>>', section_id)
            print('>>>>', api_doc.scribus_doc.others)
        if 'functions' in section:
            if 'list' in section['functions']:
                for command in section['functions']['list']:
                    api_doc.add_function(section_id, command)
        if 'classes' in section:
            if 'list' in section['classes']:
                for class_name in section['classes']['list']:
                    api_doc.add_class(section_id, scribus_doc.classes[class_name])
        if 'constants' in section:
            for constants in section['constants']:
                if 'list' in constants:
                    api_doc.add_constants(section_id, constants['list'], constants['doc'])
                if 'regex' in constants:
                    api_doc.add_constants_by_regex(section_id, constants['regex'], constants['doc'])
    # for functions we need a second pass for regexes (and avoid that regexes match functions that are also in lists)
    for section_id, section in config['sources'].items():
        if 'functions' in section:
            if 'regex' in section['functions']:
                api_doc.add_function_by_regex(section_id, section['functions']['regex'])

    # create the markdown files
    if not os.path.exists(OUTPUT_DOCS_PATH):
        os.mkdir(OUTPUT_DOCS_PATH)

    content_toc = '# Scribus Scripter API\n\n'
    with open(INPUT_PATH.joinpath('mkdocs.yml'), 'r') as f:
        content_mkdocs = f.read()
    for section_id, title in config['output'].items():
        if section_id not in api_doc.sections:
            logging.warning('%s is not a target', section_id)
            continue

        content_file = section_id + '.md'
        content_toc += f'- [{title}]({CONTENT_PATH}/{content_file})\n'
        content_mkdocs += f'- {title}: {content_file}\n'

        content = f'# {title}\n\n'

        if api_doc.sections[section_id]['doc']:
            content += api_doc.sections[section_id]['doc'] + '\n\n'

        for _, doc in sorted(api_doc.sections[section_id]['functions'].items()):
            content += function_doc_to_md(doc) + '\n\n'

        if api_doc.sections[section_id]['constants']:
            content += '## Constants' + '\n\n'
            for constants_set in api_doc.sections[section_id]['constants']:
                content += constants_set['doc'] + '\n\n'
                for constant in constants_set['list']:
                    content += f'- `{constant}`\n'
                content += '\n'

        if api_doc.sections[section_id]['members']:
            content += '## Member variables' + '\n\n'
            for member, doc in sorted(api_doc.sections[section_id]['members'].items()):
                content += f'### {member}\n\n{doc}\n\n'

        if api_doc.sections[section_id]['classes']:
            for cl in sorted(api_doc.sections[section_id]['classes'], key=lambda x: x['name']):
                content += f'## class {cl["name"]}\n\n'
                if cl['doc']:
                    content += cl['doc'] + '\n\n'
                for _, doc in sorted(cl['functions'].items()):
                    content += '#' + function_doc_to_md(doc) + '\n\n'
                if cl['members']:
                    content += '### Members\n\n'
                    for member, doc in sorted(cl['members'].items()):
                        content += f'#### {member}\n\n{doc}\n\n'

        with open(OUTPUT_DOCS_PATH.joinpath(content_file), 'w') as f:
            f.write(content)

    with open(OUTPUT_PATH.joinpath('toc.md'), 'w') as f:
        f.write(content_toc)
    with open(OUTPUT_PATH.joinpath('mkdocs.yml'), 'w') as f:
        f.write(content_mkdocs)
    if 'files' in config:
        for i, o in config['files'].items():
            shutil.copyfile(SCRIPT_PATH.joinpath(i), OUTPUT_DOCS_PATH.joinpath(o))
    with open(OUTPUT_DOCS_PATH.joinpath('index.md'), 'w') as f:
        f.write('# ' + scribus.__doc__ + f"\n\nThis API documentation has been generated from Scribus {scribus.scribus_version} ({datetime.datetime.now():%Y-%m-%d}).")

    for f, d in api_doc.scribus_doc.functions.items():
        # print(f)
        logging.warning('Unprocessed function\n%s\n%s', f, d)
    for f, _ in api_doc.scribus_doc.constants.items():
        logging.warning('Unprocessed constant\n%s', f)
    for f, d in api_doc.scribus_doc.members.items():
        logging.warning('Unprocessed member\n%s\n%s', f, d)
    for f, _ in api_doc.scribus_doc.classes.items():
        logging.warning('Unprocessed class\n%s', f)
    for f, _ in api_doc.scribus_doc.others.items():
        logging.warning('Other unprocessed\n%s', f)

def run_scribus():
    """Start Scribus with this same script as the script to run"""
    # if len(sys.argv) < 2:
    #     print(f'Usage: python3 {sys.argv[0]} filename')
    #     return

    call_args = ['scribus', '-g', '-py', sys.argv[0]]
    # call_args += ['--', sys.argv[1]]
    subprocess.call(call_args)

def main():
    try:
        import scribus
        run_script()
    except ImportError:
        run_scribus()

if __name__ == '__main__':
    main()
