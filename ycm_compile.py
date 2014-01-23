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
CLANG_SITE = 'http://llvm.org/releases/3.4/'
CLANG_FILE = 'clang+llvm-3.4-x86_64-linux-gnu-ubuntu-13.10.tar.xz'
CLANG_URL = '{}{}'.format(CLANG_SITE, CLANG_FILE)
CLANG_DIR = 'clang'
B_DIR = 'build'

# Classes

# Functions


def get_procs():
    """ Use BASH one liner to determine number of threads available. """
    f1 = open('temp', 'w')
    subprocess.call('cat /proc/cpuinfo | grep "processor" | wc -l',
                    stdout=f1, shell=True)
    f1.close()

    f1 = open('temp', 'r')
    procs = int(f1.read())
    f1.close()

    os.remove('temp')

    return procs


def check_clang():
    """ Check if we have clang, else retrieve it. """
    ext_index = CLANG_FILE.rindex('.tar')
    extracted_dir = CLANG_FILE[0:ext_index]
    list_dir = os.listdir()

    # Protection if clang dir exists.
    if CLANG_DIR in list_dir:
        return

    if CLANG_FILE not in list_dir:
        print('Please wait, downloading clang.')
        urllib.request.urlretrieve(CLANG_URL, CLANG_FILE)
        print('Finished download.')

    if extracted_dir in list_dir:
        shutil.rmtree(extracted_dir)

    tar_file = tarfile.open(CLANG_FILE, 'r')
    tar_file.extractall()
    os.remove(CLANG_FILE)
    os.rename(extracted_dir, CLANG_DIR)

# Main
if __name__ == '__main__':
    check_clang()

    # Protection in case build exists prior.
    if B_DIR in os.listdir():
        shutil.rmtree(B_DIR)

    os.mkdir(B_DIR)
    os.chdir(B_DIR)

    NUM_PROCS = get_procs()
    print(NUM_PROCS)
    subprocess.call(['cmake', '-GUnix Makefiles',
                     '-DPATH_TO_LLVM_ROOT=../{}'.format(CLANG_DIR), '.',
                     '~/.vim/bundle/YouCompleteMe/cpp'])
    subprocess.call(['make', '-j{}'.format(NUM_PROCS), 'ycm_support_libs'])

    os.chdir('..')
    shutil.rmtree(B_DIR)
    shutil.rmtree(CLANG_DIR)
