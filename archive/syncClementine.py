#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Update the clementine ratings between two different DBs.

Often switch between OSes and want to keep ratings up to date.
If you only want a subset of the songs, modify the QUERY_RATING variable.

Pass in db locations to the program as SRC and DST, ratings from SRC will OVERWRITE ratings
of matched title/artist combinations in DST.

Database Locations
------------------
* Linux: ~/.config/Clementine/clementine.db
* Windows: C:/Users/USERNAME/.config/Clementine/clementine.db
"""
from __future__ import print_function
import os
import sys

import argparse
from argparse import RawDescriptionHelpFormatter as RawDescriptionHelp
import sqlite3

# Ratings go from 0.1 - 1.0, only update rated songs
LOC_FILE = os.path.expanduser('~/.clem_locs')
RATINGS = [float(x) / 10.0 for x in range(1, 11)]
QUERY_RATING = unicode('SELECT rating, artist, title FROM songs WHERE rating = ?')
QUERY_ALL = unicode('SELECT rating, artist, title FROM songs WHERE artist = ? AND title = ?')
UPDATE = unicode('UPDATE songs SET rating = ? WHERE artist = ? AND title = ?')


def read_locs(fname):
    """
    Return a dictionary, keys are terms to put in command. Values are file paths.
    """
    paths = {}
    if not os.path.exists(fname):
        return paths
    with open(fname) as fin:
        for line in fin:
            key, val = line.rstrip().split(':')
            paths[key] = os.path.join(os.path.expanduser(val),
                                      '.config', 'Clementine', 'clementine.db')

    return paths

def update_db(src_db, dst_db):
    """
    Update the dst with all ratings made in src for all artists/title combinations
    in dst.
    """
    for rating in RATINGS:
        with sqlite3.connect(src_db) as con_src:
            results = con_src.execute(QUERY_RATING, (rating,))
        with sqlite3.connect(dst_db) as con_dst:
            con_dst.executemany(UPDATE, results)
            # To verify
            # for tupl in results:
                # for line in con_dst.execute(QUERY_ALL, tupl[1:]):
                    # print(line)

def main():
    locs = read_locs(LOC_FILE)
    mesg = sys.modules[__name__].__doc__
    parser = argparse.ArgumentParser(prog=__name__, description=mesg,
                                     formatter_class=RawDescriptionHelp)
    parser.add_argument('-v', '--version', action='version', version='0.1')
    parser.add_argument('src', help='The SRC db, ratings will be read FROM src.',
                        choices=locs.keys())
    parser.add_argument('dst', help='The DST db, ratings will be updated TO dst.',
                        choices=locs.keys())

    args = parser.parse_args()
    args.src = locs.get(args.src, os.path.expanduser(args.src))
    args.dst = locs.get(args.dst, os.path.expanduser(args.dst))

    try:
        assert os.path.exists(args.src)
        assert os.path.exists(args.dst)
        update_db(args.src, args.dst)
    except AssertionError:
        if not os.path.exists(args.src):
            print('The SRC database is NOT a valid file: ' + args.src)
        if not os.path.exists(args.dst):
            print('The DST database is NOT a valid file: ' + args.dst)


if __name__ == "__main__":
    main()
