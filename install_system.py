#!/usr/bin/env python3
# Common tools:
#	pip/pip3 : install packages
#	pylint/pychecker : verify syntax
#	unittest package for xUnit.
''' Implements code to support my templating system for source files. '''

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
    print("Update done.")

    for pack in packages:
        package = cache[pack]
        if not package.is_installed:
            package.mark_install()

    cache.commit()
    cache.close()


def setup_dev():
    """ Setup the dev environment, stuff goes in ~ and ~/.optSoftware. """
    src = './vim_and_bash_config/{}'
    dst = os.path.expanduser('~')

    # Copy config files for vim and bash into home.
    for fil in ['.vimrc', '.bash_aliases']:
        shutil.copy2(src.format(fil), dst)
    shutil.copytree(src.format('.vim'), dst + '/.vim')


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
        setup_dev()
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
