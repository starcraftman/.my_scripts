#!/usr/bin/env bash
# This file contains all bash modifications apart from .bashrc.

# Neat bash tricks, http://blog.sanctum.geek.nz/category/bash
# Some other tricks, http://www.tldp.org/LDP/abs/html/sample-bashrc.html
# List of BASH vals https://www.gnu.org/software/bash/manual/html_node/Bash-Variables.html

# When debugging bash, $LINENO refers to current line of script
# Also $RANDOM gives val from 0-32767
# Note that `caller expr` builtin prints call stack, where expr is framenumber.
# Uses BASH_LINENO BASH_SOURCE & FUNCNAME arrays
############################################################################
# Path Settings
############################################################################
#{{{
# .software is for any precompiled programs & libraries I install.
# .opt is for programs compiled from src, sources stay in OPT/src while bins to OPT/bin
export SOFT=~/.software
export OPTDIR=~/.opt

# Personal scripts go here to stay outside of root.
MYSCRIPTS=~/.my_scripts

# Dir to locally install cabal for haskell.
HASKELL_BIN=~/.cabal/bin

# Exported paths.
ANDROID=$SOFT/android-sdk/tools:$SOFT/android-sdk/platform-tools:$SOFT/android-ndk
export JAVA_HOME=$SOFT/jdk
export CLASSPATH=$SOFT/jlibs:$JAVA_HOME/lib:/usr/share/ant/lib:/usr/share/java:$CLASSPATH
# /usr/lib/ccache on path -> links gcc, g++ to ccache aliases, put at front.
export PATH=$MYSCRIPTS:$OPTDIR/bin:$JAVA_HOME/bin:$HASKELL_BIN:$ANDROID:$PATH
export CPATH=$SOFT/libs/include:$CPATH
export LIBRARY_PATH=$SOFT/libs/lib:$LIBRARY_PATH

# Paths for specific tools.
export ANT_HOME=/usr/share/ant
#}}}
############################################################################
# Environment Variables
############################################################################
#{{{
# Default editor for things like sudoedit.
if valid_name vim; then
    export EDITOR=vim
fi

# If you want to have a fallback path lookup, use CDPAth.
#export CDPATH=~/programming

#CCache Directory
#Info: https://ccache.samba.org/manual.html
export CCACHE_DIR=~/.ccache

# Ignore files with these suffixes for bash completion
# NB: For dirs like .bzr, bzr line will ignore anything ending in bzr.
export FIGNORE=bzr:git:hg:svn:.class:.o:.pyc

# Change grep color to bold blue
export GREP_COLORS='ms=01;34:mc=01;34:sl=:cx=:fn=35:ln=32:bn=32:se=36'

# Merge tool for hg
export HGMERGE=/usr/bin/kdiff3

# Bash history options
# Set large history file & line limit
export HISTFILESIZE=100000
export HISTSIZE=100000

# Ignore some commands
#export HISTIGNORE='ls *:l *:bg:fg:history'

# Timestamps in history file
export HISTTIMEFORMAT='%F %T '

# Ignore duplicate commands in history
export HISTCONTROL=ignoredups:erasedups

# The number of EOF to ignore before terminating shell
export IGNOREEOF=2

# Default pager
export PAGER=less
#}}}
############################################################################
# Aliases
############################################################################
#{{{
# Note: First word of alias is expanded as alias, others ignored. Hence ll, expands ls.

# Keep home configs when switching to root
alias su='su --preserve-environment'

# Make ls more convenient
alias l='\ls --color=auto -F --group-directories-first'
alias ls='l --sort=extension'
alias ll='ls -Alh'
alias la='l -A'

# Different sorts
alias lx='ll -XB'  # Extension
alias lk='ll -Sr'  # File size
alias lu='ll -tur' # Access time
alias lc='ll -tcr' # CTime, last change to attributes (fperms, ownership)
alias lt='ll -tr'  # Modification time

# Recursive cp
alias cpr='cp -r'

# Always create non-existing parent dirs
alias mkdir='mkdir -vp'

# Alias for use of pushd/popd
alias pu="pushd"
alias po="popd"

# Grep should always print line
alias grep='grep --color=auto -n --exclude-dir=.git --exclude-dir=.hg --exclude-dir=.bzr --exclude-dir=.svn --exclude-dir=.cvs'
# Re alias these to take advantage of above
alias egrep='grep -E'
alias fgrep='grep -F'
alias rgrep='grep -r'

# Reruns the last command with sudo.
alias please='sudo $(fc -l -n -1)'

# type used to determine what command is, list all entries
alias types='type -a'

# Always open with splits
alias vims='vim -o'

# df/du defaults, du -L to follow symlinks
alias df='df -hT'
alias du='du -h'
if valid_name dfc; then
    alias dfc='dfc -T'
fi

# Colored cat output
if valid_name pygmentize; then
    alias ccat='pygmentize -g'
fi

# Default ack options, use smart case, sort output by file and follow symlinks.
# Filter by type with --type, supported types `ack --help-types`
if valid_name ack; then
    alias ack='ack --smart-case --sort-files --follow --color-match="bold blue"'
    # Alias for ack find file by name
    alias ackf='ack -g'
    # Alias for ack find file by contents
    alias ackl='ack -il'
fi

# Alias for silver search
# For type use --type, i.e. --cpp. supported types -> 'ag --list-file-types
if valid_name ag; then
    alias ag='ag --smart-case --follow --color-match="1;34"'
    # Alias for ag find file by name
    alias agf='ag -g'
    # Alias for ag find file by contents
    alias agl='ag -il'
fi

# Add an "alert" alias for long running commands. Example:
#   sleep 10; alert
if valid_name notify-send; then
    alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'
fi

# Apt aliases
if valid_name apt-get; then
    alias apti='sudo apt-get -y install'
    alias aptr='sudo apt-get -y remove'
    alias aptu='sudo apt-get update && sudo apt-get -y dist-upgrade'
fi

# Alias for color tools.
if valid_name colordiff; then
    alias cod='colordiff'
fi
if valid_name colorgcc; then
    alias cog='colorgcc'
fi
if valid_name colormake; then
    alias com='colormake'
fi

# Silence parallel
if valid_name parallel; then
    alias parallel='parallel --no-notice'
fi

# Use trash instead of RM, have had bad accidents. Need trash-cli library for python.
if valid_name trash-put; then
    alias trash-restore='restore-trash'
    alias tre='restore-trash'
    alias tp='trash-put'
    alias tl='trash-list'
    alias te='trash-empty'
    alias rm='echo "Don''t use. If must, \rm -Rf file."; false'
fi

# Tree program, use instead of recursive ls. Very pretty.
if valid_name tree; then
    alias tree='tree -Csuh'
fi

# Aliases for vimpager
if valid_name vimpager; then
    alias vcat='vimcat'
    alias vpager='vimpager'
fi

# BASH ONLY
# Print alias for echo with escape codes
alias print='echo -e'
#}}}
############################################################################
# Functions
############################################################################
#{{{
# Take a directory. If it doesn't exist, make it.
take()
{
    local dir="$1"
    mkdir "$dir"
    cd "$dir"
}

# Toggles bash debug mode, when on:
#  * Turns on tracing of every command (xtrace).
#  * Prevents unsetting vars (nounset).
#  * Prints lines before execution (verbose).
#  * Disables bash prompt to avoid pollution with xtrace.
debug()
{
    local BRed='\e[1;31m'
    local BGreen='\e[1;32m'
    local NC="\e[m"
    # If command is blank, turn off debug mode
    if [ "x" == "x${PROMPT_COMMAND}" ]; then
        #set +o nounset
        set +o extdebug
        set +o verbose
        set +o xtrace
        PROMPT_COMMAND="$PROMPT_OLD_COMMAND"
        unset PROMPT_OLD_COMMAND
        print "Bash Debug Mode: ${BRed}DISABLED${NC}"
    else
        PROMPT_OLD_COMMAND="$PROMPT_COMMAND"
        PROMPT_COMMAND=""
        export PS1="${PS1_REDBOLD} >>DEBUG<< ${NC}${GIT_PROMPT_START}${GIT_PROMPT_END}"
        #set -o nounset
        set -o extdebug
        set -o verbose
        set -o xtrace
        print "Bash Debug Mode: ${BGreen}ENABLED${NC}"
        print "Careful with ${BRed}nounset${NC} breaks some completion."
    fi
}

# Function to go back up when deep in directories.
# Example: .. 3 == cd ../../..
..()
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

# Repeat a command n times, example:
#   repeat 10 echo foo
repeat()
{
    local count="$1" i
    shift
    for i in $(seq 1 "$count"); do
        eval "$@"
    done
}

# Check if connection up at all by pinging google dns
conTest()
{
    for url in "8.8.8.8" "8.8.4.4"; do
        ping -c 3 $url
    done
}

# Check if term supports 256 -> http://www.robmeerman.co.uk/unix/256colours
termColor()
{
    curl http://www.robmeerman.co.uk/_media/unix/256colors2.pl > c.pl 2>/dev/null
    perl ./c.pl
    \rm c.pl
}

# Format a json file to be pretty
jsonFix()
{
    for file ; do
        cat "$file" | python -m json.tool > "fix_$file"
    done
}

# Useful functions inspired by:
#http://www.tldp.org/LDP/abs/html/sample-bashrc.html
# Get info on all network interfaces
listNics()
{
    local BGreen='\e[1;32m'
    local NC="\e[m"
    local INTS=($(ifconfig -s | awk ' /^wlan.*|eth.*/ { print $1 }'))
    # Ample use of awk/sed for field extraction.
    for INT in ${INTS[@]} ; do
        local   MAC=$(ifconfig $INT | awk '/Waddr/ { print $5 } ')
        local    IP=$(ifconfig $INT | awk '/inet / { print $2 } ' | sed -e s/addr://)
        local BCAST=$(ifconfig $INT | awk '/inet / { print $3 } ' | sed -e s/Bcast://)
        local  MASK=$(ifconfig $INT | awk '/inet / { print $4 } ' | sed -e s/Mask://)
        local   IP6=$(ifconfig $INT | awk '/inet6/ { print $3 } ')

        print "Interface: ${BGreen}$INT${NC}"
        print "\tMac:   ${MAC}"
        print "\tIPv4:  ${IP:-"Not connected"}"
        if [[ -n ${IP} ]]; then
            print "\tBCast: ${BCAST}"
            print "\tMask:  ${MASK}"
            print "\tIPv6:  ${IP6:-"N/A."}"
        fi
    done
}

# Pretty print of df, like dfc.
prettyDf()
{
    for fs ; do

        if [ ! -d $fs ]; then
            print $fs" :No such file or directory"
            continue
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
        print $out
    done
}

# Get information on current system
ii()
{
    local BBlue='\e[1;34m'
    local NC="\e[m"
    local TOP=$(top -n 1 -o %CPU | sed '/^$/d' | head -n 12 | tail -n 11)
    print
    print "${BBlue}$USER$NC is logged on ${BBlue}$HOSTNAME"
    print "${BBlue}Additionnal information :$NC " ; uname -a
    print "${BBlue}Users logged on :$NC " ; w -hs |
             cut -d " " -f1 | sort | uniq
    print "${BBlue}Current date :$NC " ; date
    print "${BBlue}Machine stats :$NC " ; uptime
    print "${BBlue}Diskspace :$NC "
    if valid_name dfc; then
        dfc
    else
        local mounts=$(mount -v | awk '/\/dev\/s/ { print $3 }')
        prettyDf $mounts
    fi
    print "${BBlue}Memory stats :$NC " ; free -h
    print "${BBlue}Top 5 CPU% :$NC " ; print "$TOP" | head -n 2 ; print "$TOP" | tail -n 6
    print "${BBlue}Top 5 MEM% :$NC " ; top -n 1 -o %MEM | sed '/^$/d' | head -n 12 | tail -n 5
    print "${BBlue}Network Interfaces :$NC" ; listNics
    print "${BBlue}Open connections :$NC "; netstat -pan --inet;
    print
}

# Highlight many terms with different colors
# Usage: find . | h term1 term2 term3
source ~/.shell/.hhighlighter/h.sh
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
#shopt -s cdable_vars

# When making small typos with cd, go to best match
shopt -s cdspell

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# Multiline commands to be on single lines in history
shopt -s cmdhist

# Ensure extended globbing allowed
# http://www.linuxjournal.com/content/bash-extended-globbing
shopt -s extglob

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
shopt -s globstar

# Always append instead of overwriting history
shopt -s histappend

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
if valid_name xmodmap; then
    xmodmap -e 'keycode 133 = F13'
fi

# Disable the Ctrl+s/q button that freezes terminal output.
if valid_name stty; then
    stty -ixon
fi

# Set bash tabstop to 4 spaces, default is 8 too wide
if valid_name tabs; then
    tabs 4
    clear
fi

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
if [ $UID -eq 0 ]; then
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
prompt_callback()
{
    local HG=$(hg prompt "[${PS1_MAGENTA}{branch}${PS1_R}{ ${PS1_RED}↓{incoming|count}${PS1_R}}{${PS1_GREEN}↑{outgoing|count}${PS1_R}}|${PS1_YELLOW}{status}{update}${PS1_R}]" 2>/dev/null)

    # Strip everything except where status to outgoing would be.
    local T=${HG##*|}
    T=${T%%]}

    # Insert check mark only if T doesn't contain other codes like status or update, see regexp.
    if [ "x${HG}" != "x" ] && [[ ! ${T} =~ [!?^↓↑] ]]; then
        HG="${HG%%]}${PS1_GREENBOLD}✔${PS1_R}]"
    fi

    # Print don't print extra space unless need to.
    if [ "x$HG" == "x" ]; then
        print -n ""
    else
        print -n " $HG"
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
GIT_PROMPT_START="$PS1_R\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}{ $PS1_DIR\w$PS1_R }"
GIT_PROMPT_END="\n$PS1_USER\u$PS1_R@$PS1_HOST\h$PS1_R\\$ "

# Shows status of last command.
GIT_PROMPT_SHOW_LAST_COMMAND_INDICATOR=1

source ~/.shell/.bash-git-prompt/gitprompt.sh

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
