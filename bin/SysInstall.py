#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
""" Install packages and setup home configs on fresh system. """
from __future__ import print_function
import argparse
import functools
import glob
import os
import shlex
import shutil
import subprocess
try:
    import apt
except ImportError:
    print("Don't use `debian` option.")
try:
    from argcomplete import autocomplete
except ImportError:
    def autocomplete(_):
        """ Dummy func. """
        pass

from BuildSrc import get_code

# Packages to install follow, broken down into categories.
MINIMUM = """ \
    pv vim build-essential git-core mercurial automake ccache fontconfig gdb lynx \
    colormake colordiff colorgcc exuberant-ctags dkms python-dev python-pip \
    tcl p7zip-full rar zip unzip gzip lzip xz-utils liblzma5 libcurl4-dev \
    htop dos2unix tree dfc flex bison sphinx-common gettext libfile-next-perl \
    libexpat-dev liblzma-dev libpcre3-dev libcurl4-dev libarchive-dev libevent-dev \
    """

PROGRAMS = """ \
    htop iotop itop mytop pkg-config aptitude synaptic dos2unix \
    oxygen-molecule kubuntu-restricted-extras kubuntu-restricted-addons \
    brother-cups-wrapper-laser brother-cups-wrapper-laser1 \
    brother-lpr-drivers-laser brother-lpr-drivers-laser1 brother-lpr-drivers-common \
    k3b kid3 krita kolourpaint4 kchmviewer yakuake plasma-widget-quickaccess \
    muon software-properties-gtk \
    clementine amarok kcharselect k4dirstat keepassx screen tmux \
    chromium-browser firefox \
    abiword baobab dvdrip easytag chm2pdf dia catdoc \
    gimp gimp-plugin-registry \
    fuse gparted extlinux quicksynergy tree dfc sharutils sharutils-doc \
    libnotify-bin libnotify-dev \
    redshift geoclue geoclue-hostip numlockx nautilus-dropbox \
    samba samba-dev cifs-utils wireshark libwireshark-dev \
    wondershaper vlc ffmpeg ffmpeg-doc mplayer mencoder \
    p7zip-full rar zip unzip gzip lzip xz-utils liblzma-dev liblzma5 \
    virtualbox-qt wine-stable vagrant \
    keepass2 abiword-common trash-cli ttf-xfree86-nonfree \
    unrar virtualbox virtualbox-dkms xterm xclip zsync \
    """

KEYRINGS = """ \
    debian-keyring debian-archive-keyring gnome-keyring \
    debian-ports-archive-keyring python-keyring \
    ubuntu-keyring \
    """

# Removed for now:
# qml-module-qtquick-xmllistmodel qtquick1-5-dev qtquick1-qml-plugins
# lldb rust-lldb(4.0)
PROGRAMMING = """ \
    build-essential debianutils ubuntu-dev-tools mesa-utils openssh-server \
    autotools-dev autoconf automake autopoint gperf checkinstall checkbox-ng \
    python3-checkbox-ng python3-checkbox-ng-doc \
    libtool-bin dkms docbook make-doc lynx kdiff3 kdiff3-doc patch rpm2cpio rpm \
    qtcreator codeblocks kdevelop qt-sdk graphviz graphviz-dev -graphviz-doc \
    colormake colordiff colorgcc jq nmap \
    vim vim-doc vim-gtk vim-rails vim-syntax-go vim-syntax-gtk vim-doc \
    re2c flex flex-doc bison bison-doc exuberant-ctags cloc \
    sphinx-common sphinx-doc pandoc \
    bash-doc bash-builtins bats bashdb shellcheck shunit2 \
    zsh zsh-dev zsh-doc zshdb \
    clisp clisp-doc clisp-dev clisp-module-gdbm \
    coffeescript coffeescript-doc \
    docutils-common docutils-doc asciidoc xmlto docbook2x \
    erlang erlang-eunit \
    gdc golang golang-doc golang-src golang-codesearch-dev \
    gcc gcc-doc gcc-5-source libcunit1 gdb gdb-doc cgdb xxgdb ccache \
    valgrind kcachegrind gcovr lcov \
    cmake ninja-build clang clang-tidy clang-format cppcheck llvm \
    libboost-all-dev libglm-dev libglew-dev libglfw3-dev ncurses-doc \
    libncurses5-dev libncursesw5-dev libpcre3-dev zlib1g-dev libbz2-dev \
    libgnome2-dev libgnomeui-dev libgtk2.0-dev libatk1.0-dev libbonoboui2-dev \
    libcairo2-dev libx11-dev libxpm-dev libxt-dev libgmp3-dev libmpc-dev \
    libmpfr-dev libcurl4-openssl-dev libevent-dev libarchive-dev libxslt1-dev \
    libblas-dev liblapack-dev libyaml-dev libsqlite3-dev \
    freeglut3 freeglut3-dev \
    openmpi-bin openmpi-doc openmpi-common \
    gfortran \
    ghc ghc-doc ghc-prof haskell-debian-utils \
    groovy groovy-doc \
    haskell-devscripts haskell-doc haskell-stack cabal-install \
    maven ant ant-doc \
    lua5.3 lua-doc luadoc lua-ldoc liblua5.3-dev \
    nodejs nodejs-dev npm \
    perl perl-doc libperl-dev perl-modules libpadwalker-perl \
    libfile-next-perl \
    php-all-dev phpunit \
    swi-prolog swi-prolog-doc \
    python python-dev python-doc python-pip \
    python3 python3-dev python3-doc python3-pip jython jython-doc pypy pypy-doc \
    pychecker pylint pep8 python-autopep8 \
    python-virtualenv python-flake8 pylint python-tox \
    python-matplotlib python-numpy python-scipy python-pytest python-pygments \
    ruby-full bundler \
    rustc rust-gdb cargo cargo-doc \
    tcl-dev tcl-doc \
    tex-common texlive-latex-base texlive-font-utils \
    bzr bzr-builddeb bzr-doc python-bzrlib bzrtools git git-gui git-doc \
    mercurial subversion cvs \
    aspectj aspectj-doc aspectc++ \
    yamllint \
    """

BABUN = """ \
    clisp lua perl python python3 ruby make cmake colordiff colorgcc \
    p7zip unzip zip gzip ncurses pcre mercurial bzr subversion \
    libboost-devel libboost_python-devel cppunit
    """

CABAL = "buildwrapper scion-browser hoogle terminfo happy hlint"

PY_PACKS = """ \
    argcomplete argparse cram neovim pygments trash-cli ipython pyyaml \
    tox pytest sphinx coverage flake8 pep8 pylint virtualenv \
    pygraphviz networkx pyandoc \
    """

DOT_FILES = os.path.join('.shell', 'dot', 'files')
HOME_BAK = '.home_bak'


class NotSudo(Exception):
    """ Throw this if we aren't sudo but need to be. """
    pass


def do_in_home(some_func):
    """ Simple decorator, executes some_func in users $HOME. """
    def inner():
        """ Inner part of decorator. """
        oldcwd = os.getcwd()
        print('oldcwd: {0}'.format(oldcwd))
        os.chdir(os.path.expanduser('~'))
        some_func()
        os.chdir(oldcwd)
    return inner


@do_in_home
def home_config():
    """ Setup the dev environment, stuff goes in the user's home folder. """
    # Get shell utilities
    shell_dir = '.shell'
    git_urls = [
        'git@github.com:pakit/base_recipes.git',
        'git@github.com:starcraftman/dot.git',
        #  'https://github.com/starcraftman/dot.git',
        'https://github.com/google/styleguide',
        'https://github.com/magicmonty/bash-git-prompt.git',
        'https://github.com/mernen/completion-ruby/',
        'https://github.com/starcraftman/zsh-git-prompt.git',
        'https://github.com/zsh-users/zsh-completions.git',
        'https://github.com/zsh-users/zsh-syntax-highlighting.git',
        'https://github.com/starcraftman/hhighlighter.git',
    ]
    for url in git_urls:
        target = url[url.rindex('/')+1:url.rindex('.git')]
        get_code(url, os.path.join(shell_dir, target))

    get_code('https://bitbucket.org/sjl/hg-prompt/',
             os.path.join(shell_dir, 'hg-prompt'))

    # Setup powerline fonts if not done.
    font_dir = '.fonts'
    if not os.path.exists(font_dir) and \
            subprocess.call(['which', 'fc-cache']) == 0:
        get_code('https://github.com/Lokaltog/powerline-fonts',
                 os.path.join(font_dir, 'powerline'))
        subprocess.call(['fc-cache', '-vf', font_dir])

    files = [os.path.basename(x) for x in
             glob.glob(os.path.join(DOT_FILES, '*'))]
    for fil in files:
        sfile, dfile = os.path.join(DOT_FILES, fil), '.' + fil
        if not os.path.exists(dfile):
            print("{0} >>>>> {1}".format(sfile, dfile))
            os.symlink(sfile, dfile)

    print("NOTE: Remember to add user to smb.\nsudo smbpasswd -a username")


@do_in_home
def home_restore():
    """ Undo changes by home_config & restore backup if exists. """
    for folder in ('.shell', '.fonts', '.ccache',):
        try:
            shutil.rmtree(folder)
        except OSError:
            pass

    # Clear existing configs if they are symlinks
    files = [os.path.basename(x) for x in
             glob.glob(os.path.join(DOT_FILES, '*'))]
    for fil in files:
        if os.path.islink(fil):
            os.remove(fil)

    arc_files = [os.path.basename(x) for x in
                 glob.glob(os.path.join(HOME_BAK, '.*'))]
    for fil in arc_files:
        sfile, dfile = os.path.join(HOME_BAK, fil), fil
        if not os.path.exists(dfile):
            print("{0} >>>>> {1}".format(sfile, dfile))
            os.rename(sfile, dfile)

    try:
        os.rmdir(HOME_BAK)
    except OSError:
        pass


@do_in_home
def home_save():
    """ Save existing home configs to a backup dir. """
    if not os.path.exists(HOME_BAK):
        os.makedirs(HOME_BAK)

    files = ['.' + os.path.basename(x) for x in
             glob.glob(os.path.join(DOT_FILES, '*'))]
    files = [x for x in files if os.path.exists(x)]

    for fil in files:
        sfile, dfile = fil, os.path.join(HOME_BAK, fil)
        if not os.path.exists(dfile):
            print("{0} >>>>> {1}".format(sfile, dfile))
            os.rename(sfile, dfile)


def packs_babun():
    """ Setup a fresh babun install. """
    # Install packages
    cmd = 'pact install ' + BABUN
    subprocess.call(shlex.split(cmd))

    home_save()
    home_config()


def packs_cabal():
    """ Installs haskell packages for Eclipse Haskell plugin. """
    cmd = 'cabal update'
    subprocess.call(shlex.split(cmd))

    cmd = 'cabal install ' + CABAL
    subprocess.call(shlex.split(cmd))


def packs_debian(server=False):
    """ Install packages on the current system. """
    if os.getuid() != 0:
        raise NotSudo

    if server:
        packages = MINIMUM.split()
    else:
        packages = (PROGRAMS + PROGRAMMING + KEYRINGS).split()

    cache = apt.Cache()
    print("One moment while we update cache.")
    cache.update()
    cache.open(None)
    print("Update done.")

    cmd = 'sudo apt-get -y install'.split()
    failed_debs = []
    for pack in packages:
        try:
            package = cache[pack]
            if not package.is_installed:
                cmd.append(pack)
        except KeyError:
            print("Package couldn't be selected: %s" % pack)
            failed_debs.append(pack)

    print("Writing failed debs to {}".format(os.path.join(os.getcwd(), 'failed_debs')))
    with open('failed_debs', 'w') as fout:
        fout.write(os.linesep.join(failed_debs))

    print("Please wait, running: " + " ".join(cmd))
    subprocess.call(cmd)


def packs_py():
    """ Installs python packages using pip. """
    # Use python package manager.
    cmd = 'pip install --upgrade ' + PY_PACKS
    subprocess.call(shlex.split(cmd))

    # Install python completion to system bash_completion.d.
    cmd = 'activate-global-python-argcomplete --user'
    subprocess.call(shlex.split(cmd))


def install_jshint():
    """ Setup jshint for progrmaming javascript with vim. """
    cmd = 'npm install jshint -g'
    subprocess.call(shlex.split(cmd))


def main():
    """ Main function. """
    mesg = """This script sets up a dev environment.

    choice       effect
    ------------------------------------------------------
    home         Setup home config files.
    home_restore Restore home files and undo home_save.
    home_save    Save existing home files.
    babun        Install babun packages.
    cabal        Install haskell packages for eclipse.
    debian       Install debian packages.
    server       Install debian packages for server, minimal.
    jshint       Install jshint via npm for javascript vim.
    pip          Install python libraries via pip.
    """
    # Use a dict of funcs to process args
    actions = {
        'home':         home_config,
        'home_restore': home_restore,
        'home_save':    home_save,
        'babun':        packs_babun,
        'cabal':        packs_cabal,
        'debian':       packs_debian,
        'server':       functools.partial(packs_debian, True),
        'jshint':       install_jshint,
        'pip':          packs_py,
    }
    parser = argparse.ArgumentParser(description=mesg,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('stages', nargs='+', help='stages to execute',
                        choices=sorted(actions.keys()))

    autocomplete(parser)
    args = parser.parse_args()  # Default parses argv[1:]

    try:
        for stage in args.stages:
            actions[stage]()
    except NotSudo:
        print("Rerun this part of script with sudo.")


if __name__ == '__main__':
    main()
