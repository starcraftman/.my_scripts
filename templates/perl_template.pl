#!/usr/bin/env perl
use strict;
use diagnostics;
#use feature "say";
#use feature "switch";
#use feature "state";
#use 5.012
use 5.014;

# Matching // = m//. Some modifiers : /i, ignore case, /s make . match over \n, /x allow arbitrary whitespace, /g for global, /m for multi lines (changes ^ and $ to anchor at \n).
# Note: For grouping, to not put in memory use : /(?:test)/
# Regular matches: \g{1}, for named matches /(?<label>pattern)/, i.e. /(?<name>\w+)/. Retrieve in $+{name}. Back reference \g{name}.
# Note special regex automatic vars: print " $` <$&> $' ". ` has before match, & has matched, ' has string after match
# Case substitution: \l \u, next char is lower/upper. \L \U, all remaining chars lower/upper. \E to end case mod.
# RE ops: split /pattern/, "string", join "glue", @pieces.
# Quantifiers: Nongreedy match as little as possible: *?, +?, ??.	
# Use eval to trap errors. Eval errors in $@ variable.  Map, grep for operations.
