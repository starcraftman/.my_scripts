#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Solves my own personal tagging post ripping with EAC problem.

Expected input.txt format (blank lines ignored):
Disc 1
Track name 1
Track name 2
Disc 2
Track name 1
...

Expected directory structure:
 /Felix Mendelssohn
   /input.txt
   /01
     /01 Track 01.flac
     /02 Track 02.flac
     ...
   /02
     ...
"""
from __future__ import print_function, absolute_import

import glob
import os
import subprocess
import sys


class WrongDir(Exception):
    """
    Program was started in the wrong directory.
    """
    pass


def get_root():
    """
    Simple argument processing to get root.
    """
    if len(sys.argv) > 2:
        raise Exception('Only argument should be folder root!')
    elif len(sys.argv) == 2:
        root = os.path.abspath(sys.argv[1])
    else:
        root = os.getcwd()

    return root


def parse_input(input_file):
    """
    Processes the input with song titles.
    See above format.

    Returns a dict of mapping number -> [title1, title2, ...]
    """
    tdb = {}
    disc_no = -1
    with open(input_file) as fin:
        for line in fin:
            line = line.strip()
            if 'disc' in line.lower() or 'disk' in line.lower():
                disc_no += 1
                tdb[disc_no] = []
            elif line != '':
                tdb[disc_no].append(line)

    return tdb


def update_titles(sdir, titles, disc_no):
    """
    For every fname in the subdirectory, update title name and disc number.
    N.B. DEPENDS on metaflac being installed.
    """
    fnames = [os.path.join(sdir, fname) for fname in sorted(os.listdir(sdir))]
    try:
        assert len(fnames) == len(titles)
        for fname, title in zip(fnames, titles):
            print('Log', fname, title)
            subprocess.call(['metaflac', '--remove-tag', 'TITLE', fname])
            subprocess.call(['metaflac', '--set-tag',
                             'TITLE={}'.format(title), fname])
            subprocess.call(['metaflac', '--remove-tag', 'DISCNUMBER', fname])
            subprocess.call(['metaflac', '--set-tag',
                             'DISCNUMBER=' + str(disc_no), fname])
    except AssertionError:
        print('The # of files and titles in the text file do not match!')
        print('# of files: {} | # of names in file: {}'.format(len(fnames),
                                                               len(titles)))
        print('FNAMES >>>>>>>>>')
        print(str(fnames))
        print('TITLES <<<<<<<<<')
        print(str(titles))


def main():
    """
    It is the main.
    """
    root = get_root()
    print("Operating in root: ", root)

    try:
        finput = glob.glob(os.path.join(root, '*.txt'))
        assert len(finput) == 1
        tdb = parse_input(finput[0])

        sdirs = [os.path.join(root, dname) for dname in sorted(os.listdir(root))
                 if os.path.isdir(dname)]
        for char in sdirs[0]:
            if not str.isdigit(char):
                raise WrongDir

        for num in range(0, len(sdirs)):
            update_titles(sdirs[num], tdb[num], num + 1)
    except AssertionError:
        print('The input file is missing. Please place it at: {}'.format(root))
        print('Alternatively, tagger was started in the wrong dir.')
    except WrongDir:
        print('Started in wrong directory.')
        print('Please cd to the root with dirs of form 001, 002, 003 ..')


if __name__ == "__main__":
    main()
