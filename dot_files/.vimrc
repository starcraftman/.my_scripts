" If you are confused by not seeing a lot of text, push zi
" For more info, see :help folding
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Vimrc General Notes
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" {{{

" Quick Links
"""""""""""""
" {{{

" * Vim Cheatsheet and Tutorial:
"       http://www.viemu.com/a_vi_vim_graphical_cheat_sheet_tutorial.html
"
" * Vim regex:
"       http://www.vimregex.com/
"
" * Vim Script: Learn to make plugins and contructs like loops, vars and commands
"       http://learnvimscriptthehardway.stevelosh.com/
"
" * Vim Syntax/Indent Files:
"       http://robots.thoughtbot.com/writing-vim-syntax-plugins
"
" * Vim NETRW remote editting
"       http://www.vim.org/scripts/script.php?script_id=1075
"
" * Explore plugins at:
"       http://vimawesome.com/

" * For detailed breakdown of basic vim options, I started by looking at this one:
"       http://amix.dk/vim/vimrc.html
"
" * For color schemes:
"       Large selection of schemes: https://github.com/flazz/vim-colorschemes
"       Put schemes in ~/.vim/colors or use Vundle
"       Favourites In Order:
"           molokai, jellybeans, desert256, wombat256mod, mrkn256, xoria256, twilight256
"
" }}}
" Installation Procedure
""""""""""""""""""""""""
" {{{

"   1) Install Vim 7.4 with Python, Lua & Signs:
"     a) Linux Package
"       http://ubuntuhandbook.org/index.php/2013/08/upgrade-vim-7-4-ubuntu/
"
"     b) POSIX Source Build
"       BuildSrc.py vim
"       OR
"       https://github.com/Valloric/YouCompleteMe/wiki/Building-Vim-from-source
"
"     b) Windows
"       Download and extract:
"       http://tuxproject.de/projects/vim/complete.7z
"       Put the lua52.dll in the root project
"       http://sourceforge.net/projects/luabinaries/files/5.2/Windows%20Libraries/Dynamic/"
"
"     c) Windows Babun (Cygwin)
"       https://github.com/babun/babun
"
"   2) Check Support for features:
"       :echo has('lua') && has('python') && has('signs')
"
"   3) Next setup config fils (.vim, .vimrc and so on)
"     a) Python Script
"       SysInstall home
"           Symbolically links .vim & .vimrc to home.
"           Downloads Vundle.vim to .vim/bundle.
"           Sets up powerline fonts for airline.
"
"     b) Manually link/copy/download above. See ~/.my_scripts/dot_files
"       Link from ~/.my_scripts/dot_files to $HOME
"       Get Vundle:
"           mkdir -p ~/.vim/bundle
"           git clone https://github.com/gmarik/vundle.git ~/.vim/bundle/vundle
"       Further information:
"           https://github.com/gmarik/vundle
"
"   4) Open vim and install plugins
"       :PluginInstall
"
"   5) Further Config:
"       YouCompleteMe: Requires cpp compilation, see BuildSrc.py ycm.
"       vim-airline: Requires powerline font modification
"       TagBar: Requires exhuberant tags instead of gnu ctags
"       ag.vim: Install 'silversearcher-ag' package.
"       ack.vim: Check for ack package.
"       eclim: Follow install at: http://eclim.org/install.html

" }}}
" Plugin Information
""""""""""""""""""""
" {{{

"   Vundle:
"       Very good plugin manager, only supports git
"       Need to look into revision support, doesn't work at this time
"       https://github.com/gmarik/vundle
"
"   YouCompleteMe:
"       Very good autocomplete, includes path completion,
"       automatic function indexing and clang checking with syntastic
"       Info at url below or use ycm_compile.py in my repo
"       https://github.com/Valloric/YouCompleteMe
"
"   Syntastic:
"       Syntax checking without running code usually on buffer write
"       https://github.com/scrooloose/syntastic
"       Extra Info: http://blog.jpalardy.com/posts/how-to-configure-syntastic/
"
"   vim-airline:
"       Plugin that gives nice colored status line
"       https://github.com/bling/vim-airline
"       See :help airline and AirlineToggle
"       NB: Be sure to patch ~/.fonts with powerline-fonts
"       See: https://powerline.readthedocs.org/en/latest/installation/linux.html#font-installation
"
"   ultisnips:
"       Same as SnipMate, seems that project may be unmaintained
"       https://github.com/SirVer/ultisnips
"       Required default snippets now externalized to below
"       https://github.com/honza/vim-snippets
"
"   vim-sneak:
"       Provies quick motion for cursor
"       Keys:
"           s<char><char> - search for word
"           s/; - next word
"           S/, - prev word match
"           ctrl + o - back to start
"       https://github.com/justinmk/vim-sneak
"
"   CtrlP:
"       Fuzzy file finding that is a bit easier than CtrlT
"       Searches under root, looks for .hg/.git or so to define top
"       Use Ctlr+P to access
"       https://github.com/kien/ctrlp.vim
"
"   TagBar:
"       A outline of the files contents
"       Uses exuberant ctags, not GNU ctags
"       See info at: https://github.com/majutsushi/tagbar
"
"   Gundo:
"       Graphical tree like explorer for visualizing undo history
"       Project: https://github.com/sjl/gundo.vim
"       Usage: http://sjl.bitbucket.org/gundo.vim/#Usage
"
"  abolish:
"       Help for renaming, has easy syntax alternative to regexp.
"       https://github.com/tpope/vim-abolish
"
"   NERDComment:
"       Bunch of comment commands. Mainly <leader>ci to comment line
"       https://github.com/scrooloose/nerdcommenter
"
"   vim-surround:
"       Modify the tags or brackets of code
"       https://github.com/tpope/vim-surround
"
"   vim-matchit:
"       Extends the % command to jump to matching xml or if/fi tags
"       https://github.com/edsono/vim-matchit
"
"   A.vim:
"       Swap between a c source and header file with :A
"       https://github.com/vim-scripts/a.vim
"
"   DeleteTrailingWhitespace:
"       Use [Range]DeleteTrailingWhitespace, where range is an optional line range
"       https://github.com/vim-scripts/DeleteTrailingWhitespace
"
"   vim-Markdown:
"       Adds support for markdown syntax
"       https://github.com/plasticboy/vim-markdown/
"
"   vim-signify:
"       Shows the diff of file being eddited to left of numbers, i.e. 'gutter'
"       https://github.com/mhinz/vim-signify
"
"   vim-sleuth:
"       Detects the right whitespace useage based on file detection.
"       https://github.com/tpope/vim-sleuth
"
"   open-browser:
"       Provides OpenBrowser URI to go directly to your local browser.
"       https://github.com/tyru/open-browser.vim
"
"   vim-togglelist:
"       Provides simple keystroke to toggle lists.
"       https://github.com/kshenoy/vim-togglelist
"
"   ag.vim (Silver Searcher):
"       Searches code quickly, faster than grep. Requires silversearcher-ag.
"       https://github.com/rking/ag.vim
"
"   ack.vim:
"       Same as ag.vim, though based on ack-grep a perl file.
"       https://github.com/mileszs/ack.vim
"
"   FastFold:
"       Make folding bit faster.
"       https://github.com/zaiste/tmux.vim
"
"   Tabular:
"       Align text easily with regex patterns.
"       https://github.com/godlygeek/tabular
"
"   tmux.vim:
"       Syntax highlighting for .tmux.conf files.
"       https://github.com/zaiste/tmux.vim
"
"   vim-zsh:
"       Better syntax highlighting for zsh.
"       https://github.com/clones/vim-zsh
"
"   csv.vim:
"       Whole suite to make editting csv easier.
"       https://github.com/chrisbra/csv.vim
"
"   LaTeX-Box:
"       Better highlighting and functions for LaTeX.
"       https://github.com/LaTeX-Box-Team/LaTeX-Box
"
"   vim-bookmarks:
"       Better marking, nice sign usage.
"       https://github.com/'MattesGroeger/vim-bookmarks
"
"   Version Control:
"       GIT -> https://github.com/tpope/vim-fugitive
"       Hg -> https://github.com/ludovicchabant/vim-lawrencium

" }}}
" Less Used Plugins
"""""""""""""""""""
" {{{

"   neocomplete:
"       Fairly complete YCM replacement for on Windows.
"       https://github.com/Shougo/neocomplete.vim
"
"   NERDTree:
"       Plugin that is a pretty NETRW replacement. I'm not sure I want it, but may re-evaluate
"       Open with :NERDTree command
"       https://github.com/scrooloose/nerdtree
"
"   Local Vimrc:
"       Allows project specific settings with .lvimrc files
"       https://github.com/embear/vim-localvimrc
"
"   Cmd Alias:
"       Better command remapping instead of cabbr.
"       http://www.vim.org/scripts/script.php?script_id=746
"       https://github.com/vim-scripts/cmdalias.vim
"
"   CtrlP Switcher:
"       Finds files in the tree similar to current buffer
"       https://github.com/ivan-cukic/vim-ctrlp-switcher
"
"   SnipMate:
"       Allows you to expand boilerplate code
"       https://github.com/msanders/snipmate.vim
"       Usage: http://www.bestofvim.com/plugin/snipmate/
"       Related: https://github.com/scrooloose/snipmate-snippets
"
"   EasyMotion
"       Provides alternative motion for word jumping
"       Use <leader><leader>w to jump then select
"       https://github.com/Lokaltog/vim-easymotion
"
"   Golden View:
"       Based on golden ratio for windows.
"       https://github.com/zhaocai/GoldenView.vim
"
"   Golden Ratio:
"       Plugin that resizes windows on focus gain. Neat.
"       https://github.com/roman/golden-ratio
"
"   html5.vim:
"       Provides better highlighting for new html5 elements.
"       https://github.com/Sothree/html5.vim
"
"   vim-css-color:
"       Provides highlighting of color codes like hex and regular words like red.
"       https://github.com/ap/vim-css-color
"
"   vim-css3-syntax:
"       Provides better highlighting for css3 files.
"       https://github.com/hail2u/vim-css3-syntax
"
"   vim-javascript:
"       Has some improvements to syntax and indents.
"       https://github.com/pangloss/vim-javascript
"
"   jshint:
"       Provides javascript checking, requires node.js and other installation steps.
"       https://github.com/Shutnik/jshint2.vim
"
"   jQuery:
"       Plugin provides better highlighting for jQuery.
"       https://github.com/vim-scripts/jQuery
"
"   php.vim:
"       Improved php syntax files.
"       https://github.com/elzr/vim-json
"
"  vim-ruby:
"       Provides better syntax, indent and config for ruby dev.
"       https://github.com/vim-ruby/vim-ruby/wiki/VimRubySupport
"
"   Pathogen:
"       A manual alternative to Vundle
"       https://github.com/tpope/vim-pathogen

" }}}
" Notes To Remember
"""""""""""""""""""
" {{{

" * To indent:
"       5>>: Indent next 5 lines 1 tab
"       5<<: De-Indent next 5 lines 1 tab
"
" * Use :help [option|key] to get info
"   For plugins: :help syntastic, :help YCM
"
" * To override language specific settings, see ~/.vim/ftplugin for lang files
"
" * With auto indent on, need to use: set paste|nopaste or <F2> to toggle
"   paste mode that will prevent the auto indenting/format
"
" * See scrolloff value for interesting effect on vim
"   Keeps certain amount of lines always below cursor when scrolling
"
" * See list for ability to see trailing whitespace
"
" * Omni complete within file: <CTRL> + p, <CTRL> + n for previous and following identifier
"
" * To see all errors list:
"   open -> :Errors
"   close -> :lclose
"   NB: Overrides location list when called
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
"
" * To see conflicting maps:
"       :verbose map <leader>jd
"
" * To repeat last command (colon): `@:`, to repeat last register `@@`.
"
" * To fix tabs, see `retab`. By default, %retab!
"
" * To paste yanked text in for Command, Ctrl + R then " (double quote)
"
" * With cursor over work, push K in nmode. Opens manpage.

" }}}

" }}}
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Plugins with Vundle
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" {{{

" Plugins
"""""""""
" {{{

" Vundle docs -> :help vundle
set nocompatible
filetype off

" On Windows with cmd.exe use vimfiles, else use normal unix .vim folder.
let g:win_shell = (has('win32') || has('win64')) && &shellcmdflag =~ '/'
let g:cygwin_shell = has('win32unix')
let g:vim_dir = g:win_shell ? '$HOME/vimfiles' : '$HOME/.vim'
let &runtimepath .= ',' . expand(g:vim_dir . '/bundle/Vundle.vim')
call vundle#begin(expand(g:vim_dir . '/bundle'))

if exists(':Plugin')
    " Let Vundle manage itself.
    Plugin 'gmarik/Vundle.vim'

    " Completion & Syntax Checking (Heavyiest Stuff)
    Plugin 'Valloric/YouCompleteMe'
    "Plugin 'Shougo/neocomplete.vim'
    "Plugin 'starcraftman/vim-eclim'
    Plugin 'scrooloose/syntastic'
    Plugin 'SirVer/ultisnips'
    Plugin 'honza/vim-snippets' " Default snippets for ultisnips

    " UI & Enhancements
    Plugin 'bling/vim-airline'
    Plugin 'edkolev/tmuxline.vim'
    Plugin 'edsono/vim-matchit'
    Plugin 'godlygeek/tabular'
    Plugin 'justinmk/vim-sneak'
    Plugin 'Konfekt/FastFold'
    Plugin 'majutsushi/tagbar'
    Plugin 'MattesGroeger/vim-bookmarks'
    Plugin 'scrooloose/nerdcommenter'
    Plugin 'sjl/gundo.vim'
    Plugin 'vim-scripts/taghighlight'

    " Searching & Files
    Plugin 'kien/ctrlp.vim'
    Plugin 'mileszs/ack.vim'
    Plugin 'rking/ag.vim'
    "Plugin 'scrooloose/nerdtree'

    " Diffing
    Plugin 'ludovicchabant/vim-lawrencium'
    Plugin 'mhinz/vim-signify'
    Plugin 'tpope/vim-fugitive'

    " Utility
    Plugin 'kshenoy/vim-togglelist'
    Plugin 'tpope/vim-abolish'
    Plugin 'tpope/vim-sleuth'
    Plugin 'tpope/vim-surround'
    Plugin 'tyru/open-browser.vim'
    Plugin 'vim-scripts/a.vim'
    Plugin 'vim-scripts/DeleteTrailingWhitespace'

    " Syntax / File Specific
    "Plugin 'chrisbra/csv.vim'
    Plugin 'clones/vim-zsh'
    Plugin 'elzr/vim-json'
    "Plugin 'LaTeX-Box-Team/LaTeX-Box'
    Plugin 'plasticboy/vim-markdown'
    Plugin 'tomswartz07/vim-todo'
    Plugin 'zaiste/tmux.vim'

    " Web Programming
    "Plugin 'othree/html5.vim'
    "Plugin 'ap/vim-css-color'
    "Plugin 'hail2u/vim-css3-syntax'
    "Plugin 'kchmck/vim-coffee-script'
    "Plugin 'pangloss/vim-javascript'
    "Plugin 'vim-scripts/jQuery'
    "Plugin 'Shutnik/jshint2.vim'
    "Plugin 'StanAngeloff/php.vim'
    "Plugin 'vim-ruby/vim-ruby'

    " Very Large Number of Colorschemes
    "Plugin 'flazz/vim-colorschemes'

    " Turn on after vundle works
    call vundle#end()
    filetype plugin indent on
endif

" }}}
" Plugin Configuration
""""""""""""""""""""""
" {{{

" YouCompleteMe
"""""""""""""""
" Global fall back if no config present.
let g:ycm_global_ycm_extra_conf = '~/.ycm_extra_conf.py'

" Allow completion of identifiers in comments too
let g:ycm_complete_in_comments = 1

" Allow ctags for identifier help
"let g:ycm_collect_identifiers_from_tags_files = 1

" Use next line to disable ultisnips completion
"let g:ycm_use_ultisnips_completer = 0

" Use the following to whitelist dirs for .ycm_extra_conf.py
let g:ycm_extra_conf_globlist = [
    \ '~/programming/*' ]

" Neocomplete
"""""""""""""
" Uses enter key to accept completion
" Enable neocomplete at startup
let g:neocomplete#enable_at_startup = 1

" Use smartcase
let g:neocomplete#enable_smart_case = 1

" Automatically select first option.
let g:neocomplete#enable_auto_select = 1

" Eclim
"""""""
" For eclim, YCM will query for completion
let g:EclimCompletionMethod = 'omnifunc'

" Fix for signs
let g:EclimShowQuickfixSigns = 0

" Syntastic
"""""""""""
" Set what chechers are active or passive
let g:syntastic_mode_map = {
        \ 'mode': 'active',
        \ 'active_filetypes': ['c', 'cpp', 'java', 'lisp', 'python', 'perl', 'ruby',
        \                      'sh', 'xml', 'json', 'xhtml', 'html', 'css', 'javascript']
    \ }

" Check syntax on file open
"let g:syntastic_check_on_open = 1

" Show errors in the line numbers to left
let g:syntastic_enable_signs = 1

" Format the syntastic message
let g:syntastic_stl_format = '[%E{Err: %fe #%e}%B{, }%W{Warn: %fw #%w}]'

" List of files to ignore checking, may be useful later
let g:syntastic_ignore_files = [ '\m^/usr/include/' ]

" Always use location list
let g:syntastic_always_populate_loc_list = 1

" Override, don't think I'll run any unsecure perl files.
let g:syntastic_enable_perl_checker = 1

" Manually set important checkers:
let g:syntastic_python_checkers = ['python', 'pychecker', 'pylint']
let g:syntastic_perl_checkers = ['perl', 'perlcritic']

" UltiSnips
"""""""""""
" Set dir to .vim section
let g:UltiSnipsSnippetsDir = expand(g:vim_dir . '/snippets')

" Force a version of python
"let g:UltiSnipsUsePythonVersion = 2

" Sneak
"""""""
" Allows quick motion when more than 2 matches
let g:sneak#streak = 1

" Allows smart case usage of sneak
let g:sneak#use_ic_scs = 1

" Toggle to allow or prevent sneak in netrw
" When enabled, moves old s binding to <leader>s/S
let g:sneak#map_netrw = 1

" CtrlP
"""""""
" Index hidden files
"let g:ctrlp_show_hidden = 1

" TagBar
""""""""
" Close on selecting an option
let g:tagbar_autoclose = 1

" Focus on open
let g:tagbar_autofocus = 1

" Compact the menu
let g:tagbar_compact = 1

" Nerdtree
"""""""""""""
" Show hidden files by default
let g:NERDTreeShowHidden = 1

" Don't need window after selecting file
let g:NERDTreeQuitOnOpen = 1

" Classic theme with |'s instead of >'s.
let g:NERDTreeDirArrows = 0

" Width of window
let g:NERDTreeWinSize = 50

" Don't replace netrw (i.e. :e directory), defualt is 1
"let g:NERDTreeHijackNetrw = 0

" DeleteTrailingWhitespace
""""""""""""""""""""""""""
" Always delete trailing whitespace from lines on save
"let g:DeleteTrailingWhitespace = 1
"let g:DeleteTrailingWhitespace_Action = 'delete'

" Ack.vim
"""""""""
" Options when using ack
let g:ack_default_options = ' -s -H --nocolor --nogroup --column --sort-files --smart-case --follow'

" Ag (Silver Searcher)
""""""""""""""""""""""
" Options to use when searching with ag
let g:agprg = 'ag --column --smart-case --follow'

" OpenBrowser
"""""""""""""
" Default engine to duckduck
let g:openbrowser_default_search = 'duckduckgo'

" TmuxLine
""""""""""
" Preset for my tmux line.
let g:tmuxline_preset = {
        \'a'       : '#h',
        \'b'       : '#(curl icanhazip.com)',
        \'win'     : '#I #W',
        \'cwin'    : '#I #W',
        \'y'       : ['#S', '#I', '#P'],
        \'z'       : ['%d %b %Y', '%H:%M:%S'],
        \'options' : {'status-justify' : 'left'}
    \ }

" Unused options to display other addrs
    "\'c'    : ['#(ifconfig en0 | grep "inet " | awk {print "en0" $2})',
    "\       '#(ifconfig en1 | grep "inet " | awk {print "en1" $2})',
    "\       '#(ifconfig tun0 | grep "inet " | awk {print "vpn" $2})'],

" Bookmarks
"""""""""""
" Center on jumping to bookmark
let g:bookmark_center = 1

" When jumping from quicklist, close it
let g:bookmark_auto_close = 1

" }}}

" }}}
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Status line
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" {{{

" vim-Airline
"""""""""""""
" Enable syntastic integration
let g:airline_enable_syntastic = 1

" Enable a smart tab top
let g:airline#extensions#tabline#enabled = 1

" Enable powerline fonts
let g:airline_powerline_fonts = 1

" Regular Status Line
"""""""""""""""""""""
" Syntastic modification to line, only if installed
let s:syn_status = ''
if filereadable(expand(g:vim_dir . '/bundle/syntastic/LICENCE'))
    let s:syn_status = '|| %{SyntasticStatuslineFlag()}'
endif

" Not prettiest, but functional
let &statusline  = '%<%1* %t%m %y || %{&fenc?&fenc:&enc}[%{&ff}] ' . s:syn_status
let &statusline .= '%= %b(0x%B) || buf: %n || %p%% %l,%c %0*'
set laststatus=2

" }}}
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Key Mappings
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" {{{

" For custom key combos, use leader
let mapleader = ","

" Apparently used for buffer/filetype specific bindings
let maplocalleader = '\\'

" Never use ex mode
map Q <nop>

" Aliasing some commands to make tabs/buffers easy to manage
" Some of these exist, I put them here to remember
" Note with hidden set, buffers and tabs are largely the same
cnoreabbrev bn bnext
cnoreabbrev bp bprevious
cnoreabbrev tn tabn
cnoreabbrev tp tabp
cnoreabbrev te tabe
cnoreabbrev td tabclose

" I always forget for explore, make some shortcuts, Ev for v split, Et for tab
cnoreabbrev E Explore
cnoreabbrev Et Texplore
cnoreabbrev Ev Sexplore!

" Shortcuts for bundle management
cnoreabbrev pi PluginInstall
cnoreabbrev pu PluginUpdate
cnoreabbrev pc PluginClean
cnoreabbrev ps PluginSearch

" Faster binding to escape insert/visual
inoremap jk <esc>
vnoremap i  <esc>
"inoremap <esc> <nop>

" Arrow keys to move through buffers/tabs
nnoremap <right> :bnext<CR>
nnoremap <left>  :bprevious<CR>
nnoremap <up>    :tabn<CR>
nnoremap <down>  :tabp<CR>

" Remap Space + direction to move between split windows
nnoremap <silent> <space>k :wincmd k<CR>
nnoremap <silent> <space>j :wincmd j<CR>
nnoremap <silent> <space>h :wincmd h<CR>
nnoremap <silent> <space>l :wincmd l<CR>

" Change window down (<C-W>j) then maximize buffer height (<C-W>_)
nnoremap <C-J> <C-W>j<C-W>_
nnoremap <C-K> <C-W>k<C-W>_
" Change window right (<C-W>l) then maximize buffer width (<C-W>|)
nnoremap <C-L> <C-W>l:vertical resize<CR>:AirlineToggle<CR>:AirlineToggle<CR>
nnoremap <C-H> <C-W>h:vertical resize<CR>:AirlineToggle<CR>:AirlineToggle<CR>

" Toggles for the location and quickfix
nnoremap <silent> <leader>q :ToggleQF<CR>
nnoremap <silent> <leader>l :ToggleLL<CR>

" Make all windows equal in size
"nnoremap <leader>q <C-W>=

" Open netrw in current buffer
nnoremap <silent> <leader>e :Explore<CR>

" Open netrw vertically or horizontally
nnoremap <silent> <leader>v :call <SID>VexToggle()<CR>
"nnoremap <silent> <leader>h :Hexplore!<CR>

" To open NERDTree when used
nnoremap <silent> <leader>n :NERDTreeToggle<CR>

" Find the current file in the source tree
nnoremap <silent> <leader>nf :NERDTreeFind<CR>

" Signify binding to jump between hunks.
nmap <leader>hj <plug>(signify-next-hunk)
nmap <leader>hk <plug>(signify-prev-hunk)

" Key bindings for UltiSnips, all of these are ctrl + key
let g:UltiSnipsExpandTrigger       = '<c-j>'
let g:UltiSnipsListSnippets        = '<c-l>'
let g:UltiSnipsJumpForwardTrigger  = '<c-j>'
let g:UltiSnipsJumpBackwardTrigger = '<c-k>'

" Open the filetype specific file
nnoremap <leader>ft :OpenFT<CR>

" Binding for extra search modes
nnoremap <leader>p :CtrlPBuffer<CR>
nnoremap <leader>pm :CtrlPMRUFiles<CR>
nnoremap <leader>ps :CtrlPBuffer<CR>

" Add shortcut to jump to definition/declaration of c file
nnoremap <leader>j :YcmCompleter GoTo<CR>

" Shortcut to swap to header file, horizontal split
nnoremap <leader>a :AS<CR>

" Shortcut to swap to header file, vertical split
nnoremap <leader>av :AV<CR>

" Mapping to trigger make build and run
nnoremap <leader>m :!make && make run<CR>

" Hex editting command on x
nnoremap <leader>x :%!xxd<CR>
nnoremap <leader>X :%!xxd -r<CR>

" Fix oneline json files
nnoremap <leader>jq :%!jq .<CR>
nnoremap <leader>jQ :%!jq . -c<CR>

" Paste toggle button, disables f1 help use command instead
set pastetoggle=<F1>

" Shortcut for tagbar outline of file
nnoremap <silent> <F2> :TagbarToggle<CR>
inoremap <silent> <F2> <Esc>:TagbarToggle<CR>:call feedkeys('i', 'n')<CR>

" Shortcut for gundo sidebar
nnoremap <silent> <F3> :GundoToggle<CR>
inoremap <silent> <F3> <Esc>:GundoToggle<CR>:call feedkeys('i', 'n')<CR>

" Toggle line numbers
nnoremap <silent> <F5> :set number!<CR>:sign unplace *<CR>
inoremap <silent> <F5> <Esc>:set number!<CR>:sign unplace *<CR>:call feedkeys('i', 'n')<CR>

" Toggle showing whitespace
nnoremap <silent> <F6> :set list!<CR>
inoremap <silent> <F6> <Esc>:set list!<CR>:call feedkeys('i', 'n')<CR>

" Shortcut to remember how to reindent file
nnoremap <F12> mzgg=G'z

" }}}
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => General Options & Features
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" {{{

" Ensure backspace works as you'd expect, over lines/indents.
set backspace=indent,eol,start

" This is the timeout on key combos and map commands.
set timeout
set timeoutlen=500

" Set to auto read when a file is changed from the outside
set autoread

" Allow hiding of files, when using standard :e filename option
set hidden

" Set UTF-8 for file enconding
set encoding=utf8

" Folding method, for most code use indent, no need to clutter source
set foldmethod=syntax
set foldminlines=6
set foldnestmax=2

" Enable folding at the syntax level
let g:javaScript_fold    = 1
let g:php_folding        = 1
let g:r_syntax_folding   = 1
let g:ruby_fold          = 1
let g:sh_fold_enabled    = 1
let g:vimsyn_folding     = 'af'
let g:xml_syntax_folding = 1

" Sets how many lines of history & undo VIM has to remember
set history=1000
set undolevels=1000

" Keep a persistent backup file, preserves undo history between edit sessions
if has('persistent_undo')
    let &undodir = expand(g:vim_dir . '/undo')
    set undofile
endif

" Autocomplete feature for command mode (i.e. :command)
set wildmenu
set wildmode=longest,list,full

" Turn backup off, since most files in a VCS
set nobackup
set nowritebackup
set noswapfile

" No annoying sound on errors
set noerrorbells
set visualbell
set t_vb=

" }}}
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => VIM User Interface & Search
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" {{{

" Set minimum screen size for GVim, on console just fill
if has('gui_running')
    set lines=80 columns=140
endif

" Enable the mouse in all modes of operation
"set mouse=a

" Show end of line and tabs on screen
"set list
set listchars=eol:$,tab:→→,trail:✘

" Set line numbering on left
set number

" Set position indicator on bottom right
set ruler

" Show command in last line, usually on by default
set showcmd

" Highlight current line in number side
set cursorline

" Minimum number of lines that will always be above/below cursor
set scrolloff=10

" Highlight search results
set hlsearch

" Incrementally highlight first matching word as you type a search
set incsearch

" Show matching brackets when text indicator is over them
set showmatch
" How many tenths of a second to blink when matching brackets
set matchtime=1

" For regular expressions turn magic on, don't need to \* in regex
set magic

" When searching ignore case unless contains a capital
" Override with \c/\C flag in regex -- /\cword
set ignorecase
set smartcase

" More intiutive when new splits at right and bottom
set splitbelow
set splitright

" }}}
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Colors and Fonts
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" {{{

syntax off

" Set dark background before, else colors off
set background=dark
if &diff && (has('gui_running') || &t_Co > 255)
    colorscheme jellybeans
elseif has('gui_running') || &t_Co > 255
    colorscheme molokai
    " Molokai CursorLine isn't bright enough.
    hi CursorLine  ctermbg=236
else
    colorscheme desert
endif
" Other good colorschemes:
"   molokai, desert256, jellybeans, wombat256mod, mrkn256, xoria256, twilight256

syntax on

" Highlight with ColorColumn lines over a certain  limit.
"highlight ColorColumn ctermbg=8
call matchadd('ColorColumn', '\%100v', 100)

" Set font when using gui version
if has('gui_running')
    if has('gui_gtk2')
        set guifont=DejaVu\ Sans\ Mono\ for\ Powerline\ 10
    elseif has('gui_win32')
        set guifont=DejaVu_Sans_Mono_for_Powerline:h10:cANSI
    endif
endif

" }}}
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Tab & Indents
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" {{{

" 1 tab == 4 spaces
set softtabstop=4
set shiftwidth=4
set tabstop=4

" Use spaces instead of tabs
set expandtab

" When push tab in insert shift by tabstop, when backspace delete tabstop amount
set smarttab

" Copy indent at current when inserting new line
set autoindent

" Wrap lines when hit right side, doesn't affect buffer
set wrap

" Makes smarter decisions about what stays on wrapped line
set linebreak

" When inserting text, force a line break at this amount
" Set to 0 to disable
set textwidth=150

" }}}
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => NETRW File Explorer & File Ignore
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" {{{

" Customize netrw use a tree style and ignore some extensions
let g:netrw_liststyle = 3

" Set the explorer sorting to case insensitive
let g:netrw_sort_options = 'i'

" Controls what happens when you push enter over file, default open in buffer
let g:netrw_browse_split = 0

" This list is used to build the strings for wildignore and netrw_list_hide
" Any file ending in one of these extensions will be ignored in command completion & netrw browser
let s:hide_exts =  ['jpg', 'jpeg', 'png', 'svg', 'bmp', 'gif', 'xpm', 'so', 'dll', 'exe', 'o', 'a']
let s:hide_exts += ['pyc', 'class', 'com', 'rar', 'zip', 'gz', 'bz2', '7z', 'iso', 'jar', 'dmg']
let s:hide_exts += ['deb', 'pdf']

" Add to ignore docs
"let s:hide_exts += ['doc', 'docx', 'odt', 'xls', 'xlsx', 'ods', 'ppt', 'pptx', 'odp']

" Processing here to build the large regexp
let s:wild_regex = ''
let s:netrw_regex = ''

for ext in s:hide_exts
    let s:wild_regex .= '*.' . ext . ','
    let s:netrw_regex .= ext . '\|'
endfor

" Don't leave trailing separator
let s:wild_regex = s:wild_regex[:-2]
let s:netrw_regex = s:netrw_regex[:-3]

" Hide VCS folders in this list.
let s:vcs_hide = '\.git/,\.hg/,\.svn/,\.bzr/'

" When using autocomplete tab, ignore all matching strings
let &wildignore = s:wild_regex . ',' . s:vcs_hide

" When browsing with netrw, ignore all matching files to this regex
let g:netrw_list_hide = '\w\+\.\(' . s:netrw_regex . '\)\*\?$\c,' . s:vcs_hide
let g:NERDTreeIgnore = split(g:netrw_list_hide, ',')

" Sort by extensions commonly found
let s:sort_exts =  ['h', 'hh', 'hpp', 'hxx', 'c', 'cc', 'cpp', 'cxx', 'java']
let s:sort_exts += ['py', 'pl', 'rb', 'html', 'css', 'js', 'xml', 'json']

let g:netrw_sort_sequence = '[\/]$,\<core\%(\.\d\+\)\=\>,'
for ext in s:sort_exts
    let g:netrw_sort_sequence .= '\.' . ext . '$,'
endfor
let g:netrw_sort_sequence .= '*,\.info$,\.swp$,\.bak$,\~$'
let g:NERDTreeSortOrder = split(g:netrw_sort_sequence, ',')

" }}}
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Autocommands & Filetype Specific
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" {{{

" Protection against older Vim versions. Gvim reports falsely augroup = 0 sometimes.
if has('autocmd')
    if has('gui')
        augroup gui_cmds
            autocmd!
            " Stop bell on gvim.
            autocmd GuiEnter * set visualbell t_vb=
        augroup END
    endif

    augroup buf_cmds
        autocmd!
        " Prevent undo files in some paths
        autocmd BufWritePre /tmp/* setlocal noundofile
        " All .md files should be markdown
        autocmd BufRead,BufNewFile *.md set filetype=markdown
        " When change vimrc, reload it on write.
        "autocmd BufWritePost $MYVIMRC source $MYVIMRC
        " When leaving window, save state to a file. Restore on return
        " Includes cursor position, fold states,
        "au BufWinLeave *.* silent! mkview
        "au BufWinEnter *.* silent! loadview
    augroup END

    " Register funcs with filetype load
    augroup ftype_cmds
        autocmd!
        " missing keywords for bash statement syntax
        autocmd FileType sh exec 'syntax keyword shStatement source shopt'
    augroup END

    augroup netrw_cmds
        autocmd!
        autocmd FileType netrw nmap <buffer> <leader>x gh
        autocmd FileType netrw nmap <buffer> <silent> <leader>z :call <SID>ShowSyms()<CR>
        autocmd FileType netrw nmap <buffer> <silent> q :call <SID>VexClose()<CR>
        autocmd FileType netrw nunmap <buffer> <C-L>
    augroup END
endif

" }}}
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Useful Functions
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" {{{

" Command declarations, functions below
command! -nargs=0 NScheme call s:NextScheme(0)
command! -nargs=0 PScheme call s:NextScheme(1)
command! -nargs=0 PickScheme call s:PickScheme()
command! -nargs=+ -range=% ChangeSpace call s:ChangeSpace(<line1>, <line2>, <f-args>)
command! -nargs=0 OpenFT call s:OpenFT()

function! s:InitScheme(remDefaults)
    if exists('s:c_init')
        return
    endif
    let s:c_init = 1

    " Populate list
    let schemes = split(globpath(&rtp, 'colors/*.vim'), '\n')
    if a:remDefaults == 1
        let pattern = g:win_shell ? 'vim7.4withLua' : 'share/vim'
        let schemes = filter(schemes, "v:val !~ pattern")
    endif
    let s:c_list= sort(map(schemes, "fnamemodify(v:val, ':t')[0:-5]"))

    " Find current index
    let s:c_ind = 0
    for scheme in schemes
        if scheme ==? g:colors_name
            break
        endif
        let s:c_ind += 1
    endfor
    let s:c_default = s:c_ind + 1

    if (len(s:c_list) > 26)
        echom 'too many schemes, listing first 26'
        return
    endif

    " Create Message
    let msg = ""
    let char = "A"
    for s in s:c_list
        let msg .= "&" . char . s . "\n"
        let char = nr2char(char2nr(char) + 1)
        " Stop at 26th
        if char == "["
            break
        endif
    endfor
    let s:c_msg = msg[0:-2]
endfunction

function! s:SetScheme()
    " Set new scheme
    syntax off
    set background=dark
    exec 'colorscheme ' . s:c_list[s:c_ind]
    syntax on
    echom 'colorscheme is now: ' . g:colors_name
endfunction

function! s:NextScheme(reverse)
    call s:InitScheme(1)

    " Set next index
    let s:c_ind = (a:reverse ? s:c_ind - 1 : s:c_ind + 1) % len(s:c_list)

    call s:SetScheme()
endfunction

function! s:PickScheme()
    call s:InitScheme(1)

    " Returns index of 1 - n choices
    let s:c_ind = confirm("Pick Scheme From:", s:c_msg, s:c_default) - 1

    call s:SetScheme()
endfunction

function! s:ChangeSpace(line1, line2, old_tab, new_tab)
    let l:rtab_cmd = printf('%s,%sretab', a:line1, a:line2)

    let l:old = printf('set ts=%s sts=%s sw=%s noet', a:old_tab, a:old_tab, a:old_tab)
    exec l:old
    exec l:rtab_cmd . '!'

    let l:new = printf('set ts=%s sts=%s sw=%s et', a:new_tab, a:new_tab, a:new_tab)
    exec l:new
    exec l:rtab_cmd
endfunction

function! s:OpenFT()
    let l:file = printf('%s/ftplugin/%s.vim', g:vim_dir, &ft)
    exec 'sp ' . l:file
endfunction

function! s:ExtractFullPath(line)
    let l:left = 0
    let l:right = len(a:line) - 1

    let l:char = a:line[l:left]
    while l:char == ' ' || l:char == '|'
        let l:left += 1
        let l:char = a:line[l:left]
    endwhile

    let char = a:line[l:right]
    while l:char =~ '[/*|@=]$'
        let right -= 1
        let char = a:line[l:right]
    endwhile

    let l:link = strpart(a:line, l:left, l:right - l:left + 1)

    if len(l:link) > s:max_link
        let s:max_link = len(l:link)
    endif

    return [l:link, resolve(getcwd() . "/" . l:link)]
endfunction

function! s:ShowSyms()
    let l:count = 1
    let l:files = []
    let s:max_link = 0

    for l:line in getline(1, '$')
        if l:line =~ '@$'
            let l:files  += [[l:count] + s:ExtractFullPath(l:line)]
        endif

        let l:count += 1
    endfor

    let l:output = ""
    let l:fmt = "ln: %5d %" . s:max_link . "s -> %s\n"
    for l:entry in l:files
        let l:output .= printf(l:fmt, l:entry[0], l:entry[1], l:entry[2])
    endfor
    echo l:output
endfunction

function! s:VexOpen()
    let t:vex = {'orig_buf': winnr(), 'orig_bsplit': g:netrw_browse_split}
    let g:netrw_browse_split = 4

    execute 'new'
    execute 'topleft Vexplore'
    wincmd H

    let t:vex.new_buf = bufnr('%')
endfunction

function! s:VexClose()
    let vex_buf = bufwinnr(t:vex.new_buf)

    if vex_buf != -1
        execute vex_buf . ' wincmd w'
        close
        execute t:vex.orig_buf . ' wincmd w'
    endif

    let g:netrw_browse_split = t:vex.orig_bsplit
    unlet t:vex
endfunction

function! s:VexToggle()
    if exists('t:vex')
        call s:VexClose()
    else
        call s:VexOpen()
    endif
endfunction

" }}}
" vim: set foldmethod=marker:
