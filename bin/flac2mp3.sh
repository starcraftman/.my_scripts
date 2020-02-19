#!/usr/bin/env bash
# This program batch converts all flac files under $ROOT
# to mp3. I strongly recommend using GNU Parallel.
ROOT=$(readlink -f .)
if [ "$#" -gt 0 ];then
    ROOT=$(readlink -f "$1")
fi

FFMPEG=x
if avconv --help > /dev/null 2>&1; then
    FFMPEG=avconv
fi
if ffmpeg --help > /dev/null 2>&1; then
    FFMPEG=ffmpeg
fi
if [ "${FFMPEG}" == "x" ]; then
    echo "This program requires 'ffmpeg' or 'avconv' to convert flac."
    exit 1
fi

# Encode mp3 to about 150kbps
# qscale chart: https://trac.ffmpeg.org/wiki/Encode/MP3
QSCALE=4
if [ "$#" -gt 1 ];then
    QSCALE="$2"
fi

echo "Conversion will use $FFMPEG library, qscale of $QSCALE"
echo "Will convert to mp3 all flac files under $ROOT"
read -rp "Continue? Y/n " INPUT
INPUT=$(tr [:upper:] [:lower:] < <(echo "$INPUT"))

if [ "$INPUT" != "y" ]; then
    echo "Cancelling conversion."
    exit
fi

OLDCWD=$(pwd)
cd "$ROOT" || exit 1
find . -name "*.flac" > input.txt


if valid_name parallel; then
    parallel -a input.txt $FFMPEG -i "{}" -qscale:a $QSCALE -map_metadata 0:g:0 "{.}.mp3"
else
    while read -r file; do
        $FFMPEG -i "$file" -qscale:a $QSCALE -map_metadata 0:g:0 "${file%flac}mp3"
    done
fi

rm input.txt
cd "$OLDCWD" || exit 1
