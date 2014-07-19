##!/usr/bin/env zsh
#
############################################################################
# Shell Compatability Settings
############################################################################
# Case insensitive
autoload -U compinit
compinit -C

## case-insensitive (all),partial-word and then substring completion
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}' \
    'r:|[._-]=* r:|=*' 'l:|=* r:|=*'

# Don't exit with ctrl + D
setopt ignore_eof

# Enable prompt var substitution & root/user bang.
setopt prompt_bang
setopt prompt_subst

# Zero index arrays, like normal people
#setopt ksh_arrays

# Set compatible globbing.
#setopt ksh_glob

############################################################################
# Environment Variables
############################################################################
#{{{
# Default editor for things like sudoedit.
if hash vim 2>/dev/null; then
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
#export HISTTIMEFORMAT='%F %T '

# Ignore duplicate commands in history
export HISTCONTROL=ignoredups:erasedups

# Default pager
export PAGER=less
#}}}
############################################################################
# Path Settings
############################################################################
#{{{
# .software is for any precompiled programs & libraries I install.
# .opt is for programs compiled from src, sources stay in OPT/src while bins to OPT/bin
export SOFT=~/.software
export OPT=~/.opt

# Personal scripts go here to stay outside of root.
MYSCRIPTS=~/.my_scripts

# Dir to locally install cabal for haskell.
HASKELL_BIN=~/.cabal/bin

# Exported paths.
ANDROID=$SOFT/android-sdk/tools:$SOFT/android-sdk/platform-tools:$SOFT/android-ndk
export JAVA_HOME=$SOFT/jdk
export CLASSPATH=$SOFT/jlibs:$JAVA_HOME/lib:/usr/share/ant/lib:/usr/share/java:$CLASSPATH
# /usr/lib/ccache on path -> links gcc, g++ to ccache aliases, put at front.
export PATH=$MYSCRIPTS:$OPT/bin:$JAVA_HOME/bin:$HASKELL_BIN:$ANDROID:$PATH
export CPATH=$SOFT/libs/include:$CPATH
export LIBRARY_PATH=$SOFT/libs/lib:$LIBRARY_PATH

# Paths for specific tools.
export ANT_HOME=/usr/share/ant
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
alias please='sudo `fc -l -n -1`'

# type used to determine what command is, list all entries
alias types='type -a'

# Always open with splits
alias vims='vim -o'

# df/du defaults, du -L to follow symlinks
alias df='df -hT'
alias du='du -h'
if hash dfc 2>/dev/null; then
    alias dfc='dfc -T'
fi

# Colored cat output
if hash pygmentize 2>/dev/null; then
    alias ccat='pygmentize -g'
fi

# Default ack options, use smart case, sort output by file and follow symlinks.
# Filter by type with --type, supported types `ack --help-types`
if hash ack 2>/dev/null; then
    alias ack='ack --smart-case --sort-files --follow --color-match="bold blue"'
    # Alias for ack find file
    alias ackf='ack -g'
fi

# Alias for silver search
# For type use --type, i.e. --cpp. supported types -> 'ag --list-file-types
if hash ag 2>/dev/null; then
    alias ag='ag --smart-case --follow --color-match="1;34"'
    # Alias for file name searc
    alias agf='ag -g'
fi

# Add an "alert" alias for long running commands. Example:
#   sleep 10; alert
if hash notify-send 2>/dev/null; then
    alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'
fi

# Apt aliases
if hash apt-get 2>/dev/null; then
    alias apti='sudo apt-get -y install'
    alias aptr='sudo apt-get -y remove'
    alias aptu='sudo apt-get update && sudo apt-get -y dist-upgrade'
fi

# Alias for color tools.
if hash colordiff 2>/dev/null; then
    alias cod='colordiff'
fi
if hash colorgcc 2>/dev/null; then
    alias cog='colorgcc'
fi
if hash colormake 2>/dev/null; then
    alias com='colormake'
fi

# Silence parallel
if hash parallel 2>/dev/null; then
    alias parallel='parallel --no-notice'
fi

# Use trash instead of RM, have had bad accidents. Need trash-cli library for python.
if hash trash-put 2>/dev/null; then
    alias trash-restore='restore-trash'
    alias tre='restore-trash'
    alias tp='trash-put'
    alias tl='trash-list'
    alias te='trash-empty'
    alias rm='echo "Don''t use. If must, \rm -Rf file."; false'
fi

# Tree program, use instead of recursive ls. Very pretty.
if hash tree 2>/dev/null; then
    alias tree='tree -Csuh'
fi

# Zsh only aliases
alias help='run-help'
#}}}
############################################################################
# Functions
############################################################################
#{{{
# Needed by zsh.
autoload conTest debug ii jsonFix listNics prettyDf termColor unarchive

# Toggles bash debug mode, when on:
#  * Turns on tracing of every command (xtrace).
#  * Prevents unsetting vars (nounset).
#  * Prints lines before execution (verbose).
#  * Disables bash prompt to avoid pollution with xtrace.
function debug()
{
    local BRed='\e[1;31m'
    local BGreen='\e[1;32m'
    local NC="\e[m"
    # If command is blank, turn off debug mode
    if [ "x" == "x${PROMPT}" ]; then
        echo 'turn off debug'
        #set +o nounset
        set +o verbose
        set +o xtrace
        PROMPT_COMMAND="$PROMPT_OLD_COMMAND"
        unset PROMPT_OLD_COMMAND
        echo -e "Bash Debug Mode: ${BRed}DISABLED${NC}"
    else
        echo 'turn on debug'
        PROMPT_OLD_COMMAND="$PROMPT_COMMAND"
        PROMPT_COMMAND=""
        export PS1="${PS1_REDBOLD} >>DEBUG<< ${NC}${GIT_PROMPT_START}${GIT_PROMPT_END}"
        #set -o nounset
        set -o verbose
        set -o xtrace
        echo -e "Bash Debug Mode: ${BGreen}ENABLED${NC}"
        echo -e "Careful with ${BRed}nounset${NC} breaks some completion."
    fi
}

# Universal extract function, later versions of tar -xvf may work
# more universally but not with older versions.
function unarchive()
{
    local tmpdir=$HOME/loopback
    for file ; do
        if [ ! -f $file ] ; then
            echo "'$file' is not a valid file!"
            continue
        fi

        case $file in
            *.deb)               ar p "$file" data.tar.gz | tar zx ;;
            *.rpm)               rpm2cpio "$file" | cpio -vid      ;;
            *.jar)               jar xf "$file"                    ;;
            *.iso)               7z x "$file"                      ;;
            *.tar)               tar xvf "$file"                   ;;
            *.tbz2|*.tar.bz2)    tar xvjf "$file"                  ;;
            *.tgz|*.tar.gz)      tar xvzf "$file"                  ;;
            *.tar.lz|*.tar.lzma) lzcat "$file" | tar xvf -         ;;
            *.tar.xz)            xzcat "$file" | tar xvf -         ;;
            *.tar.Z)             zcat "$file" | tar xvf -          ;;
            *.bz|*.bz2)          bunzip2 "$file"                   ;;
            *.gz)                gunzip "$file"                    ;;
            *.lzma)              unlzma "$file"                    ;;
            *.rar)               unrar "$file"                     ;;
            *.xz)                unxz "$file"                      ;;
            *.Z)                 uncompress "$file"                ;;
            *.zip)               unzip "$file"                     ;;
            *.7z)                7z x "$file"                      ;;
            *.dmg)
                echo "'$file' mounted at '$tmpdir'."
                mkdir $tmpdir
                mount -o loop -t hfs "$file" $tmpdir               ;;
            *.img|*.dd)
                echo "'$file' mounted at '$tmpdir'."
                mkdir $tmpdir
                mount -o loop -t iso9660 "$file" $tmpdir           ;;
            *)  echo "${FUNCNAME[0]}: Cannot extract '$file'"      ;;
        esac
    done
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

# Check if connection up at all by pinging google dns
function conTest()
{
    for url in "8.8.8.8" "8.8.4.4"; do
        ping -c 3 $url
    done
}

# Check if term supports 256 -> http://www.robmeerman.co.uk/unix/256colours
function termColor()
{
    curl http://www.robmeerman.co.uk/_media/unix/256colors2.pl > c.pl 2>/dev/null
    perl ./c.pl
    \rm c.pl
}

# Format a json file to be pretty
function jsonFix()
{
    for file ; do
        cat "$file" | python -m json.tool > "fix_$file"
    done
}

# Useful functions inspired by:
#http://www.tldp.org/LDP/abs/html/sample-bashrc.html
# Get info on all network interfaces
function listNics()
{
    local BGreen='\e[1;32m'
    local NC="\e[m"
    local INTS=($(ifconfig -s | awk ' /^wlan.*|eth.*/ { print $1 }'))
    # Ample use of awk/sed for field extraction.
    for INT in $INTS ; do
        local   MAC=$(ifconfig $INT | awk '/Waddr/ { print $5 } ')
        local    IP=$(ifconfig $INT | awk '/inet / { print $2 } ' | sed -e s/addr://)
        local BCAST=$(ifconfig $INT | awk '/inet / { print $3 } ' | sed -e s/Bcast://)
        local  MASK=$(ifconfig $INT | awk '/inet / { print $4 } ' | sed -e s/Mask://)
        local   IP6=$(ifconfig $INT | awk '/inet6/ { print $3 } ')

        echo -e "Interface: ${BGreen}$INT${NC}"
        echo -e "\tMac:   ${MAC}"
        echo -e "\tIPv4:  ${IP:-"Not connected"}"
        if [[ -n ${IP} ]]; then
            echo -e "\tBCast: ${BCAST}"
            echo -e "\tMask:  ${MASK}"
            echo -e "\tIPv6:  ${IP6:-"N/A."}"
        fi
    done
}

# Pretty print of df, like dfc.
function prettyDf()
{
    for fs ; do

        if [ ! -d $fs ]; then
            echo -e $fs" :No such file or directory"
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
        echo -e $out
    done
}

# Get information on current system
function ii()
{
    local BBlue='\e[1;34m'
    local NC="\e[m"
    local TOP=`top -n 1 -o %CPU | sed '/^$/d' | head -n 12 | tail -n 11`
    echo
    echo -e "You are logged on ${BBlue}$HOSTNAME"
    echo -e "${BBlue}Additionnal information :$NC " ; uname -a
    echo -e "${BBlue}Users logged on :$NC " ; w -hs |
             cut -d " " -f1 | sort | uniq
    echo -e "${BBlue}Current date :$NC " ; date
    echo -e "${BBlue}Machine stats :$NC " ; uptime
    echo -e "${BBlue}Diskspace :$NC "
    if hash dfc 2>/dev/null; then
        dfc
    else
        local mounts=$(mount -v | awk '/\/dev\/s/ { print $3 }')
        prettyDf $mounts
    fi
    echo -e "${BBlue}Memory stats :$NC " ; free -h
    echo -e "${BBlue}Top 5 CPU% :$NC " ; echo "$TOP" | head -n 2 ; echo "$TOP" | tail -n 6
    echo -e "${BBlue}Top 5 MEM% :$NC " ; top -n 1 -o %MEM | sed '/^$/d' | head -n 12 | tail -n 5
    echo -e "${BBlue}Network Interfaces :$NC" ; listNics
    echo -e "${BBlue}Open connections :$NC "; netstat -pan --inet;
    echo
}

# Highlight many terms with different colors
# Usage: find . | h term1 term2 term3
source $HOME/.hhighlighter/h.sh
#}}}
############################################################################
# Misc Options
############################################################################
#{{{
# Enable the windows key on Ubuntu as F13
if hash xmodmap 2>/dev/null; then
    xmodmap -e 'keycode 133 = F13'
fi

# Disable the Ctrl+s/q button that freezes terminal output.
if hash stty 2>/dev/null; then
    stty -ixon
fi

# Set bash tabstop to 4 spaces, default is 8 too wide
if hash tabs 2>/dev/null; then
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
# PS1 Prompt
############################################################################
function prompt_precmd()
{
    if [ $? -eq 0 ]; then
        LAST="%F{green}✔%f"
    else
        LAST="%F{red}✘%f"
    fi
}

autoload add-zsh-hook
add-zsh-hook precmd prompt_precmd

# Just aliases for common colors used later.
PS1_DIR=%B%F{red}
PS1_USER=%F{cyan}
PS1_HOST=%F{green}
PS1_R=%f%b

# If root, highlight it
if [ $UID -eq 0 ]; then
    PS1_USER=%F{yellow}
fi

# If using ssh, usually set
if [ -n "$SSH_CLIENT" ] || [ -n "$SSH_TTY" ] || [ -n "$SSH_CONNECTION" ];then
    PS1_HOST=%B%F{purple}
fi

PS1='$LAST { %B%F{red}%~%f%b }
%F{cyan}%n%f@%F{green}%m%f%# '

# vim: set foldmethod=marker:
