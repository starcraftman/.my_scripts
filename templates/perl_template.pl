#!/usr/bin/env perl
use strict;
use diagnostics;
#use feature "say";
#use feature "switch";
#use feature "state";
#use 5.012
use 5.014;

# N.B. Put ; at end of all statements.

# Variables:
#   my $var = 5 # Declares a locally scoped var set to 5.
#   local($var), # Declares local that only temporarily eclipses, get global with $::var.
#   my ($var1, $var2, @array1);
#
#   Array:
#   $test[2] = "test"
#   $lastIndex = $#test # Get the last index of a list.
#   @array = (1..6) # Assigns the list 1, 2, 3...6 to @array.
#   @copy = @array # Performs a copy of the array.
#
#   Manipulate Arrays:
#   $var = pop(@array) # Pop last element, 6 if previous list.
#   push(@array, 7) # Push on the end of array.
#   $var = shift(@array) # Take first element, 1 in example.
#   unshift(@array, 9) # Puts 9 at front of array.
#
#   List assignment: ($f1, $f2) = ("test1", "test2");

# Subroutines:
#   sub funcName{ statements; } # Last statement is the automatic return value. Otherwise use return keyword.
#   Invocation:
#       &funcName(args) # & Is optional only if name resolution unambigous.
#
#   Func params: $_[0].... $_[1] and so on, @_ has whole list of params.
#       my($var) = unshift @_ # Take first variable from @_ and process.
#

# List Vs. Scalar Context:
#
#   $back = reverse qw/ yab dab doo/ # Returns oodbadbay string.
#   Force scalar:
#       print("I have ", scalar @rocks, "rocks!\n")
#
#   chomp(@lines = <STDIN>) # Reads as many lines as there are until eof, pass through chomp.
#

# Operator Notes:
#   Line Input: <STDIN> -> Alternatively,  use FILE opened. Returns line up to \n. <> -> defaults to STDIN.
#
#   String Concatenation: $var . "test"
#   String Repetition:  "fre" x 3  -> "frefrefre"
#   String Interpolation: "This is var $vari.\n" -> Evaluates contents of vari in string.
#   String Var Explicit: "This var: ${vari}." -> Print line.
#
#   Numeric Compare: ==, !=, <, >, <=, >=. String compare: eq, ne, lt, gt, le, ge.
#
#   System Execution Result: `expression` # Returns a string result back.

# Control Constructs
#
# IF
#   if ($name gt "fred") {
#   } else {}
#
# WHILE
#   while ($cnt > 1) {}
#
# FOREACH
#   foreach $var (qw(test test2 test3 test4)) {
#       print($var."\n");
#   }

# Common Funcs:
#   print() # No new line.
#   say() # New line at end.
#   chomp() # String new line at end.
#   define() # Check if the variable is defined.
#   undef $foo # Undefine the value.
#   qw/ word word2 word3/ # Returns a quoted list of enclosed words, replace '/' with any punctuation marker.
#   reverse(list) # Reverse the list.
#   sort(@rocks) # Sort the array.


# Matching // = m//. Some modifiers : /i, ignore case, /s make . match over \n, /x allow arbitrary whitespace, /g for global, /m for multi lines (changes ^ and $ to anchor at \n).
# Note: For grouping, to not put in memory use : /(?:test)/
# Regular matches: \g{1}, for named matches /(?<label>pattern)/, i.e. /(?<name>\w+)/. Retrieve in $+{name}. Back reference \g{name}.
# Note special regex automatic vars: print " $` <$&> $' ". ` has before match, & has matched, ' has string after match
# Case substitution: \l \u, next char is lower/upper. \L \U, all remaining chars lower/upper. \E to end case mod.
# RE ops: split /pattern/, "string", join "glue", @pieces.
# Quantifiers: Nongreedy match as little as possible: *?, +?, ??.
# Use eval to trap errors. Eval errors in $@ variable.  Map, grep for operations.
