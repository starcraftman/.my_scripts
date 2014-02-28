#!/usr/bin/env bash
# I know this file is traditionally for user aliases.
# I am using it for all my custom bash modifications from standard.

# Check if term supports 256 -> http://www.robmeerman.co.uk/unix/256colours
# File to test: http://www.robmeerman.co.uk/_media/unix/256colors2.pl

# Default editor for things like sudoedit.
export EDITOR=vim

# Detect session type, may want ps1 mods for ssh.
if [ -n "$SSH_CLIENT" ] || [ -n "$SSH_TTY" ] || [ -n "$SSH_CONNECTION" ];then
    PS1_SSH=true
fi

############################################################################
# Path Settings
############################################################################
# Local dir to install to.
LOCAL=~/.optSoftware

# Personal scripts go here to stay outside of root.
MYSCRIPTS=~/.my_scripts

# Dir to locally install cabal for haskell.
HASKELL_BIN=~/.cabal/bin

# Exported paths.
ANDROID=$LOCAL/android-sdk-linux/tools:$LOCAL/android-sdk-linux/platform-tools:$LOCAL/android-ndk-r9c
EXTRALIB=$LOCAL/JDKExtraJARs/ExtraLibraryClasses:$LOCAL/JDKExtraJARs/JunitLibs
LIBDIR=/usr/local/lib
export JAVA_HOME=$LOCAL/jdk1.7.0_51
export LD_LIBRARY_PATH=$LIBDIR:$JAVA_HOME/jre/lib/amd64:$LD_LIBRARY_PATH
export LD_RUN_PATH=$LIBDIR:$LD_RUN_PATH
export PATH=$JAVA_HOME/bin:$MYSCRIPTS:$HASKELL_BIN:$ANDROID:$LOCAL/bin:$PATH
export CLASSPATH=$JAVA_HOME/lib:$EXTRALIB:.

# Paths for specific tools.
export ANT_HOME=/usr/share/ant
export HGMERGE=/usr/bin/kdiff3

#CCache Directory
#Info: https://ccache.samba.org/manual.html
export CCACHE_DIR=~/code/ccache

############################################################################
# Aliases
############################################################################
#Bash Aliases
alias lla='ls -la'
alias mkdir='mkdir -vp'

# Reruns the last command with sudo.
alias please='sudo `fc -l -n -1`'

# Use trash instead of RM, have had bad accidents. Need trash-cli library for python.
alias trash-restore="restore-trash"
alias tr="restore-trash"
alias tp="trash-put"
alias tl="trash-list"
alias te="trash-empty"
alias rm='echo "Don''t use. If must, \rm -Rf file."; false'

############################################################################
# Misc Options
############################################################################
# Enable the windows key on Ubuntu as F13
xmodmap -e 'keycode 133 = F13'

# Disable the Ctrl+s/q button that freezes terminal output.
stty -ixon

# KDE DEV Options:

# I have a kde-bashrc file with shortcuts for building.
# http://techbase.kde.org/Getting_Started/Build/Environment
#. ~/.kde-bashrc
#echo "NOTE IMPORTANT: make is now aliased to makeobj. Remove line from .bash_alias."

# Set default config environment. If need specialize, copy into dir of src tree.
#. ~/.build-config-default

############################################################################
# Functions
############################################################################
# Universal extract function, later versions of tar -xvf may work
# more universally but not with older versions.
function extract()
{
    if [ -f $1 ] ; then
        case $1 in
            *.deb)       ar p "$1" data.tar.gz | tar zx ;;
            *.rpm)       rpm2cpio "$1" | cpio -vid ;;
            *.tar)       tar xvf "$1"     ;;
            *.tar.bz2)   tar xvjf "$1"    ;;
            *.tar.gz)    tar xvzf "$1"    ;;
            *.tar.xz)    tar xvf "$1"     ;;
            *.tbz2)      tar xvjf "$1"    ;;
            *.tgz)       tar xvzf "$1"    ;;
            *.bz2)       bunzip2 "$1"     ;;
            *.gz)        gunzip "$1"      ;;
            *.rar)       unrar x "$1"     ;;
            *.zip)       unzip "$1"       ;;
            *.Z)         uncompress "$1"  ;;
            *.7z)        7z x "$1"        ;;
            *)           echo "'$1' cannot be extracted via >extract<" ;;
        esac
    else
        echo "'$1' is not a valid file!"
    fi
}

# Function to go back up when deep in directories.
# Example: .. 3 == cd ../../..
..() {
    if [ $1 -ge 0 2> /dev/null ]; then
        x=$1;
    else
        x=1;
    fi;

    for (( i = 0; i < $x; i++ )); do
        cd ..;
    done
}

############################################################################
# ALL PS1 past this point. This stuff used to modify the bash prompt to show
# the status of git and hg repos as well as move directory line up one.
############################################################################

# PS1 Color Codes
PS1_BLACK="\[\033[0;30m\]"
PS1_BLACKBOLD="\[\033[1;30m\]"
PS1_RED="\[\033[0;31m\]"
PS1_REDBOLD="\[\033[1;31m\]"
PS1_GREEN="\[\033[0;32m\]"
PS1_GREENBOLD="\[\033[1;32m\]"
PS1_YELLOW="\[\033[0;33m\]"
PS1_YELLOWBOLD="\[\033[1;33m\]"
PS1_BLUE="\[\033[0;34m\]"
PS1_BLUEBOLD="\[\033[1;34m\]"
PS1_PURPLE="\[\033[0;35m\]"
PS1_PURPLEBOLD="\[\033[1;35m\]"
PS1_CYAN="\[\033[0;36m\]"
PS1_CYANBOLD="\[\033[1;36m\]"
PS1_WHITE="\[\033[0;37m\]"
PS1_WHITEBOLD="\[\033[1;37m\]"
PS1_MAGENTA="\[\033[1;95m\]"
# To (R)eset colors.
PS1_R="\[\033[00m\]"

# Set colors for user/directory different if root or over ssh..
PS1_DIR=$PS1_REDBOLD
PS1_USER=$PS1_BLUEBOLD
PS1_HOST=$PS1_GREENBOLD
if [[ $UID -eq 0 ]]; then
    PS1_USER=$PS1_WHITEBOLD
fi
if [ -n "$PS1_SSH" ]; then
    PS1_HOST=$PS1_PURPLEBOLD
fi

# I am modifying the PS1 prompt to give info for both git and hg vcs.
# This callback fetches the hg stuff to insert only if in hg repo, looks like bash-git-prompt message.
# HG Prompt: http://sjl.bitbucket.org/hg-prompt/
# Git Prompt: https://github.com/magicmonty/bash-git-prompt
function prompt_callback {
    local HG=`hg prompt "[${PS1_MAGENTA}{branch}${PS1_R}{ ${PS1_RED}↓{incoming|count}${PS1_R}}{ ${PS1_GREEN}↑{outgoing|count}${PS1_R}}|${PS1_YELLOW}{status}{update}${PS1_R}]" 2>/dev/null`

    # Strip everything except where status to outgoing would be.
    local T=${HG##*|}
    T=${T%%]}

    # Insert check mark only if T doesn't contain other codes like status or update, see regexp.
    if [ "x${HG}" != "x" ]; then
        if [[ ${T} =~ [!?^↓↑] ]]; then
            :
        else
            HG="${HG%%]}${PS1_GREENBOLD}✔${PS1_R}]"
        fi
    fi

    # Print don't print extra space unless need to.
    if [ "x$HG" == "x" ]; then
        echo -n ""
    else
        echo -n " $HG"
    fi
}

# Formats to:
# directory
# user@host [vcsInfo]
#GIT_PROMPT_START="\[\e]0;\u@\h:\w\a\]${debian_chroot:+($debian_chroot)}$PS1_DIR\w$PS1_R\n$PS1_USER\u$PS1_R@$PS1_HOST\h$PS1_R$"
#GIT_PROMPT_END=' '

# Formats to:
# directory [vcsInfo]
# user@host
GIT_PROMPT_START="\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}$PS1_DIR\w$PS1_R"
GIT_PROMPT_END="\n$PS1_USER\u$PS1_R@$PS1_HOST\h$PS1_R$ "

. ~/.bash-git-prompt/gitprompt.sh

# Old PS1 modification.
# PS1 config options
#export GIT_PS1_SHOWDIRTYSTATE=1
#export GIT_PS1_SHOWSTASHSTATE=1
#export GIT_PS1_SHOWUNTRACKEDFILES=1
#export GIT_PS1_SHOWUPSTREAM="auto verbose"

# PS1 changes for git.
# http://techbase.kde.org/Development/Git/Configuration
# More info: http://blog.sanctum.geek.nz/bash-prompts/
# PS1='\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\u@\h:\w\$ $(__git_ps1 "${color_blue}(%s)${color_reset}")'
