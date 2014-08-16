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
import sys
import tarfile
import zipfile
try:
    import apt
except ImportError:
    print('not on debian system, don\'t use option install linux packages')
try:
    from argcomplete import autocomplete
except ImportError:
    def autocomplete(dummy):
        """ Dummy func. """
        pass
# Packages to install follow, broken down into categories.

PROGRAMS = """ \
    htop iotop itop mytop pkg-config aptitude synaptic dos2unix oxygen-molecule \
    kubuntu-restricted-extras kubuntu-restricted-addons \
    brother-cups-wrapper-laser brother-cups-wrapper-laser1 \
    brother-lpr-drivers-laser brother-lpr-drivers-laser1 \
    k3b kid3 krita kolourpaint4 kchmviewer yakuake plasma-widget-quickaccess \
    kdirstat \
    chromium-browser firefox rekonq \
    abiword baobab dvdrip easytag chm2pdf dia catdoc \
    gimp gimp-plugin-registry \
    fuse gparted quicksynergy tree dfc sharutils sharutils-doc \
    libnotify-bin libnotify-dev \
    redshift geoclue geoclue-hostip numlockx \
    samba samba-doc samba-dev samba-dbg wireshark libwireshark-dev wondershaper \
    vlc ffmpeg ffmpeg-doc mplayer mencoder \
    p7zip-full rar zip unzip gzip xz-utils liblzma-dev liblzma5 \
    virtualbox-qt wine \
    ttf-xfree86-nonfree \
    """

KEYRINGS = """ \
    debian-keyring debian-archive-keyring gnome-keyring \
    debian-ports-archive-keyring python-gnomekeyring python-keyring \
    ubuntu-keyring \
    """

PROGRAMMING = """ \
    build-essential debianutils ubuntu-dev-tools mesa-utils \
    automake automake1.9-doc ant ant-doc checkinstall checkbox \
    dkms docbook make-doc lynx kdiff3 kdiff3-doc patch rpm2cpio rpm \
    codeblocks kdevelop qt-sdk \
    colormake colordiff colorgcc jq \
    vim vim-doc vim-gtk vim-rails vim-syntax-go vim-syntax-gtk vim-doc \
    flex flex-doc bison bison-doc graphviz exuberant-ctags \
    bash-doc bash-builtins bashdb zsh zsh-dbg zsh-dev zsh-doc zsh-lovers zshdb \
    clisp clisp-doc clisp-dev clisp-module-gdbm \
    docutils-common docutils-doc \
    erlang erlang-eunit \
    gdc golang golang-doc golang-src golang-codesearch-dev \
    gcc gcc-doc gcc-4.7-source libcunit1 gdb gdb-doc cgdb xxgdb ccache \
    libboost-all-dev libglm-dev libglew-dev libglfw-dev ncurses-doc \
    libncurses5-dev libncursesw5-dev libpcre3-dev zlib1g-dev liblzma-dev libbz2-dev \
    libgnome2-dev libgnomeui-dev libgtk2.0-dev libatk1.0-dev libbonoboui2-dev \
    libcairo2-dev libx11-dev libxpm-dev libxt-dev libgmp3-dev libmpc-dev libmpfr-dev \
    openmpi-bin openmpi-checkpoint openmpi-common \
    gfortran \
    ghc ghc-doc ghc-haddock ghc-prof haskell-debian-utils \
    haskell-devscripts haskell-doc cabal-install \
    junit junit-doc maven openjdk-7-doc openjdk-7-jdk openjdk-7-dbg \
    openjdk-7-source openjdk-7-demo icedtea-7-plugin \
    lua5.2 lua5.2-doc luadoc liblua5.2-dev \
    nodejs nodejs-dev nodejs-legacy npm \
    perl perl-doc libperl-dev perl-modules libpadwalker-perl libfile-next-perl \
    php5 php5-mysql phpunit php5-dev \
    swi-prolog swi-prolog-doc \
    python python-dev python-doc python-pip \
    python3 python3-dev python3-doc python3-pip jython jython-doc \
    pychecker pylint pep8 python-autopep8 ruby-full shunit2 \
    tcl-dev tcl-doc \
    tex-common texlive-latex-base texlive-font-utils \
    bzr bzr-builddeb bzr-doc python-bzrlib bzrtools git git-gui git-doc \
    mercurial subversion cvs \
    """

BABUN = """ \
    clisp lua perl python python3 ruby make cmake colordiff colorgcc \
    p7zip unzip zip gzip ncurses pcre mercurial bzr subversion \
    libboost-devel libboost_python-devel cppunit
    """

CABAL = "buildwrapper scion-browser hoogle terminfo happy hlint"

PY_PACKS = "argcomplete Pygments pytest trash-cli"

URL_PYTHON = 'https://www.python.org/ftp/python/2.7.8/Python-2.7.8.tgz'
URL_ZSH = 'http://sourceforge.net/projects/zsh/files/zsh/5.0.5/\
zsh-5.0.5.tar.bz2/download'

if os.name == 'posix':
    NUM_JOBS = int(subprocess.check_output('cat /proc/cpuinfo | \
        grep processor | wc -l', shell=True))
else:
    NUM_JOBS = 2

# Classes

class NotSudo(Exception):
    """ Throw this if we aren't sudo but need to be. """
    pass

class ArchiveNotSupported(Exception):
    """ Archive can't be processed. """
    pass

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

def get_archive(url, target):
    """ Fetch an archive from a site. Works on regular ftp & sourceforge.
    url: location to get archive
    target: where to extract to
    """
    arc_ext = None
    for ext in ['.tgz', '.tbz2', '.tar.bz2', '.tar.gz', 'tar.xz',
            '.xz', '.rar', '.zip', '.7z']:
        right = url.rfind(ext)
        if right != -1:
            right += len(ext)
            left = url.rfind(os.sep, 0, right) + 1
            arc_ext = ext
            break

    if arc_ext == None:
        raise ArchiveNotSupported

    # download and extract archive
    arc_name = url[left:right]
    cmd = 'wget -O %s %s' % (arc_name, url)
    subprocess.call(cmd.split())

    if arc_ext in ['.tgz', '.tbz2', '.tar.bz2', '.tar.gz']:
        with tarfile.open(arc_name) as tarf:
            tarf.extractall()
    elif arc_ext == '.zip':
        with zipfile.ZipFile(arc_name) as zipf:
            zipf.extractall()
    else:
        cmd = 'unarchive ' + arc_name
        subprocess.call(cmd.split())

    # extracted dir doesn't always match arc_name, glob to be sure
    arc_front = re.split('[-_]', arc_name)[0] + '*'
    extracted = None
    for name in glob.glob(arc_front):
        if name.rfind(arc_ext) == -1:
            extracted = name

    if not os.path.exists(os.path.dirname(target)):
        os.makedirs(target)
        os.rmdir(target)
    os.rename(extracted, target)
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

def make_cmd(src, dst):
    """ Generator for helper. """
    def cmd_when_dst_empty(files, command, opts=None):
        """ Execute a command if destination empty. """
        if opts == None:
            opts = []
        for fil in files:
            sfile = src + fil
            dfile = dst + fil
            if not os.path.exists(dfile):
                print("{} >>>>> {}".format(dfile, sfile))
                command(sfile, dfile, *opts)
    return cmd_when_dst_empty

def home_config():
    """ Setup the dev environment, stuff goes in the user's home folder. """
    script_path = os.path.relpath(__file__)
    script_dir = os.path.dirname(script_path)
    if script_dir == '':
        script_dir = '.'

    # Leaving trailing sep for ease later.
    src = script_dir + os.sep + 'dot_files' + os.sep
    home = os.path.expanduser('~') + os.sep

    # Helper function
    helper = make_cmd(src, home)

    # Glob all files in dot_files and link them to home
    files = glob.glob(src + '.*')
    files = [x[x.rindex(os.sep)+1:] for x in files]
    helper(files, os.symlink)

    # Init vundle for vim plugin install.
    ddir = home + '.vim' + os.sep + 'bundle' + os.sep
    get_code('https://github.com/gmarik/Vundle.vim.git', ddir + 'Vundle.vim')

    # Get shell utilities
    shell_dir = home + '.shell' + os.sep
    get_code('http://bitbucket.org/sjl/hg-prompt/', shell_dir + '.hg-prompt')

    git_urls = [
        'https://github.com/magicmonty/bash-git-prompt.git',
        'https://github.com/starcraftman/zsh-git-prompt.git',
        '--branch ag_add_completions https://github.com/starcraftman/zsh-completions.git',
        'https://github.com/zsh-users/zsh-syntax-highlighting.git',
        'https://github.com/starcraftman/hhighlighter.git',
    ]

    for url in git_urls:
        target = '.' + url[url.rindex('/')+1:url.rindex('.git')]
        get_code(url, shell_dir + target)

    # Setup powerline fonts if not done.
    ddir = home + '.fonts'
    dpow = ddir + os.sep + 'powerline-fonts'
    if not os.path.exists(ddir):
        os.mkdir(ddir)
        get_code('https://github.com/Lokaltog/powerline-fonts', dpow)
        cmd = 'fc-cache -vf ' + ddir
        subprocess.call(cmd.split())

    # Create dir for ccache
    ddir = home + '.ccache'
    if not os.path.exists(ddir):
        os.mkdir(ddir)

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
    except ArchiveNotSupported:
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

def build_python():
    """ Build python from source. """
    build = {
        'name' : 'python',
        'check': 'bin/python',
        'url'  : URL_PYTHON,
        'tdir' : os.environ['OPTDIR'],
        'cmds' : [
            './configure --prefix=TARGET',
            'make',
            'make install',
        ],
    }

    build_src(build)

def build_vim():
    """ Build vim if very old. """
    build = {
        'name' : 'vim',
        'check': 'bin/vim',
        'url'  : 'https://code.google.com/p/vim/',
        'tdir' : os.environ['OPTDIR'],
        'cmds' : [
            './configure --with-features=huge --enable-gui=gtk2 \
            --enable-cscope --enable-multibyte --enable-luainterp \
            --enable-perlinterp --enable-pythoninterp \
            --with-python-config-dir=/usr/lib/python2.7/config \
            --enable-rubyinterp --enable-tclinterp --prefix=TARGET',
            'make VIMRUNTIMEDIR=TARGET/share/vim/vim74',
            'make install',
        ],
    }

    build_src(build)

def build_zsh():
    """ Build zsh from source. """
    build = {
        'name' : 'zsh',
        'check': 'bin/zsh',
        'url'  : 'https://github.com/zsh-users/zsh.git',
        'tdir' : os.environ['OPTDIR'],
        'cmds' : [
            './Util/preconfig',
            'autoconf',
            './configure --prefix=TARGET',
            'make',
            'make install',
        ],
    }

    build_src(build)

def src_programs():
    """ Download sources and install to enironment OPT directory. """
    # Store all compilations into opt from environment
    optdir = os.environ['OPTDIR']
    home = os.path.expanduser('~') + os.sep

    # Only use on posix systems.
    if not os.name == 'posix' or os.path.exists(home + '.babunrc'):
        print("This command only for unix.")
        return

    builds = \
    [
        {
            'name' : 'ack',
            'check': 'bin/ack',
            'url'  : 'https://github.com/petdance/ack2.git',
            'tdir' : optdir,
            'cmds' : [
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
        {
            'name' : 'ag',
            'check': 'bin/ag',
            'url'  : 'https://github.com/ggreer/the_silver_searcher.git',
            'tdir' : optdir,
            'cmds' : [
                './build.sh --prefix=TARGET',
                'make install',
            ],
        },
        {
            'name' : 'doxygen',
            'check': 'bin/doxygen',
            'url'  : 'https://github.com/doxygen/doxygen.git',
            'tdir' : optdir,
            'cmds' : [
                './configure --prefix=TARGET',
                'make -jJOBS',
            ],
            'globs': [
                ('bin/doxygen', 'bin/'),
                ('doc/*.1', 'share/man/man1/'),
            ],
        },
        {
            'name' : 'parallel',
            'check': 'bin/parallel',
            'url'  : 'http://ftp.gnu.org/gnu/parallel/parallel-latest.tar.bz2',
            'tdir' : optdir,
            'cmds' : [
                './configure --prefix=TARGET',
                'make -jJOBS install',
            ],
        },
        {
            'name' : 'vimpager',
            'check': 'bin/vimpager',
            'url'  : 'https://github.com/rkitover/vimpager.git',
            'tdir' : optdir,
            'globs': [
                ('vimcat', 'bin/'),
                ('vimpager', 'bin/'),
                ('*.1', 'share/man/man1/'),
            ],
        },
        {
            'name' : 'zsh_docs',
            'check': 'share/man/man1/zshall.1',
            'url'  : URL_ZSH,
            'tdir' : optdir,
            'globs': [
                ('Doc/*.1', 'share/man/man1/'),
            ],
        },
    ]

    # build the programs based on above json
    for build in builds:
        build_src(build)

def packs_babun():
    """ Setup a fresh babun install. """
    # Install packages
    cmd = 'pact install ' + BABUN
    subprocess.call(cmd.split())

    # Now prepare then invoke regular setup link common files
    home = os.path.expanduser('~') + os.sep

    # Prevent fonts from running with home_config
    ddir = home + '.fonts'
    if not os.path.exists(ddir):
        os.mkdir(ddir)

    # Backup defaults and allow for new ones
    for name in ['.gitconfig', '.vim']:
        dfile = home + name
        dfile_bak = dfile + '_bak'
        if os.path.exists(dfile) and not os.path.exists(dfile_bak):
            os.rename(dfile, dfile_bak)

    home_config()

def packs_cabal():
    """ Installs haskell packages for Eclipse Haskell plugin. """
    cmd = 'cabal update'
    subprocess.call(cmd.split())

    cmd = 'cabal install ' + CABAL
    subprocess.call(cmd.split())

def packs_debian():
    """ Install packages on the current system. """
    if os.getuid() != 0:
        raise NotSudo

    packages = (PROGRAMS + PROGRAMMING + KEYRINGS).split()

    cache = apt.Cache()
    print("One moment while we update cache.")
    cache.update()
    cache.open(None)
    print("Update done.")

    cmd = 'sudo apt-get install'.split()
    for pack in packages:
        try:
            package = cache[pack]
            if not package.is_installed:
                cmd.append(pack)
        except KeyError:
            print("Package couldn't be selected: %s" % pack)

    print("Please wait, running: " + " ".join(cmd))
    subprocess.call(cmd)

def packs_py():
    """ Installs python packages using pip. """
    if os.getuid() != 0:
        raise NotSudo

    # Use python package manager.
    cmd = 'sudo pip install ' + PY_PACKS
    subprocess.call(cmd.split())

    # Install python completion to system bash_completion.d.
    cmd = 'activate-global-python-argcomplete --user'
    subprocess.call(cmd.split())

def install_jshint():
    """ Setup jshint for progrmaming javascript with vim. """
    cmd = 'npm install jshint -g'
    subprocess.call(cmd.split())

def install_pipelight():
    """ Silverlight plugin for firefox/chrome on linux.
    http://www.webupd8.org/2013/08/pipelight-use-silverlight-in-your-linux.html
    """
    if os.getuid() != 0:
        raise NotSudo

    cmds = [
        'sudo apt-get remove flashplugin-installer',
        'sudo apt-add-repository ppa:pipelight/stable',
        'sudo apt-get update',
        'sudo apt-get install pipelight-multi',
        'pipelight-plugin --enable silverlight',
        'pipelight-plugin --enable flash',
    ]
    cmds = [x.split() for x in cmds]
    for cmd in cmds:
        subprocess.call(cmd)
    print("Installation over, remember to use a useragent switcher.")

def main():
    """ Main function. """
    mesg = """This script sets up a dev environment.

    choice      effect
    ------------------------------------------------------
    home        Setup home config files.
    debian      Install debian packages.
    babun       Install babun packages.
    pip         Install python libraries via pip.
    cabal       Install haskell packages for eclipse.
    jshint      Install jshint via npm for javascript vim.
    pipelight   Install pipelight flash & silverlight.
    src         Build standard dev progs like ag, ack, parallel.
    python      Build latest python from source.
    vim         Build latest vim from source..
    zsh         Build latest zsh from source.
    """
    # Use a dict of funcs instead of a case switch
    actions = {
        'home':         home_config,
        'debian':       packs_debian,
        'babun':        packs_babun,
        'pip':          packs_py,
        'cabal':        packs_cabal,
        'jshint':       install_jshint,
        'pipelight':    install_pipelight,
        'src':          src_programs,
        'python':       build_python,
        'vim':          build_vim,
        'zsh':          build_zsh,
    }

    parser = argparse.ArgumentParser(description=mesg,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('choice', nargs='+', action='append', help='the stages',
            choices=actions.keys())

    autocomplete(parser)
    args = parser.parse_args()  # Default parses argv[1:]
    choices = args.choice[0]

    try:
        [actions[x]() for x in choices]
    except IOError as exc:
        print('Failed to install: {}'.format(exc))
    except NotSudo:
        print("Rerun this part of script with sudo.")

if __name__ == '__main__':
    main()
