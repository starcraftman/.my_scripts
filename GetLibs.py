#!/usr/bin/env python
""" Build C libraries for development. """
from __future__ import print_function
from BuildSrc import build_pool
import argparse
import functools
import os
try:
    from argcomplete import autocomplete
except ImportError:
    def autocomplete(dummy):
        """ Dummy func. """
        pass

URL_ARGTBLE = 'http://prdownloads.sourceforge.net/argtable/argtable2-13.tar.gz'
URL_BOOST = 'http://sourceforge.net/projects/boost/files/boost/1.57.0/' \
            'boost_1_57_0.tar.bz2/download'
URL_GTEST = 'https://googletest.googlecode.com/files/gtest-1.7.0.zip'
URL_GNUMP = 'https://ftp.gnu.org/gnu/gmp/gmp-6.0.0a.tar.bz2'

BUILDS = {
    'cppunit': {
        'name': 'cppunit',
        'check': 'lib/libcppunit.a',
        'url': 'git://anongit.freedesktop.org/git/libreoffice/cppunit/',
        'cmds': [
            './autogen.sh',
            './configure --prefix=TARGET',
            'make -jJOBS install',
        ],
    },
    'gtest': {
        'name': 'gtest',
        'check': 'lib/libgtest.a',
        'url': URL_GTEST,
        'cmds': [
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
        'name': 'boost',
        'check': 'lib/libboost_thread.a',
        'url': URL_BOOST,
        'cmds': [
            './bootstrap.sh --prefix=TARGET',
            './b2 install',
        ],
        'globs': [
            ('libs/date_time/data/*', 'share/boost/date_time/'),
        ],
    },
    'gnump': {
        'name': 'gnump',
        'check': 'lib/libgnump.a',
        'url': URL_GNUMP,
        'cmds': [
            './configure --prefix=TARGET',
            'make -jJOBS',
            'make install',
        ],
    },
    'jsoncpp': {
        'name': 'jsoncpp',
        'check': 'lib/libjsoncpp.so',
        'url': 'https://github.com/open-source-parsers/jsoncpp',
        'cmds': [
            'cmake -DCMAKE_INSTALL_PREFIX=TARGET -DCMAKE_BUILD_TYPE=debug '
            '-DJSONCPP_LIB_BUILD_SHARED=ON .',
            'make install',
        ],
    },
    'jsonrpc': {
        'name': 'jsonrpc',
        'check': 'lib/libjsonrpc.so',
        'url': 'https://github.com/cinemast/libjson-rpc-cpp',
        'cmds': [
            'cmake -DCMAKE_INSTALL_PREFIX=TARGET .',
            'make -jJOBS install',
        ],
    },
    'SDL': {
        'name': 'SDL',
        'check': 'lib/libSDL.a',
        'url': 'http://hg.libsdl.org/SDL',
        'cmds': [
            'hg update SDL-1.2',
            './autogen.sh',
            './configure --prefix=TARGET',
            'make -jJOBS install',
        ],
    },
    'SDL2': {
        'name': 'SDL2',
        'check': 'lib/libSDL2.a',
        'url': 'http://hg.libsdl.org/SDL',
        'cmds': [
            './configure --prefix=TARGET',
            'make -jJOBS install',
        ],
    },
    'argtable': {
        'name': 'argtable',
        'check': 'lib/libargtable2.a',
        'url': URL_ARGTBLE,
        'cmds': [
            './configure --prefix=TARGET',
            'make -jJOBS install',
        ],
    },
    'cunit': {
        'name': 'cunit',
        'check': 'lib/libcunit.a',
        'url': 'svn://svn.code.sf.net/p/cunit/code/trunk',
        'cmds': [
            'sh ./bootstrap TARGET',
            'make -jJOBS install',
        ],
    },
    'jansson': {
        'name': 'jansson',
        'check': 'lib/libjansson.so',
        'url': 'https://github.com/akheron/jansson',
        'cmds': [
            'autoreconf -i',
            './configure --prefix=TARGET',
            'make -jJOBS install',
        ],
    },
    'libxml': {
        'name': 'libxml',
        'check': 'lib/libxml2.so',
        'url': 'ftp://xmlsoft.org/libxml2/libxml2-git-snapshot.tar.gz',
        'cmds': [
            './configure --prefix=TARGET',
            'make -jJOBS install',
        ],
    },
}


def main():
    """ Main function. """
    mesg = """This script installs locally c libs.

    choice      desciption

    C++ Libraries
    ------------------------------------------------------
    cppunit     Install the cppunit library.
    gtest       Install the gtest library.
    boost       Install latest boost dev library.
    gnump       Install the GNU multiprecision library.
    jsonrpc     Install jsonrpc-cpp library. Beta lib & build not working atm.
    jsoncpp     Install json parsing library.
    SDL         Install the SDL1.xx game library.
    SDL2        Install the SDL2.xx game library.

    C Libraries
    ------------------------------------------------------
    argtable    Install args parsing library..
    cunit       Install the cunit test library.
    jansson     Install a json parsing library.
    libxml      Install a xml parsing library.
    """
    parser = argparse.ArgumentParser(description=mesg,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('-l', '--ldir', nargs='?', default='./libs',
                        help='library directory to install to')
    parser.add_argument('libs', nargs='+', help='libs selected for install',
                        choices=sorted(BUILDS.keys(), key=str.lower))

    autocomplete(parser)
    args = parser.parse_args()  # Default parses argv[1:]
    ldir = os.path.abspath(args.ldir)

    builds = []
    actions = {}
    for key in BUILDS.keys():
        actions[key] = functools.partial(builds.append, BUILDS[key])

    try:
        # Need this for jam to build mpi & graph_parallel.
        config = os.path.expanduser('~') + os.sep + 'user-config.jam'
        with open(config, 'w') as f_conf:
            f_conf.write('using mpi ;')

        for lib in args.libs:
            actions[lib]()

        # Multiprocess to overlap builds
        build_pool(builds, ldir)
    finally:
        try:
            os.remove(config)
            os.removedirs(ldir + os.path.sep + 'src')
            os.removedirs(ldir)
        except OSError:
            pass

if __name__ == '__main__':
    main()
