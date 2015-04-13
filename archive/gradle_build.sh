#!/usr/bin/env bash
ROOT="$(readlink -f .)"
DIR="${ROOT}/gbuild"

usage() {
  echo "Builds gradle projects.
  --dir DIR : Install to DIR.
  gradle    : Build gradle.
  groovy    : Build groovy."
}

build_gradle() {
  git clone --depth 1 -b REL_2.3 https://github.com/gradle/gradle
  pushd gradle
  ./gradlew --parallel install -Pgradle_installPath="$DIR" -x test -x integTest
  popd
  rm -rf gradle
}

build_groovy() {
  curl -fLo groovy.zip http://dl.bintray.com/groovy/maven/groovy-src-2.4.3.zip
  unarchive groovy.zip
  rm groovy.zip
  pushd groovy-*
  ./gradlew --parallel clean dist
  unarchive ./target/distributions/groovy-sdk-2.4.3.zip
  mv groovy* "$DIR"
  popd
  rm -rf groovy-*
}

if [ "$#" -eq 0 ]; then
  usage
  exit
fi

while (( $# > 0 )); do
  arg="$1"
  shift
  case "$arg" in
    *help|-h)
      usage
      exit
      ;;
    *dir)
      DIR="${ROOT}/$1"
      echo "Will now build to: $DIR"
      shift
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
