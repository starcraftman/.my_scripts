#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Windows max filename length sucks!
"""
from __future__ import print_function

import argparse
import os


FNAME_MAX = 150
END = '\033[0m'
ULINE = '\033[93m\033[4m'


def trunc(fname, maxlen):
    """
    Truncate to the nearest word below max.
    """
    front, back = fname.rsplit('.', 1)
    front_pieces = front.split(' ')
    new_max = maxlen - len(back) - 1

    while len(front) >= new_max:
        front_pieces = front_pieces[:-1]
        if front_pieces[-1] == '-':
            front_pieces = front_pieces[:-1]
        front = ' '.join(front_pieces)

    new_fname = front + '.' + back
    return new_fname.replace(',.' + back, '.' + back)  # remove trailing commas


def collect(dname='.'):
    """
    Collect files into a dict indexed by fname length.
    """
    files = {}

    for paths in os.walk(dname):
        for fname in paths[2]:
            flen = len(fname)
            fpath = os.path.join(paths[0], fname)
            try:
                files[flen].append(fpath)
            except KeyError:
                files[flen] = [fpath]

    return files


def word_diff(old, new):
    """
    Return diff of word, highlighting deletions.
    """
    dpos = len(old) - len(new)
    front, back = old.rsplit('.', 1)
    return front[:-dpos] + ULINE + front[-dpos:] + END + '.' + back


def main():
    mesg = 'Truncate a bunch of files in a folder to a maximum length.'
    parser = argparse.ArgumentParser(prog='wintrunc', description=mesg)
    parser.add_argument('-m', '--max', type=int, default=FNAME_MAX, help='the max len')
    parser.add_argument('-d', '--dname', default=os.getcwd(), help='truncate files under DNAME')
    parser.add_argument('-b', '--base', help='consider only base of fname', action='store_false')
    args = parser.parse_args()
    args.dname = os.path.abspath(args.dname)

    print('Searching for files under: ' + args.dname)
    files = collect(args.dname)

    rlist = []
    for key in files.keys():
        if key < args.max:
            continue

        if args.base:
            for fname in files[key]:
                dname, truncated = os.path.dirname(fname), trunc(os.path.basename(fname), args.max)
                rlist.append([fname, os.path.join(dname, truncated)])
        else:
            for fname in files[key]:
                rlist.append([fname, trunc(fname, args.max)])

    print('Preview of changes, underline will be removed.')
    for ent in rlist:
        print(word_diff(ent[0], ent[1]))

    choice = raw_input('Continue with renames? Y/n  ')
    if choice.lower()[0] == 'y' and len(rlist) != 0:
        for ent in rlist:
            os.rename(ent[0], ent[1])


if __name__ == "__main__":
    main()
