#!/usr/bin/env python
# Common tools:
#	pip/pip3 : install packages
#	pep8/pylint/pychecker : verify syntax
#	unittest package for xUnit.
""" This is a simple script to recompile ycm everytime it gets updated. """

# Imports
from __future__ import print_function
import os
import shutil
import subprocess
import urllib
import sys

# Data
CLANG_SITE = 'http://llvm.org/releases/3.4.1/'
CLANG_FILE = 'clang+llvm-3.4.1-x86_64-unknown-ubuntu12.04.tar.xz'
CLANG_URL = '{}{}'.format(CLANG_SITE, CLANG_FILE)
CLANG_DIR = 'clang'
B_DIR = 'build'

# Classes

# Functions

def out(msgs):
    """ Immediate flush for hook. """
    sys.stdout.write("".join(msgs))
    sys.stdout.flush()

def get_procs():
    """ Use BASH one liner to determine number of threads available. """
    tfile = open('temp', 'w')
    subprocess.call('cat /proc/cpuinfo | grep "processor" | wc -l',
                    stdout=tfile, shell=True)
    tfile.close()

    tfile = open('temp', 'r')
    procs = int(tfile.read())
    tfile.close()

    os.remove('temp')
    return procs

def gen_report(progress):
    """ Report hook generator. """
    def report_down(block_count, bytes_per_block, total_size):
        """ Simple report hook. """
        if block_count == 0:
            print("Download Started")
        elif total_size < 0:
            print("Read %d blocks" % block_count)
        else:
            total_down = block_count * bytes_per_block
            percent = (total_down * 100.0) / total_size
            if total_down >= total_size or progress.check_percent(percent):
                progress.inc()
                progress.draw()
    return report_down

class Progress(object):
    """ Draw a simple progress bar. """
    def __init__(self, tick, empty, total_ticks):
        self.tick = tick
        self.empty = empty
        self.total_ticks = total_ticks
        self.num_ticks = 0
        self.old_percent = 0
    def check_percent(self, new_percent):
        if new_percent >= self.old_percent + self.tick_threshold():
            self.old_percent = new_percent
            return True
        else:
            return False
    def inc(self):
        self.num_ticks += 1
    def draw(self):
        num_empty = self.total_ticks - self.num_ticks
        sys.stdout.write("Download Progress: [")
        sys.stdout.write(self.tick * self.num_ticks)
        sys.stdout.write(self.empty * num_empty)
        sys.stdout.write("]\n")
        sys.stdout.flush()
    def tick_threshold(self):
        return 100 / self.total_ticks
    @staticmethod
    def default_prog():
        return Progress('=', '*', 20)

def cleanup():
    """ Simple cleanup function. """
    for fil in [B_DIR, CLANG_DIR, CLANG_FILE]:
        if fil in os.listdir('.'):
            if os.path.isdir(fil):
                shutil.rmtree(fil)
            else:
                os.remove(fil)

def get_clang():
    """ Download clang for ycm. """
    ext_index = CLANG_FILE.rindex('.tar')
    extracted_dir = CLANG_FILE[0:ext_index]

    print('Please wait, downloading clang.')
    cfile = urllib.URLopener()
    cfile.retrieve(CLANG_URL, CLANG_FILE,
            gen_report(Progress.default_prog()))

    cmd = ('tar xf ' + CLANG_FILE).split()
    subprocess.call(cmd)
    os.rename(extracted_dir, CLANG_DIR)

def build_ycm():
    """ Build the shared library for ycm. """
    os.mkdir(B_DIR)
    os.chdir(B_DIR)

    n_procs = get_procs()
    cmd = ['cmake', '-GUnix Makefiles',
                '-DPATH_TO_LLVM_ROOT=../{}'.format(CLANG_DIR), '.',
                '~/.vim/bundle/YouCompleteMe/third_party/ycmd/cpp']
    subprocess.call(cmd)

    cmd = 'make -j{} ycm_support_libs'.format(n_procs).split()
    subprocess.call(cmd)

def main():
    """ Main function. """
    origdir = os.path.realpath(os.curdir)

    try:
        if CLANG_DIR not in os.listdir('.'):
            get_clang()
        build_ycm()
    finally:
        os.chdir(origdir)
        cleanup()

# Main
if __name__ == '__main__':
    main()
