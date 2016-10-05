#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
""" Install packages and setup home configs on fresh system. """
from __future__ import print_function
from BuildSrc import get_code
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
    def autocomplete(dummy):
        """ Dummy func. """
        pass

# Packages to install follow, broken down into categories.
MINIMUM = """ \
    pv vim build-essential git-core mercurial automake ccache fontconfig gdb lynx \
    colormake colordiff colorgcc exuberant-ctags dkms python-dev python-pip \
    tcl p7zip-full rar zip unzip gzip lzip xz-utils liblzma5 libcurl4-dev \
    htop dos2unix tree dfc flex bison sphinx-common gettext libfile-next-perl \
    libexpat-dev liblzma-dev libpcre3-dev libcurl4-dev libarchive-dev libevent-dev \
    """

PROGRAMS = """ \
    htop iotop itop mytop pkg-config aptitude synaptic dos2unix unetbootin \
    oxygen-molecule kubuntu-restricted-extras kubuntu-restricted-addons \
    brother-cups-wrapper-laser brother-cups-wrapper-laser1 \
    brother-lpr-drivers-laser brother-lpr-drivers-laser1 \
    k3b kid3 krita kolourpaint4 kchmviewer yakuake plasma-widget-quickaccess \
    kcharselect k4dirstat keepassx screen tmux \
    chromium-browser firefox rekonq \
    abiword baobab dvdrip easytag chm2pdf dia catdoc \
    gimp gimp-plugin-registry \
    fuse gparted quicksynergy tree dfc sharutils sharutils-doc \
    libnotify-bin libnotify-dev \
    redshift geoclue geoclue-hostip numlockx nautilus-dropbox \
    samba samba-doc samba-dev samba-dbg cifs-utils wireshark libwireshark-dev \
    wondershaper vlc ffmpeg ffmpeg-doc mplayer mencoder \
    p7zip-full rar zip unzip gzip lzip xz-utils liblzma-dev liblzma5 \
    virtualbox-qt wine vagrant \
    ttf-xfree86-nonfree \
    """

KEYRINGS = """ \
    debian-keyring debian-archive-keyring gnome-keyring \
    debian-ports-archive-keyring python-gnomekeyring python-keyring \
    ubuntu-keyring \
    """

PROGRAMMING = """ \
    build-essential debianutils ubuntu-dev-tools mesa-utils openssh-server \
    automake automake1.9-doc autopoint gperf checkinstall checkbox \
    dkms docbook make-doc lynx kdiff3 kdiff3-doc patch rpm2cpio rpm \
    codeblocks kdevelop qt-sdk graphviz graphviz-dev \
    colormake colordiff colorgcc jq nmap \
    vim vim-doc vim-gtk vim-rails vim-syntax-go vim-syntax-gtk vim-doc \
    re2c flex flex-doc bison bison-doc exuberant-ctags \
    sphinx-common sphinx-doc pandoc \
    qml-module-qtquick-xmllistmodel \
    bash-doc bash-builtins bashdb \
    zsh zsh-dbg zsh-dev zsh-doc zsh-lovers zshdb \
    clisp clisp-doc clisp-dev clisp-module-gdbm \
    coffeescript coffeescript-doc \
    docutils-common docutils-doc asciidoc xmlto docbook2x \
    erlang erlang-eunit \
    gdc golang golang-doc golang-src golang-codesearch-dev \
    gcc gcc-doc gcc-5-source libcunit1 gdb gdb-doc cgdb xxgdb ccache \
    libboost-all-dev libglm-dev libglew-dev libglfw-dev ncurses-doc \
    libncurses5-dev libncursesw5-dev libpcre3-dev zlib1g-dev libbz2-dev \
    libgnome2-dev libgnomeui-dev libgtk2.0-dev libatk1.0-dev libbonoboui2-dev \
    libcairo2-dev libx11-dev libxpm-dev libxt-dev libgmp3-dev libmpc-dev \
    libmpfr-dev libcurl4-openssl-dev libevent-dev libarchive-dev libxslt1-dev \
    libblas-dev liblapack-dev libyaml-dev \
    openmpi-bin openmpi-checkpoint openmpi-common \
    gfortran \
    ghc ghc-doc ghc-haddock ghc-prof haskell-debian-utils \
    groovy groovy-doc \
    haskell-devscripts haskell-doc cabal-install \
    maven ant ant-doc \
    lua5.2 lua5.2-doc luadoc liblua5.2-dev \
    monodevelop-debugger-gdb monodevelop-nunit \
    nodejs nodejs-dev nodejs-legacy npm \
    perl perl-doc libperl-dev perl-modules libpadwalker-perl \
    libfile-next-perl \
    php5 php5-mysql phpunit php5-dev \
    swi-prolog swi-prolog-doc \
    python python-dev python-doc python-pip \
    python3 python3-dev python3-doc python3-pip jython jython-doc \
    pychecker pylint pep8 python-autopep8 ruby-full shunit2 \
    python-matplotlib python-numpy python-scipy \
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
        'https://github.com/magicmonty/bash-git-prompt.git',
        'https://github.com/starcraftman/zsh-git-prompt.git',
        'https://github.com/zsh-users/zsh-completions.git',
        'https://github.com/zsh-users/zsh-syntax-highlighting.git',
        'https://github.com/starcraftman/hhighlighter.git',
        'https://github.com/starcraftman/dot.git',
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

def install_pipelight():
    """ Silverlight plugin for firefox/chrome on linux.
    NB: Stuck on old build, no xenial support yet.
    http://www.webupd8.org/2013/08/pipelight-use-silverlight-in-your-linux.html
    """
    if os.getuid() != 0:
        raise NotSudo

    cmds = []
    cmd = subprocess.check_output('grep -rh pipelight/stable/ubuntu /etc/apt'.split())
    if 'pipelight' not in cmd:
        cmds += [
            'rm -rf ' + os.path.expanduser('~/.wine-pipelight'),
            'sudo add-apt-repository ppa:pipelight/stable',
            'sudo apt-get update',
            'sudo apt-get -y remove flashplugin-installer',
            'sudo apt-get -y install --install-recommends pipelight-multi',
        ]

    cmds += [
        'sudo pipelight-plugin --create-mozilla-plugins',
        'sudo pipelight-plugin --accept --enable flash',
        'sudo pipelight-plugin --accept --enable silverlight5.1',
        'sudo pipelight-plugin --create-mozilla-plugins',
    ]

    for cmd in cmds:
        subprocess.call(shlex.split(cmd))
    print("Installation over, remember to use a useragent switcher.")
    print("After running firefox installers, you may need to execute again:")
    print("  sudo pipelight-plugin --create-mozilla-plugins")


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
    pipelight    Install pipelight flash & silverlight.
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
        'pipelight':    install_pipelight,
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
