#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
""" Install packages and setup home configs on fresh system. """

# Imports
from __future__ import print_function
from BuildSrc import get_code
import argparse
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
PROGRAMS = """ \
    htop iotop itop mytop pkg-config aptitude synaptic dos2unix oxygen-molecule \
    kubuntu-restricted-extras kubuntu-restricted-addons \
    brother-cups-wrapper-laser brother-cups-wrapper-laser1 \
    brother-lpr-drivers-laser brother-lpr-drivers-laser1 \
    k3b kid3 krita kolourpaint4 kchmviewer yakuake plasma-widget-quickaccess \
    kdirstat keepassx screen tmux \
    chromium-browser firefox rekonq \
    abiword baobab dvdrip easytag chm2pdf dia catdoc \
    gimp gimp-plugin-registry \
    fuse gparted quicksynergy tree dfc sharutils sharutils-doc \
    libnotify-bin libnotify-dev \
    redshift geoclue geoclue-hostip numlockx \
    samba samba-doc samba-dev samba-dbg cifs-utils wireshark libwireshark-dev wondershaper \
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
    build-essential debianutils ubuntu-dev-tools mesa-utils openssh-server \
    automake automake1.9-doc ant ant-doc checkinstall checkbox \
    dkms docbook make-doc lynx kdiff3 kdiff3-doc patch rpm2cpio rpm \
    codeblocks kdevelop qt-sdk \
    colormake colordiff colorgcc jq nmap \
    vim vim-doc vim-gtk vim-rails vim-syntax-go vim-syntax-gtk vim-doc \
    flex flex-doc bison bison-doc graphviz exuberant-ctags sphinx-common sphinx-doc \
    bash-doc bash-builtins bashdb zsh zsh-dbg zsh-dev zsh-doc zsh-lovers zshdb \
    clisp clisp-doc clisp-dev clisp-module-gdbm \
    coffeescript coffeescript-doc \
    docutils-common docutils-doc \
    erlang erlang-eunit \
    gdc golang golang-doc golang-src golang-codesearch-dev \
    gcc gcc-doc gcc-4.7-source libcunit1 gdb gdb-doc cgdb xxgdb ccache \
    libboost-all-dev libglm-dev libglew-dev libglfw-dev ncurses-doc \
    libncurses5-dev libncursesw5-dev libpcre3-dev zlib1g-dev liblzma-dev libbz2-dev \
    libgnome2-dev libgnomeui-dev libgtk2.0-dev libatk1.0-dev libbonoboui2-dev \
    libcairo2-dev libx11-dev libxpm-dev libxt-dev libgmp3-dev libmpc-dev libmpfr-dev \
    libcurl4-openssl-dev libevent-dev libarchive-dev libcurl4-gnutls-dev \
    openmpi-bin openmpi-checkpoint openmpi-common \
    gfortran \
    ghc ghc-doc ghc-haddock ghc-prof haskell-debian-utils \
    haskell-devscripts haskell-doc cabal-install \
    junit junit-doc maven openjdk-7-doc openjdk-7-jdk openjdk-7-dbg \
    openjdk-7-source openjdk-7-demo icedtea-7-plugin \
    lua5.2 lua5.2-doc luadoc liblua5.2-dev \
    monodevelop-debugger-gdb monodevelop-nunit \
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

PY_PACKS = "argcomplete Pygments pytest trash-cli"

# Classes

class NotSudo(Exception):
    """ Throw this if we aren't sudo but need to be. """
    pass

# Functions

def make_cmd(src, dst):
    """ Generate a function helper. """
    def cmd_when_dst_empty(files, command, opts=None):
        """ When dst doesn't have file do:
                command(src + file, dst + file, *opts)
        """
        if opts == None:
            opts = ()
        for fil in files:
            sfile, dfile = [x + fil for x in (src, dst)]
            if not os.path.exists(dfile):
                print("{0} >>>>> {1}".format(dfile, sfile))
                command(sfile, dfile, *opts)
    return cmd_when_dst_empty

def home_config():
    """ Setup the dev environment, stuff goes in the user's home folder. """
    script_path = os.path.relpath(__file__)
    script_dir = os.path.dirname(script_path)
    if script_dir == '':
        script_dir = '.'

    # Leaving trailing sep for ease later.
    src = script_dir + os.sep + 'dot_files' + os.sep
    home = os.path.expanduser('~') + os.sep

    # Glob all files in dot_files and link them to home
    files = glob.glob(src + '.*')
    files = [x[x.rindex(os.sep)+1:] for x in files]
    helper = make_cmd(src, home)
    helper(files, os.symlink)

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
        cmd = 'fc-cache -vf ' + ddir
        subprocess.call(shlex.split(cmd))

    # Create dir for ccache
    ddir = home + '.ccache'
    if not os.path.exists(ddir):
        os.mkdir(ddir)

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
    files = glob.glob(dot_dir + '.*')
    files = [x[x.rindex(os.sep)+1:] for x in files]
    for fil in [home + fil for fil in files]:
        if os.path.islink(fil):
            os.remove(fil)

    arc_files = glob.glob(arc_dir + '.*')
    arc_files = [x[x.rindex(os.sep)+1:] for x in arc_files]

    helper = make_cmd(arc_dir, home)
    helper(arc_files, os.rename)

    os.rmdir(arc_dir)

def home_save():
    """ Save existing home configs to a backup dir. """
    arc_dir = os.path.expanduser('~/.home_bak/')
    home = os.path.expanduser('~/')
    dot_dir = home + '.my_scripts' + os.path.sep + 'dot_files' + os.path.sep

    if not os.path.exists(arc_dir):
        os.makedirs(arc_dir)

    files = glob.glob(dot_dir + '.*')
    files = [x[x.rindex(os.sep)+1:] for x in files]
    files = [x for x in files if os.path.exists(home + x)]

    helper = make_cmd(home, arc_dir)
    helper(files, os.rename)

def packs_babun():
    """ Setup a fresh babun install. """
    # Install packages
    cmd = 'pact install ' + BABUN
    subprocess.call(shlex.split(cmd))

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
    cmd = 'cabal update'
    subprocess.call(shlex.split(cmd))

    cmd = 'cabal install ' + CABAL
    subprocess.call(shlex.split(cmd))

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
        'pipelight-plugin --enable silverlight',
        'pipelight-plugin --enable flash',
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
        'jshint':       install_jshint,
        'pip':          packs_py,
        'pipelight':    install_pipelight,
    }
    parser = argparse.ArgumentParser(description=mesg,
            formatter_class=argparse.RawDescriptionHelpFormatter)
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
