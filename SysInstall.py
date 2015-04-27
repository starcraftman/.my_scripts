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
    vim build-essential git-core mercurial automake ccache fontconfig gdb lynx \
    colormake colordiff colorgcc exuberant-ctags dkms python-dev python-pip \
    tcl p7zip-full rar zip unzip gzip lzip xz-utils liblzma5 \
    htop dos2unix tree dfc flex bison sphinx-common gettext libfile-next-perl \
    libexpat-dev liblzma-dev libpcre3-dev libcurl4-dev libarchive-dev libevent-dev \
    """

PROGRAMS = """ \
    htop iotop itop mytop pkg-config aptitude synaptic dos2unix \
    oxygen-molecule kubuntu-restricted-extras kubuntu-restricted-addons \
    brother-cups-wrapper-laser brother-cups-wrapper-laser1 \
    brother-lpr-drivers-laser brother-lpr-drivers-laser1 \
    k3b kid3 krita kolourpaint4 kchmviewer yakuake plasma-widget-quickaccess \
    k4dirstat keepassx screen tmux \
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
    automake automake1.9-doc ant ant-doc checkinstall checkbox \
    dkms docbook make-doc lynx kdiff3 kdiff3-doc patch rpm2cpio rpm \
    codeblocks kdevelop qt-sdk graphviz \
    colormake colordiff colorgcc jq nmap \
    vim vim-doc vim-gtk vim-rails vim-syntax-go vim-syntax-gtk vim-doc \
    re2c flex flex-doc bison bison-doc exuberant-ctags sphinx-common sphinx-doc \
    bash-doc bash-builtins bashdb \
    zsh zsh-dbg zsh-dev zsh-doc zsh-lovers zshdb \
    clisp clisp-doc clisp-dev clisp-module-gdbm \
    coffeescript coffeescript-doc \
    docutils-common docutils-doc asciidoc xmlto docbook2x \
    erlang erlang-eunit \
    gdc golang golang-doc golang-src golang-codesearch-dev \
    gcc gcc-doc gcc-4.7-source libcunit1 gdb gdb-doc cgdb xxgdb ccache \
    libboost-all-dev libglm-dev libglew-dev libglfw-dev ncurses-doc \
    libncurses5-dev libncursesw5-dev libpcre3-dev zlib1g-dev libbz2-dev \
    libgnome2-dev libgnomeui-dev libgtk2.0-dev libatk1.0-dev libbonoboui2-dev \
    libcairo2-dev libx11-dev libxpm-dev libxt-dev libgmp3-dev libmpc-dev \
    libmpfr-dev libcurl4-openssl-dev libevent-dev libarchive-dev libxslt1-dev \
    openmpi-bin openmpi-checkpoint openmpi-common \
    gfortran \
    ghc ghc-doc ghc-haddock ghc-prof haskell-debian-utils \
    groovy groovy-doc \
    haskell-devscripts haskell-doc cabal-install \
    junit junit-doc maven openjdk-7-doc openjdk-7-jdk openjdk-7-dbg \
    openjdk-7-source openjdk-7-demo icedtea-7-plugin \
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

PY_PACKS = "argcomplete cram neovim Pygments pytest trash-cli"


class NotSudo(Exception):
    """ Throw this if we aren't sudo but need to be. """
    pass


def make_cmd(src, dst):
    """ Generate a function helper. """
    def cmd_when_dst_empty(files, command, opts=None):
        """ When dst doesn't have file do:
                command(src + file, dst + file, *opts)
        """
        if opts is None:
            opts = ()
        for fil in files:
            sfile, dfile = [x + fil for x in (src, dst)]
            if not os.path.exists(dfile):
                print("{0} >>>>> {1}".format(sfile, dfile))
                command(sfile, dfile, *opts)
    return cmd_when_dst_empty


def home_config():
    """ Setup the dev environment, stuff goes in the user's home folder. """
    script_path = os.path.relpath(__file__)
    script_dir = os.path.dirname(script_path)
    if script_dir == '':
        script_dir = '.'

    dot_dir = script_dir + os.sep + 'dot_files' + os.sep
    home = os.path.expanduser('~') + os.sep

    # Get shell utilities
    shell_dir = home + '.shell' + os.sep
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

    get_code('https://bitbucket.org/sjl/hg-prompt/', shell_dir + '.hg-prompt')

    # Setup powerline fonts if not done.
    ddir = home + '.fonts'
    dpow = ddir + os.sep + 'powerline-fonts'
    if not os.path.exists(ddir) and subprocess.call(['which', 'fc-cache']) == 0:
        os.mkdir(ddir)
        get_code('https://github.com/Lokaltog/powerline-fonts', dpow)
        subprocess.call(['fc-cache', '-vf', ddir])

    ddir = home + '.ccache'
    if not os.path.exists(ddir):
        os.mkdir(ddir)

    files = [os.path.basename(x) for x in glob.glob(dot_dir + '.*')]
    helper = make_cmd(dot_dir, home)
    helper(files, os.symlink)

    print("NOTE: Remember to add user to smb.\nsudo smbpasswd -a username")


def home_restore():
    """ Undo changes by home_config & restore backup if exists. """
    arc_dir = os.path.expanduser('~/.home_bak/')
    home = os.path.expanduser('~/')
    dot_dir = home + '.my_scripts' + os.path.sep + 'dot_files' + os.path.sep

    for folder in ('.shell', '.fonts', '.ccache',):
        try:
            shutil.rmtree(home + folder)
        except OSError:
            pass

    # Clear existing configs if they are symlinks
    files = [os.path.basename(x) for x in glob.glob(dot_dir + '.*')]
    for fil in [home + fil for fil in files]:
        if os.path.islink(fil):
            os.remove(fil)

    arc_files = [os.path.basename(x) for x in glob.glob(arc_dir + '.*')]
    helper = make_cmd(arc_dir, home)
    helper(arc_files, os.rename)

    try:
        os.rmdir(arc_dir)
    except OSError:
        pass


def home_save():
    """ Save existing home configs to a backup dir. """
    arc_dir = os.path.expanduser('~/.home_bak/')
    home = os.path.expanduser('~/')
    dot_dir = home + '.my_scripts' + os.path.sep + 'dot_files' + os.path.sep

    if not os.path.exists(arc_dir):
        os.makedirs(arc_dir)

    files = [os.path.basename(x) for x in glob.glob(dot_dir + '.*')]
    files = [x for x in files if os.path.exists(home + x)]

    helper = make_cmd(home, arc_dir)
    helper(files, os.rename)


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
    http://www.webupd8.org/2013/08/pipelight-use-silverlight-in-your-linux.html
    """
    if os.getuid() != 0:
        raise NotSudo

    cmds = [
        'sudo apt-get remove flashplugin-installer',
        'sudo apt-add-repository ppa:pipelight/stable',
        'sudo apt-get update',
        'sudo apt-get install pipelight-multi',
        'pipelight-plugin --accept --enable silverlight',
        'pipelight-plugin --accept --enable flash',
    ]
    cmds = [x.split() for x in cmds]
    for cmd in cmds:
        subprocess.call(cmd)
    print("Installation over, remember to use a useragent switcher.")


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
