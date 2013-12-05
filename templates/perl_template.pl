#!/usr/bin/env perl
# For Doc: perldoc name/module
# use File::Basename qw(dirname) # Import from a module, these subs.
use strict;
use diagnostics;
#use feature "say"; # Import specific features outside of version.
use 5.014; # Version forcing.

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
#	use feature "state"; state ($var1, var2);  # Use for persistent variables, same between calls.
# 		See more info at: http://perldoc.perl.org/perlsub.html#Persistent-Private-Variables
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
#
#   Regex Funcs:
#   @fields = split /:/, "abc:def:g:h" # @fields has -> ("abc", "def", "g", "h")
#   $line = join "-", 4, 5, 6, 7, 8 # Gives "4-5-6-7-8".
#   $line = joing "-", @fields # Gives "abc-def-g-h"
#

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

# Files: More at page 179.
#   if (! open CONFIG, "X", "filename") {} # For X, use: < readIn, > writeOut, >> append to file. Returns 0 for success.
#   while (<CONFIG>) {}
#   close CONFIG
#
#   Change default handle for print (STDIN usually)
#   $OLD = select(NEWHANDLE)
#
#   In place file editing:
#       $^I = ".bak" # See page 144.

# List Vs. Scalar Context:
#   $back = reverse qw/ yab dab doo/ # Returns oodbadbay string.
#   Force scalar:
#       print("I have ", scalar @rocks, "rocks!\n") # Prints length of array.
#
#   chomp(@lines = <STDIN>) # Reads as many lines as there are until eof, pass through chomp.
#
#   my ($first, $second, $third) = /(\S+) (\S+) (\S+)/ # Puts into the objects instead of memory $1 and so.

# Operator Notes:
#   SMART MATCH: Page 224 i
#       if ($name ~~ /Fred/) # Does appropriate match based on two operands. Numeric, string, regex, or binding.
#       say "Found fred." if %names ~~ /Fred/ # Match if Fred in keys.
#
#       if (@array1 ~~ @array2) # Check two arrays are equal.
#
#   BINDING OPERATOR:
#       $var =~ /\brub./ # Apply the regex on var, instead of $_.
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
#
#   Exponentiation: (-2)**4.

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

# Regular Expressions:
#   Precedence: Page 130.
#
#   Special Characters (Outside Classes):
#       . : Match any single character.
#       \ : Escape character, match period use \.
#       * : Match previous character 0 or more times. Greedy, match as much as possible.
#       ? : Match previous character 0 or 1 times. Greedy, match as much as possible.
#       + : Match previous character >= 1 times. Greedy, match as much as possible.
#       *? : Non-greedy, match least 0 or more of previous.
#       +? : Non-greedy, match least 1 or more of previous.
#       ?? : Non-greedy, match least of or or 1 of previous.
#       | : Match left or right, ( |\t)? matches 1 or or more space or tabs.
#       ^ : Anchor at front of string.
#       $ : Anchor at end of string.
#       \b : Match word boundary, /\bfred\b/, matches "fred" but not "freddie" or "manfred"
#           The word between \b is the equivalent of \w+.
#       {m,n} : General quantifier, used to specify number of repeats.
#       {3,} : >= 3, {,2} <=2, {2} exactly 2, {2,3} 2 or 3.
#
#   Special Characters (Inside Classes):
#       - : Match a range of characters, to match hyphen put at end. [ -] Matches space or hypen.
#       ^ : Negate this character class, must be first char. [^abc].
#
#   Character Classes:
#       [abcz] : Match one of the 4 chars a,b,c,z.
#       [a-zA-z] : Any letter.
#       [^abc] : Matches any character not a, b or c.
#
#   Class Shortcuts:
#       \d : Matches [0-9].
#       \D : Matches [^0-9].
#       \w : Matches [a-zA-Z0-9_]
#       \W : Negate above.
#       \s : Matches [\f\t\n\r ], any whitespace.
#       \S : Matches anything not whitespace.
#       \h : Match only [\t ], horizontal.
#       \v : Match only vertical whitespace. [\f\n\r]
#       \R : Match either \r or \n, any new line.
#
#   Grouping Matches:
#       Use () to group matchers. Then back reference then with \1, \2... numbers match bracket groups by opening.
#       Example: /(.)\1/ matches any double characters like bb, cc
#       Alternative notation: \{num}, i.e. \{1}
#           New notation used when ambiguous, i.e. (.)\{1}11
#
#       Negative Relative Indexing: Only with new brackets. (.)(.)\{-1}, refers to second group, one immediately to left.
#
#       Each group stores result in a memory location, $1...$n.
#       Memory stays until next matcher run.
#
#       (?:Fred) : Don't put this into memory i.e. $1. (just ?:)
#
#       Named Captures: Use to override storage in $1 to a special var.
#           (?<name>/fred/)
#       Will be stored in $+{name} and back referenced with \g{name}.
#
#       Special Default Memory:
#           $& : Matched entirely what was in m//.
#           $`: Whatever came BEFORE $& on the line(s).
#           $': Whatever came AFTER $& on the lines(s).
#
#   Matching operator and Modifiers:
#       // = m//, can use any chars so m<>, m[], m{}, m!fred!.
#       /fred/i : Match case insensitive fred.
#       /Fred.*Barney/s : Cross the \n boundary to match everything.
#       / -? \d+ \.? \d* /x : Allows you to pad with whitespace ignored.
#       /This is a line.\nNext line./m # Match beyond \n barrier.
#
#       Variables in patterns: /$var/ if var = 'fred' means /fred/
#
#   Substitution:
#       m/// = /// = /word/newword/ Make only first replacement in line. Otherwise, use g.
#       ///g : Turn on global matching, match as many times in string.
#
#       Case Shifting: Change matched case to lower or upper.
#           s/(fred|barney)/\U${1}/gi # This matches any case of fred or barney, then makes to FRED or BARNEY.
#           \U Makes everything upper that comes after. \L makes it lower. Turn off case shifting with \E.
#           \u or \l make ONLY the next char upper or lowercase.
#           Example:
#           s/(fred|barney)(.*)/\u\L${1}\E${2}/gi # Make fred/barney into Fred/Barney and ignore rest for case change.]
#
# Case substitution: \l \u, next char is lower/upper. \L \U, all remaining chars lower/upper. \E to end case mod.
# RE ops: split /pattern/, "string", join "glue", @pieces.
# Quantifiers: Nongreedy match as little as possible: *?, +?, ??.
# Use eval to trap errors. Eval errors in $@ variable.  Map, grep for operations.
