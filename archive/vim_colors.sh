#!/usr/bin/env bash
# Update the color schemes in .vim/colors
DST=~/.vim/colors
URL=http://github.com/
THEMES=( 'chriskempson/vim-tomorrow-theme' 'nanotech/jellybeans.vim' 'Lokaltog/vim-distinguished' \
'morhetz/gruvbox' 'tomasr/molokai' 'tpope/vim-vividchalk' 'vim-scripts/desert256.vim' 'w0ng/vim-hybrid' )
TMP_DIR=/tmp/vim_colors

update_themes() {
    for theme ; do
        local gUrl="$URL$theme"
        git clone "$gUrl" "$TMP_DIR"
        cp -f $TMP_DIR/colors/*.vim $DST
        rm -rf "$TMP_DIR"
    done
}

if [ ! -d ~/.vim/colors ]; then
    mkdir ~/.vim/colors
fi

update_themes ${THEMES[@]}
