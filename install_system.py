#!/usr/bin/env python3
# Common tools:
#	pip/pip3 : install packages
#	pylint/pychecker : verify syntax
#	unittest package for xUnit.
""" This module helps setup a fresh install the way I like it. """

# Imports
import apt
import argparse
import os
import shutil
import subprocess

# Packages to install follow, broken down into categories.

PROGRAMS = """ \
    aptitude synaptic \
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
    vlc ffmpeg-doc ffmpeg mplayer mencoder \
    p7zip-full rar zip unzip gzip \
    virtualbox-qt wine \
    ttf-xfree86-nonfree"""

# Series of packages follow, separated to be easily modified.
KEYRINGS = """ \
    debian-keyring debian-archive-keyring gnome-keyring \
    debian-ports-archive-keyring python-gnomekeyring python-keyring \
    ubuntu-keyring"""

PROGRAMMING = """ \
    build-essential debianutils ubuntu-dev-tools \
    automake automake1.9-doc ant ant-doc checkinstall checkbox \
    dkms docbook make-doc lynx kdiff3 kdiff3-doc patch rpm2cpio rpm \
    codeblocks kdevelop qt-sdk \
    colormake colordiff colorgcc \
    vim vim-doc vim-gtk vim-rails vim-syntax-go vim-syntax-gtk vim-doc \
    flex flex-doc bison bison-doc graphviz exuberant-ctags \
    clisp clisp-doc clisp-dev clisp-module-gdbm \
    erlang erlang-eunit \
    gcc gcc-doc gcc-4.7-source libcunit1 gdb gdb-doc cgdb xxgdb \
    libboost-all-dev libglm-dev libglew-dev libglfw-dev \
    libncursesw5-dev \
    gfortran \
    ghc ghc-doc ghc-haddock ghc-prof haskell-debian-utils \
    haskell-devscripts haskell-doc cabal-install \
    junit junit-doc maven openjdk-7-doc openjdk-7-jdk openjdk-7-dbg \
    openjdk-7-source openjdk-7-demo icedtea-7-plugin \
    lua5.2 lua5.2-doc luadoc \
    perl perl-doc perl-modules libpadwalker-perl \
    php5 php5-mysql phpunit php5-dev \
    python python-doc python3-doc jython jython-doc \
    ruby1.9.1-full shunit2 \
    bzr bzr-builddeb bzr-doc python-bzrlib bzrtools git git-gui git-doc \
    mercurial subversion cvs"""

CABAL = "buildwrapper scion-browser hoogle terminfo happy hlint"


class NotSudo(Exception):
    """ Throw this if we aren't sudo but need to be. """
    pass

# Functions


def install_packages():
    """ Installs required packages on this system. """
    if os.getuid() != 0:
        raise NotSudo('This stage must be run as root.')

    packages = '{} {} {}'.format(PROGRAMS, PROGRAMMING, KEYRINGS)
    packages = packages.split()

    cache = apt.Cache()
    print("One moment while we update cache.")
    cache.update()
    cache.open(None)
    print("Update done.")

    for pack in packages:
        package = cache[pack]
        if not package.is_installed:
            package.mark_install()

    cache.commit()
    cache.close()


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
    script_dir = script_dir[0:script_dir.rindex(os.path.sep)]
    src = script_dir + '/vim_and_bash_config/{}'
    dst = os.path.expanduser('~')

    # Link to config files, copy .vim folder.
    for fil in ['.vimrc', '.bash_aliases']:
        dfile = dst + '/' + fil
        if not os.path.exists(dfile):
            os.symlink(src.format(fil), dfile)

    # Copy vim folder if not there.
    ddir = dst + '/.vim'
    if not os.path.exists(ddir):
        shutil.copytree(src.format('.vim'), ddir)

    # Init NeoBundle.
    ddir = dst + '/.vim/bundle'
    if not os.path.exists(ddir):
        print('Creating bunlde dir {}.'.format(ddir))
        os.mkdir(ddir)
    get_code('git clone https://github.com/Shougo/neobundle.vim',
             dst + '/.vim/bundle/neobundle.vim')

    # Setup git/hg prompt.
    get_code('hg clone http://bitbucket.org/sjl/hg-prompt/',
             dst + '/.hg-prompt')
    get_code('git clone git@github.com:magicmonty/bash-git-prompt.git',
             dst + '/.bash-git-prompt')

    # Setup powerline fonts if not done.
    ddir = dst + '/.fonts'
    if not os.path.exists(ddir):
        os.mkdir(ddir)
        get_code('git clone https://github.com/Lokaltog/powerline-fonts',
                 ddir + '/powerline-fonts')
        subprocess.call(['fc-cache', '-vf', ddir])


def install_cabal():
    """ Installs locally some haskell packages for Eclipse Haskell plugin. """
    cmd = ['cabal', 'update']
    subprocess.call(cmd)

    cmd = 'cabal install {}'.format(CABAL)
    cmd = cmd.split()
    subprocess.call(cmd)


def take_choice(choice):
    """ Simple wrapper function to select right action. """
    choice = int(choice)
    if choice == 1:
        install_packages()
    elif choice == 2:
        setup_config()
    elif choice == 3:
        install_cabal()

if __name__ == '__main__':
    DESC = """ This program sets up a vanilla Ubuntu install.
    Pass a number to determine step.
    1 -> Install most packages.
    2 -> Setup vim, bash_aliases and development environment.
    3 -> Setup cabal for haskell development.
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
