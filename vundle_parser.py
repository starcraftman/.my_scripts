#!/usr/bin/env python3
# Common tools:
#	pip/pip3 : install packages
#	pep8/pylint/pychecker : verify syntax
#	unittest package for xUnit.
"""Module level doc string."""

# Imports
import sys
import os

# Data

# Classes

# Functions
def main(path):
    fin = open(path, 'r')
    cnt = 0
    last = 1
    first = 1
    for l in fin:
        cnt += 1
        try:
            val = float(l[0:3])
            if l.count('~') > 0:
                if first:
                    first = 0
                    print('{}'.format(l.rstrip()), end='')
                else:
                    print(' ---> L{}-L{}\n{}'.format(last, cnt-1, l.rstrip()), end='')
                last = cnt
        except ValueError:
            pass
    print(' ---> L{}-L{}'.format(last, cnt-1))

# Main
if __name__ == '__main__':
    if len(sys.argv) < 2:
        path = '~/.vim/bundle/vundle/doc/vundle.txt'
    else:
        path = sys.argv[1]
    main(os.path.expanduser(path))
