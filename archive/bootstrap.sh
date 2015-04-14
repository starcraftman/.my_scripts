#!/usr/bin/env bash
GRADLE_TAG=REL_2.3
GROOVY_TAG=GROOVY_2_4_3
PYTHON_URL=https://www.python.org/ftp/python/2.7.9/Python-2.7.9.tar.xz
ZSH_TAG=zsh-5.07
ROOT="$(readlink -f .)"
DIR="${ROOT}/build"

build_gradle() {
  git clone --depth 1 -b $GRADLE_TAG https://github.com/gradle/gradle
  pushd gradle
  ./gradlew --parallel install -Pgradle_installPath="$DIR" -x test -x integTest
  popd
  rm -rf gradle
}

build_groovy() {
  git clone --depth 1 -b $GROOVY_TAG https://github.com/groovy/groovy-core
  pushd groovy-core
  ./gradlew clean dist -x test
  unarchive ./target/distributions/groovy-sdk-2.4.3.zip
  mv groovy* "$DIR"
  popd
  rm -rf groovy-core
}

build_python2() {
  local pyarc=python.tar.xz
  curl -flo "$pyarc" $PYTHON_URL
  xzcat "$pyarc" | tar xvf -
  pushd Python*
  ./configure --prefix=$DIR
  make
  make install
  popd
  rm -rf Python* "$pyarc"
}

build_zsh() {
  git clone --depth 1 -b $ZSH_TAG https://github.com/zsh-users/zsh.git
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
  --ldir DIR : Install into $(pwd)/folder.
  --path PATH: Install into full path.
  gradle     : A java build system.
  groovy     : A python like dynamic lang on jvm.
  python     : Install a local python 2.x.
  zsh        : Latest zsh from source."
}

if [ "$#" -lt 1 -o "$1" == '--help' -o "$1" == '-h' ]; then
  usage
  exit
fi

while (( $# > 0 )); do
  arg="$1"
  shift
  case "$arg" in
    *ldir*)
      DIR="${ROOT}/$1"
      shift
      ;;
    *path*)
      DIR="$1"
      shift
      ;;
    py*)
      build_python2
      ;;
    zsh)
      build_zsh
      ;;
    gradle)
      build_gradle
      ;;
    groovy)
      build_groovy
      ;;
    *) # Default
      echo "$arg: Not Recognized!"
      usage
      ;;
  esac
done
