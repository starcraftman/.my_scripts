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
    htop pkg-config aptitude synaptic dos2unix oxygen-molecule \
    kubuntu-restricted-extras kubuntu-restricted-addons \
    brother-cups-wrapper-laser brother-cups-wrapper-laser1 \
    brother-lpr-drivers-laser brother-lpr-drivers-laser1 \
    k3b kid3 krita kolourpaint4 kchmviewer yakuake plasma-widget-quickaccess \
    kdirstat \
    chromium-browser firefox rekonq \
    abiword baobab dvdrip easytag chm2pdf dia catdoc \
    gimp gimp-plugin-registry \
    fuse gparted quicksynergy tree dfc \
    libnotify-bin libnotify-dev \
    redshift geoclue geoclue-hostip numlockx \
    samba samba-doc samba-tools wireshark wondershaper \
    vlc ffmpeg ffmpeg-doc mplayer mencoder \
    p7zip-full rar zip unzip gzip xz-utils liblzma-dev liblzma5 \
    virtualbox-qt wine \
    ttf-xfree86-nonfree"""

KEYRINGS = """ \
    debian-keyring debian-archive-keyring gnome-keyring \
    debian-ports-archive-keyring python-gnomekeyring python-keyring \
    ubuntu-keyring"""

PROGRAMMING = """ \
    build-essential debianutils ubuntu-dev-tools mesa-utils \
    automake automake1.9-doc ant ant-doc checkinstall checkbox \
    dkms docbook make-doc lynx kdiff3 kdiff3-doc patch rpm2cpio rpm \
    codeblocks kdevelop qt-sdk \
    colormake colordiff colorgcc jq \
    vim vim-doc vim-gtk vim-rails vim-syntax-go vim-syntax-gtk vim-doc \
    flex flex-doc bison bison-doc graphviz exuberant-ctags \
    bash-doc bash-builtins bashdb tcsh zsh zsh-dbg zsh-dev zsh-doc zsh-lovers zshdb \
    clisp clisp-doc clisp-dev clisp-module-gdbm \
    docutils-common docutils-doc \
    erlang erlang-eunit \
    gcc gcc-doc gcc-4.7-source libcunit1 gdb gdb-doc cgdb xxgdb ccache \
    libboost-all-dev libglm-dev libglew-dev libglfw-dev \
    libncursesw5-dev libpcre3-dev zlib1g-dev liblzma-dev \
    openmpi-bin openmpi-checkpoint openmpi-common \
    gfortran \
    ghc ghc-doc ghc-haddock ghc-prof haskell-debian-utils \
    haskell-devscripts haskell-doc cabal-install \
    junit junit-doc maven openjdk-7-doc openjdk-7-jdk openjdk-7-dbg \
    openjdk-7-source openjdk-7-demo icedtea-7-plugin \
    lua5.2 lua5.2-doc luadoc \
    nodejs nodejs-dev nodejs-legacy npm \
    perl perl-doc perl-modules libpadwalker-perl libfile-next-perl \
    php5 php5-mysql phpunit php5-dev \
    swi-prolog swi-prolog-doc \
    python python-doc python3-doc python-pip python3-pip jython jython-doc \
    pychecker pylint pep8 python-autopep8 ruby1.9.1-full shunit2 \
    tex-common texlive-latex-base texlive-font-utils \
    bzr bzr-builddeb bzr-doc python-bzrlib bzrtools git git-gui git-doc \
    mercurial subversion cvs"""

BABUN = """ \
    clisp lua perl python python3 ruby make cmake colordiff colorgcc \
    p7zip unzip zip gzip ncurses pcre mercurial bzr subversion \
    libboost-devel libboost_python-devel cppunit
    """

CABAL = "buildwrapper scion-browser hoogle terminfo happy hlint"

PY_PACKS = "argcomplete Pygments trash-cli"

# Classes

class NotSudo(Exception):
    """ Throw this if we aren't sudo but need to be. """
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
    script_dir = script_path[0:script_path.rindex(os.sep)]

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
    if not os.path.exists(ddir):
        os.mkdir(ddir)
    get_code('git clone https://github.com/gmarik/Vundle.vim.git',
            ddir + 'Vundle.vim')

    # Setup git/hg prompt.
    get_code('hg clone http://bitbucket.org/sjl/hg-prompt/',
            home + '.hg-prompt')
    get_code('git clone https://github.com/magicmonty/bash-git-prompt.git',
            home + '.bash-git-prompt')

    # Highlighter to replace grepping a pipe
    get_code('git clone https://github.com/starcraftman/hhighlighter.git',
            home + '.hhighlighter')

    # Setup powerline fonts if not done.
    ddir = home + '.fonts'
    dpow = ddir + os.sep + 'powerline-fonts'
    if not os.path.exists(ddir):
        os.mkdir(ddir)
        get_code('git clone https://github.com/Lokaltog/powerline-fonts', dpow)
        cmd = ('fc-cache -vf ' + ddir).split()
        subprocess.call(cmd)

    # Create dir for ccache
    ddir = home + '.ccache'
    if not os.path.exists(ddir):
        os.mkdir(ddir)

def build_ack(optdir):
    """ Build ack from source, move to target dir. """
    srcdir = optdir + 'src' + os.sep + 'ack' + os.sep
    get_code('git clone https://github.com/petdance/ack2.git', srcdir)

    PDir.push(srcdir)
    cmd = 'perl Makefile.PL'.split()
    subprocess.call(cmd)
    cmd = 'make ack-standalone'.split()
    subprocess.call(cmd)
    cmd = 'make manifypods'.split()
    subprocess.call(cmd)
    PDir.pop()

    shutil.copy(srcdir + 'ack-standalone', optdir + 'bin' + os.sep + 'ack')
    for man in glob.glob(srcdir + 'blib' + os.sep + 'man1' + os.sep + '*.1*'):
        shutil.copy(man, optdir + 'share' + os.sep + 'man' + os.sep + 'man1')

def build_ag(optdir):
    """ Build ag from source, move to target dir. """
    srcdir = optdir + 'src' + os.sep + 'ag' + os.sep
    get_code('git clone https://github.com/ggreer/the_silver_searcher.git',
            srcdir)

    PDir.push(srcdir)
    cmd = ('./build.sh --prefix=' + optdir).split()
    subprocess.call(cmd)
    cmd = 'make install'.split()
    subprocess.call(cmd)
    PDir.pop()

    # Seems to strip srcdir, redownload to have a copy left
    shutil.rmtree(srcdir)
    get_code('git clone https://github.com/ggreer/the_silver_searcher.git',
            srcdir)

def build_doxygen(optdir):
    """ Build doxygen from source, move to target dir. """
    srcdir = optdir + 'src' + os.sep + 'doxygen' + os.sep
    get_code('git clone https://github.com/doxygen/doxygen.git', srcdir)

    PDir.push(srcdir)
    cmd = ('./configure --prefix=' + optdir).split()
    subprocess.call(cmd)
    cmd = 'make -j{}'.format(num_jobs()).split()
    subprocess.call(cmd)
    PDir.pop()

    # Odd behaviour when using --prefix with build, so just copy manually
    shutil.copy(srcdir + 'bin' + os.sep + 'doxygen', optdir + 'bin')
    for man in glob.glob(srcdir + 'doc' + os.sep + '*.1'):
        shutil.copy(man, optdir + 'share' + os.sep + 'man' + os.sep + 'man1')

def build_parallel(optdir):
    """ Build GNU Parallel from source, move to target dir. """
    archive = 'parallel.tar.bz2'
    url = 'http://ftp.gnu.org/gnu/parallel/parallel-latest.tar.bz2'
    srcdir = optdir + 'src' + os.sep + 'parallel' + os.sep

    try:
        # Fetch program
        print("Downloading latest parallel source.")
        prog = Progress.default_prog()
        tfile = urllib.URLopener()
        tfile.retrieve(url, archive, gen_report(prog))
        tarfile.open(archive).extractall()
        tdir = glob.glob('parallel-*')[0]
        os.rename(tdir, srcdir)

        # Build & clean
        PDir.push(srcdir)
        cmd = ('./configure --prefix=' + optdir).split()
        subprocess.call(cmd)
        cmd = 'make -j{} install'.format(num_jobs()).split()
        subprocess.call(cmd)
        PDir.pop()
    finally:
        os.remove(archive)

def src_programs():
    """ Download sources and install to enironment OPT directory. """
    # Store all compilations into opt from environment
    optdir = os.environ['OPT'] + os.sep
    home = os.path.expanduser('~') + os.sep

    # Only use on posix systems.
    if not os.name == 'posix' or os.path.exists(home + '.babunrc'):
        print("This command only for unix.")
        return

    # Ensure opt dirs exist
    for odir in [optdir + 'bin', optdir + 'src',
            optdir + 'share' + os.sep + 'man' + os.sep + 'man1']:
        if not os.path.exists(odir):
            os.makedirs(odir)

    funcs = {'ag':      build_ag,
            'ack':      build_ack,
            'doxygen':  build_doxygen,
            'parallel': build_parallel,
            }

    # Build programs and copy bins to bindir.
    for name in sorted(funcs.keys()):
        prog = optdir + 'bin' + os.sep + name
        srcdir = optdir + 'src' + os.sep + name + '_src'
        if not os.path.exists(prog):
            if os.path.exists(srcdir):
                shutil.rmtree(srcdir)
            funcs[name](optdir)
            print('Finished building ' + prog)

def packs_babun():
    """ Setup a fresh babun install. """
    # Install packages
    cmd = ('pact install ' + BABUN).split()
    subprocess.call(cmd)

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
    cmd = 'cabal update'.split()
    subprocess.call(cmd)

    cmd = ('cabal install ' + CABAL).split()
    subprocess.call(cmd)

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
    cmd = ('sudo pip install ' + PY_PACKS).split()
    subprocess.call(cmd)

    # Install python completion to system bash_completion.d.
    cmd = 'activate-global-python-argcomplete --user'.split()
    subprocess.call(cmd)

def install_jshint():
    """ Setup jshint for progrmaming javascript with vim. """
    cmd = 'npm install jshint -g'.split()
    subprocess.call(cmd)

def install_pipelight():
    """ Silverlight plugin for firefox/chrome on linux.
    http://www.webupd8.org/2013/08/pipelight-use-silverlight-in-your-linux.html
    """
    if os.getuid() != 0:
        raise NotSudo

    cmds = ['sudo apt-get remove flashplugin-installer',
            'sudo apt-add-repository ppa:pipelight/stable',
            'sudo apt-get update',
            'sudo apt-get install pipelight-multi',
            'pipelight-plugin --enable silverlight',
            'pipelight-plugin --enable flash',]
    cmds = [x.split() for x in cmds]
    [subprocess.call(x) for x in cmds]
    print("Installation over, remember to use a useragent switcher.")

def main():
    """ Main function. """
    mesg = """This script sets up a dev environment.

    choice      effect
    ------------------------------------------------------
    home        Setup home config files.
    src         Install some development programs from source.
    debian      Install debian packages.
    babun       Install babun packages.
    python      Install python libraries via pip.
    cabal       Install haskell packages for eclipse.
    jshint      Install jshint via npm for javascript vim.
    pipelight   Install pipelight flash & silverlight.
    """
    # Use a dict of funcs instead of a case switch
    actions = {'debian': packs_debian,
                'babun': packs_babun,
                'home': home_config,
                'python': packs_py,
                'cabal': packs_cabal,
                'jshint': install_jshint,
                'pipelight': install_pipelight,
                'src': src_programs,
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
