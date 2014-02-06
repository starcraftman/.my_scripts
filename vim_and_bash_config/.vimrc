" Place marker, ch 32 in vim script hard way.
" If you are confused by not seeing a lot of text, push zi.
" For more info, see :help folding
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Vimrc General Notes
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" {{{

" This vimrc tailors vim to be a good programmers tool.
"
" * Vim Cheatsheet and Tutorial:
"       http://www.viemu.com/a_vi_vim_graphical_cheat_sheet_tutorial.html
"
" * Vim regex: http://www.vimregex.com/
"
" * Vim Script: Used to make plugins and in vimrc for looping etc...
"       http://learnvimscriptthehardway.stevelosh.com/
"
" * Vim NETRW remote editting.
"       http://www.vim.org/scripts/script.php?script_id=1075
"
" * For detailed breakdown of basic vim options, I started by looking at this one:
"       http://amix.dk/vim/vimrc.html
"
" * For color schemes:
"       Large selection of schemes: https://github.com/flazz/vim-colorschemes
"       For molokai latest: https://github.com/tomasr/molokai
"       Put colors folder into ~/.vim/ or use vundle install from github.
"       Favourites: molokai, desert256, jellybeans, wombat256mod, mrkn256, xoria256, twilight256
"
" * To install the plugins:
"   1) Update Vim:
"       YCM Requires Vim 7.4:
"       http://ubuntuhandbook.org/index.php/2013/08/upgrade-vim-7-4-ubuntu/
"       If can't install, try build from source:
"       https://github.com/Valloric/YouCompleteMe/wiki/Building-Vim-from-source
"
"   2) Ensure Vim Python Support:
"       Some plugins use pyhon (like Gundo), check support.
"       If not, recompile with it. See above for debian or source compile.
"       :echo has('python')
"
"   Two Options to continue, use automated script or manually setup.
"   3a) install_system.py 2
"       Will symbolically link .vimrc and .bash_aliases to .my_scripts.
"       Copys basic .vim folder to users home folder.
"       Will download Vundle to right location.
"       Will download powerline fonts for airline.
"       Will download and setup hg-prompt and git-bash-prompt.
"
"   3b) Manually continue to do the above. Copy/link manually.
"   Get Vundle:
"       Plugin to manage installation of others.
"       For initial setup:
"           mkdir -p ~/.vim/bundle
"           git clone https://github.com/gmarik/vundle.git ~/.vim/bundle/vundle
"       Further information:
"       https://github.com/gmarik/vundle
"
"   4) Run BundleInstall:
"       Run the command to get all bundles.
"
"   5) Further Config:
"       YouCompleteMe: Requires cpp compilation, see notes.
"       vim-airline: Requires powerline font modification.
"       TagBar: Requires exhuberant tags instead of gnu ctags.
"       Dirs: Make ~/.vim/undo and ~/.vim/snippets
"
"Plugin Info:
"
"   Vundle:
"       Very good plugin manager, only supports git.
"       Need to look into revision support, doesn't work at this time.
"       https://github.com/gmarik/vundle
"
"   YouCompleteMe:
"       Very good autocomplete, you need to compile with clang for c completion functions.
"       Info at url below or use ycm_compile.py in my repo (assumes you have build tools for c++ compilation).
"       https://github.com/Valloric/YouCompleteMe
"
"   Syntastic:
"       Syntax checking without running code usually on buffer write. Errors highlighted in left margin.
"       https://github.com/scrooloose/syntastic
"       Extra Info: http://blog.jpalardy.com/posts/how-to-configure-syntastic/
"
"   A.vim:
"       Swap between a c source and header file with :A.
"       https://github.com/vim-scripts/a.vim
"
"   NERDComment:
"       Bunch of comment commands. Mainly <leader>ci to comment line.
"       https://github.com/scrooloose/nerdcommenter
"
"   vim-airline:
"       Plugin that gives nice colored status line.
"       https://github.com/bling/vim-airline
"       See :help airline and AirlineToggle
"       NB: Be sure to patch ~/.fonts with powerline-fonts
"       See: https://powerline.readthedocs.org/en/latest/installation/linux.html#font-installation
"
"   DeleteTrailingWhitespace:
"       Use [Range]DeleteTrailingWhitespace, where range is an optional line range.
"       https://github.com/vim-scripts/DeleteTrailingWhitespace
"
"   vim-surround:
"       Modify the tags or brackets of code.
"       https://github.com/tpope/vim-surround
"
"   TagBar:
"       A outline of the files contents.
"       Uses exuberant ctags, not GNU ctags.
"       See info at: https://github.com/majutsushi/tagbar
"
"   CtrlP:
"       Fuzzy file finding that is a bit easier than CtrlT.
"       Searches under root, looks for .hg/.git or so to define top.
"       Use Ctlr+P to access.
"       https://github.com/kien/ctrlp.vim
"
"   Gundo:
"       Graphical tree like explorer for visualizing undo history.
"       Project: https://github.com/sjl/gundo.vim
"       Usage: http://sjl.bitbucket.org/gundo.vim/#Usage
"
"   vim-sneak:
"       Provies quick motion for cursor.
"       Keys:
"           s<char><char> - search for word
"           s/; - next word
"           S/, - prev word match
"           ctrl + o - back to start
"       https://github.com/justinmk/vim-sneak
"
"   vim-matchit:
"       Extends the % command to jump to matching xml or if/fi tags.
"       https://github.com/edsono/vim-matchit
"
"   ultisnips:
"       Same as SnipMate, seems that project may be unmaintained.
"       https://github.com/SirVer/ultisnips
"
"   Version Control:
"       GIT -> https://github.com/tpope/vim-fugitive
"       Hg -> https://github.com/ludovicchabant/vim-lawrencium
"
"Unused Plugins:
"
"   EasyMotion
"       Provides alternative motion for word jumping.
"       Use <leader><leader>w to jump then select.
"       https://github.com/Lokaltog/vim-easymotion
"
"   SnipMate:
"       Allows you to expand boilerplate code.
"       https://github.com/msanders/snipmate.vim
"       Usage: http://www.bestofvim.com/plugin/snipmate/
"       Related: https://github.com/scrooloose/snipmate-snippets
"
"   NERDTree:
"       Plugin that is a pretty NETRW replacement. I'm not sure I want it, but may re-evaluate.
"       Open with :NERDTree command.
"       https://github.com/scrooloose/nerdtree
"
"   Completion Alternatives:
"       omniPerl and pydiction.
"       https://github.com/rkulla/pydiction
"
"   Pathogen:
"       A manual alternative to Vundle.
"       https://github.com/tpope/vim-pathogen
"
" Notes:
"
" * To indent:
"       5>>: Indent next 5 lines 1 tab.
"       5<<: De-Indent next 5 lines 1 tab.
"
" * Use :help [option|key] to get info.
"   For plugins: :help syntastic, :help YCM
"
" * To override language specific settings, see ~/.vim/ftplugin for lang files.
"
" * With auto indent on, need to use: set paste|nopaste or <F2> to toggle
"   paste mode that will prevent the auto indenting/format.
"
" * See scrolloff value for interesting effect on vim. Keeps certain amount of lines always below cursor when scrolling.
"
" * See list for ability to see trailing whitespace.
"
" * Omni complete within file: <CTRL> + p, <CTRL> + n for previous and following identifier.
"
" * To see all errors list:
"   open -> :Errors
"   close -> :lclose
"   NB: Overrides location list when called.
"
" * Code comment:
"   current line -> , c c
"   block comment (with visual) -> V (select) , c c
"   toggle comment for lines: , c i
"
" * Reindent a file:
"       Whole File: ,t
"       Some Lines: <movement>=
"
" * To see folded code:
"       za

" }}}
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Plugins with Vundle
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" {{{
" :BundleList          - list configured bundles
" :BundleInstall(!)    - install (update) bundles
" :BundleSearch(!) foo - search (or refresh cache first) for foo
" :BundleClean(!)      - confirm (or auto-approve) removal of unused bundles
"
" see :h vundle for more details or wiki for FAQ
" NOTE: comments after Bundle commands are not allowed.

" Disable compatability mode. Set runtime path.
set nocompatible
set runtimepath+=~/.vim/bundle/vundle/

" Turn off filetype stuff during Bundle ops.
filetype off

" Init call.
call vundle#rc()

" List bundles after here. No comments on bundle line.
Bundle 'gmarik/vundle'

" Heaviest plugins.
Bundle 'Valloric/YouCompleteMe'
Bundle 'scrooloose/syntastic'
Bundle 'bling/vim-airline'
Bundle 'SirVer/ultisnips'

" Regular plugins.
Bundle 'edsono/vim-matchit'
Bundle 'justinmk/vim-sneak'
Bundle 'kien/ctrlp.vim'
Bundle 'ludovicchabant/vim-lawrencium'
Bundle 'majutsushi/tagbar'
Bundle 'scrooloose/nerdcommenter'
Bundle 'sjl/gundo.vim'
Bundle 'tpope/vim-fugitive'
Bundle 'tpope/vim-surround'
Bundle 'vim-scripts/a.vim'
Bundle 'vim-scripts/DeleteTrailingWhitespace'

" Color schemes
Bundle 'tomasr/molokai'
" Large number of schemes to try:
"Bundle 'flazz/vim-colorschemes'

" Turn on after vundle works.
filetype plugin indent on

" Perl Autocomplete, allow : to be in keywords.
" set iskeyword+=:

" Syntastic
"""""""""""
" Set what chechers are active or passive.
let g:syntastic_mode_map={ 'mode': 'active',
                     \ 'active_filetypes': ['c', 'cpp', 'java', 'python', 'perl', 'ruby', 'sh', 'xml', 'json'],
                     \ 'passive_filetypes': ['lisp', 'xhtml', 'html', 'css', 'javascript'] }

" Check syntax on file open.
let g:syntastic_check_on_open = 1

" Show errors in the line numbers to left. Signs can be configured, see help.
let g:syntastic_enable_signs = 1

" Format the syntastic message
let g:syntastic_stl_format = '[%E{Err: %fe #%e}%B{, }%W{Warn: %fw #%w}]'

" List of files to ignore checking, may be useful later.
let g:syntastic_ignore_files = ['\m^/usr/include/']

" Manually set important checkers:
let g:syntastic_python_checkers = ['python', 'pep8', 'pylint']
let g:syntastic_perl_checkers = ['perl', 'perlcritic']

" YouCompleteMe
"""""""""""""""
" Allow completion of identifiers in comments too.
let g:ycm_complete_in_comments = 1

" Allow ctags for identifier help.
"let g:ycm_collect_identifiers_from_tags_files = 1

" Use next line to disable ultisnips completion.
"let g:ycm_use_ultisnips_completer = 0

" Use the following to whitelist dirs with .ycm_extra_conf.py, see my_scripts dir for template. It is a bunch of dir paths.
let g:ycm_extra_conf_globlist = [ '~/programming/ReconstructingCaveStory/.ycm_extra_conf.py' ]

" UltiSnips
"""""""""""
" Set dir to .vim section.
let g:UltiSnipsSnippetsDir = '~/.vim/snippets'

" Key bindings for UltiSnips. All of these are ctrl + key.
let g:UltiSnipsExpandTrigger       = '<c-j>'
let g:UltiSnipsListSnippets        = '<c-l>'
let g:UltiSnipsJumpForwardTrigger  = '<c-j>'
let g:UltiSnipsJumpBackwardTrigger = '<c-k>'

" Sneak
"""""""
" Allows quick motion when more than 2 matches.
let g:sneak#streak = 1

" Allows smart case usage of sneak.
let g:sneak#use_ic_scs = 1

" Toggle to allow or prevent sneak in netrw.
" When enabled, moves old s binding to <leader>s/S.
let g:sneak#map_netrw = 1

" CtrlP
"""""""
" Index hidden files.
let g:ctrlp_show_hidden = 1

" DeleteTrailingWhitespace
""""""""""""""""""""""""""
" Always delete trailing whitespace from lines on save.
"let g:DeleteTrailingWhitespace = 1
"let g:DeleteTrailingWhitespace_Action = 'delete'

" }}}
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Status line
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" {{{

" vim-Airline
"""""""""""""
" Enable syntastic integration.
let g:airline_enable_syntastic = 1

" Enable a smart tab top.
let g:airline#extensions#tabline#enabled = 1

" Enable powerline fonts.
let g:airline_powerline_fonts = 1

" Regular Status Line
"""""""""""""""""""""
set statusline=%<%1*===\ %5*%f%1*%(\ ===\ %4*%h%1*%)%(\ ===\ %4*%m%1*%)%(\ ===\ %4*%r%1*%)\ ===%====\ %2*%b(0x%B)%1*\ ===\ %3*%l,%c%V%1*\ ===\ %5*%P%1*\ ===%0* laststatus=2

" Syntastic modification to line.
set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*

" Old line without syntastic.
" set statusline=%<%1*===\ %5*%f%1*%(\ ===\ %4*%h%1*%)%(\ ===\ %4*%m%1*%)%(\ ===\ %4*%r%1*%)\ ===%====\ %2*%b(0x%B)%1*\ ===\ %3*%l,%c%V%1*\ ===\ %5*%P%1*\ ===%0* laststatus=2

" }}}
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Key Mappings
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" {{{

" For custom key combos, use leader. See :help <leader>
let mapleader = ","

" Apparently used for buffer/filetype specific bindings.
let maplocalleader = '\\'

" Rebinding some commands for managing edits and tabs. Some of these exist, I put them here to remember.
" For regular sessions, use :e file, :bn, :bp to move next, prev buffer. :bd to delete current.
" The tab commands attach to current session for easy swapping.
cnoreabbrev bn bnext
cnoreabbrev bp bprevious
cnoreabbrev tn tabn
cnoreabbrev tp tabp
cnoreabbrev te tabe
cnoreabbrev td tabclose

" I always forget for explore, make some shortcuts. Ev for v split, Et for tab.
cnoreabbrev E Explore
cnoreabbrev Et Texplore
cnoreabbrev Ev Sexplore!

" Shortcuts for bundle management.
cnoreabbrev bi BundleInstall
cnoreabbrev bu BundleUpdate
cnoreabbrev bc BundleClean

" Faster binding to escape insert.
inoremap <leader>i <esc>
"inoremap <esc> <nop>

" To open NERDTree when used.
"nnoremap <silent> <leader>n :NERDTreeToggle<CR>

" Remap Alt + Arrow keys to move between split windows.
nnoremap <silent> <A-Up> :wincmd k<CR>
nnoremap <silent> <A-Down> :wincmd j<CR>
nnoremap <silent> <A-Left> :wincmd h<CR>
nnoremap <silent> <A-Right> :wincmd l<CR>

" Add shortcut to jump to definition/declaration of c file.
nnoremap <leader>jd :YcmCompleter GoToDefinitionElseDeclaration<CR>

" Shortcut to remember how to reindent file.
nnoremap <leader>t gg=G

" Paste toggle button, disables f1 help use command instead.
set pastetoggle=<F1>

" Shortcut for tagbar outline of file.
nnoremap <silent> <F2> :TagbarToggle<CR>

" Shortcut for gundo sidebar.
nnoremap <silent> <F3> :GundoToggle<CR>

" }}}
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => General Options
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" {{{

" Sets how many lines of history VIM has to remember
set history=1000
set undolevels=1000

" Keep a persistent backup file, preserves undo history between edit sessions.
if has('persistent_undo')
    set undodir=~/.vim/undo
    set undofile
endif

" Set to auto read when a file is changed from the outside
set autoread

" Minimum number of lines that will always be above/below cursor.
set scrolloff=10

" Allow hiding of files, when using standard :e filename option.
set hidden

" Show whitespace markers on screen, disabled by default.
"set list

" Autocomplete feature for command mode (i.e. :command).
set wildmenu
set wildmode=longest,list,full

" Show command in last line, usually on by default.
set showcmd

" Turn backup off, since most files in a VCS.
set nobackup
set nowritebackup
set noswapfile

" No annoying sound on errors.
set noerrorbells
set novisualbell
set t_vb=
set tm=500

" Folding method.
set foldmethod=marker

" }}}
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => VIM User Interface & Search
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" {{{

" Set line numbering on left.
set number

" Set position indicator on bottom right.
set ruler

" Highlight search results.
set hlsearch

" Incrementally highlight first matching word as you type a search.
set incsearch

" Show matching brackets when text indicator is over them.
set showmatch
" How many tenths of a second to blink when matching brackets.
set matchtime=1

" For regular expressions turn magic on. Means don't need to \* in regex.
set magic

" When searching ignore case unless contains a cap. Override with \c|\C to force at end of regexp.
set smartcase

" }}}
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => NETRW File Explorer
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" {{{

" This list is used to build the strings for wildignore and netrw_list_hide.
" Any file ending in one of these extensions will be ignored in command completion & netrw browser.
let exts = ['jpg', 'jpeg', 'png', 'svg', 'bmp', 'gif', 'xpm', 'so', 'dll', 'exe', 'o', 'a']
let exts += ['pyc', 'class', 'com', 'rar', 'zip', 'gz', 'bz2', '7z', 'iso', 'jar', 'dmg', 'deb', 'pdf']

" Add to ignore docs.
"let exts += ['doc', 'docx', 'odt', 'xls', 'xlsx', 'ods', 'ppt', 'pptx', 'odp']

" Processing here to build a large regexp, basically ignores all files ending in above extensions.
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

" Set the explorer sorting to case insensitive.
let g:netrw_sort_options = 'i'

" }}}
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Colors and Fonts
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" {{{

" Enable syntax highlighting
syntax enable

" Required to make molokai work. Sets color mode to 256.
set t_Co=256

" Set dark background before, else colors off.
set background=dark
colorscheme molokai
" Other good colorschemes:
"   molokai, desert256, jellybeans, wombat256mod, mrkn256, xoria256, twilight256

" Set UTF-8 for file enconding.
set encoding=utf8

" The order of EOL symbols to try. Prefer unix.
set fileformats=unix,dos,mac

" Set font when using gui version.
if has('gui_running')
    set guifont=DejaVu\ Sans\ Mono\ for\ Powerline
endif

" }}}
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Text, tab and indent related
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" {{{

" 1 tab == 4 spaces
set softtabstop=4
set shiftwidth=4
set tabstop=4

" Use spaces instead of tabs.
set expandtab

" When push tab in insert shift by tabstop, when backspace delete tabstop amount.
set smarttab

" Copy indent at current when inserting new line.
set autoindent

" Automatically insert some indents after certain actions.
set smartindent

" Wrap lines when hit right side, doesn't affect buffer.
set wrap

" Makes smarter decisions about what stays on wrapped line.
set linebreak

" When inserting text, force a line break at this amount. Set to 0 to disable.
set textwidth=500

" }}}
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Filetype Specific (avoids too many files)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" {{{

" Always wrap autocmds in this structure, autocmds get duped on each source of this file.
augroup filetype_funcs
    autocmd!
    autocmd FileType ruby call SetRubyOptions()
augroup END

function SetRubyOptions()
    " Set tabs to 2 spaces, seems ruby tradition.
    setl softtabstop=2
    setl shiftwidth=2
    setl tabstop=2
endfunction

" }}}
