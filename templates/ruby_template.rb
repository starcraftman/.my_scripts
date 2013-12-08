#!/usr/bin/ruby -w
# Imports - See require, alternatively load, autoload.

# Classes

# Funcs

# Main
puts("I am a template file.")


# Variables:
#   Lowercase first for vars. my_var, hello.
#   Uppercase first for constants: Constant, ConstantValueHere  
#
# Modifiers:
#   $: Global vars accessed via this.
#   @: Instance variables of a class.
#   @@: Class variables. Favor class instance variables, @var inside class, outside def.
#   ?: Methods return bool end in ?, i.e. isdigit?
#   !: Methods ending in ! may mutate params, use caution.
#   =: Methods ending in = may be used in assignment and trigger, method= .

# Common Funcs:
#   res = `ls -la` : System execution like perl, captures string result.
#   print() : Just print without any new line.
#   puts() : Print with new line.
#   x = gets.chomp : Get input and remove \n.

# Control Structs:
#   If: Most constructs return their value. 
#     x = if x < 10 then
#           x + 1
#         elsif x == 5 then
#           x + 20
#         else
#           x = -1
#         end
#
#   Unless: Reversed if as in perl. No elsif.
#     unless x > 10 then
#       55
#     else
#       100
#     end  
#
# Ternary:
#     cond ? true : false.
#
# Case: Note uses === equality test. Several syntax short hand. Range ops can be in test.
#   name = case x
#     when x == 1 then "one"
#     when 2
#       "two"
#     when 3 then "three"
#     when 4; "four"
#     when 0..7550  "in range" # Tests if x in the range.
#     else "many"
#   end
#
# While: Note, do is optional.
#   while x < 10 do 
#     puts x
#     x += 1
#   end
#
# Until: Reverse of while logic.
#
# For: For each over an iterator. Collection must have each method.
# array = [1, 2, 3, 4]
# for ele in array
#   puts ele
# end
#
# Iterators:
# Often use yield mechanism to retain state.
# Examples:
#   3.times { puts "thanks" }
#   data.each { |x| puts x } # Each element in x.
#   [1, 2, 3].map {|x| x*x} # Map function over array.
#   2.upto(n) {|x| puts x + 5}   
#
# Mapping iterators: collect (map), select, reject, inject.
# 1.upto(4) do |x;y,z| # Declare y, z to be local block vars.
#
# Iterator Modifiers:
#   rewind: Restart at the beginning.
#   break: Standard
#   next: Like continue.
#   redo: Restart loop or iterator from current.
#   retry: Restart an iterator and evaluate again.
#   throw/catch: Used for labelled breaks.
# Example:
#   catch :missing_data do
#     ....
#   throw :missing_data unless value # Put back to the above label.

# Literals:
#   Conversion:
#     To String: obj.to_s
#     To int:  obj.to_i
#     To char: obj.to_a
#     To float: obj.to_f
#     
# true/false
#   if obj # Means obj is not nil, else would be false. 
#   true, false, nil -> like NULL, indicates nothingness.
#     N.B. 0, "", [], {} are true. Only nil and false are false.
#
# Number:
#   Numbers with underscore: 1Mil = 1_000_000.
#   Num literals:
#     0xA1 : hex num, 047 : octal, 0b1101 : binary
#
# String:
#   '' string no special characters, standard for "".
#   String interpolation:
#     Normal Vars: "#{num}", Globals: "#$var"
#   No implicit conversion with to_s, must force.
#   Quote a string: %Q|This is a single string.|
#     '|' is any delim of punctuation.
#     %Q() for "string", %q for 'string'
#
# Arrays:
#   x = [1, 2, 3]
#   words = %w[this is a test], # array of strings, seperated by " ".
#     w for 'strings' and W for "strings"
#
# Array Class:
#   empty = Array.new(3) # Returns [nil, nil, nil]
#   zero = Array.new(2, 0) # Returns [0, 0]
#   array << [3,4,5] # Append the list.
#   a1 - a2 # Remove all elements of 2 from a1. Supports set with &, |.
#
# Hashes (Dictionary):
#   numbers = { :one => 1, :two => 2, :three => 3 } # Preferred syntax, uses symbols
#   numbers = Hash.new; numbers["one"] = 1   
#   numbers = { "one" => 1...} # Alternative, with strings.
#   numbers = { one: 1, two: 2 ... } # Shortest syntax, 1.9.
#
#   Index: numbers[:one] # Uses symbolic keys best, else use "one".
#
# Ranges:
#   1..10 # 1 to 10 including 10.
#   1...10 # Exclude 10.
#   Test in range: cold_war = 1045..1989; cold_war.include? birdate.year
#   Iteration: cold_war.each {|l| puts("[#{l}]")}
#
# Symbols:
#   Used for efficient lookup in hashes and other cases.
#   They are immutable and NEVER collected, permanently in table.
#   :symbol is short for -> :"symbol" . 
#
# Objects:
#   obj = myClass.new(1, 2) # Use constructor.
#   obj.object_id # The identity of an object, same throughout life. Fixnum.
#   obj.class.superclass # First gets class of obj, then superclass of it.
#   obj.instance_of? String # Does NOT check inheritance, obj MUST be String object.
#   obj.is_a? Object # Test if Object is a Superclass or class.
#   obj.respond_to? :"<<" # Check if obj supports the method append.
#   obj.equal?(b) # Test object equality, MUST BE SAME OBJECT i.e. obj.object_id == b.object_id.
#   obj.eql?(b) # Test exactly equality, no type conversion.
#   obj == b # Test if the values of obj and b are equal. Equivalent to java equals.
#   obj === b # Case equality, left is some range or applies to right.
#       /\d+/ === "123" # Matches, regex applies to right.
#   1 <=> 5 returns -1 # Use ordering operator, look at Comparable interface. 0 if equal, -1 if left before right, else 1.
#
#   obj.dup or obj.clone # Shallow copies, see slight differences.
#   def deepcopy(o) Marshal.load(Marshal.dump(o)) end # Marshalling to dump state, or load.
#   obj.freeze # Make it immutable.
#   obj.tainted? and obj.untrusted? # Mark object as not trustworth, web programming if took user input.

# Operators: 
#   Precedence : Location 3478.
#
#   << : Append the right to the left obj.
#   "." * 3 gives "..." : String multi.
#   =~ : Standard regex binding operator for string.
#   defined? : Acts as an operator telling you if object exists, if does what is it? (method, local var, global...)
#
# Operator packing:
#   Unpacking: Example x, y, z = 1, *[2, 3] # The star is like a python unpack, making 2,3 values go to y, z.
#    Packing: Example x, *y = 1, 2, 3 # Y gets packed with [2,3].

# Exceptions:
#   Exception Hierarchy: Location 5506, has all built ins from ruby book.
#   Subclass StandardError to make new exceptions.
#   Interesting note: Can attach rescue, else, ensure blocks to def, catches exceptions from method.
#   Rescue can even be attached to normal statements that could raise exceptions like func calls or num ops.
# 
# Throw Exception:
#   raise StanardError("Message to send.")
#   raise "Message." # Raise a RuntimeError with Message. If no message, raise same Error.
#
# Try/Catch Block:
#   Example code: => Are comments on code example.
#   begin
#     => code goes here...
# rescue => ex
#     => Check all exceptions from above here. Exception is in $! global if not named (i.e. just rescue).
#     => Specify a class(s) and name with syntax: rescue TypeError, ArgumentError => ex.
#     => Rerun the begin->rescue code by using retry in the rescue block. Transient errors.
# else
#     => Runs only if NO EXCEPTIONS were raised.
#     => Note: Won't run in code in begin used flow controls like break, return, next, redo .
# ensure
#     => Ensure code ALWAYS runs, if exception raised or not, even if return in begin code.
#     => Use to close I/O or other serious things.
# end
#

# Class:
#   Reader or Read/Set methods: attr_reader :x; attr_accessor :y, :z # Make reader for x, others set/get.
#   Class Method: def self.method(args) ... # Alternative: def className.method...
#     Class methods are part of the eigenclass.
#     Common syntax to get at this class:
#   class << self # Eigen of class, alternatively self -> className
#   def class_method1
#     => code here.
#   end        
#
#   Class code is executed like Python, ORDER IS IMPORTANT!
#   Use def initialize as equal to constructor/__init__
#   Inheritance: class Test < SuperClass # No multiple inheritance.
#   Superclass Invocation: super(x, y) # Call the same method in super class with x, y args.
#
#   Include another class, example comparable for ordering:
#   include Comparable
#   def <=>(other)
#
# Protection: Public unless otherwise modified. Other vals = protected, private.
#   class Test
#   public # Note, this is implicit, except for initialize.
#     => code...
#   protected
#     => code...
#   private
#     => code...
#   end
#
# Private class Method: A class method that is private, can't be used publicly.
#   private_class_method :new, :otherfunc # Makes new no longer public.
#

# Modules:
#   Put constants at top level, can be shared with sub modules/classes.
#   Put def functions inside to make module specific funtions.
#   Example:
#     module Test
#       def Test.helper ....
#
#   Special Init/Close code:
#     BEGIN { init code }
#     END { end code }
#

# Fiber Class:
#   Creates a generator like object that can bidirectionally communicate. Yield returns control to caller, even outside file.
# 
#   Example:
#     f = fiber.new do |message|
#       puts "Caller said: #{message}"
#       Fiber.yield("Hello.")
#     end
#
#   For complete features, require 'fiber'.
