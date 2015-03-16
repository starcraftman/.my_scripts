#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
""" Build any program I want from source code, deploy locally.
    Depends on wget -- archive downloads, blame SourceForge  --
    and standard c++ build tools.
"""
from __future__ import print_function
import argparse
import functools
import glob
import itertools
import multiprocessing
import os
import re
import shlex
import shutil
import subprocess
import tarfile
import zipfile
try:
    from argcomplete import autocomplete
except ImportError:
    def autocomplete(dummy):
        """ Dummy func. """
        pass


class WorkerInterrupted(Exception):
    """ Workers handle Exception's easier than intterupts. """
    pass

URL_CMAKE = 'http://www.cmake.org/files/v3.1/cmake-3.1.3.tar.gz'
URL_GIT = 'https://www.kernel.org/pub/software/scm/git/git-2.3.1.tar.xz'
URL_PYTHON = 'https://www.python.org/ftp/python/2.7.9/Python-2.7.9.tgz'
URL_PYTHON3 = 'https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tar.xz'
URL_TMUX = 'http://sourceforge.net/projects/tmux/files/tmux/tmux-1.9/' \
            'tmux-1.9a.tar.gz/download?use_mirror=hivelocity'
URL_ZSH = 'http://sourceforge.net/projects/zsh/files/zsh/5.0.7/' \
            'zsh-5.0.7.tar.bz2/download'

TMP_DIR = '/tmp/BuildSrc'
BUILDS = {
    'ack': {
        'name': 'ack',
        'check': 'bin/ack',
        'url': 'https://github.com/petdance/ack2.git',
        'cmds': [
            'perl Makefile.PL',
            'make ack-standalone',
            'make manifypods',
        ],
        'globs': [
            ('ack-standalone', 'bin/'),
            ('ack-standalone', 'bin/ack'),
            ('blib/man1/*.1*', 'share/man/man1/'),
        ],
    },
    'ag': {
        'name': 'ag',
        'check': 'bin/ag',
        'url': 'https://github.com/ggreer/the_silver_searcher.git',
        'cmds': [
            './build.sh --prefix=TARGET',
            'make install',
        ],
    },
    'atom': {
        'name': 'atom',
        'check': 'bin/atom',
        'url': 'https://github.com/atom/atom',
        'cmds': [
            'script/build',
            'script/grunt install --install-dir TARGET',
        ],
    },
    'cmake': {
        'name': 'cmake',
        'check': 'bin/cmake',
        'url': URL_CMAKE,
        'cmds': [
            './bootstrap --prefix=TARGET --docdir=share/doc/cmake-3.0 '
            '--mandir=share/man --system-libs --enable-ccache --qt-gui '
            '--sphinx-man --sphinx-html',
            'make -jJOBS install',
        ],
    },
    'ctags': {
        'name': 'ctags',
        'check': 'bin/ctags',
        'url': 'https://github.com/fishman/ctags.git',
        'cmds': [
            'autoreconf -fiv',
            './configure --prefix=TARGET',
            'make install',
        ],
    },
    'doxygen': {
        'name': 'doxygen',
        'check': 'bin/doxygen',
        'url': 'https://github.com/doxygen/doxygen.git',
        'cmds': [
            './configure --prefix=TARGET',
            'make',
        ],
        'globs': [
            ('bin/doxygen', 'bin/'),
            ('doc/*.1', 'share/man/man1/'),
        ],
    },
    'git': {
        'name': 'git',
        'check': 'bin/git',
        'url': URL_GIT,
        'cmds': [
            'make configure',
            './configure --prefix=TARGET',
            'make -jJOBS',
            'make install',
        ],
    },
    'neovim': {
        'name': 'neovim',
        'check': 'bin/nvim',
        'url': 'https://github.com/neovim/neovim',
        'cmds': [
            'make CMAKE_EXTRA_FLAGS="-DCMAKE_INSTALL_PREFIX:PATH=TARGET" '
            'install',
        ],
    },
    'parallel': {
        'name': 'parallel',
        'check': 'bin/parallel',
        'url': 'http://ftp.gnu.org/gnu/parallel/parallel-latest.tar.bz2',
        'cmds': [
            './configure --prefix=TARGET',
            'make -jJOBS install',
        ],
    },
    'python': {
        'name': 'python',
        'check': 'bin/python',
        'url': URL_PYTHON,
        'cmds': [
            './configure --prefix=TARGET',
            'make -jJOBS install',
        ],
    },
    'python3': {
        'name': 'python3',
        'check': 'bin/python3',
        'url': URL_PYTHON3,
        'cmds': [
            './configure --prefix=TARGET',
            'make -jJOBS install',
        ],
    },
    'tmux': {
        'name': 'tmux',
        'check': 'bin/tmux',
        'url': URL_TMUX,
        'cmds': [
            './configure --prefix=TARGET',
            'make install',
        ],
    },
    'vim': {
        'name': 'vim',
        'check': 'bin/vim',
        'url': 'https://code.google.com/p/vim/',
        'cmds': [
            './configure --with-features=huge --enable-gui=gtk2 '
            '--enable-cscope --enable-multibyte --enable-luainterp '
            '--enable-rubyinterp --enable-pythoninterp --prefix=TARGET',
            'make VIMRUNTIMEDIR=TARGET/share/vim/vim74',
            'make -jJOBS install',
        ],
    },
    'vimpager': {
        'name': 'vimpager',
        'check': 'bin/vimpager',
        'url': 'https://github.com/rkitover/vimpager.git',
        'globs': [
            ('vimcat', 'bin/'),
            ('vimpager', 'bin/'),
            ('*.1', 'share/man/man1/'),
        ],
    },
    'zsh': {
        'name': 'zsh',
        'check': 'bin/zsh',
        'url': 'https://github.com/zsh-users/zsh.git',
        'cmds': [
            './Util/preconfig',
            'autoconf',
            './configure --prefix=TARGET --enable-cap --enable-pcre '
            '--enable-maildir-support',
            'make -jJOBS install',
        ],
    },
    'zsh_docs': {
        'name': 'zsh_docs',
        'check': 'share/man/man1/zshall.1',
        'url': URL_ZSH,
        'globs': [
            ('Doc/*.1', 'share/man/man1/'),
        ],
    },
}


class ArchiveNotSupported(Exception):
    """ Archive can't be processed. """
    pass


class PDir(object):
    """ Pushd analog for personal use. """
    dirs = []

    @staticmethod
    def push(new_dir):
        """ Push curdir to stack and change to new_dir. """
        curdir = os.path.abspath(os.curdir)
        PDir.dirs.append(curdir)
        os.chdir(new_dir)
        print("%s >>> %s" % (curdir, new_dir))

    @staticmethod
    def pop():
        """ Pop the dirstack and return to it. """
        old_dir = PDir.dirs.pop()
        os.chdir(old_dir)
        print(">>> %s" % old_dir)


def find_archive(url):
    """ Given a url, returns archive name found inside.
    If extension not supported throws excetion. """
    arc_ext = None
    for ext in ['.tgz', '.tbz2', '.tar.bz2', '.tar.gz', 'tar.xz',
                '.xz', '.rar', '.zip', '.7z']:
        right = url.rfind(ext)
        if right != -1:
            right += len(ext)
            left = url.rfind(os.sep, 0, right) + 1
            arc_ext = ext
            break

    if arc_ext is None:
        raise ArchiveNotSupported

    return url[left:right]


def extract_archive(archive):
    """ Given an archive, extract it. Prefer python libs if supported. """
    if tarfile.is_tarfile(archive):
        tarf = tarfile.open(archive)
        tarf.extractall()
    elif zipfile.is_zipfile(archive):
        zipf = zipfile.ZipFile(archive)
        zipf.extractall()
    else:
        # Fall back to shell tools to extract
        unarc_src = 'https://raw.githubusercontent.com/starcraftman/' \
                    '.my_scripts/master/unarchive'
        cmds = ['curl -o una ' + unarc_src, 'bash ./una ' + archive]
        for cmd in cmds:
            proc = subprocess.Popen(shlex.split(cmd))
            proc.wait()
            if proc.returncode != 0:
                raise OSError('Some shell util like curl unavailable.')
        os.remove('una')


def get_archive(url, target):
    """ Fetch an archive from a site. Works on regular ftp & sourceforge.
    Wish sourceforge wasn't a pain...

    url: location to get archive
    target: where to extract to
    """
    arc_name = find_archive(url)

    tmp_file = TMP_DIR + os.path.sep + arc_name
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)

    if not os.path.exists(target):
        os.makedirs(target)
        os.rmdir(target)

    try:
        # Using wget because of sourceforge corner case
        cmd = 'wget -O %s %s' % (tmp_file, url)
        subprocess.call(shlex.split(cmd))

        extract_archive(tmp_file)

        # Infer target dir by chopping off target right most folder
        target_r_index = target.rfind(os.path.sep, 0, len(target) - 2)
        target_dir = target[0:target_r_index]

        # extracted dir doesn't always match arc_name, glob to be sure
        arc_front = re.split('[-_]', arc_name)[0] + '*'
        extracted = None
        for name in glob.glob(arc_front):
            if name not in [arc_name, target_dir]:
                extracted = name

        os.rename(extracted, target)
    finally:
        if os.path.exists(tmp_file):
            os.remove(tmp_file)
        if os.path.exists(extracted):
            shutil.rmtree(extracted)


def get_code(url, target):
    """ Wrapper function to clone repos, only executes if target doesn't exist
    url: The origin to clone
    target: Where to clone to
    """
    cmd = ' %s %s' % (url, target)
    retry = None
    # Git urls always end in .git
    if url.find('git') != -1:
        cmd = 'git clone --recursive --depth 1' + cmd
        retry = lambda: subprocess.call(shlex.split(
            cmd.replace('git', '/usr/bin/git', 1)))
    # svn always at front of proto
    elif url.find('svn') != -1:
        cmd = 'svn checkout' + cmd
    else:
        cmd = 'hg clone' + cmd

    if not os.path.exists(target):
        ret = subprocess.call(shlex.split(cmd))
        if retry and ret != 0:
            retry()



def build_src(build, target=None):
    """ Build a project downloeaded from url. build is a json object.
        The format is described below.
        Cmds are executed in srcdir, then if globs non-empty copy files as
        described in glob/target pairs.
        Required names prefixed with R.
        {
          R 'name': 'ack',
          R 'check': 'path/to/check',
          R 'url': 'https://github.com/petdance/ack2.git',
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
    tdir = os.path.abspath(build.get('tdir', target))
    srcdir = '%s/src/%s' % (tdir, build['name'])

    # Guard if command exists
    if os.path.exists(tdir + os.sep + build['check']):
        return

    try:
        get_archive(build['url'], srcdir)
    except ArchiveNotSupported:
        get_code(build['url'], srcdir)

    try:
        # Code should be at srcdir by here.
        PDir.push(srcdir)
        for cmd in build.get('cmds', []):
            cmd = cmd.replace('TARGET', tdir)
            cmd = cmd.replace('JOBS', '%d' % multiprocessing.cpu_count())
            subprocess.call(shlex.split(cmd))
        PDir.pop()

        # Manual copies sometimes required to finish install
        for pattern, target in build.get('globs', []):
            dest = tdir + os.sep + target
            if dest.endswith('/') and not os.path.exists(dest):
                os.makedirs(dest)

            for sfile in glob.glob(srcdir + os.sep + pattern):
                if os.path.isfile(sfile):
                    shutil.copy(sfile, dest)
    finally:
        shutil.rmtree(srcdir)


def build_wrap(args):
    """ Wrapper for build_src in process pool.
        Pool doesn't handle interrupt well, throw a different one. """
    try:
        build_src(*args)
    except KeyboardInterrupt:
        raise WorkerInterrupted


def build_pool(builds, target):
    """ Take a series of build objects and use a pool of workers
        to build them and install to target.
        NB: Blocks until all workers finished.
    """
    pool_args = itertools.izip(builds, itertools.repeat(target))
    pool = multiprocessing.Pool()
    try:
        pool.map(build_wrap, pool_args, 1)
        pool.close()
    except IOError as exc:
        print('Failed to install: {}'.format(exc))
        pool.terminate()
    except (KeyboardInterrupt, Exception) as exc:
        pool.terminate()
    finally:
        pool.join()


def main():
    """ Main function. """
    mesg = """Build some tools from source to get latest.

    choice       effect
    ------------------------------------------------------
    atom         Build the latest atom editor.
    cmake        Build the latest cmake.
    ctags        Build the latest exhuberant ctags github fork.
    dev          Build ack, ag, parallel, vimpager & zsh_docs.
    doxygen      Build the latest doxygen.
    git          Build the latest git release.
    neovim       Build neovim from source (still alpha).
    python       Build the latest python 2.x.
    python3      Build the latest python 3.x.
    tmux         Build the latest tmux.
    vim          Build the latest vim.
    zsh          Build the latest zsh.
    """

    # Simple wrapper saves func
    odir = os.path.expanduser('~/.opt1')
    builds = []

    # Use a dict of funcs to process args
    dev_keys = (BUILDS['ack'], BUILDS['ag'], BUILDS['parallel'],
                BUILDS['vimpager'], BUILDS['zsh_docs'])
    actions = {
        'dev':  functools.partial(builds.extend, dev_keys),
    }
    for key in BUILDS.keys():
        if key not in dev_keys:
            actions[key] = functools.partial(builds.append, BUILDS[key])

    parser = argparse.ArgumentParser(description=mesg,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('-o', '--odir', nargs='?', default=None,
                        help='install dir')
    parser.add_argument('keys', nargs='+', help='progs to build',
                        choices=sorted(actions.keys()))

    autocomplete(parser)
    args = parser.parse_args()  # Default parses argv[1:]

    # Nicer override than OPTDIR
    if args.odir is not None:
        odir = args.odir

    try:
        for key in args.keys:
            actions[key]()

        # build the components in parallel
        build_pool(builds, odir)
    finally:
        try:
            os.removedirs(odir + os.path.sep + 'src')
            os.removedirs(odir)
        except OSError:
            pass

if __name__ == '__main__':
    main()
