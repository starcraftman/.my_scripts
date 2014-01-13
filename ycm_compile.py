#!/usr/bin/env python3
# Common tools:
#	pip/pip3 : install packages
#	pep8/pylint/pychecker : verify syntax
#	unittest package for xUnit.
""" This is a simple script to recompile ycm everytime it gets updated. """

# Imports
import os
import shutil
import subprocess
import urllib.request
import tarfile

# Data
B_DIR = 'build'
CLANG_SITE = 'http://llvm.org/releases/3.4/'
CLANG_FILE = 'clang+llvm-3.4-x86_64-linux-gnu-ubuntu-13.10.tar.xz'
CLANG_URL = "{}{}".format(CLANG_SITE, CLANG_FILE)
CLANG_DIR = 'clang'

# Classes

# Functions


def check_clang():
    """ Check if we have clang, else retrieve it. """
    file_no_ext = CLANG_FILE[0:CLANG_FILE.rindex(".tar")]
    list_dir = os.listdir()

    if CLANG_DIR in list_dir:
        return

    if CLANG_FILE not in list_dir:
        print("Please wait, downloading clang.")
        urllib.request.urlretrieve(CLANG_URL, CLANG_FILE)
        print("Finished download.")

    if file_no_ext in list_dir:
        shutil.rmtree(file_no_ext)

    tar_file = tarfile.open(CLANG_FILE, 'r')
    tar_file.extractall()
    os.rename(file_no_ext, CLANG_DIR)
    os.remove(CLANG_FILE)

# Main
if __name__ == '__main__':
    if B_DIR in os.listdir():
        shutil.rmtree(B_DIR)

    check_clang()

    os.mkdir(B_DIR)
    os.chdir(B_DIR)

    subprocess.call(['cmake', '-GUnix Makefiles',
                     '-DPATH_TO_LLVM_ROOT=../{}'.format(CLANG_DIR), '.',
                     '~/.vim/bundle/YouCompleteMe/cpp'])
    subprocess.call(['make', '-j8', 'ycm_support_libs'])

    os.chdir('..')
    shutil.rmtree(B_DIR)
