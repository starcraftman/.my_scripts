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
    htop iotop itop mytop pkg-config aptitude synaptic dos2unix oxygen-molecule \
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

PY_PACKS = "argcomplete Pygments trash-cli"

# Classes

class NotSudo(Exception):
    """ Throw this if we aren't sudo but need to be. """
    pass

class ArchiveException(Exception):
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
    cmd = 'wget ' + url
    subprocess.call(cmd.split())

    arc_ext = None
    for ext in ['.tar.bz2', '.tar.gz', '.rar', '.zip', '.7z']:
        right = url.rfind(ext)
        if right != -1:
            right += len(ext)
            left = url.rfind(os.sep, 0, right) + 1
            arc_ext = ext
            break

    if arc_ext == None:
        raise ArchiveException

    # Corner case for source forge, file is download
    arc_name = url[left:right]
    if url.rfind('/download') != -1:
        os.rename('download', arc_name)

    if arc_ext.find('tar') != -1:
        tarfile.open(arc_name).extractall()
    else:
        cmd = 'unarchive ' + arc_name
        subprocess.call(cmd.split())

    # extracted dir doesn't always match arc_name, glob to be sure
    arc_front = re.split('[-_]', arc_name)[0] + '*'
    arc_dir = None
    for name in glob.glob(arc_front):
        if name.rfind(arc_ext) == -1:
            arc_dir = name

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
    get_code('https://github.com/gmarik/Vundle.vim.git', ddir + 'Vundle.vim')

    # Get shell utilities
    shell_dir = home + '.shell' + os.sep
    get_code('http://bitbucket.org/sjl/hg-prompt/', shell_dir + '.hg-prompt')

    git_urls = [
            'https://github.com/magicmonty/bash-git-prompt.git',
            'https://github.com/starcraftman/zsh-git-prompt.git',
            'https://github.com/zsh-users/zsh-completions.git',
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
        cmd = ('fc-cache -vf ' + ddir).split()
        subprocess.call(cmd)

    # Create dir for ccache
    ddir = home + '.ccache'
    if not os.path.exists(ddir):
        os.mkdir(ddir)

def build_src(optdir, name, url, build_cmds, post_globs):
    """ Build from source a project downloeaded from url.
        The build_cmds will be executed in the srcdir.
        post_globs format -> [(glob, target), (glob, target), ...]
        All files matching glob, moved to target.
    """
    srcdir = optdir + 'src' + os.sep + name + os.sep

    try:
        get_archive(url, srcdir)
    except ArchiveException:
        get_code(url, srcdir)

    # Code should be at srcdir by here.
    PDir.push(srcdir)
    for cmd in build_cmds:
        subprocess.call(cmd.split())
    PDir.pop()

    # Manual copies sometimes required to finish install
    for pattern, target in post_globs:
        for sfile in glob.glob(srcdir + pattern):
            shutil.copy(sfile, target)

    shutil.rmtree(srcdir)

def build_ack(optdir):
    """ Build ack from source, move to target dir. """
    srcdir = optdir + 'src' + os.sep + 'ack' + os.sep
    get_code('https://github.com/petdance/ack2.git', srcdir)

    PDir.push(srcdir)
    cmds = ['perl Makefile.PL',
            'make ack-standalone',
            'make manifypods']
    for cmd in cmds:
        subprocess.call(cmd.split())
    PDir.pop()

    shutil.copy(srcdir + 'ack-standalone', optdir + 'bin' + os.sep + 'ack')
    for man in glob.glob(srcdir + 'blib' + os.sep + 'man1' + os.sep + '*.1*'):
        shutil.copy(man, optdir + 'share' + os.sep + 'man' + os.sep + 'man1')

def build_ag(optdir):
    """ Build ag from source, move to target dir. """
    srcdir = optdir + 'src' + os.sep + 'ag' + os.sep
    get_code('https://github.com/ggreer/the_silver_searcher.git', srcdir)

    PDir.push(srcdir)
    cmds = ['./build.sh --prefix=' + optdir,
            'make install']
    for cmd in cmds:
        subprocess.call(cmd.split())
    PDir.pop()

    # Seems to strip srcdir, redownload to have a copy left
    shutil.rmtree(srcdir)
    get_code('https://github.com/ggreer/the_silver_searcher.git', srcdir)

def build_doxygen(optdir):
    """ Build doxygen from source, move to target dir. """
    srcdir = optdir + 'src' + os.sep + 'doxygen' + os.sep
    get_code('https://github.com/doxygen/doxygen.git', srcdir)

    PDir.push(srcdir)
    cmds = ['./configure --prefix=' + optdir,
            'make -j{}'.format(num_jobs())]
    for cmd in cmds:
        subprocess.call(cmd.split())
    PDir.pop()

    # Odd behaviour when using --prefix with build, so just copy manually
    shutil.copy(srcdir + 'bin' + os.sep + 'doxygen', optdir + 'bin')
    for man in glob.glob(srcdir + 'doc' + os.sep + '*.1'):
        shutil.copy(man, optdir + 'share' + os.sep + 'man' + os.sep + 'man1')

    shutil.rmtree(srcdir)

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
        cmds = ['./configure --prefix=' + optdir,
                'make -j{} install'.format(num_jobs())]
        for cmd in cmds:
            subprocess.call(cmd.split())
        PDir.pop()
    finally:
        os.remove(archive)

def build_vim():
    """ Build vim if very old. """
    # Store all compilations into opt from environment
    optdir = os.environ['OPTDIR'] + os.sep
    srcdir = optdir + 'src' + os.sep + 'vim_src' + os.sep

    get_code('https://code.google.com/p/vim/', srcdir)

    try:
        PDir.push(srcdir)
        cmds = ['./configure --with-features=huge --enable-gui=gtk2 \
            --enable-cscope --enable-multibyte  \
            --enable-luainterp --enable-perlinterp \
            --enable-pythoninterp \
            --with-python-config-dir=/usr/lib/python2.7/config \
            --enable-rubyinterp --enable-tclinterp \
            --prefix=' + optdir,
            'make VIMRUNTIMEDIR=%sshare/vim/vim74' % optdir,
            'make install']
        for cmd in cmds:
            subprocess.call(cmd.split())
    finally:
        PDir.pop()
        shutil.rmtree(srcdir)

def build_vimpager(optdir):
    """ Vimpager is a neat tool that pages with vim, also vimcat. """
    srcdir = optdir + 'src' + os.sep + 'vimpager' + os.sep
    get_code('https://github.com/rkitover/vimpager.git', srcdir)

    # Simply move the required files to optdir
    shutil.copy(srcdir + 'vimcat', optdir + 'bin')
    shutil.copy(srcdir + 'vimpager', optdir + 'bin')
    for man in glob.glob(srcdir +  os.sep + '*.1'):
        shutil.copy(man, optdir + 'share' + os.sep + 'man' + os.sep + 'man1')

    shutil.rmtree(srcdir)

# If switch to build later:
# https://gist.github.com/nicoulaj/715855
def build_zsh_docs(optdir):
    """ Ubuntu zsh missing docs, get them from archive. """
    url = 'http://sourceforge.net/projects/zsh/files/zsh/5.0.5/zsh-5.0.5.tar.bz2/download'
    srcdir = optdir + 'src' + os.sep + 'zsh_docs' + os.sep

    try:
        get_archive(url, srcdir)
        manfiles = glob.glob(srcdir + 'Doc' + os.sep + '*.1')
        for man in manfiles:
            shutil.copy(man, optdir + os.sep + 'share' + os.sep
                    + 'man' + os.sep + 'man1')
        # Copy a file to bin just as guard
        shutil.copy(manfiles[0], optdir + os.sep + 'bin' + os.sep + 'zsh_docs')
    finally:
        shutil.rmtree(srcdir)

def src_programs():
    """ Download sources and install to enironment OPT directory. """
    # Store all compilations into opt from environment
    optdir = os.environ['OPTDIR'] + os.sep
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
            'vimpager': build_vimpager,
            'zsh_docs': build_zsh_docs,
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
    vim         Install latest vim into source location.
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
                'vim': build_vim,
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
