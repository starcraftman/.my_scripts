#!/usr/bin/env python3
# Common tools:
#	pip/pip3 : install packages
#	pylint/pychecker : verify syntax
#	unittest package for xUnit.

# Imports

# Classes

# Functions

# Main
if __name__ == '__main__':
	print("Main")

# Python Tuts:
#   Multiprocess (threads) -> http://pymotw.com/2/multiprocessing/basics.html

# Namespace resolution:
# 	LEGB Rule: Local first, Enclosed Scope, Global (to Module), then Built-In scope.
#	Namespaces: Order is local, nonlocal, global, builtin. Use nonlocal x to access enclosing, global x to get global.

# Imports:
#	import long_module_name_that_annoys as short # Shorten modules.
#
#	from imp import reload
#	reload(module) # Resets the module object to default after import.
#
#	dynamic import from string:
#		modname = 'string'
#		stringMod = __import__(modname)
#
# 	from . import spam # In this package dir, look for spam module and import.
# 	from .string import name, name2 # Inside this package.string, import names
# 	from .. import spam # Spam is a sybling package to the current, check in parent dir.
#
# 	To prevent * name import pollution, name internal vars/funcs to _Name
# 	Alternatively, init __all__ to a list of names to export
#
#   Common Imports:
#     import logging # General logging, use with multi.
#     import multiprocessing # True threading even on cpython due to GIL. multiprocessing.log_to_stderr(logging.DEBUG)
#     import sys # Python interpreter params here, including argv.
#     import os # OS indepedent stuff like paths.
#     import time # Time system.

# General Notes:
#	FORCE KEYWORD:
#		def foo(pos, *, forcenamed): # The function must use keyword argument to pass forcedname.
#
#	XML: See page 935, packages: xml.dom, xml.sax, xml.etree
#	RAW STRINGS: r'C:\test\path\works' # Raw strings, ignores all backspaces and special chars.
#
#	Slicing strings: s[start:end:step], returns copy of string for deep copies.
#	Comprehensions:
#	List type: [expression for x in list1 if cond]
#	Example:
#		[floor(x+y) for x in listPos if x > 50 for y in list if y < 40]
#	Generators: (expression for x in list1 if cond)
#	Set comprehension: {x*x for x in range(10)}
#	Dict comprehension: {x: x*x for x in range(10)}
#
#	Sets {1,2,3}, Tuple (1,2,3), List [1,2,3], Dictionary {1:'a', 2:'b'}
#	General iteration requires support for __next__() function.
#		Use next(obj) to call.
#		If not supported, make iterator with iter(obj), then call next(iterator).
#
#	Lambda:
#	expRm = (lambda n: x ** n) -> Remember whatever value of x in enclosing space.
#	exp = (lambda x,n: x ** n)
#	exp(2, 5) -> Use.
#
#	Def args:
#	def t(x=x) -> X arg takes x from the enclosing space, like default arg.
#	Var args:
#	def func(*name) -> Puts all extra args into tuple, **name puts them in dict. (See Python page 443)
#
#	Assert:
#	assert False, "This is always false." # Boolean expression followed by string.
#
#	__slots__: Set this and only these attributes allowed, space saving feature.

#Documentation:
#	use """ doctstring tags at top file, under classes, under functions.
#
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

# With/As Expression:
#	Files:
#       f = open('filename', 'w')
#       f.close()
#
# 	with open(r'./file.txt') as myfile, B() as BExample:
#		code here
#
# 	Object must define: __enter__, __exit__ methods. Enter opens object and returns to as. Exit handles close.

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

# Class:
# 	class Test(Super1, Super2):
#		body
#
# 	class Test:
#		... # Alternatively, pass: Means no code at this time, can be replaced or modified at runtime.
#
# 	Name Mangling: Prevent collisions of reused names down inheritance tree. No trailing __, only leading. Page 750
# 		class C1:
#			def set(self): self.__X # IMPORTANT, mangled to become self._C1__X at run time. Prevents collision with other X.
#			def get(self): print(self.__X)
#
# 	SPECIAL NB: We must redefine all operator overloads even if inheriting, like __add__ and __str__
# 	class Mgr(Person):
#		def func(self):
#			Person.methodInA(self, args) # Force call to superclass function by invoking name. Person.__init__() for constructor
#
# 	Embed Object Inside Class: Delegates calls not on this object, to embedded.
# 	class ManagerEmbed:
#    		def __init__(self, name, pay):
#       		/self.person = Person(name, 'mgr', pay)
#    		def __getattr__(self, attr):
#        		return getattr(self.person, attr)
#
# 	Abstract classes: Prevent instatiation with special syntax, for 2.x remove inheritance and put under __metaclass__ = ABCMeta.
# 	from abc import ABCMeta, abstractmethod
# 	class Abstract(metaclass=ABCMeta):
#		@abstractmethod
# 		def abstractFunc(self):
#			pass
#
#	Class Decorators:
#		@classmethod -> Gets class as first option, use for class instrospection.
#		@staticmethod -> Standard static function.

# Exceptions
# 	Custom Exception: Derive from Exception or lower class.
#
# 	raise Exception # Raise an exception by class
# 	raise Exception(args) # Use constructor
#
# 	Rethrow current exception: raise # Nothing else.
#
# 	raise TypeError from E # Raise new exception, derived from E (instance of an Exception)
#
# 	Standard block:
# 	try:
#		code
# 	except (Exception1, Exception2) as e2: # Catch all exceptions in tuple
#		code
# 	except ExceptionClass as e: # Capturing the instance as e.
#		code
# 	except:
#		code for all other exceptions not above
# 	else:
#		code if no exceptions raised
# 	finally:
#		clean up code

# Binary/Strings
# 	bytes objects immutable, bytearrays mutable arrays of binary.
#
# 	b = b'test' # Make bytes obj. bytearray(str, encoding) # make byte array
#
# 	str.encode(), bytes(str, encoding) # Convert to bytes.
# 	bytes.decode(), str(bytes, 'utf-8') # Convert to str.
#
# 	chr(int), ord(ch) # Convert to character from int code, reverse.

# Attribute access
# 	__getattr__, __setattr__ : Methods called for routing undefined attributes and assignment of all attrs. Not for op overload.
#	__delattr__ : For deleting attr from obj.
#	__getattribute__ : Routing for all attributes in new classes.
#	NB: When dealing, be careful to avoid recursive calls to same method causing loop.
#	Fine for __get_attr.
#	For getattribute: x = object.__getattribute__(self, 'other') # Forces call through object superclass, avoid my func.
#	For setattribute: self.__dict__['other'] = val # Avoid me by using dict index.
#
#
#	Properties:
#		attribute = property(aGet, aSet, aDel, aDocString) # Set property for attribute.
#
#	With Decorators:
#	@property
#	def name(self):
#		"doc string here"
#
#	@name.setter, @name.deleter
#	def name(self, value) or (self): followed by code.
#
#	Descriptors:  Page 950
#	class Name:
#		"Descriptor class docstring"
#		def __get__(self, instance, owner): # self is descriptor, instance is object attached, owner is class.
#			get code
#		def __set__(self, instance, owner):
#		def __del__(self, instance, owner):
#
#	class UseDescriptor:
#		val = Name()

#OS Library:
#	import os
#	p = os.popen('pwd') -> Shell execute a command and return result.
#	cwd = os.getcwd() # Get pwd.
