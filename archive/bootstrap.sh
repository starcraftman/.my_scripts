#!/usr/bin/env bash
PYTHON_URL=https://www.python.org/ftp/python/2.7.9/Python-2.7.9.tar.xz
ZSH_URL=https://github.com/zsh-users/zsh.git
DIR=~/.opt1

build_python2() {
    local pyarc=python.tar.xz
    curl $PYTHON_URL > "$pyarc"
    xzcat "$pyarc" | tar xvf -
    pushd Python*
    ./configure --prefix=$DIR
    make
    make install
    popd
    rm -rf Python* "$pyarc"
}


build_zsh() {
    git clone https://github.com/zsh-users/zsh.git
    pushd zsh
    ./Util/preconfig
    autoconf
    ./configure --prefix=$DIR
    make
    make install
    popd
    rm -rf zsh
}

usage() {
    echo "$(basename $0) arg1 arg2 ...

    dir ./newPath >>> set DIR to install to, be careful.
    py|python     >>> build python 2 and install to DIR.
    zsh           >>> build latest zsh, install to DIR.
    "
}

if [ "$#" -lt 1 -o "$1" == '--help' -o "$1" == '-h' ]; then
    usage
    exit
fi

while (( $# > 0 )); do
    arg="$1"
    shift
    case "$arg" in
        dir*)
            DIR="$1"
            shift
            ;;
        py*)
            build_python2
            ;;
        zsh)
            build_zsh
            ;;
        *)
            usage
            exit
            ;;
    esac
done
