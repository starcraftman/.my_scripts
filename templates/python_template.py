#!/bin/python3
# Imports

# Function declarations

# Main
if __name__ == '__main__':
	print("Main")


# Notes:
#	Slicing strings: s[start:end:step], returns copy of string for deep copies.
#	Comprehensions: for i in collection: print(i, end=" ")
#	Sets {1,2,3}, Tuple (1,2,3), List [1,2,3], Dictionary {1:'a', 2:'b'}
#	General iteration requires support for __next__() function.
#		Use next(obj) to call.
#		If not supported, make iterator with iter(obj), then call next(iterator).


#Documentation:
#	dir(obj) -> Lists all attributes on object.
#	help(obj) -> Lists pyDoc help for object.
#	obj.__doc__ -> Module wide comments, i.e. str.__doc__	

#Built Ins:
#	Zip to make dictionary:
#		k,v = ('a','b','c','d'), list(range(1,5))
#		d = dict(zip(k,v))
#
#	Enumerate: Make a generator that gives both the item and an offset counter.
#	for (offset, item) in enumerate(s):
#    		print(item, 'appears at ofset', offset)
#
#	sorted(list, sortCriteria)
#
#	filter(boolean, list)
#	Example:
#	list(filter(f1, iterable)) -> Define a function f1 that determines if to include the line, content.
#	
#	IN Test:
#	for x IN col -> Go through all members of col, if without for test membership.
#
#	pass -> Empty statement
#	
#	reduce: Take a function and pass pairs of args to it from iterable at right.
#	import functools
#	functools.reduce(operator.add, list)
#
#	MISC Operators that take list, names explain, all of form func(list).
#	sum, any, all, max, min
#	


#Python Constructs for Control/Loops:
#	IF:
#	if x:	elif y:		else:
#
#	while x:
#		pass
#	else:
#		Do this if didn't hit a "break" statement.
#
#	Ternary: X = Y if Z else X
#





#OS Library:
#	import os
#	p = os.popen('pwd') -> Shell execute a command and return result.
#
	
