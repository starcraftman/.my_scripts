#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Provide a tool to copy music files from one directory to destination
if they are rated >= to a cutoff.
Affects only FLAC and MP3 files.
"""
import argparse
import functools
import hashlib
import logging
import multiprocessing as multi
import os
import pathlib
import shutil
import subprocess as sub
import sys
import tempfile


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
    try:
        out = sub.check_output(['metaflac', '--list', fname]).decode()
        ind = out.rindex("METADATA block #3")
        for line in out[ind:].split('\n'):
            if "FMPS_RATING=" in line:
                rating = float(line.split('=')[1])
                break
    except sub.CalledProcessError as exc:
        logging.error("Failed to query file: %s\n%s\n%s", fname, str(exc))

    if rating >= cutoff:
        new_file = os.path.join(destination, fname)
        try:
            os.makedirs(os.path.dirname(new_file))
        except OSError:
            pass
        if not os.path.exists(new_file) or not same_files(fname, new_file):
            logging.debug("Copying to destination: %s", fname)
            shutil.copyfile(fname, new_file)


def mp3_rating(cutoff, destination, fname):
    """
    MP3 rating of a file. 0 if no rating found.

    :param fname String: The filename to investigate.
    """
    rating = 0.0
    try:
        out = sub.check_output(['mid3v2', '-l', fname]).decode()
        for line in out.split('\n'):
            if line.startswith("TXXX=FMPS_Rating"):
                rating = float(line.split('=')[2])
                break
    except sub.CalledProcessError as exc:
        logging.error("Failed to query file: %s\n%s\n%s", fname, str(exc))

    if rating >= cutoff:
        new_file = os.path.join(destination, fname)
        try:
            os.makedirs(os.path.dirname(new_file))
        except OSError:
            pass
        if not os.path.exists(new_file) or not same_files(fname, new_file):
            logging.debug("Copying to destination: %s", fname)
            shutil.copyfile(fname, new_file)


def make_parser():
    """
    Create a simple parser for this program.
    """
    parser = argparse.ArgumentParser(description="Delete songs below cutoff rating")
    parser.add_argument('folder', help="The folder that you want to scrape.")
    parser.add_argument('destination', help="The folder that you want to copy to on match.")
    parser.add_argument('--cutoff', '-c', type=float, default=1.0,
                        help="The cutoff to use. Default 1.0. Scale is 0.0 - 1.0, 4 stars = 0.8")

    return parser


def check_prereqs():
    """
    Check the prerequisites for inspecting ID3 tags.

    If not met, print how to resolve and exit.
    """
    try:
        sub.check_output(['metaflac', '--version'])
    except sub.CalledProcessError:
        print("Missing command: metaflac\n\nsudo apt install flac")
        sys.exit(1)

    try:
        sub.check_output(['mid3v2', '--version'])
    except sub.CalledProcessError:
        print("Missing command: mid3v2\n\npip install mutagen")
        sys.exit(1)


def main():
    """
    Main entry for this program.
    """
    tfile = tempfile.NamedTemporaryFile(delete=False)
    print("Log for this usage will be: " + tfile.name)
    print("Please sit back and enjoy tea. Tail -f file for updates.")
    logging.basicConfig(filename=tfile.name, level=logging.DEBUG)

    args = make_parser().parse_args()
    args.destination = os.path.abspath(args.destination)
    check_prereqs()

    try:
        orig = os.getcwd()
        os.chdir(args.folder)
        # Ensure globs are relative to root for joining

        pat = pathlib.Path(".")
        mp3s = [str(x) for x in pat.glob("**/*.mp3")]
        flacs = [str(x) for x in pat.glob("**/*.flac")]
        if not mp3s and not flacs:
            print("Nothing matched, please check: " + args.folder)
            sys.exit(1)

        with multi.Pool(8) as pool:
            pool.map(functools.partial(flac_rating, args.cutoff, args.destination), flacs)
            pool.map(functools.partial(mp3_rating, args.cutoff, args.destination), mp3s)
    finally:
        tfile.close()
        os.chdir(orig)


if __name__ == "__main__":
    main()
