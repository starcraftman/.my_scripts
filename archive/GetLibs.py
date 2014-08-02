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
import shutil
import subprocess
import sys
import tarfile
import urllib
import zipfile

# Classes

class Progress(object):
    """ Draw a simple progress bar. """
    def __init__(self, tick, empty, total_ticks):
        self.tick = tick
        self.empty = empty
        self.total_ticks = total_ticks
        self.num_ticks = 0
        self.old_percent = 0
    def check_percent(self, new_percent):
        """ Helper, check if passed a point. """
        if new_percent >= self.old_percent + self.tick_threshold():
            self.old_percent = new_percent
            return True
        else:
            return False
    def draw(self):
        """ Draw a bar for progress after incrementing. """
        self.num_ticks += 1
        num_empty = self.total_ticks - self.num_ticks
        line = "Download Progress: [%s%s]\n" % (self.tick * self.num_ticks,
            self.empty * num_empty)
        sys.stdout.write(line)
        sys.stdout.flush()
    def tick_threshold(self):
        """ Return number of % per tick on bar. """
        return 100 / self.total_ticks
    @staticmethod
    def default_prog():
        """ Factory method, makes a bar with defaults. """
        return Progress('*', '-', 20)

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
                progress.draw()
    return report_down

def get_code(command, target):
    """ Wrapper function to clone repos.
    Protects against overwriting if target exists.
    command: The command that would run in bash.
    target: Where to clone to.
    """
    cmd = command.split()
    cmd.append(target)
    if not os.path.exists(target):
        subprocess.call(cmd)

def num_jobs():
    """ Use BASH one liner to determine number of threads available. """
    jobs = subprocess.check_output('cat /proc/cpuinfo | grep "processor"\
            | wc -l', shell=True)
    return int(jobs)

def build_sdl(libdir):
    """ Build ack from source, move to target dir. """
    srcdir, srcdir2 = 'sdl', 'sdl2'
    jobs = num_jobs()
    cmds_sdl1 = ['./autogen.sh',
            './configure --prefix=%s' % libdir,
            'make -j%d install' % jobs
            ]
    cmds_sdl2 = ['hg update default',
            './configure --prefix=%s' % libdir,
            'make -j%d install' % jobs
            ]
    build = {srcdir: cmds_sdl1,
            srcdir2: cmds_sdl2
            }

    try:
        # Fetch code & copy for 2
        get_code('hg clone -u SDL-1.2 http://hg.libsdl.org/SDL', srcdir)
        cmd = ('cp -r %s %s' % (srcdir, srcdir)).split()
        subprocess.call(cmd)

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
    archive = 'gtest.zip'
    url = 'https://googletest.googlecode.com/files/gtest-1.7.0.zip'

    try:
        # Fetch program
        print("Downloading gtest source.")
        prog = Progress.default_prog()
        zfile = urllib.URLopener()
        zfile.retrieve(url, archive, gen_report(prog))
        zipfile.ZipFile(archive).extractall()
        srcdir = glob.glob('gtest-*')[0]

        # Build & clean
        PDir.push(srcdir)
        cmd = 'chmod u+x configure ./scripts/*'.split()
        subprocess.call(cmd)
        cmd = './configure --prefix={}'.format(libdir).split()
        subprocess.call(cmd)
        subprocess.call('make')

        # Copy out file structure
        os.mkdir(libdir + os.sep + 'lib')
        shutil.copytree('include', libdir + os.sep + 'include')
        for fil in glob.glob('lib' + os.sep + '.libs' + os.sep + '*.a'):
            shutil.copy(fil, libdir + os.sep + 'lib')
    finally:
        PDir.pop()
        os.remove(archive)
        shutil.rmtree(srcdir)

def build_cunit(libdir):
    """ Build classic cunit, good test lib for c code. """
    srcdir = 'cunit'
    get_code('svn checkout svn://svn.code.sf.net/p/cunit/code/trunk', srcdir)

    # Build & clean
    PDir.push(srcdir)
    # Shell true is due to some bug via normal way
    subprocess.call('./bootstrap {}'.format(libdir), shell=True)
    cmd = 'make -j{} install'.format(num_jobs()).split()
    subprocess.call(cmd)
    PDir.pop()

    shutil.rmtree(srcdir)

def build_boost(libdir):
    """ Build latest boost release for c++. """
    url = 'http://sourceforge.net/projects/boost/files/boost/1.55.0/boost_1_55_0.tar.bz2/download'
    archive = 'download'
    config = os.path.expanduser('~') + os.sep + 'user-config.jam'

    try:
        # Fetch program
        print("Downloading latest zsh source.")
        cmd = ('wget %s' % url).split()
        subprocess.call(cmd)
        tarfile.open(archive).extractall()
        srcdir = glob.glob('boost_*')[0]

        # Need this for jam to build mpi & graph_parallel.
        f_conf = open(config, 'w')
        f_conf.write('using mpi ;')
        f_conf.close()

        PDir.push(srcdir)
        cmd = ('./bootstrap.sh --prefix=%s' % libdir).split()
        subprocess.call(cmd)
        cmd = './b2 install'.split()
        subprocess.call(cmd)
    finally:
        PDir.pop()
        shutil.rmtree(srcdir)
        os.remove(config)
        os.remove(archive)

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
