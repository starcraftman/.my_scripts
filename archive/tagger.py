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

import os
import subprocess
import sys


def get_root():
    """
    Simple argument processing to get root.
    """
    if len(sys.argv) > 2:
        raise Exception('Only argument should be folder root!')
    elif len(sys.argv) == 2:
        root = sys.argv[1]
    else:
        root = os.getcwd()

    return root


def parse_input(root):
    """
    Processes the input with song titles.
    See above format.

    Returns a dict of mapping number -> [title1, title2, ...]
    """
    tdb = {}
    disc_no = -1
    with open(os.path.join(root, 'input.txt')) as fin:
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
    assert len(fnames) == len(titles)
    for fname, title in zip(fnames, titles):
        print('Log', fname, title)
        subprocess.call(['metaflac', '--remove-tag', 'TITLE', fname])
        subprocess.call(['metaflac', '--set-tag',
                         'TITLE={}'.format(title), fname])
        subprocess.call(['metaflac', '--remove-tag', 'DISCNUMBER', fname])
        subprocess.call(['metaflac', '--set-tag',
                         'DISCNUMBER=' + disc_no, fname])


def main():
    """
    It is the main.
    """
    root = get_root()
    print("Operating in root: ", root)
    sdirs = [os.path.join(root, dname) for dname in sorted(os.listdir(root))
             if os.path.isdir(dname)]
    tdb = parse_input(root)

    for num in range(0, len(sdirs)):
        update_titles(sdirs[num], tdb[num], num + 1)


if __name__ == "__main__":
    main()
