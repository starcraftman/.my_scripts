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
import functools
import glob
import itertools
import multiprocessing
import os
import re
import shutil
import subprocess
import sys
import tarfile
import zipfile
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
    colormake colordiff colorgcc jq \
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
    libcurl4-openssl-dev libevent-dev \
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

PY_PACKS = "argcomplete Pygments pytest trash-cli"

URL_CMAKE = 'http://www.cmake.org/files/v3.0/cmake-3.0.2.tar.gz'
URL_PYTHON = 'https://www.python.org/ftp/python/2.7.8/Python-2.7.8.tgz'
URL_TMUX = 'http://sourceforge.net/projects/tmux/files/tmux/tmux-1.9/\
tmux-1.9a.tar.gz/download?use_mirror=hivelocity'
URL_ZSH = 'http://sourceforge.net/projects/zsh/files/zsh/5.0.6/\
zsh-5.0.6.tar.bz2/download'

if os.path.exists('/proc/cpuinfo'):
    NUM_JOBS = int(subprocess.check_output('cat /proc/cpuinfo | \
        grep processor | wc -l', shell=True))
else:
    NUM_JOBS = 2

TMP_DIR = '/tmp/SysInstall'
BUILDS = {
    'ack': {
        'name' : 'ack',
        'check': 'bin/ack',
        'url'  : 'https://github.com/petdance/ack2.git',
        'cmds' : [
            'perl Makefile.PL',
            'make ack-standalone',
            'make manifypods',
        ],
        'globs': [
            ('ack-standalone', 'bin/'),
            ('ack-standalone', 'bin/ack'),
            ('blib/man1/*.1*', 'share/man/man1/'),
        ],
    },
    'ag': {
        'name' : 'ag',
        'check': 'bin/ag',
        'url'  : 'https://github.com/ggreer/the_silver_searcher.git',
        'cmds' : [
            './build.sh --prefix=TARGET',
            'make install',
        ],
    },
    'atom': {
        'name' : 'atom',
        'check': 'bin/atom',
        'url'  : 'https://github.com/atom/atom',
        'cmds' : [
            'script/build',
            'script/grunt install --install-dir TARGET',
        ],
    },
    'cmake': {
        'name' : 'cmake',
        'check': 'bin/cmake',
        'url'   : URL_CMAKE,
        'cmds' : [
            './bootstrap --prefix=TARGET --docdir=share/doc/cmake-3.0 \
            --mandir=share/man --enable-ccache --qt-gui --sphinx-man \
            --sphinx-html',
            'make -jJOBS',
            'make install',
        ],
    },
    'doxygen': {
        'name' : 'doxygen',
        'check': 'bin/doxygen',
        'url'  : 'https://github.com/doxygen/doxygen.git',
        'cmds' : [
            './configure --prefix=TARGET',
            'make -jJOBS',
        ],
        'globs': [
            ('bin/doxygen', 'bin/'),
            ('doc/*.1', 'share/man/man1/'),
        ],
    },
    'parallel': {
        'name' : 'parallel',
        'check': 'bin/parallel',
        'url'  : 'http://ftp.gnu.org/gnu/parallel/parallel-latest.tar.bz2',
        'cmds' : [
            './configure --prefix=TARGET',
            'make -jJOBS install',
        ],
    },
    'python': {
        'name' : 'python',
        'check': 'bin/python',
        'url'  : URL_PYTHON,
        'cmds' : [
            './configure --prefix=TARGET',
            'make',
            'make install',
        ],
    },
    'tmux': {
        'name' : 'tmux',
        'check': 'bin/tmux',
        'url'  : URL_TMUX,
        'cmds' : [
            './configure --prefix=TARGET',
            'make -jJOBS install',
        ],
    },
    'vim': {
        'name' : 'vim',
        'check': 'bin/vim',
        'url'  : 'https://code.google.com/p/vim/',
        'cmds' : [
            './configure --with-features=huge --enable-gui=gtk2 \
            --enable-cscope --enable-multibyte --enable-luainterp \
            --enable-perlinterp --enable-pythoninterp \
            --with-python-config-dir=/usr/lib/python2.7/config \
            --prefix=TARGET',
            'make VIMRUNTIMEDIR=TARGET/share/vim/vim74',
            'make install',
        ],
    },
    'vimpager': {
        'name' : 'vimpager',
        'check': 'bin/vimpager',
        'url'  : 'https://github.com/rkitover/vimpager.git',
        'globs': [
            ('vimcat', 'bin/'),
            ('vimpager', 'bin/'),
            ('*.1', 'share/man/man1/'),
        ],
    },
    'zsh': {
        'name' : 'zsh',
        'check': 'bin/zsh',
        'url'  : 'https://github.com/zsh-users/zsh.git',
        'cmds' : [
            './Util/preconfig',
            'autoconf',
            './configure --prefix=TARGET --enable-cap --enable-pcre \
            --enable-maildir-support',
            'make',
            'make install',
        ],
    },
    'zsh_docs': {
        'name' : 'zsh_docs',
        'check': 'share/man/man1/zshall.1',
        'url'  : URL_ZSH,
        'globs': [
            ('Doc/*.1', 'share/man/man1/'),
        ],
    },
}

# Classes

class NotSudo(Exception):
    """ Throw this if we aren't sudo but need to be. """
    pass

class ArchiveNotSupported(Exception):
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
        curdir = os.path.abspath(os.curdir)
        PDir.dirs.append(curdir)
        os.chdir(new_dir)
        print("%s >>> %s" % (curdir, new_dir))
    @staticmethod
    def pop():
        """ Pop the dirstack and return to it. """
        old_dir = PDir.dirs.pop()
        os.chdir(old_dir)
        print(">>> %s" % old_dir)

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

def find_archive(url):
    """ Given a url, returns archive name found inside.
    If extension not supported throws excetion. """
    arc_ext = None
    for ext in ['.tgz', '.tbz2', '.tar.bz2', '.tar.gz', 'tar.xz',
            '.xz', '.rar', '.zip', '.7z']:
        right = url.rfind(ext)
        if right != -1:
            right += len(ext)
            left = url.rfind(os.sep, 0, right) + 1
            arc_ext = ext
            break

    if arc_ext == None:
        raise ArchiveNotSupported

    return url[left:right]

def extract_archive(archive):
    """ Given an archive, extract it. Prefer python libs if supported. """
    if tarfile.is_tarfile(archive):
        with tarfile.open(archive) as tarf:
            tarf.extractall()
    if zipfile.is_zipfile(archive):
        with zipfile.ZipFile(archive) as zipf:
            zipf.extractall()
    else:
        cmd = 'unarchive ' + archive
        subprocess.call(cmd.split())

def get_archive(url, target):
    """ Fetch an archive from a site. Works on regular ftp & sourceforge.
    Wish sourceforge wasn't a pain...

    url: location to get archive
    target: where to extract to
    """
    arc_name = find_archive(url)

    tmp_file = TMP_DIR + os.path.sep + arc_name
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)

    if not os.path.exists(target):
        os.makedirs(target)
        os.rmdir(target)

    try:
        # Using wget because of sourceforge corner case
        cmd = 'wget -O %s %s' % (tmp_file, url)
        subprocess.call(cmd.split())

        extract_archive(tmp_file)

        # extracted dir doesn't always match arc_name, glob to be sure
        arc_front = re.split('[-_]', arc_name)[0] + '*'
        extracted = None
        for name in glob.glob(arc_front):
            if name != arc_name:
                extracted = name

        os.rename(extracted, target)
    finally:
        if os.path.exists(tmp_file):
            os.remove(tmp_file)
        if os.path.exists(extracted):
            shutil.rmtree(extracted)

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

def build_src(build, target=None):
    """ Build a project downloeaded from url. build is a json object.
        The format is described below.
        Cmds are executed in srcdir, then if globs non-empty copy files as
        described in glob/target pairs.
        Required names prefixed with R.
        {
          R 'name': 'ack',
          R 'check': 'path/to/check',
          R 'url' : 'https://github.com/petdance/ack2.git',
            'tdir': /path/to/install/to,
            'cmds': [
                'perl Makefile.PL',
                'make ack-standalone',
                'make manifypods'
            ],
            'globs': [
                ('ack-standalone', 'bin/ack'),
                ('blib/man1/*.1*', 'share/man/man1')
            ]
        }
    """
    tdir = os.path.abspath(build.get('tdir', target))
    srcdir = '%s/src/%s' % (tdir, build['name'])

    # Guard if command exists
    if os.path.exists(tdir + os.sep + build['check']):
        return

    try:
        get_archive(build['url'], srcdir)
    except ArchiveNotSupported:
        get_code(build['url'], srcdir)

    try:
        # Code should be at srcdir by here.
        PDir.push(srcdir)
        for cmd in build.get('cmds', []):
            cmd = cmd.replace('TARGET', tdir)
            cmd = cmd.replace('JOBS', '%d' % NUM_JOBS)
            subprocess.call(cmd.split())
        PDir.pop()

        # Manual copies sometimes required to finish install
        for pattern, target in build.get('globs', []):
            dest = tdir + os.sep + target
            if dest.endswith('/') and not os.path.exists(dest):
                os.makedirs(dest)

            for sfile in glob.glob(srcdir + os.sep + pattern):
                if os.path.isfile(sfile):
                    shutil.copy(sfile, dest)
    finally:
        shutil.rmtree(srcdir)

    print('Finished building ' + build['name'])

def build_wrap(args):
    """ Wrapper for build_src in process pool. """
    build_src(*args)

def build_pool(builds, target):
    """ Take a series of build objects and use a pool of workers
        to build them and install to target.
        NB: Blocks until all workers finished.
    """
    pool_args = itertools.izip(builds, itertools.repeat(target))
    pool = multiprocessing.Pool()
    pool.map_async(build_wrap, pool_args)
    pool.close()
    pool.join()

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
                print("{} >>>>> {}".format(dfile, sfile))
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

    # Init vundle for vim plugin install.
    ddir = home + '.vim' + os.sep + 'bundle' + os.sep
    get_code('https://github.com/gmarik/Vundle.vim.git', ddir + 'Vundle.vim')

    # Get shell utilities
    shell_dir = home + '.shell' + os.sep
    get_code('http://bitbucket.org/sjl/hg-prompt/', shell_dir + '.hg-prompt')

    git_urls = [
        'https://github.com/magicmonty/bash-git-prompt.git',
        'https://github.com/starcraftman/zsh-git-prompt.git',
        'https://github.com/starcraftman/zsh-completions.git',
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
        subprocess.call(cmd.split())

    # Create dir for ccache
    ddir = home + '.ccache'
    if not os.path.exists(ddir):
        os.mkdir(ddir)

    print("NOTE: Remember to add user to smb.\nsudo smbpasswd -a username")

def restore_home():
    """ Undo changes by home_config & restore backup if exists. """
    arc_dir = os.path.expanduser('~/.home_bak/')
    home = os.path.expanduser('~/')
    dot_files = home + '.my_scripts' + os.path.sep + 'dot_files' + os.path.sep

    for folder in ('.shell', '.fonts', '.ccache',):
        shutil.rmtree(home + folder)

    # Clear existing configs if they are symlinks
    files = glob.glob(dot_files + '.*')
    files = [x[x.rindex(os.sep)+1:] for x in files]
    for fil in [home + fil for fil in files]:
        if os.path.islink(fil):
            os.remove(fil)

    arc_files = glob.glob(arc_dir + '.*')
    arc_files = [x[x.rindex(os.sep)+1:] for x in arc_files]

    helper = make_cmd(arc_dir, home)
    helper(arc_files, os.rename)

    os.rmdir(arc_dir)

def save_home():
    """ Save existing home configs to a backup dir. """
    arc_dir = os.path.expanduser('~/.home_bak/')
    home = os.path.expanduser('~/')
    dot_files = home + '.my_scripts' + os.path.sep + 'dot_files' + os.path.sep

    if not os.path.exists(arc_dir):
        os.makedirs(arc_dir)

    files = glob.glob(dot_files + '.*')
    files = [x[x.rindex(os.sep)+1:] for x in files]
    files = [x for x in files if os.path.exists(home + x)]

    helper = make_cmd(home, arc_dir)
    helper(files, os.rename)

def packs_babun():
    """ Setup a fresh babun install. """
    # Install packages
    cmd = 'pact install ' + BABUN
    subprocess.call(cmd.split())

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
    subprocess.call(cmd.split())

    cmd = 'cabal install ' + CABAL
    subprocess.call(cmd.split())

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
    subprocess.call(cmd.split())

    # Install python completion to system bash_completion.d.
    cmd = 'activate-global-python-argcomplete --user'
    subprocess.call(cmd.split())

def install_jshint():
    """ Setup jshint for progrmaming javascript with vim. """
    cmd = 'npm install jshint -g'
    subprocess.call(cmd.split())

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
    save_home    Save existing home files.
    restore_home Restore home files and undo home_config.
    debian       Install debian packages.
    babun        Install babun packages.
    pip          Install python libraries via pip.
    cabal        Install haskell packages for eclipse.
    jshint       Install jshint via npm for javascript vim.
    pipelight    Install pipelight flash & silverlight.
    atom         Build latest atom editor by GitHub.
    cmake        Build latest cmake from source.
    dev          Build standard dev progs like ag, ack, parallel.
    doxygen      Build latest doxygen from source.
    python       Build latest python from source.
    tmux         Build the latest tmux from source.
    vim          Build latest vim from source.
    zsh          Build latest zsh from source.
    """

    # Simple wrapper saves func
    odir = os.path.expanduser('~/.opt1')
    builds = []

    # Use a dict of funcs to process args
    actions = {
        'home':         home_config,
        'restore_home': restore_home,
        'save_home':    save_home,
        'debian':       packs_debian,
        'babun':        packs_babun,
        'pip':          packs_py,
        'cabal':        packs_cabal,
        'jshint':       install_jshint,
        'pipelight':    install_pipelight,
        'dev':          functools.partial(builds.extend, ('ag', 'ack',
                        'parallel', 'vimpager', 'zsh_docs')),
    }
    # Generate this part dynamically
    gen_actions = {key: functools.partial(builds.append, key)
        for key in ('atom', 'cmake', 'doxygen', 'python', 'tmux', 'vim', 'zsh')}
    actions.update(gen_actions)

    parser = argparse.ArgumentParser(description=mesg,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-o', '--odir', nargs='?', default=None,
            help='install dir')
    parser.add_argument('stages', nargs='+', help='stages to execute',
            choices=actions.keys())

    autocomplete(parser)
    args = parser.parse_args()  # Default parses argv[1:]

    # Nicer override than OPTDIR
    if args.odir != None:
        odir = args.odir

    try:
        for stage in args.stages:
            actions[stage]()

        # build the components in parallel
        build_objs = [BUILDS[name] for name in builds]
        build_pool(build_objs, odir)

    except IOError as exc:
        print('Failed to install: {}'.format(exc))
    except NotSudo:
        print("Rerun this part of script with sudo.")

if __name__ == '__main__':
    main()
