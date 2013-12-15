" For customization details: http://amix.dk/vim/vimrc.html
"
" For color schemes:
" https://github.com/flazz/vim-colorschemes
" Put colors folder into ~/.vim/
" 
" For molokai latest: https://github.com/tomasr/molokai
"
" Important Notes:
" * With auto indent on, need to use: set paste|nopaste or <F2> to toggle
"   paste mode that will prevent the auto indenting/format.
"
" * See scrolloff value for interesting effect on vim.
"
" * See list for ability to see trailing whitespace.
"
" * Don't forget that "acommand puts the result into the buffer.
" 
" * Vim regex: http://www.vimregex.com/
"
" * Use :help [option|key] to get info.
" 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => General
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Turn off vi compatability to get latest vim features.
set nocompatible

" Sets how many lines of history VIM has to remember
set history=1000
set undolevels=1000

" Keep a persistent backup file, preserves undo history between edit sessions.
if has('persistent_undo')
    set undodir=~/.vim/.undo
    set undofile               
endif

" Enable filetype plugins and indenting.
filetype plugin on
filetype indent on

" Set to auto read when a file is changed from the outside
set autoread

" Minimum number of lines that will always be above/below cursor.
set scrolloff=10

" Paste toggle button.
set pastetoggle=<F2>

" Allow hiding of files, when using standard :e filename option.
set hidden

" Show whitespace markers on screen, disabled by default.
"set list

" Autocomplete feature for command mode (i.e. :command).
set wildmenu

" Show command in last line, usually on by default.
set showcmd

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => VIM user interface
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set nu "set left side numbers
set ruler "set position in bottom right

" Ignore compiled code.
set wildignore=*.0,*~,*.pyc,*.exe,*.class,*.o,*.so,*.dll,*.com,*.swp,*.bak

" Highlight search results
set hlsearch

" Show matching brackets when text indicator is over them
set showmatch
" How many tenths of a second to blink when matching brackets
set mat=1

" For regular expressions turn magic on
set magic

" No annoying sound on errors
set noerrorbells
set novisualbell
set t_vb=
set tm=500

" Rebinding some commands for managing edits and tabs.
" For regular sessions, use :e file, :n, :p.
" The tab commands attach to current session for easy swapping.
ca p prev
ca tn tabn
ca tp tabp
ca te tabe

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Colors and Fonts
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Enable syntax highlighting
syntax enable

set t_Co=256 " Required to make molokai work.
let g:molokai_original = 0 " Option to molokai theme.
colorscheme molokai_sjl 
set background=dark

" Set utf8 as standard encoding and en_US as the standard language
set encoding=utf8

" Use Unix as the standard file type
set ffs=unix,dos,mac

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Files, backups and undo
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Turn backup off, since most stuff is in SVN, git et.c anyway...
"set nobackup
"set nowb
"set noswapfile

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Text, tab and indent related
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Use spaces instead of tabs
set expandtab

" Be smart when using tabs ;)
set smarttab

" 1 tab == 4 spaces
set softtabstop=4
set shiftwidth=4
set tabstop=4

" Linebreak on 500 characters
set lbr
set tw=500

" Indenting options and wrapping lines.
set ai "Auto indent
set si "Smart indent
set wrap "Wrap lines

""""""""""""""""""""""""""""""
" => Status line
"""""""""""""""""""""""""""""""
set statusline=%<%1*===\ %5*%f%1*%(\ ===\ %4*%h%1*%)%(\ ===\ %4*%m%1*%)%(\ ===\ %4*%r%1*%)\ ===%====\ %2*%b(0x%B)%1*\ ===\ %3*%l,%c%V%1*\ ===\ %5*%P%1*\ ===%0* laststatus=2

