#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Delete all songs below a certain cutoff rating.
Affects only FLAC and MP3 files.
"""
import argparse
import functools
import hashlib
import multiprocessing as multi
import os
import shutil
import subprocess as sub
import sys
import pathlib


def same_files(fname, fname2):
    """
    Two files are the same if they have the same hash.

    :param fname String: The first filename.
    :param fname2 String: The second filename.
    """
    try:
        hash1 = hashlib.sha512()
        with open(fname, 'rb') as fin:
            hash1.update(fin.read())

        hash2 = hashlib.sha512()
        with open(fname2, 'rb') as fin:
            hash2.update(fin.read())

        return hash1.hexdigest() == hash2.hexdigest()
    except IOError:
        return False


def flac_rating(cutoff, destination, fname):
    """
    FLAC rating of a file. 0 if no rating found.

    :param fname String: The filename to investigate.
    """
    rating = 0.0
    out = sub.check_output(['metaflac', '--list', fname]).decode()
    ind = out.rindex("METADATA block #3")
    for line in out[ind:].split('\n'):
        if "FMPS_RATING=" in line:
            rating = float(line.split('=')[1])
            break

    if rating >= cutoff:
        new_file = os.path.join(destination, fname)
        try:
            os.makedirs(os.path.dirname(new_file))
        except OSError:
            pass
        if not os.path.exists(new_file) and not same_files(fname, new_file):
            shutil.copyfile(fname, new_file)


def mp3_rating(cutoff, destination, fname):
    """
    MP3 rating of a file. 0 if no rating found.

    :param fname String: The filename to investigate.
    """
    rating = 0.0
    out = sub.check_output(['mid3v2', '-l', fname]).decode()
    for line in out.split('\n'):
        if line.startswith("TXXX=FMPS_Rating"):
            rating = float(line.split('=')[2])
            break

    if rating >= cutoff:
        new_file = os.path.join(destination, fname)
        try:
            os.makedirs(os.path.dirname(new_file))
        except OSError:
            pass
        if not os.path.exists(new_file) and not same_files(fname, new_file):
            shutil.copyfile(fname, new_file)


def make_parser():
    """
    Create a simple parser for this program.
    """
    parser = argparse.ArgumentParser(description="Delete songs below cutoff rating")
    parser.add_argument('folder', help="The folder that you want to scrape.")
    parser.add_argument('destination', help="The folder that you want to copy to on match.")
    parser.add_argument('--cutoff', '-c', type=float, default=1.0,
                        help="The cutoff to use. Default 1.0")

    return parser


def main():
    """
    Main entry for this program.
    """
    args = make_parser().parse_args()
    if len(sys.argv) > 1:
        pat = pathlib.Path(args.folder)
    else:
        pat = pathlib.Path(".")

    mp3s = list(pat.glob("**/*.mp3"))
    flacs = list(pat.glob("**/*.flac"))

    with multi.Pool(8) as pool:
        if flacs:
            pool.map(functools.partial(flac_rating, args.cutoff, args.destination), flacs)
        if mp3s:
            pool.map(functools.partial(mp3_rating, args.cutoff), args.destination, mp3s)


if __name__ == "__main__":
    main()
