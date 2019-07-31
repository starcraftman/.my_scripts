#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Delete all songs below a certain cutoff rating.
Affects only FLAC and MP3 files.
"""
import argparse
import functools
import multiprocessing as multi
import os
import subprocess as sub
import sys
import pathlib


def flac_rating(cutoff, fname):
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

    if rating < cutoff:
        os.remove(fname)


def mp3_rating(cutoff, fname):
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

    if rating < cutoff:
        os.remove(fname)


def make_parser():
    """
    Create a simple parser for this program.
    """
    parser = argparse.ArgumentParser(description="Delete songs below cutoff rating")
    parser.add_argument('folder', help="The folder that you want to scrape.")
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

    mp3s = pat.glob("**/*.mp3")
    flacs = pat.glob("**/*.flac")

    with multi.Pool(8) as pool:
        pool.map(functools.partial(flac_rating, args.cutoff), flacs)
        pool.map(functools.partial(mp3_rating, args.cutoff), mp3s)


if __name__ == "__main__":
    main()
