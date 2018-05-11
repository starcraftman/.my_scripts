#!/usr/bin/env bash

# This program batch converts all flac files under $ROOT
# to mp3. I strongly recommend using GNU Parallel.

ROOT=$(readlink -f .)
if [ "$#" -gt 0 ];then
    ROOT=$(readlink -f "$1")
fi

echo "Will convert to mp3 all flac files under $ROOT"
read -p "Continue? Y/n " INPUT
INPUT=$(tr [:upper:] [:lower:] < <(echo "$INPUT"))

if [ "$INPUT" != "y" ]; then
    echo "Cancelling conversion."
    exit
fi

OLDCWD=$(pwd)
cd "$ROOT"
find . -name "*.flac" > input.txt


# Encode mp3 to 160kbs, alternatives: https://trac.ffmpeg.org/wiki/Encode/MP3
if valid_name parallel; then
    parallel -a input.txt avconv -i "{}" -qscale:a 5 -map_metadata 0:g:0 "{.}.mp3"
else
    while read file; do
        avconv -i "$file" -qscale:a 5 -map_metadata 0:g:0 "${file%flac}mp3"
    done
fi

rm input.txt
cd "$OLDCWD"
