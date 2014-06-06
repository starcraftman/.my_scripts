My Scripts
==========

This repo contains some scripts I use.
If anyone else likes them, use them.
I've also added in some configs that I don't want to lose like my vimrc and eclipse settings.

mksource.py
-----------
* I like to use templates when I write scripts/c, this file copies them.
* See templates folder, some like python maybe should be separated to a notes file...

ycm_compile.py
--------------
* See my vim directory, this helper function compiles ycm for use.
* YCM requires other things, see vimrc for details.

install_system.py
-----------------
* Keeps track of packages I need and reinstalls them on a fresh Ubuntu machine.
* Does basic file copy of config and local cabal update for eclipseFp plugin.

repo
----
* Bash script to simply repeat a git command over several git repos.
* Useful for when you have many and want to pull without fear or get status.

eclipseBackup
--------------
* Folder stores list of plugins I use and my metadata folder.
* Extract that to .metadata in workspace to have settings.

dot_files
-------------------
* Stores my [`.vimrc`](https://github.com/starcraftman/.my_scripts/blob/master/dot_files/.vimrc) file for vim config.
* Read it, some plugins require extra steps like vundle/YCM.
* .vim folder has some stuff I don't download with vundle like colors, ftplugin custom files and such.
* [`.bash_aliases`](https://github.com/starcraftman/.my_scripts/blob/master/dot_files/.bash_aliases) some cool PS1 hacks for git/hg and other assorted bash conveniences.
* .gitconfig, .gitignore_global, .hgrc are my config files for vcs. Some very useful aliases and excludes.

archive
-------
* Old templating source before rewrote it in python.
* Some scripts to manage mpi programs on the university cluster.
