##!/usr/bin/env zsh
# This config is based on a combination of existing .bashrc & .bash_aliases in
# this directory, adapted to work on zsh.
# Large number of configs:
# http://stackoverflow.com/questions/171563/whats-in-your-zshrc
# For more info, also consult man pages starting with zsh...
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

# Change grep color to bold blue
export GREP_COLORS='ms=01;34:mc=01;34:sl=:cx=:fn=35:ln=32:bn=32:se=36'

# Merge tool for hg
export HGMERGE=/usr/bin/kdiff3

# Bash history options
# Set large history file & line limit
export HISTFILE=~/.zsh_history
export HISTSIZE=100000
export SAVEHIST=100000

# Ignore some commands
#export HISTIGNORE='ls *:l *:bg:fg:history'

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
    # Alias for ack find file by name
    alias ackf='ack -g'
    # Alias for ack find file by contents
    alias ackl='ack -il'
fi

# Alias for silver search
# For type use --type, i.e. --cpp. supported types -> 'ag --list-file-types
if hash ag 2>/dev/null; then
    alias ag='ag --smart-case --follow --color-match="1;34"'
    # Alias for ag find file by name
    alias agf='ag -g'
    # Alias for ag find file by contents
    alias agl='ag -il'
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

# History with time stamps
alias history='history -E'

# Debug alias, appears xtrace can't be set except outside functions.
alias debug='if debug; then setopt xtrace; else unsetopt xtrace; clear; fi'
#}}}
############################################################################
# Functions
############################################################################
#{{{
# contains(string, substring)
#
# Returns 0 if the specified string contains the specified substring,
# otherwise returns 1.
function contains()
{
    string="$1"
    substring="$2"
    if test "${string#*$substring}" != "$string"; then
        return 0    # $substring is in $string
    else
        return 1    # $substring is not in $string
    fi
}

# Save hooks if arge is 1, else restore them.
function save_hooks()
{
    if [ "$1" = "1" ]; then
        chpwd_functions=
        precmd_functions=
        preexec_functions=
    else
        add-zsh-hook precmd prompt_precmd
        source ~/.zsh-git-prompt/zshrc.sh
    fi
}

# Toggles bash debug mode, when on:
#  * Turns on tracing of every command (xtrace).
#  * Prevents unsetting vars (nounset).
#  * Prints lines before execution (verbose).
#  * Disables bash prompt to avoid pollution with xtrace.
#
#  N.B. zsh bug that xtrace can't be set in a function
function debug()
{
    local BRed="$fg_bold[red]"
    local BGreen="$fg_bold[green]"
    local NC="$reset_color"
    # If ps1 contains debug word, turn off debug mode
    if contains "$PS1" "DEBUG"; then
        PS1="$PS1_STD"
        #unsetopt nounset
        unsetopt sourcetrace
        unsetopt verbose
        unsetopt warncreateglobal
        #unsetopt xtrace
        save_hooks 0
        print "Bash Debug Mode: ${BRed}DISABLED${NC}"
        return 1
    else
        PS1="$PS1_DEBUG"
        #setopt nounset
        setopt sourcetrace
        setopt verbose
        unsetopt warncreateglobal
        #setopt xtrace
        save_hooks 1
        print "Bash Debug Mode: ${BGreen}ENABLED${NC}"
        print "Careful with ${BRed}nounset${NC} breaks some completion."
        return 0
    fi
}

# Universal extract function, later versions of tar -xvf may work
# more universally but not with older versions.
function unarchive()
{
    local tmpdir=$HOME/loopback
    for file ; do
        if [ ! -f $file ] ; then
            print "'$file' is not a valid file!"
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
                print "'$file' mounted at '$tmpdir'."
                mkdir $tmpdir
                mount -o loop -t hfs "$file" $tmpdir               ;;
            *.img|*.dd)
                print "'$file' mounted at '$tmpdir'."
                mkdir $tmpdir
                mount -o loop -t iso9660 "$file" $tmpdir           ;;
            *)  print "${FUNCNAME[0]}: Cannot extract '$file'"      ;;
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
    local BGreen="$fg_bold[green]"
    local NC="$reset_color"
    INTS=( "${(@f)$(ifconfig -s | awk ' /^wlan.*|eth.*/ { print $1 }')}" )
    # Ample use of awk/sed for field extraction.
    for INT in $INTS ; do
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
    unset INTS
}

# Pretty print of df, like dfc.
function prettyDf()
{
    for fs ; do

        if [ ! -d $fs ]; then
            print $fs" :No such file or directory"
            continue
        fi

        info=( "${(s/ /)$(command df -P $fs | awk 'END{ print $2,$3,$5 }')}" )
        local free="${(@f)$(command df -Pkh $fs | awk 'END{ print $4 }')}"
        local nbstars=$(( 20 * $info[2] / $info[1] ))
        local out="["
        for ((j=0;j<20;j++)); do
            if [ ${j} -lt ${nbstars} ]; then
               out=$out"*"
            else
               out=$out"-"
            fi
        done
        out=$info[3]" "$out"] ("$free" free on "$fs")"
        print $out
    done
    unset info
}

# Get information on current system
function ii()
{
    local BBlue="$fg_bold[blue]"
    local NC="$reset_color"
    TOP=$(top -n 1 -o %CPU | sed '/^$/d' | head -n 12 | tail -n 11)
    print
    print "${BBlue}$USERNAME$NC is logged on ${BBlue}$HOST"
    print "${BBlue}Additionnal information :$NC " ; uname -a
    print "${BBlue}Users logged on :$NC " ; w -hs |
             cut -d " " -f1 | sort | uniq
    print "${BBlue}Current date :$NC " ; date
    print "${BBlue}Machine stats :$NC " ; uptime
    print "${BBlue}Diskspace :$NC "
    if hash dfc 2>/dev/null; then
        dfc
    else
        mounts=( "${(@f)$(mount -v | awk '/\/dev\/s/ { print $3 }')}" )
        prettyDf $mounts
        unset mounts
    fi
    print "${BBlue}Memory stats :$NC " ; free -h
    print "${BBlue}Top 5 CPU% :$NC " ; print "$TOP" | head -n 2 ; print "$TOP" | tail -n 6
    print "${BBlue}Top 5 MEM% :$NC " ; top -n 1 -o %MEM | sed '/^$/d' | head -n 12 | tail -n 5
    print "${BBlue}Network Interfaces :$NC" ; listNics
    print "${BBlue}Open connections :$NC "; netstat -pan --inet;
    print
    unset TOP
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
# Autoload, Completion & Setopt
############################################################################
#{{{
# Zcalc is a neat cmdline calculator
autoload -U zcalc

# Load zsh shell colors
autoload -U colors && colors
# Loaded colors will be in associated arrays called: fg_no_bold, fg_bold, bg
#   KEYS: red green yellow blue magenta cyan black white
# RESET COLOR $reset_color
# EXAMPLE: print "$fg_no_bold[red] hello $reset_color"

# Allows us to override shell hooks like for before prompt
autoload -U add-zsh-hook

# Use vcs info for bzr & svn
autoload -Uz vcs_info

# Case insensitive
autoload -U compinit
compinit -C

## case-insensitive (all),partial-word and then substring completion
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}' \
    'r:|[._-]=* r:|=*' 'l:|=* r:|=*'

# Faster completion with cache
zstyle ':completion::complete:*' use-cache 1

# Don't complete directory we are already in (../here)
zstyle ':completion:*' ignore-parents parent pwd

# generate descriptions with magic.
zstyle ':completion:*' auto-description 'specify: %d'

# # Don't prompt for a huge list, page it!
zstyle ':completion:*:default' list-prompt '%S%M matches%s'

# # Don't prompt for a huge list, menu it if over 2 eles!
zstyle ':completion:*:default' menu 'select=2'

# # Have the newer files last so I see them first
zstyle ':completion:*' file-sort modification reverse

# # color code completion!!!!  Wohoo!
#zstyle ':completion:*' list-colors "=(#b) #([0-9]#)*=36=31"
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}

# Don't complete stuff already on the line for commands in regex
zstyle ':completion::*:(ag|ack|cp|git|hg|mv|rm|tp|vi|vim):*' ignore-line true

# Group completions by type & have blue header above.
#zstyle ':completion:*:descriptions' format $'\e[00;34m%d'
#zstyle ':completion:*:messages' format $'\e[00;31m%d'
#zstyle ':completion:*' group-name ''

# Separate man page sections.  Neat.
zstyle ':completion:*:manuals.*'  group-name   true
zstyle ':completion:*:manuals.*'  insert-sections   true
zstyle ':completion:*:manuals'    separate-sections true
zstyle ':completion:*:man:*'      menu yes select

# Make kill/killall work better
zstyle ':completion:*:*:kill:*' menu yes select
zstyle ':completion:*:kill:*' force-list always
zstyle ':completion:*:*:kill:*:processes' list-colors "=(#b) #([0-9]#)*=29=34"
zstyle ':completion:*:*:killall:*' menu yes select
zstyle ':completion:*:killall:*' force-list always

# Ignore certain files or directories, better than fignore
zstyle ':completion:*:*files' ignored-patterns '*?.(o|class|pyc)' '*?~'
zstyle ':completion:*:*:cd:*' ignored-patterns '(*/|)(bzr|git|hg|svn)'

# Settings for vcs_info
zstyle ':vcs_info:*' enable bzr cvs svn
zstyle ':vcs_info:*' check-for-changes true
# Staged Unstaged [Branch] vcs_type-repo_name
zstyle ':vcs_info:*' formats "%{$fg[green]%}%c%{$reset_color%} %{$fg[red]%}%u%{$reset_color%} [%{$fg_bold[magenta]%}%b%{$reset_color%}] %{$fg_bold[cyan]%}%r%{$reset_color%} <%{$fg[yellow]%}%s%{$reset_color%}>"

# History should append if multiple versions run
setopt APPEND_HISTORY

# History saves beginning and elapsed time for commands
setopt EXTENDED_HISTORY

# History writing better on nfs
setopt HIST_FCNTL_LOCK

# History lookup ignores duplicate commands
setopt HIST_FIND_NO_DUPS

# Ignore duplicates if they are same as previous.
setopt HIST_IGNORE_DUPS

# Ignore the history command itself
setopt HIST_NO_STORE

# If need to share history or write immediately
# see SHARE_HISTORY, INC_APPEND_HISTORY

# Allow braces to define character classes like: file{abcd1234}
setopt BRACE_CCL

# Use extended globbing
setopt EXTENDED_GLOB

# Use ksh globing, brings leading @, +() etc...
setopt KSH_GLOB

# Enable rematch (=~) to use pcre instead of shell regex.
#setopt REMATCH_PCRE

# Correct spelling mistakes only on commands
setopt CORRECT

# pushd -> pushd $HOME
setopt PUSHD_TO_HOME

# Don't exit with ctrl + D
setopt IGNORE_EOF

# Two single quotes escape to one in single quotes
setopt RC_QUOTES

# Jobs print in long format for more info
setopt LONG_LIST_JOBS

# Enable prompt var substitution & root/user bang.
setopt PROMPT_BANG
setopt PROMPT_SUBST

# RM star commands wait before proceeding.
setopt RM_STAR_WAIT

# Use vim mode
setopt VI

# Zero index arrays, like normal people
#setopt ksh_arrays

# Set compatible globbing.
#setopt ksh_glob
#}}}
############################################################################
# Key Bindings
############################################################################
#{{{
# When in completion, move backwards, key is shift+tab
bindkey '^[[Z' reverse-menu-complete

# History lookup bindings to usual r key
bindkey '^r' history-incremental-search-backward
bindkey '^s' history-incremental-search-forward

# Backspace deletes past start
bindkey '^?' backward-delete-char

# Scroll up or down a completion list
bindkey '^j' down-line-or-history
bindkey '^k' up-line-or-history

# Use my normal jk map to escape insert mode
bindkey 'jk' vi-cmd-mode

# vim-like undo and redo
bindkey -M vicmd 'u' undo
bindkey -M vicmd '^R' redo

# it's like, space AND completion. Allows for expansion of hist cmds,
# example: $1<space>
bindkey -M viins ' ' magic-space

# oh wow!  This is killer...  try it!
# Pushes current line onto a stack, comes off after next prompt
bindkey -M vicmd "q" push-line-or-edit
#}}}
############################################################################
# PS1 Prompt
############################################################################
#{{{

# Following section just for $vim_mode var hence here.
vim_ins_mode="%{$fg_bold[red]%}[INS]%{$reset_color%}"
vim_cmd_mode="%{$fg_bold[blue]%}[CMD]%{$reset_color%}"
vim_mode=$vim_ins_mode

function zle-keymap-select
{
    vim_mode="${${KEYMAP/vicmd/${vim_cmd_mode}}/(main|viins)/${vim_ins_mode}}"
    zle reset-prompt
}
zle -N zle-keymap-select

function zle-line-finish
{
    vim_mode=$vim_ins_mode
}
zle -N zle-line-finish

# HG prompt like bash-git-prompt
function hg_prompt()
{
    # Standard color escape sequences
    local RED="$fg_no_bold[red]"
    local GREEN="$fg_no_bold[green]"
    local BGREEN="$fg_bold[green]"
    local YELLOW="$fg_no_bold[yellow]"
    local MAGENTA="$fg_bold[magenta]"
    # To (R)eset colors.
    local R="$reset_color"

    local HG=`hg prompt "[${MAGENTA}{branch}${R}{ ${RED}↓{incoming|count}${R}}{ ${GREEN}↑{outgoing|count}${R}}|${YELLOW}{status}{update}${R}]" 2>/dev/null`

    # Strip everything except where status to outgoing would be.
    local T=${HG##*|}
    T=${T%%]}

    # Insert check mark only if T doesn't contain other codes like status or update, see regexp.
    if [ "x${HG}" != "x" ] && [[ ! ${T} =~ [!?^↓↑] ]]; then
        HG="${HG%%]}${BGREEN}✔${R}]"
    fi

    HG_PROMPT="$HG"
}

function prompt_precmd()
{
    if [ $? -eq 0 ]; then
        LAST="%F{green}✔%f"
    else
        LAST="%F{red}✘%f"
    fi

    if [ -d '.hg' ]; then
        hg_prompt
    else
        HG_PROMPT=""
    fi

    vcs_info
}

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
    PS1_HOST=%B%F{magenta}
fi

source ~/.zsh-git-prompt/zshrc.sh

PS1_DEBUG='%B%F{red} >>DEBUG<< ${PS1_R}$LAST { ${PS1_DIR}%~${PS1_R} }
${PS1_USER}%n${PS1_R}@${PS1_HOST}%m${PS1_R}%# '
PS1_STD='$LAST { ${PS1_DIR}%~${PS1_R} } $HG_PROMPT$(git_super_status)${vcs_info_msg_0_}
${PS1_USER}%n${PS1_R}@${PS1_HOST}%m${PS1_R}%# '
PS1="$PS1_STD"

RPROMPT='${vim_mode}'

# Zsh will print when users log in
watch=all                # watch all logins
logcheck=30              # every 30 seconds
WATCHFMT="%n from %M has %a tty%l at %T %W"
#}}}
# vim: set foldmethod=marker:
