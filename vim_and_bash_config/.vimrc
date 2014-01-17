" This vimrc is highly customised, these are my top level notes. I've tried to document clearly.
"
" * Vim Cheatsheet and Tutorial:
"       http://www.viemu.com/a_vi_vim_graphical_cheat_sheet_tutorial.html
"
" * Vim regex: http://www.vimregex.com/
"
" * For detailed breakdown of basic vim options:
"       http://amix.dk/vim/vimrc.html
"
" * For color schemes:
"       Large selection of schemes: https://github.com/flazz/vim-colorschemes
"       For molokai latest: https://github.com/tomasr/molokai
"       Put colors folder into ~/.vim/ or use vundle install
"       Favourites: molokai, desert256, jellybeans, wombat256mod, mrkn256, xoria256, twilight256
"
" * To install the plugins:
"   Update Vim:
"       YCM Requires Vim 7.4:
"       http://ubuntuhandbook.org/index.php/2013/08/upgrade-vim-7-4-ubuntu/
"       If can't install, try build from source:
"       https://github.com/Valloric/YouCompleteMe/wiki/Building-Vim-from-source
"
"   Get Vundle:
"       Plugin to manage installation of others
"       git clone https://github.com/gmarik/vundle.git ~/.vim/bundle/vundle
"
"   Run BundleInstall:
"       Run the command to get all bundles.
"       Go to below sites to see configs.
"       After install see YCM page for further compilation.
"
"   YCM Config:
"       Very good autocomplete, you need to compile with clang for c completion functions.
"       Info at url below or use ycm_compile.py in my repo (assumes you have build tools).
"       https://github.com/Valloric/YouCompleteMe
"
"   Syntastic Config:
"       Syntax checking without running code
"       https://github.com/scrooloose/syntastic
"
"   A.vim Config:
"       Swap to a c header for a file with :A.
"       https://github.com/vim-scripts/a.vim
"
"   NERDComment Config:
"       Bunch of comment commands. Mainly , c c/i to comment line.
"       https://github.com/scrooloose/nerdcommenter
"
"   Vim-airline Config:
"       Plugin that gives nice colored status line.
"       https://github.com/bling/vim-airline
"       See :help airline and AirlineToggle
"       NB: Be sure to patch ~/.fonts with https://github.com/Lokaltog/powerline-fonts
"
"   Delete Trailing Whitespace:
"       Use [Range]DeleteTrailingWhitespace, where range
"       is an optional line range.
"       https://github.com/vim-scripts/DeleteTrailingWhitespace
"
"   Vim Surround:
"       Modify the tags or brackets of code.
"       https://github.com/tpope/vim-surround
"
"   Version Control:
"       GIT -> https://github.com/tpope/vim-fugitive
"       Hg -> https://github.com/ludovicchabant/vim-lawrencium
"
"   Completion Alternatives:
"       omniPerl and pydiction.
"       https://github.com/rkulla/pydiction
"
"   Pathogen (Vundle Alternative):
"       https://github.com/tpope/vim-pathogen
"
" Notes:
"
" * To override language specific settings, see ~/.vim/ftplugin for lang files.
"
" * With auto indent on, need to use: set paste|nopaste or <F2> to toggle
"   paste mode that will prevent the auto indenting/format.
"
" * See scrolloff value for interesting effect on vim.
"
" * See list for ability to see trailing whitespace.
"
" * "acommand puts the result into the buffer a.
"
" * Omni complete within file: <CTRL> + p, <CTRL> + n for previous and following identifier.
"
" * Use :help [option|key] to get info.
"   For plugins: :help syntastic, :help YCM
"
" * To see all errors list:
"   open -> :Errors
"   close -> :lclose
"   NB: Overrides location list when called.
"
" * To add identifiers use ctags:
"       https://jeremywsherman.com/blog/2013/07/25/surf-code-with-ctags/
"
" * Code comment:
"   current line -> , c c
"   block comment (with visual) -> V (select) , c c
"   toggle comment for lines: , c i
"
""""""""""""""""""""""""""""""
" => Plugins with Vundle
""""""""""""""""""""""""""""""
" :BundleList          - list configured bundles
" :BundleInstall(!)    - install (update) bundles
" :BundleSearch(!) foo - search (or refresh cache first) for foo
" :BundleClean(!)      - confirm (or auto-approve) removal of unused bundles
"
" see :h vundle for more details or wiki for FAQ
" NOTE: comments after Bundle commands are not allowed.

" Setup required to use Vundle
set nocompatible
filetype off
set rtp+=~/.vim/bundle/vundle
call vundle#rc()

" List bundles after here.
Bundle 'gmarik/vundle'
Bundle 'bling/vim-airline'
Bundle 'ludovicchabant/vim-lawrencium'
Bundle 'scrooloose/nerdcommenter'
Bundle 'scrooloose/syntastic'
Bundle 'tpope/vim-surround'
Bundle 'tpope/vim-fugitive'
Bundle 'Valloric/YouCompleteMe'
Bundle 'vim-scripts/a.vim'
Bundle 'vim-scripts/DeleteTrailingWhitespace'

" Color schemes
" Bundle 'flazz/vim-colorschemes'
Bundle 'tomasr/molokai'

" Turn on after vundle works.
filetype plugin indent on

" Perl Autocomplete, allow : to be in keywords.
" set iskeyword+=:

" Syntastic, syntax checker.
" Info at: http://blog.jpalardy.com/posts/how-to-configure-syntastic/

" Set what chechers are active or passive.
let g:syntastic_mode_map={ 'mode': 'active',
                     \ 'active_filetypes': ['c', 'cpp', 'java', 'python', 'perl', 'ruby', 'sh', 'xml', 'json'],
                     \ 'passive_filetypes': ['lisp', 'xhtml', 'html', 'css', 'javascript'] }

" Check syntax on file open.
let g:syntastic_check_on_open = 1

" Put errors on left side
let g:syntastic_enable_signs = 1

" Format the syntastic message
let g:syntastic_stl_format = '[%E{Err: %fe #%e}%B{, }%W{Warn: %fw #%w}]'

" Manually set important checkers:
let g:syntastic_python_checkers = ['python', 'pep8', 'pylint']
let g:syntastic_perl_checkers = ['perl', 'perlcritic']

" Allow completion of identifiers in comments too.
let g:ycm_complete_in_comments = 1

" Allow ctags for identifier help.
let g:ycm_collect_identifiers_from_tags_files = 1

" Use the following to whitelist dirs with .ycm_extra_conf.py, see my_scripts dir for template. It is a bunch of dir paths.
let g:ycm_extra_conf_globlist = []

" Always delete trailing whitespace from lines on save.
"let g:DeleteTrailingWhitespace = 1
"let g:DeleteTrailingWhitespace_Action = 'delete'

""""""""""""""""""""""""""""""
" => Status line
""""""""""""""""""""""""""""""
set laststatus=2
"let g:airline_theme = 'powerlineish'
let g:airline_enable_syntastic = 1

" Enable a smart tab top.
let g:airline#extensions#tabline#enabled = 1

" Enable powerline fonts.
let g:airline_powerline_fonts = 1

" Old status line
set statusline=%<%1*===\ %5*%f%1*%(\ ===\ %4*%h%1*%)%(\ ===\ %4*%m%1*%)%(\ ===\ %4*%r%1*%)\ ===%====\ %2*%b(0x%B)%1*\ ===\ %3*%l,%c%V%1*\ ===\ %5*%P%1*\ ===%0* laststatus=2

" Syntastic modification to line.
set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*

" Old line without syntastic.
" set statusline=%<%1*===\ %5*%f%1*%(\ ===\ %4*%h%1*%)%(\ ===\ %4*%m%1*%)%(\ ===\ %4*%r%1*%)\ ===%====\ %2*%b(0x%B)%1*\ ===\ %3*%l,%c%V%1*\ ===\ %5*%P%1*\ ===%0* laststatus=2

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => General
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Sets how many lines of history VIM has to remember
set history=1000
set undolevels=1000

" Keep a persistent backup file, preserves undo history between edit sessions.
if has('persistent_undo')
    set undodir=~/.vim/.undo
    set undofile
endif

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
set wildmode=longest,list,full

" Show command in last line, usually on by default.
set showcmd

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => VIM user interface
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set nu "set left side numbers
set ruler "set position in bottom right

" Highlight search results
set hlsearch

" Show matching brackets when text indicator is over them
set showmatch
" How many tenths of a second to blink when matching brackets
set mat=1

" For regular expressions turn magic on
set magic

" When searching ignore case unless contains a cap. Override with \c|\C to force at end of regexp.
set smartcase

" No annoying sound on errors
set noerrorbells
set novisualbell
set t_vb=
set tm=500

" This list is used to build the strings for wildignore and netrw_list_hide.
let exts = ['jpg', 'jpeg', 'png', 'svg', 'bmp', 'gif', 'xpm', 'so', 'dll', 'exe', 'o', 'a']
let exts += ['pyc', 'class', 'com', 'rar', 'zip', 'gz', 'bz2', '7z', 'iso', 'jar', 'dmg', 'deb', 'pdf']

" Add to ignore docs.
"let exts += ['doc', 'docx', 'odt', 'xls', 'xlsx', 'ods', 'ppt', 'pptx', 'odp']

" Build that string.
let wild_s = ''
let hide_s = ''

for i in exts
    let wild_s .= '*.' . i . ','
    let hide_s .= i . '\|'
endfor

" Don't leave trailing separator.
let wild_s = wild_s[:-2]
let hide_s = hide_s[:-3]

" When using autocomplete tab, ignore all matching strings.
let &wildignore = wild_s

" When browsing with netrw, ignore all matching files to this regex.
let g:netrw_list_hide = '\w\+\.\(' . hide_s . '\)\*\?$,\.git/$'

" Customize netrw use a tree style and ignore some extensions.
let g:netrw_liststyle = 3

" Rebinding some commands for managing edits and tabs.
" For regular sessions, use :e file, :bn, :bp to move next, prev buffer. :bd to delete current.
" The tab commands attach to current session for easy swapping.
cnoreabbrev bn bnext
cnoreabbrev bp bprevious
cnoreabbrev tn tabn
cnoreabbrev tp tabp
cnoreabbrev te tabe
cnoreabbrev td tabclose

" I always forget for explore, make some shortcuts. sE for v split, tE for tab.
cnoreabbrev E Explore
cnoreabbrev tE Texplore
cnoreabbrev sE Sexplore!

" Remap Alt + Arrow keys to move between split windows.
nmap <silent> <A-Up> :wincmd k<CR>
nmap <silent> <A-Down> :wincmd j<CR>
nmap <silent> <A-Left> :wincmd h<CR>
nmap <silent> <A-Right> :wincmd l<CR>

" For custom key combos, use leader. See :help <Leader>
let mapleader = ","

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Colors and Fonts
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Enable syntax highlighting
syntax enable

set t_Co=256 " Required to make molokai work.
"let g:molokai_original = 1 " Option to molokai theme.
"let g:rehash256 = 1
set background=dark
colorscheme molokai
" Good colorschemes: molokai, desert256, jellybeans, wombat256mod, mrkn256, xoria256, twilight256

" Set utf8 as standard encoding and en_US as the standard language
set encoding=utf8

" Use Unix as the standard file type
set ffs=unix,dos,mac

" Set font when using gui version.
if has('gui_running')
    set guifont=DejaVu\ Sans\ Mono\ for\ Powerline
endif

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Files, backups and undo
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Turn backup off, since most stuff is in SVN, git et.c anyway...
set nobackup
set nowb
set noswapfile

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

