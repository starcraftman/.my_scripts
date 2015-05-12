![Issues][badge-issues]
[badge-issues]: http://img.shields.io/github/issues/starcraftman/.my_scripts.svg?style=flat-square

My Scripts
==========

This repo contains some scripts I use.
If anyone else likes them, use them.

All dot_files are now externalized to: https://github.com/starcraftman/dot

SysInstall.py
-------------
* Backbone of my portable configuration, see this to understand rest of this repo.
* See SysInstall.py --help for full explanation.
* `home` option sets up a user with my custom configs.
* `debian`, `babun` & `cabal` install relevant packages I use.

BuildSrc.py
-------------
* A series of other commands like `dev` or `cmake` fetch & build
  the latest versions of important programs. Default location is ~/.opt1.
* Also builds Ycm server component.

GetLibs.py
----------
* Related to above, builds C libs locally to externalize depency from system.

MkSource.py
-----------
* I like to use templates when I write scripts/c, this file copies them.
* See templates folder, some like python maybe should be separated to a notes file...

up
--
* Update script, updates platform, vim plugins & src programs from SysInstall.py
* NB: If you want to speed up recompilation install ccache.

unarchive
---------
* Universal unarchiver, does more than you might think.

valid_name
----------
* Determins if a name is available on the default path, could be function, command etc...

contains
--------
* Substring locator, find if haystack contains needle.
* Nicer than using the awful bash notation.

archive
-------
* Old templating source before rewrote it in python.
* Some scripts to manage mpi programs on the university cluster.

archive/GetLibsI.py
-------------------
* Inlined version of GetLibs.py, can be used independent of this repo.

archive/repo
------------
* Bash script to simply repeat a git command over several git repos.
* Useful for when you have many and want to pull without fear or get status.

archive/change_author.sh
------------------------
* change_author.sh, really useful if you make commit user/email mistakes.

archive/bootstrap.sh
------------------------
* Bash boostrap for python and zsh locally..
* Useful if you want either on a system without packages or without sudo power.

eclipseBackup
--------------
* Folder stores list of plugins I use and my metadata folder.
* Extract that to .metadata in workspace to have settings.

