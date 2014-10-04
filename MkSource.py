#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
# Common tools:
#	pip/pip3 : install packages
#	pylint/pychecker : verify syntax
#	unittest package for xUnit.
''' Implements code to support my templating system for source files.
    For autocomplete functionality, see the docs which contain setup info.
'''

# Imports
from __future__ import print_function
import argparse
import os
import sys
import shutil

# not always easily installed lib
try:
    from argcomplete import autocomplete
except ImportError:
    def autocomplete(dummy):
        """ Dummy func. """
        pass

TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__)) \
    + os.sep + 'templates' + os.sep

# New JSON
LANGS = {
    'c': {
        'ext': '.c',
        'hext': '.h',
    },
    'cpp': {
        'ext': '.cpp',
        'hext': '.hpp',
    },
    'lisp': {
        'ext': '.lisp',
    },
    'perl': {
        'ext': '.pl',
    },
    'prolog': {
        'ext':'.pdb',
    },
    'python': {
        'ext': '.py',
    },
    'ruby': {
        'ext': '.rb',
    },
}

CONFIGS = {
    'make' : 'Makefile',
    'maked': 'Make.defines',
    'ycm'  : '.ycm_extra_conf.py',
}

# Functions

def file_replace(target, old_text, new_text):
    """ Perform text replacements on the file.
        For each line, old_text will be replaced with new_text.
    """
    with open(target, 'r') as read:
        lines = read.readlines()

    new_lines = [line.replace(old_text, new_text) for line in lines]

    with open(target, 'w') as out:
        out.writelines(new_lines)

def copy_files(source, targets, headers=False):
    """ For each target copy source to it.
        Special handling for scripts & headers.
    """
    for target in targets:
        shutil.copy(source, target)

        # Fix the include guard, _TEST_ -> _FILENAME_
        if headers:
            filename, _ = os.path.splitext(os.path.basename(target))
            filename = filename.upper().replace('.', '_')
            file_replace(target, 'TEST_', filename + '_')


def process_args(lang, target, s_files, h_files):
    """ Based on lang object, infer sources & headers template then
        copy into the tdir the templates.
    """
    json = LANGS[lang]
    hext = json.get('hext', None)

    s_template = TEMPLATE_DIR + '%s_template%s' % (lang, json['ext'])
    sources = [target + os.sep + name + json['ext'] for name in s_files]
    copy_files(s_template, sources)

    if hext:
        h_template = TEMPLATE_DIR + '%s_template%s' % (lang, hext)
        headers = [target + os.sep + name + hext
                for name in h_files]
        copy_files(h_template, headers, True)

def main():
    """ Main function. """
    # Setup argument parser, very nice. -i for header due to help default.
    desc = """ This is my source file creator. The language is required.
    Specify as many source or header files as required.
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-c', '--config', action='append', dest='configs',
                        default=[], help='non source templates',
                        choices=CONFIGS.keys())
    parser.add_argument('-i', '--header', action='append', dest='h_files',
                        default=[], help='header file to create')
    parser.add_argument('-l', '--lang', default=None,
                        help='the language to make', choices=LANGS.keys())
    parser.add_argument('-t', '--target', nargs='?', default='.',
                        help='target dir')
    parser.add_argument('s_files', nargs='*', help='source files to create')

    autocomplete(parser)
    args = parser.parse_args()  # Default parses argv[1:]

    target = os.path.abspath(args.target)
    if not os.path.exists(target):
        os.makedirs(target)

    # BZit of a hack, some files are config instead of source, so just copy
    for config in args.configs:
        if CONFIGS.has_key(config):
            shutil.copy(TEMPLATE_DIR + CONFIGS[config], target)

    if args.lang:
        if args.lang not in LANGS:
            print("Language selected is not supported: %s" % args.lang)
            sys.exit(0)
        process_args(args.lang, target, args.s_files, args.h_files)

if __name__ == '__main__':
    main()
