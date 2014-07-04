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

def out(msg):
    """ Immediate flush for hook. """
    sys.stdout.write(msg)
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

def gen_report(cnt):
    """ Report hook generator. """
    def report_down(block_count, bytes_per_block, total_size):
        """ Simple report hook. """
        if block_count == 0:
            out("Download Progress: [")
        elif total_size < 0:
            print("Read %d blocks" % block_count)
        else:
            total_down = block_count * bytes_per_block
            if total_down > total_size:
                total_down = total_size
            percent = (total_down * 100) / total_size
            cnt.update(percent)
    return report_down

class Counter(object):
    """ Counter wrapper, makes horizontal bar based on ticks. """
    def __init__(self, init, num_ticks, tick):
        self.percent = init
        self.tick_mod = 100 / num_ticks
        self.tick = tick
    def update(self, new_percent):
        """ Check if we made over our old percent. """
        if new_percent > self.percent:
            self.percent = new_percent
            self.draw()
    def draw(self):
        """ Draw if we are on a tick. """
        if self.percent == 0:
            out("Download Progress: [")
        elif (self.percent % self.tick_mod) == 0:
            out(self.tick)
        if self.percent == 100:
            print("]")

def cleanup():
    """ Simple cleanup function. """
    for fil in [B_DIR, CLANG_DIR, CLANG_FILE]:
        if fil in os.listdir('.'):
            if os.path.isdir(fil):
                shutil.rmtree(fil)
            else:
                os.remove(fil)

def main():
    """ Main function. """
    ext_index = CLANG_FILE.rindex('.tar')
    extracted_dir = CLANG_FILE[0:ext_index]

    try:
        if CLANG_DIR not in os.listdir('.'):
            print('Please wait, downloading clang.')
            cnt = Counter(0, 20, '=')
            cfile = urllib.URLopener()
            cfile.retrieve(CLANG_URL, CLANG_FILE, gen_report(cnt))

            cmd = ('tar xf ' + CLANG_FILE).split()
            subprocess.call(cmd)
            os.rename(extracted_dir, CLANG_DIR)

        os.mkdir(B_DIR)
        os.chdir(B_DIR)

        n_procs = get_procs()
        cmd = ['cmake', '-GUnix Makefiles',
                    '-DPATH_TO_LLVM_ROOT=../{}'.format(CLANG_DIR), '.',
                    '~/.vim/bundle/YouCompleteMe/third_party/ycmd/cpp']
        subprocess.call(cmd)

        cmd = 'make -j{} ycm_support_libs'.format(n_procs).split()
        subprocess.call(cmd)
        os.chdir('..')
    finally:
        cleanup()

# Main
if __name__ == '__main__':
    main()
