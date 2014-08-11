#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
# Common tools:
#	pip/pip3 : install packages
#	pylint/pychecker : verify syntax
#	unittest package for xUnit.
""" This module helps setup a fresh install the way I like it. """

# Imports
from __future__ import print_function
import argparse
import glob
import os
import re
import shutil
import subprocess
import tarfile
import zipfile

URL_BOOST = 'http://sourceforge.net/projects/boost/files/boost/1.55.0/\
boost_1_55_0.tar.bz2/download'
URL_GTEST = 'https://googletest.googlecode.com/files/gtest-1.7.0.zip'

if os.name == 'posix':
    NUM_JOBS = int(subprocess.check_output('cat /proc/cpuinfo | \
        grep processor | wc -l', shell=True))
else:
    NUM_JOBS = 2

# Classes

class ArchiveException(Exception):
    """ Archive can't be processed. """
    pass

class PDir(object):
    """ Pushd analog for personal use. """
    dirs = []
    @staticmethod
    def push(new_dir):
        """ Push curdir to stack and change to new_dir. """
        curdir = os.path.realpath(os.curdir)
        PDir.dirs.append(curdir)
        os.chdir(new_dir)
        print("Changing to: " + new_dir)
    @staticmethod
    def pop():
        """ Pop the dirstack and return to it. """
        os.chdir(PDir.dirs.pop())

# Functions

def get_archive(url, target):
    """ Fetch an archive from a site. Works on regular ftp & sourceforge.
    url: location to get archive
    target: where to extract to
    """
    arc_ext = None
    for ext in ['.tgz', '.tbz2', '.tar.bz2', '.tar.gz', '.rar', '.zip', '.7z']:
        right = url.rfind(ext)
        if right != -1:
            right += len(ext)
            left = url.rfind(os.sep, 0, right) + 1
            arc_ext = ext
            break

    if arc_ext == None:
        raise ArchiveException

    arc_name = url[left:right]

    cmd = 'wget -O %s %s' % (arc_name, url)
    subprocess.call(cmd.split())
    if arc_ext in ['.tgz', '.tbz2', '.tar.bz2', '.tar.gz']:
        with tarfile.open(arc_name) as tarf:
            tarf.extractall()
    elif arc_ext in ['.zip']:
        with zipfile.ZipFile(arc_name) as zipf:
            zipf.extractall()
    else:
        cmd = 'unarchive ' + arc_name
        subprocess.call(cmd.split())

    # extracted dir doesn't always match arc_name, glob to be sure
    arc_front = re.split('[-_]', arc_name)[0] + '*'
    arc_dir = None
    for name in glob.glob(arc_front):
        if name.rfind(arc_ext) == -1:
            arc_dir = name

    os.makedirs(target)
    os.rmdir(target)
    os.rename(arc_dir, target)
    os.remove(arc_name)

def get_code(url, target):
    """ Wrapper function to clone repos, only executes if target doesn't exist
    url: The origin to clone
    target: Where to clone to
    """
    cmd = ' %s %s' % (url, target)
    # Git urls always end in .git
    if url.find('git') != -1:
        cmd = 'git clone --depth 1' + cmd
    # svn always at front of proto
    elif url.find('svn') != -1:
        cmd = 'svn checkout' + cmd
    else:
        cmd = 'hg clone' + cmd

    if not os.path.exists(target):
        subprocess.call(cmd.split())

def build_sdl(libdir):
    """ Build ack from source, move to target dir. """
    srcdir, srcdir2 = 'sdl', 'sdl2'
    jobs = NUM_JOBS
    cmds_sdl1 = [
        'hg update SDL-1.2',
        './autogen.sh',
        './configure --prefix=%s' % libdir,
        'make -j%d install' % jobs,
    ]
    cmds_sdl2 = [
        './configure --prefix=%s' % libdir,
        'make -j%d install' % jobs,
    ]
    build = {
        srcdir: cmds_sdl1,
        srcdir2: cmds_sdl2,
    }

    try:
        # Fetch code & copy for 2
        get_code('http://hg.libsdl.org/SDL', srcdir)
        cmd = 'cp -r %s %s' % (srcdir, srcdir2)
        subprocess.call(cmd.split())

        # Build sdl1 & 2
        for src in build.keys():
            PDir.push(src)
            for cmd in build[src]:
                subprocess.call(cmd.split())
            PDir.pop()
    finally:
        shutil.rmtree(srcdir)
        shutil.rmtree(srcdir2)

def build_gtest(libdir):
    """ Build gtest from source and put in libs. """
    srcdir = 'gtest'

    try:
        # Fetch program
        print("Downloading gtest source.")
        get_archive(URL_GTEST, srcdir)

        # Build & clean
        PDir.push(srcdir)
        cmds = [
            'chmod u+x configure ./scripts/*',
            './configure --prefix={}'.format(libdir),
            'make',
        ]
        for cmd in cmds:
            subprocess.call(cmd.split())

        # Copy out file structure
        os.mkdir(libdir + os.sep + 'lib')
        shutil.copytree('include', libdir + os.sep + 'include')
        for fil in glob.glob('lib' + os.sep + '.libs' + os.sep + '*.a'):
            shutil.copy(fil, libdir + os.sep + 'lib')
    finally:
        PDir.pop()
        shutil.rmtree(srcdir)

def build_cunit(libdir):
    """ Build classic cunit, good test lib for c code. """
    srcdir = 'cunit'
    get_code('svn://svn.code.sf.net/p/cunit/code/trunk', srcdir)

    # Build & clean
    PDir.push(srcdir)
    # Shell true is due to some bug via normal way
    cmds = [
        'sh ./bootstrap %s' % libdir,
        'make -j%d install' % NUM_JOBS,
    ]
    for cmd in cmds:
        subprocess.call(cmd)
    PDir.pop()

    shutil.rmtree(srcdir)

def build_boost(libdir):
    """ Build latest boost release for c++. """
    config = os.path.expanduser('~') + os.sep + 'user-config.jam'
    srcdir = 'boost'

    try:
        # Fetch program
        print("Downloading latest zsh source.")
        get_archive(URL_BOOST, srcdir)

        # Need this for jam to build mpi & graph_parallel.
        f_conf = open(config, 'w')
        f_conf.write('using mpi ;')
        f_conf.close()

        PDir.push(srcdir)
        cmds = [
            './bootstrap.sh --prefix=%s' % libdir,
            './b2 install'
        ]
        for cmd in cmds:
            subprocess.call(cmd.split())
    finally:
        PDir.pop()
        shutil.rmtree(srcdir)
        os.remove(config)

def main():
    """ Main function. """
    mesg = """This script sets up the libs for this project."""
    parser = argparse.ArgumentParser(description=mesg,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('target', nargs='?', default='libs',
            help='dir to put libs in')

    args = parser.parse_args()  # Default parses argv[1:]
    libdir = os.path.realpath(os.curdir + os.sep + args.target)

    if os.path.exists(libdir):
        raise OSError('Directory already exists. {}'.format(libdir))

    os.makedirs(libdir)

    build_gtest(libdir)
    #build_sdl(libdir)
    #build_cunit(libdir)
    #build_boost(libdir)

if __name__ == '__main__':
    main()
