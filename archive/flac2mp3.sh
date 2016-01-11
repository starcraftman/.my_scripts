#!/usr/bin/env bash

# This program batch converts all flac files under $ROOT
# to mp3. I strongly recommend using GNU Parallel.

ROOT=$(readlink -f .)
if [ "$#" -gt 0 ];then
    ROOT=$(readlink -f $1)
fi

echo "Will convert to mp3 all flac files under $ROOT"
read -p "Continue? Y/n " INPUT
INPUT=$(tr [:upper:] [:lower:] < <(echo "$INPUT"))

if [ "$INPUT" != "y" ]; then
    echo "Cancelling conversion."
    exit
fi

pushd $ROOT
find . -name "*.flac" > input.txt
cat input.txt

if valid_name parallel; then
    parallel -a input.txt avconv -i "{}" -qscale:a 0 "{.}.mp3"
else
    for file in **/*.flac; do
        avconv -i "$file" -qscale:a 0 "${file%flac}mp3"
    done
fi

rm input.txt
popd
