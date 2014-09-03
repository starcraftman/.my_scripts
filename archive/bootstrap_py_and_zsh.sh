#!/usr/bin/env bash
PYTHON_URL=https://www.python.org/ftp/python/2.7.8/Python-2.7.8.tar.xz
ZSH_URL=https://github.com/zsh-users/zsh.git
DIR=$(pwd)/test

build_py() {
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

echo "Simple bootstrapper to get python & zsh on systems that might\
not have packages for it."
echo "Change DIR to point to the target to install to."
