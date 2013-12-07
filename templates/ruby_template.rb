#!/usr/bin/env ruby -w
# Imports




# Variables:
#   Lowercase first for vars. my_var, hello.
#   Uppercase first for constants: Constant, ConstantValueHere  
#
#   Modifiers:
# => $: Global vars accessed via this.
# => @: Instance variables of a class.
# => @@: Class variables.
# => ?: Methods return bool end in ?, i.e. isdigit?
# => !: Methods ending in ! may mutate params, use caution.
# => =: Methods ending in = may be used in assignment and trigger, method= .

# Common Funcs:
# res = `ls -la` : System execution like perl, captures string result.
# => print() : Just print without any new line.
# => puts() : Print with new line.
#

# Control Structs:
# => If:
# =>    if x < 10 then
# =>      x = x + 1
# =>    end
#
# => While: Note, do is optional.
# =>    while x < 10 do 
# =>      puts x
# =>      x += 1
# =>    end
#
#
#


# Literals:
# Conversion:
# => To String: obj.to_s
# => To int:  obj.to_i
# => To char: obj.to_a
# => To float: obj.to_f
# => if obj # Means obj is not nil, else would be false. 
#
# true, false, nil -> like NULL, indicates nothingness.
#
# Number:
# => Numbers with underscore: 1Mil = 1_000_000.
# => Num literals:
# =>  0xA1 : hex num, 047 : octal, 0b11
#
# String:
# '' string no special characters, standard for "".
# => String interpolation:
# =>    Normal Vars: "#{num}", Globals: "#$var"
# => No implicit conversion with to_s, must force.
# => Quote a string: %Q|This is a single string.|
# =>    '|' is any delim of punctuation.
# =>    %Q() for "string", %q for 'string'
#
# Arrays:
# => x = [1, 2, 3]
# => words = %w[this is a test], # array of strings, seperated by " ".
# =>      w for 'strings' and W for "strings"
# => 
#
# Array Class:
# =>  empty = Array.new(3) # Returns [nil, nil, nil]
# =>  zero = Array.new(2, 0) # Returns [0, 0]
# =>  array << [3,4,5] # Append the list.
# =>  a1 - a2 # Remove all elements of 2 from a1. Supports set with &, |.
#
# Hashes (Dictionary):
# => numbers = { :one => 1, :two => 2, :three => 3 } # Preferred syntax, uses symbols
# => numbers = Hash.new; numbers["one"] = 1   
# => numbers = { "one" => 1...} # Alternative, with strings.
# => numbers = { one: 1, two: 2 ... } # Shortest syntax, 1.9.
#
# => Index: numbers[:one] # If symbol, else use "one".
#
# Ranges:
# => 1..10 # 1 to 10 including 10.
# => 1...10 # Exclude 10.
# => Test in range: cold_war = 1045..1989; cold_war.include? birdate.year
# => Iteration: cold_war.each {|l| puts("[#{l}]")}
#
# Symbols:
# => Used for efficient lookup in hashes and other cases.
# => They are immutable and NEVER collected, permanently in table.
# => :symbol is short for -> :"symbol" . 
#
# Objects:
# => obj = myClass.new(1, 2) # Use constructor.
# => obj.object_id # The identity of an object, same throughout life. Fixnum.
# => obj.class.superclass # First gets class of obj, then superclass of it.
# => obj.instance_of? String # Does NOT check inheritance, obj MUST be String object.
# => obj.is_a? Object # Test if Object is a Superclass or class.
# => obj.respond_to? :"<<" # Check if obj supports the method append.
# => obj.equal?(b) # Test object equality, MUST BE SAME OBJECT i.e. obj.object_id == b.object_id.
# => obj.eql?(b) # Test exactly equality, no type conversion.
# => obj == b # Test if the values of obj and b are equal. Equivalent to java equals.
# => obj === b # Case equality, left is some range or applies to right.
# =>    /\d+/ === "123" # Matches, regex applies to right.
# => 1 <=> 5 returns -1 # Use ordering operator, look at Comparable interface.
#
# => obj.dup or obj.clone # Shallow copies, see slight differences.
# => def deepcopy(o) Marshal.load(Marshal.dump(o)) end # Marshalling to dump state, or load.
# => obj.freeze # Make it immutable.
# => obj.tainted? and obj.untrusted? # Mark object as not trustworth, web programming if took user input.

# Operators:
# => << : Append the right to the left obj.
# => "." * 3 gives "..." : String multi.
# => =~ : Standard regex binding operator for string.
#
