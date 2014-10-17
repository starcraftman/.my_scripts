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
import functools
import itertools
import multiprocessing
import os
import SysInstall
try:
    from argcomplete import autocomplete
except ImportError:
    def autocomplete(dummy):
        """ Dummy func. """
        pass

URL_BOOST = 'http://sourceforge.net/projects/boost/files/boost/1.56.0/\
boost_1_56_0.tar.bz2/download'
URL_GTEST = 'https://googletest.googlecode.com/files/gtest-1.7.0.zip'

BUILDS = {
    'cppunit': {
        'name' : 'cppunit',
        'check': 'lib/libcppunit.a',
        'url'  : 'git://anongit.freedesktop.org/git/libreoffice/cppunit/',
        'cmds' : [
            './autogen.sh',
            './configure --prefix=TARGET',
            'make -jJOBS install',
        ],
    },
    'cunit': {
        'name' : 'cunit',
        'check': 'lib/libcunit.a',
        'url'  : 'svn://svn.code.sf.net/p/cunit/code/trunk',
        'cmds' : [
            'sh ./bootstrap TARGET',
            'make -jJOBS install',
        ],
    },
    'gtest': {
        'name' : 'gtest',
        'check': 'lib/libgtest.a',
        'url'  : URL_GTEST,
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
    },
    'boost': {
        'name' : 'boost',
        'check': 'lib/libboost_thread.a',
        'url'  : URL_BOOST,
        'cmds' : [
            './bootstrap.sh --prefix=TARGET',
            './b2 install',
        ],
        'globs': [
            ('libs/date_time/data/*', 'share/boost/date_time/'),
        ],
    },
    'jsonrpc': {
        'name' : 'jsonrpc',
        'check': 'lib/libjsonrpc.so',
        'url'  : 'https://github.com/cinemast/libjson-rpc-cpp',
        'cmds' : [
            'cmake -DCMAKE_INSTALL_PREFIX=TARGET ..'
            'make -jJOBS'
            'make install',
        ],
    },
    'SDL': {
        'name' : 'SDL',
        'check': 'lib/libSDL.a',
        'url'  : 'http://hg.libsdl.org/SDL',
        'cmds' : [
            'hg update SDL-1.2',
            './autogen.sh',
            './configure --prefix=TARGET',
            'make -jJOBS install',
        ],
    },
    'SDL2': {
        'name' : 'SDL2',
        'check': 'lib/libSDL2.a',
        'url'  : 'http://hg.libsdl.org/SDL',
        'cmds' : [
            './configure --prefix=TARGET',
            'make -jJOBS install',
        ],
    },
}

# Classes

# Functions

def main():
    """ Main function. """
    mesg = """This script installs locally c libs.

    choice      effect
    ------------------------------------------------------
    cunit       Install the cunit library.
    cppunit     Install the cppunit library.
    gtest       Install the gtest library.
    boost       Install latest boost dev library.
    jsonrpc     Install jsonrpc-cpp library.
    SDL         Install the SDL1.xx game library.
    SDL2        Install the SDL2.xx game library.
    """
    parser = argparse.ArgumentParser(description=mesg,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-l', '--ldir', nargs='?', default='./libs',
            help='library directory to install to')
    parser.add_argument('libs', nargs='+', help='libs selected for install',
            choices=BUILDS.keys())

    autocomplete(parser)
    args = parser.parse_args()  # Default parses argv[1:]
    ldir = os.path.abspath(args.ldir)

    builds = []
    actions = {key: functools.partial(builds.append, key)
        for key in BUILDS.keys()}

    try:
        # Need this for jam to build mpi & graph_parallel.
        config = os.path.expanduser('~') + os.sep + 'user-config.jam'
        with open(config, 'w') as f_conf:
            f_conf.write('using mpi ;')

        for lib in args.libs:
            actions[lib]()

        # Multiprocess to overlap builds
        pool_args = itertools.izip([BUILDS[name] for name in builds],
                itertools.repeat(ldir))
        pool = multiprocessing.Pool()
        pool.map_async(SysInstall.build_wrap, pool_args)
        pool.close()
        pool.join()
    finally:
        os.remove(config)

if __name__ == '__main__':
    main()
