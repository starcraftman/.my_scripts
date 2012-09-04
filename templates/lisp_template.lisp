#|
(defun func () ; Function definition.
	(print "test"))
; Combine boolean with "and" "or" "not" functions. True/False -> t/nil.
|#
;;;; Comment header for a section, use 3 for paragraph, 2 for comment next line, 1 for current line.

(print "Template file.")


#|
NOTES!
Good website -> http://www.cs.cmu.edu/Groups/AI/html/cltl/clm/index.html

ANON FUNCTIONS:
((lambda (args) (body)) arg_to_apply_lambda_to): Make an ananoymous function and apply to enclosed args.

; For global variables enclose with *, i.e. *PI*.
VARIABLES: 
(let ((x 5) (y 2)) (+ x y)): Define a variable.
(let* ((x 10) (y (* 2 x))) (* x y)): Didn't require nesting y inside x scope because of let*.
(defparameter name value): Defines a variable that can be modified.
(defconstant name value): Defines a constant.
(boundp 'name): True if the name is defined.
(setf var new_value): Examine var and update it with new_value.
(copy-list list): Return a copy of the list.
(equal var1 var2): Check if the contents of args are equal.
(eql var1 var2): Check if the two pointers are equal.

': Escapes everything that follows under its escape.
OUTPUT:
(print object): Prints its arg.
(write object): Same as print, doesn't print a new line before current.

LIST MANIPULATION:
list: Construct a list of the arguments as is.
append: Merge the contents of the lists into one.
cons: Append the first arg to the second arg (that is a list).
car: Return head of a list.
cdr: Return the tail of a list.
; Tip: Can use mutliple invocations with caddr -> will take the tail twice then return head.

PREDICATES:
null: Return true if arg is null.
atomp: Return true if arg is atom.
listp: Return true if argument is a list.
floatp: Return true if floating number.
integerp: Return true if arg is integer.
numberp: Return true if arg is a number.
zerop: Return true if arg is 0.
plusp: Return true if arg is positive.
minusp: Return true if arg is negative.
evenp: Return true if arg is even.
oddp: Return true if arg is odd.

MATH:
(sqrt a): Square root of arg.
(expt a b): Return result of a^b.
(log a): Return the natural log of a.
(abs x): Absolute value of x.
(incf x [step]): Increment x by step, if not provided step = 1.
(decf x [step]): Same as incf, but decrement.

FUNCTION MAPPING:
(mapcar function list1 list2 list3): Apply function to each list.
(funcall function arg1 arg2 arg3...): Apply function to each arg, doesn't need to be list.
(apply function arg1 arg2 ... list): Like funcall, last arg is list.

CONTROL:
(if (then) (else)): Standard control.
(loop): Create an inifinite loop.
(dotimes (n 3 t) (body): Do a loop from [0,3). n is var.
(when (condition) (execute)): Like an if conditional.
(return value): Cause flow to return.
(return-from label value): Cause flow to return from labeled block with value.
(go label): Goto equivalent, use with tagbody.

BLOCKS:
(progn body): Progn forces a block and executes each arg in order.
(block label body): Same as progn but return with return-from label value function call.
(tagbody body): Make tags with chars outside list, use (go label) to jump.
|#
