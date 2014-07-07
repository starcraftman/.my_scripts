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
import SysInstall

# Data
CLANG_FILE = 'clang+llvm-3.4.1-x86_64-unknown-ubuntu12.04.tar.xz'
CLANG_URL = 'http://llvm.org/releases/3.4.1/' + CLANG_FILE
CLANG_DIR = 'clang'
B_DIR = 'build'

# Classes

# Functions

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
    prog = SysInstall.Progress.default_prog()
    cfile = urllib.URLopener()
    cfile.retrieve(CLANG_URL, CLANG_FILE,
            SysInstall.gen_report(prog))

    cmd = ('tar xf ' + CLANG_FILE).split()
    subprocess.call(cmd)
    os.rename(extracted_dir, CLANG_DIR)

def build_ycm():
    """ Build the shared library for ycm. """
    os.mkdir(B_DIR)
    os.chdir(B_DIR)

    cmd = ['cmake', '-GUnix Makefiles',
                '-DPATH_TO_LLVM_ROOT=../{}'.format(CLANG_DIR), '.',
                '~/.vim/bundle/YouCompleteMe/third_party/ycmd/cpp']
    subprocess.call(cmd)

    num_jobs = SysInstall.num_jobs()
    cmd = 'make -j{} ycm_support_libs'.format(num_jobs).split()
    subprocess.call(cmd)

def main():
    """ Main function. """
    origdir = os.path.realpath(os.curdir)

    try:
        get_clang()
        build_ycm()
    finally:
        os.chdir(origdir)
        cleanup()

# Main
if __name__ == '__main__':
    main()
