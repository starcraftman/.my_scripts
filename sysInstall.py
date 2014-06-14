#!/usr/bin/env python
# Common tools:
#	pip/pip3 : install packages
#	pylint/pychecker : verify syntax
#	unittest package for xUnit.
""" This module helps setup a fresh install the way I like it. """

# Imports
from __future__ import print_function
import argparse
import apt
import os
import subprocess
import shutil

# Packages to install follow, broken down into categories.

PROGRAMS = """ \
    htop pkg-config aptitude synaptic dos2unix oxygen-molecule \
    kubuntu-restricted-extras kubuntu-restricted-addons \
    brother-cups-wrapper-laser brother-cups-wrapper-laser1 \
    brother-lpr-drivers-laser brother-lpr-drivers-laser1 \
    k3b kid3 krita kolourpaint4 kchmviewer yakuake plasma-widget-quickaccess \
    chromium-browser firefox rekonq \
    abiword baobab dvdrip easytag chm2pdf dia catdoc \
    gimp gimp-plugin-registry \
    fuse gparted quicksynergy \
    redshift geoclue geoclue-hostip numlockx \
    samba samba-doc samba-tools wireshark \
    ubuntuone-client ubuntuone-control-panel-qt \
    vlc ffmpeg ffmpeg-doc mplayer mencoder \
    p7zip-full rar zip unzip gzip \
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
    colormake colordiff colorgcc \
    vim vim-doc vim-gtk vim-rails vim-syntax-go vim-syntax-gtk vim-doc \
    flex flex-doc bison bison-doc graphviz exuberant-ctags \
    clisp clisp-doc clisp-dev clisp-module-gdbm \
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
    perl perl-doc perl-modules libpadwalker-perl libfile-next-perl \
    php5 php5-mysql phpunit php5-dev \
    nodejs nodejs-dev nodejs-legacy npm \
    python python-doc python3-doc python-pip python3-pip jython jython-doc \
    ruby1.9.1-full shunit2 \
    bzr bzr-builddeb bzr-doc python-bzrlib bzrtools git git-gui git-doc \
    mercurial subversion cvs"""

CABAL = "buildwrapper scion-browser hoogle terminfo happy hlint"

PY_PACKS = "argcomplete trash-cli"


class NotSudo(Exception):
    """ Throw this if we aren't sudo but need to be. """
    pass

# Functions


def install_packages():
    """ Install packages on the current system. """
    if os.getuid() != 0:
        raise NotSudo

    packages = (PROGRAMS + PROGRAMMING + KEYRINGS).split()

    cache = apt.Cache()
    print("One moment while we update cache.")
    cache.update()
    cache.open(None)
    print("Update done.")

    cmd = 'apt-get install'.split()
    for pack in packages:
        try:
            package = cache[pack]
            if not package.is_installed:
                cmd.append(pack)
        except Exception as e:
            print("Package couldn't be selected: %s" % pack)

    print("Please wait, running: " + " ".join(cmd))
    subprocess.call(cmd)

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


def setup_config():
    """ Setup the dev environment, stuff goes in the user's home folder. """
    script_path = os.path.realpath(__file__)
    script_dir = script_path[0:script_path.rindex(os.sep)]

    # Leaving trailing sep for ease later.
    src = script_dir + os.sep + 'dot_files' + os.sep
    dst = os.path.expanduser('~') + os.sep

    # Copy files that get user details in plain text
    sfile = src + '.bazaar'
    dfile = dst + '.bazaar'
    if not os.path.exists(dfile):
        shutil.copytree(sfile, dfile, True)

    files = ['.gitconfig', '.hgrc']
    for fil in files:
        sfile = src + fil
        dfile = dst + fil
        if not os.path.exists(dfile):
            shutil.copy(sfile, dfile)

    # Link to config files, and vim folder
    files = ['.bash_aliases', '.gitignore_global', '.hgignore_global',
             '.vim', '.vimrc', '.ycm_extra_conf.py']
    for fil in files:
        sfile = src + fil
        dfile = dst + fil
        if not os.path.exists(dfile):
            os.symlink(sfile, dfile)

    # Init vundle for vim plugin install.
    ddir = dst + '.vim' + os.sep + 'bundle' + os.sep
    if not os.path.exists(ddir):
        print('Creating bunlde dir ' + ddir)
        os.mkdir(ddir)
    get_code('git clone https://github.com/gmarik/Vundle.vim.git',
            ddir + 'Vundle.vim')

    # Setup git/hg prompt.
    get_code('hg clone http://bitbucket.org/sjl/hg-prompt/',
            dst + '.hg-prompt')
    get_code('git clone git@github.com:magicmonty/bash-git-prompt.git',
            dst + '.bash-git-prompt')

    # Highlighter to replace grepping a pipe
    get_code('git clone https://github.com/starcraftman/hhighlighter.git',
            dst + '.hhighlighter')

    # Ag silver, repo package is old
    ddir = dst + '.ag'
    if os.name == 'posix' and not os.path.exists(ddir):
        get_code('git clone https://github.com/ggreer/the_silver_searcher.git',
                ddir)
        cmd = (ddir + os.sep + 'build.sh').split()
        subprocess.call(cmd)
        sfile = ddir + os.sep + 'ag'
        dfile = dst + '.optSoftware' + os.sep + 'bin'
        shutil.copy(sfile, dfile)

    # Ack, may sometimes be preferred over ag
    ddir = dst + '.ack'
    if not os.path.exists(ddir):
        get_code('git clone https://github.com/petdance/ack2.git', ddir)
        os.chdir(ddir)
        cmd = 'perl Makefile.PL'.split()
        subprocess.call(cmd)
        cmd = 'make ack-standalone'.split()
        subprocess.call(cmd)
        os.chdir(dst)
        sfile = ddir + os.sep + 'ack-standalone'
        dfile = dst + '.optSoftware' + os.sep + 'bin' + os.sep + 'ack'
        shutil.copy(sfile, dfile)

    # Setup powerline fonts if not done.
    ddir = dst + '.fonts'
    dpow = ddir + os.sep + 'powerline-fonts'
    if not os.path.exists(ddir):
        os.mkdir(ddir)
        get_code('git clone https://github.com/Lokaltog/powerline-fonts', dpow)
        cmd = ('fc-cache -vf' + ddir).split()
        subprocess.call(cmd)


def install_cabal():
    """ Installs haskell packages for Eclipse Haskell plugin. """
    cmd = 'cabal update'.split()
    subprocess.call(cmd)

    cmd = ('cabal install ' + CABAL).split()
    subprocess.call(cmd)


def py_packages():
    """ Installs python packages using pip. """
    if os.geteuid() != 0:
        raise NotSudo('This stage must be run as root.')

    # Use python package manager.
    cmd = ('pip install' + PY_PACKS).split()
    subprocess.call(cmd)

    # Install python completion to system bash_completion.d.
    cmd = 'activate-global-python-argcomplete'.split()
    subprocess.call(cmd)


def setup_pipelight():
    """ Silverlight plugin for firefox/chrome on linux.
        See: http://www.webupd8.org/2013/08/pipelight-use-silverlight-in-your-linux.html """
    if os.getuid() != 0:
        raise NotSudo

    cmds = ['sudo apt-get remove flashplugin-installer',
            'sudo apt-add-repository ppa:pipelight/stable',
            'sudo apt-get update',
            'sudo apt-get install pipelight-multi',
            'pipelight-plugin --enable silverlight',
            'pipelight-plugin --enable flash',]
    map(split, cmds)
    map(subprocess.call, cmds)
    print("Installation over, remember to use a useragent switcher.")

def setup_jshint():
    """ Setup jshint for progrmaming javascript with vim. """
    if os.getuid() != 0:
        raise NotSudo

    cmd = 'sudo npm install jshint -g'.split()
    subprocess.call(cmd)

def take_choice(choice):
    """ Select cprrect action, replicates case switch. """
    choice = int(choice)
    if choice == 1:
        install_packages()
    elif choice == 2:
        setup_config()
    elif choice == 3:
        install_cabal()
    elif choice == 4:
        py_packages()
        setup_pipelight()
        setup_jshint()

if __name__ == '__main__':
    DESC = """ This program sets up a vanilla Ubuntu install.
    Pass a number to determine step.
    1 -> Install most packages.
    2 -> Setup vim, bash_aliases and development environment.
    3 -> Setup cabal for haskell development.
    4 -> Setup python packages through pip, pipelight and jshint.
    """
    PARSER = argparse.ArgumentParser(description=DESC)
    PARSER.add_argument('choice', action='store', help='the stage')

    ARGS = PARSER.parse_args()  # Default parses argv[1:]

    try:
        take_choice(ARGS.choice)
    except IOError as exc:
        print('Failed to install: {}'.format(exc))
    except NotSudo:
        print("Rerun this part of script with sudo.")
