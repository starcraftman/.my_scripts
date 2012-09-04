#|
(defun func () ; Function definition.
	(print "test"))

(print `(+ 3 2 4 5)) ; ' Disables the evaluation of list, print it.
; Combine boolean with "and" "or" "not" functions. True/False -> t/nil.
|#
;;;; Comment header for a section, use 3 for paragraph, 2 for comment next line, 1 for current line.

(print "Template file.")


#|
Function Index:
((lambda (args) (body)) arg_to_apply_lambda_to)

print: Prints its args.
': Escapes everything that follows under its escape.
(let ((x 5) (y 2)) (+ x y)): Define a variable.
(let* ((x 10) (y (* 2 x))) (* x y)): Didn't require nesting y inside x scope because of let*.
(equal x y): Examine if x and y are equal.

list: Construct a list of the arguments as is.
append: Merge the contents of the lists into one.
cons: Append the first arg to the second arg (that is a list).

car: Return head of a list.
cdr: Return the tail of a list.
(setf var new_value): Examine var and update it with new_value.

Predicates:
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

Math:
(sqrt a): Square root of arg.
(expt a b): Return result of a^b.
(log a): Return the natural log of a.
(abs x): Absolute value of x.

High Order:
(mapcar function list1 list2 list3): Apply function to each list.
(funcall function arg1 arg2 arg3...): Apply function to each arg, doesn't need to be list.
(apply function arg1 arg2 ... list): Like funcall, last arg is list.

|#
