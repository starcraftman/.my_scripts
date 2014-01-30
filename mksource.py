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
import argcomplete
import argparse
import glob
import os
import stat
import sys
from shutil import copyfile

# These are languages that get execute.
SCRIPT_LANGS = ('python', 'perl', 'ruby')

# Static data, I define here the dicts for extensions
SRC_DICT = {'perl': '.pl',
            'python': '.py',
            'ruby': '.rb',
            'lisp': '.lisp',
            'prolog': '.pdb',
            'c': '.c',
            'c++': '.cpp',
            }

H_DICT = {'c': '.h',
          'c++': '.hpp',
          }

# Functions


def header_copy(template, header, new_text):
    ''' While copying, this func will change the ifdef marker. '''
    with open(template, 'r') as src, open(header, 'w') as dst:
        for line in src:
            new_line = line.replace('_TEST_H_', "_%s_" % new_text)
            dst.write(new_line)


def add_ext(lang, sources, headers):
    ''' Returns two new lists with extensions added.
    Headers list only there if c language.
    '''
    new_sources = [s + SRC_DICT[lang] for s in sources]
    new_headers = []
    if lang in H_DICT:
        new_headers = [h + H_DICT[lang] for h in headers]

    return (new_sources, new_headers)

if __name__ == '__main__':
    # Setup argument parser, very nice. -i for header due to help default.
    DESC = """ This is my source file creator. The language is required.
    Specify as many source or header files as required.
    """
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument('lang', action='store', help='the language to make',
                        choices=SRC_DICT.keys())
    parser.add_argument('s_files', nargs='*', help='source files to create')
    parser.add_argument('-i', action='append', dest='h_files',
                        default=[], help='header file to create')

    argcomplete.autocomplete(parser)
    args = parser.parse_args()  # Default parses argv[1:]

    if args.lang not in SRC_DICT:
        print("Language selected is not supported: %s" % args.lang)
        sys.exit(0)

    src_files, h_files = add_ext(args.lang, args.s_files, args.h_files)

    # Select the template via globing relative location of file.
    script_dir = os.path.dirname(os.path.realpath(__file__))
    templates = glob.glob("{}/templates/{}_*".format(script_dir, args.lang))
    templates.sort()  # Source template first.

    # I've added extension and found template, now simply copy files.
    for s_file in src_files:
        copyfile(templates[0], s_file)

        # Scripts need execute on user.
        if args.lang in SCRIPT_LANGS:
            new_perms = stat.S_IMODE(os.stat(s_file).st_mode)
            new_perms = new_perms | stat.S_IXUSR
            os.chmod(s_file, new_perms)

    # Headers must make a define to protect against include,
    # use new header_text to replace old default.
    for h_file in h_files:
        header_text = h_file.upper().replace('.', '_')
        header_copy(templates[1], h_file, header_text)
