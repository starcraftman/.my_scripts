#!/usr/bin/env python
# Common tools:
#	pip/pip3 : install packages
#	pep8/pylint/pychecker : verify syntax
#	unittest package for xUnit.
""" This is a simple script to recompile ycm everytime it gets updated. """

# Imports
import os
import shutil
import subprocess
import SysInstall

# Data
CLANG_URL = 'http://llvm.org/releases/3.4.1/\
clang+llvm-3.4.1-x86_64-unknown-ubuntu12.04.tar.xz'
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
        [
            'cmake', '-GUnix Makefiles',
            '-DPATH_TO_LLVM_ROOT=../{}'.format(CLANG_DIR), '.',
            '~/.vim/bundle/YouCompleteMe/third_party/ycmd/cpp',
        ],
        [
            'make', '-j', unicode(SysInstall.NUM_JOBS), 'ycm_support_libs',
        ],
    ]

    for cmd in cmds:
        subprocess.call(cmd)

def main():
    """ Main function. """
    origdir = os.path.realpath(os.curdir)

    try:
        SysInstall.get_archive(CLANG_URL, CLANG_DIR)
        build_ycm()
    finally:
        os.chdir(origdir)
        cleanup()

# Main
if __name__ == '__main__':
    main()
