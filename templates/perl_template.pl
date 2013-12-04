#!/usr/bin/env perl
# For Doc: perldoc name/module
#use File::Basename qw(dirname)
use strict;
use diagnostics;
#use feature "say";
#use feature "switch";
#use feature "state";
#use 5.012
use 5.014;

# N.B. Put ; at end of all statements.

# GLOBAL NAMES:
#   @ARGV is set at program launch. Use shift.
#   %ENV is the environmental path of the SHELL.
#   STDIN, STDOUT, STDERR default file handles.
#   __END__ is the platform EOF.
#       See more literals including current file, line, package, sub: http://perldoc.perl.org/perldata.html#Special-Literals

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
#
#   Hashes:
#   $hash{$key} = 5
#   %hash = ("foo", 35, "bar", 22) # Constructs dict: $hash{"foo"} is 35
#
#   Arrow Hash:
#   %hash = ("foo" => 35,....) # NOTE: => is treated like a comma.
#
#   Manipulate Hash:
#   @keys = keys %hash # Get the keys.
#   @vals = values %hash # Get the values.
#   while ( ($key, $value) = each %hash) { do something with key/value}
#
#   exists $hash{$key} # Check if key is present.
#   delete $hash{$key} # Unset the value/key pair from hash.
#
# Common Funcs:
#   print() # No new line.
#   printf(stringFmt, args...)
#   say() # New line at end.
#   chomp() # String new line at end.
#   defined() # Check if the value of an expression is undef.
#   undef $foo # Undefine the value.
#   qw/ word word2 word3/ # Returns a quoted list of enclosed words, replace '/' with any punctuation marker.
#   reverse(list) # Reverse the list.
#   sort(@rocks) # Sort the array.
#   die(message) # If hit this func, kill with message.
#   warn(message) # Send message but continue.

# Subroutines:
#   sub funcName{ statements; } # Last statement is the automatic return value. Otherwise use return keyword.
#   Invocation:
#       &funcName(args) # & Is optional only if name resolution unambigous.
#
#   Func params: $_[0].... $_[1] and so on, @_ has whole list of params.
#       my($var) = unshift @_ # Take first variable from @_ and process.
#

# Modules:
#   use module # Import everything.
#   use File::Basename qw(dirname) # Import only qw list, if empty import nothing.

# Files:
#   if (! open CONFIG, "X", "filename") {} # For X, use: < readIn, > writeOut, >> append to file. Returns 0 for success.
#   while (<CONFIG>) {}
#   close CONFIG
#
#   Change default handle for print (STDIN usually)
#   $OLD = select(NEWHANDLE)

# List Vs. Scalar Context:
#
#   $back = reverse qw/ yab dab doo/ # Returns oodbadbay string.
#   Force scalar:
#       print("I have ", scalar @rocks, "rocks!\n") # Prints length of array.
#
#   chomp(@lines = <STDIN>) # Reads as many lines as there are until eof, pass through chomp.
#

# Operator Notes:
#   SMART MATCH: Page 224 i
#       if ($name ~~ /Fred/) # Does appropriate match based on two operands. Numeric, string, regex, or binding.
#       say "Found fred." if %names ~~ /Fred/ # Match if Fred in keys.
#
#       if (@array1 ~~ @array2) # Check two arrays are equal.
#
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
# FOREACH
#   foreach $var (qw(test test2 test3 test4)) {
#	  print($var."\n");
#   }
#
# FOR:
#   for ($i = 1: $i < 10; $i++) {
#	   code
#   }
#
# IF
#   if ($name gt "fred") {
#   } elsif {
#   } else {}
#
# TERNARY:
#   expression ? if_true : if_false;
#
# GIVEN-WHEN: Equal to c Case structure.
#   given ($ARGV[0]) {
#       when (/Fred/) { do_code; }
#       when ...
#       default { do_this_otherwise; }
#
# UNLESS
#   unless (express) {} # Reverse of an if, only executes if expression is false.
#
# WHILE
#   while ($cnt > 1) {}
#
# UNTIL
#   until (expression) {} # Loop until the expression is true.
#
# LABELED LOOP:
#   LINE: while (<>) {
#       foreach (split) {
#            last LINE if /__END__/	 # Jump out to line, even though should just break foreach.
#       }
#   }
#
# NAKED BLOCK: Use this to namespace vars away.
#   {
#	print("Test")
#   }
#
# LOOP MODIFIERS:
#   last;   # Equivalent of c++ break.
#   next;   # Equivalent of c++ continue.
#   redo;   # Go back to the top, redo iteration without modification.
#
# Control Modifiers:
#   print("This") if $I_AM_TRUE; # Can use most constructs like this.
#
# AND, OR, XOR
# High Precedence: ||, &&, !
# Low Precedence: and, or, xor, not


# Matching // = m//. Some modifiers : /i, ignore case, /s make . match over \n, /x allow arbitrary whitespace, /g for global, /m for multi lines (changes ^ and $ to anchor at \n).
# Note: For grouping, to not put in memory use : /(?:test)/
# Regular matches: \g{1}, for named matches /(?<label>pattern)/, i.e. /(?<name>\w+)/. Retrieve in $+{name}. Back reference \g{name}.
# Note special regex automatic vars: print " $` <$&> $' ". ` has before match, & has matched, ' has string after match
# Case substitution: \l \u, next char is lower/upper. \L \U, all remaining chars lower/upper. \E to end case mod.
# RE ops: split /pattern/, "string", join "glue", @pieces.
# Quantifiers: Nongreedy match as little as possible: *?, +?, ??.
# Use eval to trap errors. Eval errors in $@ variable.  Map, grep for operations.
