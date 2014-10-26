#!/usr/bin/env python
# Common tools:
#	pip/pip3 : install packages
#	pep8/pylint/pychecker : verify syntax
#	unittest package for xUnit.
""" This is a simple script to recompile ycm everytime it gets updated. """

# Imports
from BuildSrc import get_archive
import multiprocessing
import os
import shutil
import subprocess

# Data
CLANG_URL = 'http://llvm.org/releases/3.5.0/\
clang+llvm-3.5.0-x86_64-linux-gnu-ubuntu-14.04.tar.xz'
CLANG_DIR = 'clang'
B_DIR = 'build'

# Classes

# Functions

def cleanup():
    """ Simple cleanup function. """
    for fil in [B_DIR, CLANG_DIR]:
        if fil in os.listdir('.'):
            if os.path.isdir(fil):
                shutil.rmtree(fil)
            else:
                os.remove(fil)

def build_ycm():
    """ Build the shared library for ycm. """
    os.mkdir(B_DIR)
    os.chdir(B_DIR)

    cmds = [
        'cmake -DPATH_TO_LLVM_ROOT=../%s . \
~/.vim/bundle/YouCompleteMe/third_party/ycmd/cpp' % CLANG_DIR,
        'make -j%d ycm_support_libs' % multiprocessing.cpu_count(),
    ]

    for cmd in cmds:
        subprocess.call(cmd.split())

def main():
    """ Main function. """
    origdir = os.path.abspath(os.curdir)

    try:
        get_archive(CLANG_URL, CLANG_DIR)
        build_ycm()
    finally:
        os.chdir(origdir)
        cleanup()

# Main
if __name__ == '__main__':
    main()
