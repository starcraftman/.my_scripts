#!/usr/bin/env bash
# I know this file is traditionally for user aliases.
# I am using it for all my custom bash modifications from standard.

# Check if term supports 256 -> http://www.robmeerman.co.uk/unix/256colours
# File to test: http://www.robmeerman.co.uk/_media/unix/256colors2.pl

# Neat bash tricks, http://blog.sanctum.geek.nz/category/bash
# Some other tricks, http://www.tldp.org/LDP/abs/html/sample-bashrc.html
############################################################################
# Environment Variables
############################################################################
#{{{
# Default editor for things like sudoedit.
if hash vim 2>/dev/null; then
    export EDITOR=vim
fi

# Change grep color to bold blue
export GREP_COLORS='ms=01;34:mc=01;34:sl=:cx=:fn=35:ln=32:bn=32:se=36'

# Bash history options
# Set large history file & line limit
export HISTFILESIZE=100000
export HISTSIZE=100000

# Ignore some commands
export HISTIGNORE='ls *:l *:bg:fg:history'

# Timestamps in history file
export HISTTIMEFORMAT='%F %T '

# Ignore duplicate commands in history
export HISTCONTROL=ignoredups:erasedups

# Default pager
export PAGER=less
#}}}
############################################################################
# Path Settings
############################################################################
#{{{
# Local dir to install to, put binaries into ~/.optSoftware/bin.
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
#}}}
############################################################################
# Aliases
############################################################################
#{{{
# Note: First word of alias is expanded as alias, others ignored. Hence ll, expands ls.
# Make ls more convenient
alias ls='ls --color=auto -F --group-directories-first'
alias ll='ls -Alh'
alias la='ls -A'
alias l='ls'

# Different sorts
alias lx='ll -XB'
alias lk='ll -Sr'
alias lt='ll -tr'
alias lc='ll -tcr'
alias lu='ll -tur'

# Tree program, use instead of recursive ls. Very pretty.
alias tree='tree -Csuh'

# Always create non-existing parent dirs
alias mkdir='mkdir -vp'

# df/du defaults, du -L to follow symlinks
alias df='df -hT'
alias du='du -h'

# type used to determine what command is, list all entries
alias types='type -a'

# Reruns the last command with sudo.
alias please='sudo `fc -l -n -1`'

# Use trash instead of RM, have had bad accidents. Need trash-cli library for python.
alias trash-restore='restore-trash'
alias tr='restore-trash'
alias tp='trash-put'
alias tl='trash-list'
alias te='trash-empty'
alias rm='echo "Don''t use. If must, \rm -Rf file."; false'

# Silence parallel
alias parallel='parallel --no-notice'

# Alias for silver search
# For type use --type, i.e. --cpp. supported types -> 'ag --list-file-types
alias ag='ag --smart-case --follow --color-match="1;34"'
# Alias for file name searc
alias agf='ag -g'

# Default ack options, use smart case, sort output by file and follow symlinks.
# Filter by type with --type, supported types `ack --help-types`
alias ack='ack --smart-case --sort-files --follow --color-match="bold blue"'
# Alias for ack find file
alias ackf='ack -g'

# Grep should always print line
alias grep='grep --color=auto -n --exclude-dir=.git --exclude-dir=.hg --exclude-dir=.bzr --exclude-dir=.svn --exclude-dir=.cvs'
# Re alias these to take advantage of above
alias egrep='grep -E'
alias fgrep='grep -F'
alias rgrep='grep -r'

# Alias for color tools.
alias cod='colordiff'
alias com='colormake'
alias cog='colorgcc'

# Always open with splits
alias vims='vim -o'

# Set debug for bash
alias debug='set -o nounset; set -o xtrace'
alias debugoff='set +o nounset; set +o xtrace'
#}}}
############################################################################
# Functions
############################################################################
#{{{
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
function ..()
{
    if [ $1 -ge 0 2> /dev/null ]; then
        x=$1;
    else
        x=1;
    fi;

    for (( i = 0; i < $x; i++ )); do
        cd ..;
    done
}

function lastExit()
{
    echo $?
}

function jsonFix()
{
    cat "$1" | python -m json.tool > "fix_$1"
}

# Useful functions almost entirely taken from:
#http://www.tldp.org/LDP/abs/html/sample-bashrc.html
function my_ip() # Get IP adress on ethernet.
{
    MY_IP=$(/sbin/ifconfig eth0 | awk '/inet/ { print $2 } ' |
      sed -e s/addr://)
    echo ${MY_IP:-"Not connected"}
}
function mydf()         # Pretty-print of 'df' output.
{                       # Inspired by 'dfc' utility.
    for fs ; do

        if [ ! -d $fs ]
        then
          echo -e $fs" :No such file or directory" ; continue
        fi

        local info=( $(command df -P $fs | awk 'END{ print $2,$3,$5 }') )
        local free=( $(command df -Pkh $fs | awk 'END{ print $4 }') )
        local nbstars=$(( 20 * ${info[1]} / ${info[0]} ))
        local out="["
        for ((j=0;j<20;j++)); do
            if [ ${j} -lt ${nbstars} ]; then
               out=$out"*"
            else
               out=$out"-"
            fi
        done
        out=${info[2]}" "$out"] ("$free" free on "$fs")"
        echo -e $out
    done
}

function ii()   # Get current host related info.
{
    local BBlue='\e[1;34m'
    local NC="\e[m"
    echo
    echo -e "You are logged on ${BBlue}$HOSTNAME"
    echo -e "${BBlue}Additionnal information:$NC " ; uname -a
    echo -e "${BBlue}Users logged on:$NC " ; w -hs |
             cut -d " " -f1 | sort | uniq
    echo -e "${BBlue}Current date :$NC " ; date
    echo -e "${BBlue}Machine stats :$NC " ; uptime
    echo -e "${BBlue}Memory stats :$NC " ; free
    echo -e "${BBlue}Diskspace :$NC " ; mydf / $HOME
    echo -e "${BBlue}Local IP Address :$NC" ; my_ip
    echo -e "${BBlue}Open connections :$NC "; netstat -pan --inet;
    echo
}

# Highlight many terms with different colors
# Usage: find . | h term1 term2 term3
source $HOME/.hhighlighter/h.sh
#}}}
############################################################################
# Shell Settings
############################################################################
#{{{
# https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html
# Set debug flags permanently on
#set -o nounset
#set -o xtrace

# Brace expand allows: echo a{b,c}e -> abe ace
set -o braceexpand

# Bg jobs notify immediately on terminate, else only when next prompt draw
set -o notify

# http://www.gnu.org/software/bash/manual/html_node/The-Shopt-Builtin.html
# If arg to cd doesn't exist, must be var to expand
shopt -s cdable_vars

# When making small typos with cd, go to best match
shopt -s cdspell

# Always append instead of overwriting history
shopt -s histappend

# Multiline commands to be on single lines in history
shopt -s cmdhist

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# Ensure extended globbing allowed
shopt -s extglob

# Don't expand empty commands
shopt -s no_empty_cmd_completion

# Shell not needed for mail checking
shopt -u mailwarn
unset MAILCHECK
#}}}
############################################################################
# Misc Options
############################################################################
#{{{
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

#}}}
############################################################################
# PS1 Bash Propmt
############################################################################
#{{{
# ALL PS1 past this point. This stuff used to modify the bash prompt to show
# the status of git and hg repos as well as move directory line up one.
# Color code explanation, end of -> http://jamiedubs.com/ps1-collection-customize-your-bash-prompt

# PS1 Color Codes
# Old code (might still see): \[\033[x;yy;zzm\]
# General format: \[\e[x;yy;zzm\]
# Style code x: 1 -> bold, 4 -> underline, 7 -> invert color.
# Color code, yy -> 30s for foreground, zz-> background in 40s.
#PS1_BLACK="\[\e[0;30m\]"
#PS1_BLACKBOLD="\[\e[1;30m\]"
PS1_RED="\[\e[0;31m\]"
PS1_REDBOLD="\[\e[1;31m\]"
PS1_GREEN="\[\e[0;32m\]"
PS1_GREENBOLD="\[\e[1;32m\]"
PS1_YELLOW="\[\e[0;33m\]"
PS1_YELLOWBOLD="\[\e[1;33m\]"
#PS1_BLUE="\[\e[0;34m\]"
PS1_BLUEBOLD="\[\e[1;34m\]"
#PS1_PURPLE="\[\e[0;35m\]"
PS1_PURPLEBOLD="\[\e[1;35m\]"
PS1_CYAN="\[\e[0;36m\]"
#PS1_CYANBOLD="\[\e[1;36m\]"
#PS1_WHITE="\[\e[0;37m\]"
#PS1_WHITEBOLD="\[\e[1;37m\]"
PS1_MAGENTA="\[\e[1;95m\]"
# To (R)eset colors.
PS1_R="\[\e[0m\]"

# Just aliases for common colors used later.
PS1_DIR=$PS1_REDBOLD
PS1_USER=$PS1_CYAN
PS1_HOST=$PS1_GREEN

# If root, highlight it
if [[ $UID -eq 0 ]]; then
    PS1_USER=$PS1_YELLOWBOLD
fi

# If using ssh, usually set
if [ -n "$SSH_CLIENT" ] || [ -n "$SSH_TTY" ] || [ -n "$SSH_CONNECTION" ];then
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
        if ! [[ ${T} =~ [!?^↓↑] ]]; then
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
GIT_PROMPT_START="\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}{ $PS1_DIR\w$PS1_R }"
GIT_PROMPT_END="\n$PS1_USER\u$PS1_R@$PS1_HOST\h$PS1_R$ "

source ~/.bash-git-prompt/gitprompt.sh

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
#}}}
# vim: set foldmethod=marker:
