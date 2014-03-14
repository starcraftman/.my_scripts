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

# Packages to install follow, broken down into categories.

PROGRAMS = """ \
    htop aptitude synaptic oxygen-molecule \
    kubuntu-restricted-extras kubuntu-restricted-addons \
    brother-cups-wrapper-laser brother-cups-wrapper-laser1 \
    brother-lpr-drivers-laser brother-lpr-drivers-laser1 \
    k3b kid3 krita kolourpaint4 kchmviewer yakuake plasma-widget-quickaccess \
    chromium-browser firefox \
    abiword baobab dvdrip easytag chm2pdf dia \
    gimp gimp-plugin-registry \
    fuse gparted quicksynergy \
    redshift geoclue geoclue-hostip numlockx \
    samba samba-doc samba-tools wireshark \
    ubuntuone-client ubuntuone-control-panel-qt \
    vlc ffmpeg ffmpeg-doc mplayer mencoder \
    p7zip-full rar zip unzip gzip \
    virtualbox-qt wine \
    ttf-xfree86-nonfree"""

# Series of packages follow, separated to be easily modified.
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
    libncursesw5-dev \
    openmpi-bin openmpi-checkpoint openmpi-common \
    gfortran \
    ghc ghc-doc ghc-haddock ghc-prof haskell-debian-utils \
    haskell-devscripts haskell-doc cabal-install \
    junit junit-doc maven openjdk-7-doc openjdk-7-jdk openjdk-7-dbg \
    openjdk-7-source openjdk-7-demo icedtea-7-plugin \
    lua5.2 lua5.2-doc luadoc \
    perl perl-doc perl-modules libpadwalker-perl \
    php5 php5-mysql phpunit php5-dev \
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
    if os.getuid() != 0:
        raise NotSudo('This stage must be run as root.')

    packages = '{} {} {}'.format(PROGRAMS, PROGRAMMING, KEYRINGS)
    packages = packages.split()

    cache = apt.Cache()
    print("One moment while we update cache.")
    cache.update()
    cache.open(None)
    print("Update done.")

    cmd = ['apt-get', 'install']
    for pack in packages:
        try:
            package = cache[pack]
            if not package.is_installed:
                cmd.append(pack)
        except Exception as e:
            print("Package couldn't be selected: %s" % pack)

    print("Please wait, running: {}".format(" ".join(cmd)))
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
    script_dir = os.path.realpath(__file__)
    script_dir = script_dir[0:script_dir.rindex(os.sep)]

    # Leaving trailing sep for ease later.
    src = script_dir + os.sep + 'vim_and_bash_config' + os.sep
    dst = os.path.expanduser('~') + os.sep

    # Link to config files, copy .vim folder.
    for fil in ['.vimrc', '.bash_aliases']:
        sfile = src + fil
        dfile = dst + fil
        if not os.path.exists(dfile):
            os.symlink(sfile, dfile)

    # Copy vim folder if not there.
    ddir = dst + '.vim'
    if not os.path.exists(ddir):
        os.symlink(src + '.vim', ddir)

    # Init vundle for vim plugin install.
    ddir = dst + '.vim/bundle'
    if not os.path.exists(ddir):
        print('Creating bunlde dir ' + ddir)
        os.mkdir(ddir)
    get_code('git clone https://github.com/gmarik/vundle.git',
             dst + '.vim/bundle/vundle')

    # Setup git/hg prompt.
    get_code('hg clone http://bitbucket.org/sjl/hg-prompt/',
             dst + '.hg-prompt')
    get_code('git clone git@github.com:magicmonty/bash-git-prompt.git',
             dst + '.bash-git-prompt')

    # Setup powerline fonts if not done.
    ddir = dst + '.fonts'
    if not os.path.exists(ddir):
        os.mkdir(ddir)
        get_code('git clone https://github.com/Lokaltog/powerline-fonts',
                 ddir + os.sep + 'powerline-fonts')
        subprocess.call(['fc-cache', '-vf', ddir])


def install_cabal():
    """ Installs locally some haskell packages for Eclipse Haskell plugin. """
    cmd = ['cabal', 'update']
    subprocess.call(cmd)

    cmd = 'cabal install {}'.format(CABAL)
    cmd = cmd.split()
    subprocess.call(cmd)


def py_packages():
    """ Installs python packages using pip. """
    if os.geteuid() != 0:
        raise NotSudo('This stage must be run as root.')

    # Use python package manager.
    cmd = 'pip install ' + PY_PACKS
    subprocess.call(cmd.split())

    # Install python completion to system bash_completion.d.
    cmd = 'activate-global-python-argcomplete'
    subprocess.call(cmd.split())


def setup_pipelight():
    """ Silverlight plugin for firefox/chrome on linux. """
    """ See: http://www.webupd8.org/2013/08/pipelight-use-silverlight-in-your-linux.html """
    if os.getuid() != 0:
        raise NotSudo('This stage must be run as root.')

    cmd1 = ['sudo', 'apt-add-repository', 'ppa:pipelight/stable']
    cmd2 = ['sudo', 'apt-get', 'update']
    cmd3 = ['sudo', 'apt-get', 'install', 'pipelight-multi']
    cmd4 = ['pipelight-plugin', '--enable', 'silverlight']
    cmds = [cmd1, cmd2, cmd3, cmd4]
    for c in cmds:
        subprocess.call(c)

    print("Installation over, remember to use a useragent switcher.")

def take_choice(choice):
    """ Simple wrapper function to select right action. """
    choice = int(choice)
    if choice == 1:
        install_packages()
    elif choice == 2:
        setup_config()
    elif choice == 3:
        install_cabal()
    elif choice == 4:
        py_packages()
    elif choice == 5:
        setup_pipelight()

if __name__ == '__main__':
    DESC = """ This program sets up a vanilla Ubuntu install.
    Pass a number to determine step.
    1 -> Install most packages.
    2 -> Setup vim, bash_aliases and development environment.
    3 -> Setup cabal for haskell development.
    4 -> Setup python packages through pip.
    5 -> Setup pipelight to get netflix support via wine.
    """
    PARSER = argparse.ArgumentParser(description=DESC)
    PARSER.add_argument('choice', action='store', help='the stage')

    ARGS = PARSER.parse_args()  # Default parses argv[1:]

    try:
        take_choice(ARGS.choice)
    except IOError as exc:
        print('Failed to install: {}'.format(exc))
    except NotSudo as exc:
        print("Rerun this part of script with sudo.")
