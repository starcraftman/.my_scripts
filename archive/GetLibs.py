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

    if not os.path.exists(os.path.dirname(target)):
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

def build_src(build):
    """ Build a project downloeaded from url. Build is a json described below.
        Cmds are executed in srcdir, then if globs non-empty copy files as
        described in glob/target pairs..
        {
            'name': 'ack',
            'check': 'path/to/check',
            'url' : 'https://github.com/petdance/ack2.git',
            'tdir': /path/to/install/to,
            'cmds': [
                'perl Makefile.PL',
                'make ack-standalone',
                'make manifypods'
            ],
            'globs': [
                ('ack-standalone', 'bin/ack'),
                ('blib/man1/*.1*', 'share/man/man1')
            ]
        }
    """
    srcdir = '%s/src/%s' % (build['tdir'], build['name'])

    # Guard if command exists
    if os.path.exists(build['tdir'] + os.sep + build['check']):
        return

    try:
        get_archive(build['url'], srcdir)
    except ArchiveException:
        get_code(build['url'], srcdir)

    try:
        # Code should be at srcdir by here.
        PDir.push(srcdir)
        for cmd in build.get('cmds', []):
            cmd = cmd.replace('TARGET', build['tdir'])
            cmd = cmd.replace('JOBS', '%d' % NUM_JOBS)
            subprocess.call(cmd.split())
        PDir.pop()

        # Manual copies sometimes required to finish install
        for pattern, target in build.get('globs', []):
            dest = build['tdir'] + os.sep + target
            if dest.endswith('/') and not os.path.exists(dest):
                os.makedirs(dest)

            for sfile in glob.glob(srcdir + os.sep + pattern):
                if os.path.isfile(sfile):
                    shutil.copy(sfile, dest)
    finally:
        shutil.rmtree(srcdir)

    print('Finished building ' + build['name'])

def build_sdl1(libdir):
    """ Build SDL version 1.xx from source and put in tdir. """
    build = {
        'name' : 'SDL',
        'check': 'lib/libSDL.a',
        'url'  : 'http://hg.libsdl.org/SDL',
        'tdir' : libdir,
        'cmds' : [
            'hg update SDL-1.2',
            './autogen.sh',
            './configure --prefix=TARGET',
            'make -jJOBS install',
        ],
    }

    build_src(build)

def build_sdl2(libdir):
    """ Build SDL version 2.xx from source and put in tdir. """
    build = {
        'name' : 'SDL2',
        'check': 'lib/libSDL2.a',
        'url'  : 'http://hg.libsdl.org/SDL',
        'tdir' : libdir,
        'cmds' : [
            './configure --prefix=TARGET',
            'make -jJOBS install',
        ],
    }

    build_src(build)

def build_gtest(libdir):
    """ Build gtest from source and put in libs. """
    build = {
        'name' : 'gtest',
        'check': 'lib/libgtest.a',
        'url'  : URL_GTEST,
        'tdir' : libdir,
        'cmds' : [
            'chmod u+x configure ./scripts/*',
            './configure --prefix=TARGET',
            'make',
        ],
        'globs': [
            ('include/gtest/*', 'include/gtest/'),
            ('include/gtest/internal/*', 'include/gtest/internal/'),
            ('lib/.libs/*.a', 'lib/'),
        ],
    }

    build_src(build)

def build_cunit(libdir):
    """ Build classic cunit, good test lib for c code. """
    build = {
        'name' : 'cunit',
        'check': 'lib/libcunit.a',
        'url'  : 'svn://svn.code.sf.net/p/cunit/code/trunk',
        'tdir' : libdir,
        'cmds' : [
            'sh ./bootstrap TARGET',
            'make -jJOBS install',
        ],
    }

    build_src(build)

def build_boost(libdir):
    """ Build latest boost release for c++. """
    build = {
        'name' : 'boost',
        'check': 'lib/libboost_thread.a',
        'url'  : URL_BOOST,
        'tdir' : libdir,
        'cmds' : [
            './bootstrap.sh --prefix=TARGET',
            './b2 install',
        ],
    }

    # Need this for jam to build mpi & graph_parallel.
    config = os.path.expanduser('~') + os.sep + 'user-config.jam'
    with open(config, 'w') as f_conf:
        f_conf.write('using mpi ;')

    build_src(build)

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

    #build_cunit(libdir)
    build_gtest(libdir)
    #build_boost(libdir)
    #build_sdl1(libdir)
    #build_sdl2(libdir)

if __name__ == '__main__':
    main()
