#!/usr/bin/env bash
# Update the color schemes in .vim/colors

DST=~/.vim/colors
URL=http://github.com/
COLORS=( 'chriskempson/vim-tomorrow-theme' 'nanotech/jellybeans.vim' 'Lokaltog/vim-distinguished' \
'morhetz/gruvbox' 'tomasr/molokai' 'tpope/vim-vividchalk' 'vim-scripts/desert256.vim' )

update_colors()
{
    for color ; do
        local gUrl="$URL$color"
        local dir="${color##*/}"
        git clone "$gUrl"
        cp -f ./$dir/colors/*.vim $DST
        rm -rf "$dir"
    done
}

update_colors ${COLORS[@]}
