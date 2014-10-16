#!/usr/bin/env bash
PYTHON_URL=https://www.python.org/ftp/python/2.7.8/Python-2.7.8.tar.xz
ZSH_URL=https://github.com/zsh-users/zsh.git
DIR=~/.opt1

build_py()
{
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


build_zsh()
{
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

    dir=newPath >>> set DIR to install to, be careful.
    py          >>> build python 2 and install to DIR.
    zsh         >>> build latest zsh, install to DIR.
    "
}

if [ "$#" -lt 1 -o "$1" == '--help' -o "$1" == '-h' ]; then
    usage
    exit
fi

for arg; do
    case "$arg" in
        py)
            #build_py
            echo $DIR
            ;;
        zsh)
            #build_zsh
            ;;
        dir*)
            DIR=${arg##*=}
            ;;
        *)
            usage
            exit
            ;;
    esac
done
