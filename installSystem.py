#!/usr/bin/env python3
# Common tools:
#	pip/pip3 : install packages
#	pylint/pychecker : verify syntax
#	unittest package for xUnit.
''' Implements code to support my templating system for source files. '''

# Imports
import apt
import sys
import argparse
import glob
import os
import stat
from shutil import copyfile
import subprocess

# Packages to install follow, broken down into categories.

PROGRAMS = """aptitude synaptic \
    kubuntu-restricted-extras kubuntu-restricted-addons \
    brother-cups-wrapper-laser* brother-lpr-drivers-laser* \
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
KEYRINGS = """debian-keyring debian-archive-keyring gnome-keyring \
    debian-ports-archive-keyring python-gnomekeyring python-keyring \
    ubuntu-keyring"""

PROGRAMMING = """build-essential debianutils ubuntu-dev-tools \
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
    libncursesw5-dev libncursesw5-doc \
    gfortran \
    ghc ghc-doc ghc-haddock ghc-prof haskell-debian-utils \
    haskell-devscripts haskell-doc cabal-install \
    junit junit-doc maven openjdk-7-doc openjdk-7-jdk openjdk-7-dbg \
    openjdk-7-source openjdk-7-demo icedtea-7* \
    lua5.2 lua5.2-doc luadoc \
    perl perl-doc perl-modules libpadwalker-perl \
    php5 php5-mysql phpunit php5-dev \
    python python-doc python3-doc jython jython-doc \
    ruby1.9.1-full shunit2 \
    bzr bzr-builddeb bzr-doc bzr-grep bzrtools git git-gui git-doc \
    mercurial subversion cvs"""

CABAL = "buildwrapper scion-browser hoogle terminfo happy hlint"

# Functions


def install_packages():
    """ Installs required packages on this system. """
    packages = "{} {} {}".format(PROGRAMS, PROGRAMMING, KEYRINGS).split()
    cache = apt.Cache()
    cache.update()

    for pack in packages:
        package = cache[pack].mark_install()
        package.mark_install()

    cache.commit()


def setup_dev():
    """ Setup the dev environment, assumes target dir is home. """


def install_cabal():
    """ Installs locally some haskell packages for Eclipse Haskell plugin. """
    subprocess.call('sudo cabal install {}'.format(CABAL))

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

    if ARGS.choice == 1:
        install_packages()
    elif ARGS.choice == 2:
        setup_dev()
    elif ARGS.choice == 3:
        install_cabal()
