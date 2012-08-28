# Template for all src Makefiles. Use .cc for c++, .c for c.
# Useful options to make:
# 	-n : Just print recipe commands would have executed.
#	-d : Print debugging information.
#   -C : Change directory before reading make file and executing a target. (CAPITAL C)
#   -f : Read the file specified as a makefile.
#   -I dir: Specify an include path for include directives.
#   --no-print-directory : Turns off/on make reporting directory changes.
#	--print-data-base : Print all implicit rules.
#	make CPPFLAGS=' -DMALLOC=1 -g' # Override the CPPFLAGS by command.

# Usefule vars:
# 	$@, the target being made (left side of :).
#	$^, the names of all prereqs with spaces between.
#   $<, the name of the first prereq for the target.
#   $%, when the target is an archive, the target member name instead of archive given by $@.
#   $?, prereqs that are newer than the target.
# TIP: $(@D) prints directory portion, $(@F) prints file name.

# VPATH:
#	VPATH: Defines a series of directories to search for source files.
# 	i.e. : VPATH: src src2 src3
#	vpath %.suffic dir list: More specific matchers.
#	vpath %.c src | vpath %.h include

# Variables:
#	:= : Immediate simple expansion. = : Recursive lazy expansion. ?= : Conditional expansion, assigns if not defined.
# 	+= : Standard addition.
# TIP: Use @ before command in recipe to turn off echo of the command itself.
#   Pass #define flags into compilation with -DUSE_MALLOC=1. Make defines compilation only by:
#	gui.o: CPPFLAGS += -DUSE_MALLOC=1, gui.o: gui.c # Now only for gui.o and sub compilations will flag be present.

# Control:
# ifdef/ifndef CONSTANT else endif || ifeq/ifneq(a,b) endif # Can 
# Note: Make sure to not have leading tabs on control operators.
# To strip spaces: ifeq "$(strip $(OPTIONS))" "-d"

# Includes/Cmd modify:
#	include file.mk  # Have to find file.mk to continue..
#   -include file.mk # Ignore return code of the command.
#	+include file.mk # Always execute command even if in dry run mode.
# 	! include file.mk # Negate the return code.

# Functions:
#	To make macro: define name ..... endef, use \ to escape new lines.
# 	$(call name, param1, param2), params substituted for $1 in macro

include ../Make.defines

.PHONY: all clean

OBJS = $(OBJS0) $(OBJS1)
OBJ0 = first.o
OBJ1 = second.o

# Note, $@ is 
all: $(OBJS) libtest.a
	$(CC) -o $@ $^

# Update the ar, pass only those files newer than the archive.
libtest.a: test1.c test2.c
	$(AR) $(ARFLAGS) $@ $?

libcounter.a: libcounter.a(lexer.o): libcounter.a(counter.o)

clean:
	$(RM) $(OBJS) $(CLEAN_FILES)

# ------------------------ Function index ------------------------------------- 
# filter: Filter from list those that match.
#	$(ui_lib): $(filter ui/%.o,$(objects)) ... # Filter ui/*.o from objects.
#
# filter-out: Filter those that don't match pattern.
#	$(ui_lib: $(filter ui/%.o,$(objects)) ... # Filters out things that don't match ui/%.o.
#
# findstring: Find str in text. Doesn't support % wildcard.
# 	# $(findstring /test/book/admin,$(PWD) ... # Prints out to console the string if found in PWD. More portable to use @echo.
#
# subst : Substitute some text for other in a list, no wildcards.
#	sources := count.c test.c work.c	
#	objects := $(subst .c,.o,$(sources))
#
# patsubst: Substitute based on pattern match, supports %.
#	strip-slash := $(patsubt %/,%,$(dirs)
# 
# words: Counts the number of words in a list, separated space.
#	CWD := $(subst, /, ,$(HOME))
#	words:
#		@echo HOME has this many words: $(words, $(CWD)).
#
# words n, text: Returns the nth word from text.
#	@echo Second word of $HOME is $(words 2, $(HOME))
#
# firstword: Return the first word of list.
#	@echo: First word in list is $(firstword $(list)).
#
# wordlist start,end,list: Return list of words from start to end position, inclusive both.
#	@echo: The list of words from 2-6 is, $(wordlist 2,6,$(list))
#	
# sort: Take a list and do a unix sort.
#	@echo: The sorted list is $(sort $(list))
#
# shell: Pass a command directly to the shell. Can be used to use bash control functions like for.
#	stdout := $(shell echo normal message)
#
# wildcard: Do unix file globing expansion.
#	sources := $(wildcard *.c *.h)
#	dot-emacs-exist := $(wildcard ~/.emacs) # Will return empty if not exists. 
#
# dir: Return the directory portion only, same as D useage.
#	source-dirs := $(sort $(dir $(shell find . -name '*.c'))) # Find all c source files under cwd, strip to just dirs and sort.
#
# notdir: Returns the filename portion of a string.
#	class-name = $(notdir $(subst .java,,$1))
#
# suffix: Return the suffix of all words in list.
#	$(suffix $(list))
#
# basename: Returns the filename without suffix.
# 	$(basename $(word))
#
# addsuffix: Add a suffix to a list of words.
#	$(addsuffix /*,$(dirs))
#
# addprefix: Adds a prefix to a list of words.
#   $(addprefix dns,$(files))
#
# join: Take two lists and combine them together matching the same position in each.
# 	$(join $(stripped-dirs),$(filenames))
#
# strip: Remove all trailing and leading whitespace. Use for protection in if construct.
#	$(strip $(word))
#
# origin: Returns how the var was set: via makefile, environment, undefined, etc....
#   $(origin $(COMSPEC))
#
#------------------------------------ Control -----------------------------------------
#
# $(if,then,else): Conditional operation, allows to select from two choices.
#	PATH_SEP := $(if $(COMSPEC),;,:) # Select the sep, only windos has comspec.
#
#	Another common example:
#	$(if $(filter $(MAKE_VERSION),3.80),,$(error Require make at least 3.80.))
#
# $(warning Text): Same as error but doesn't cause stop.
#
# $(error Text): Prints an error message and exits make with 2. Prints current place.
#
# $(foreach var,list,body): Standard foreach loop.
#	letters := $(foreach letter,a b c d e,$(letter))
#	show-words:
#		# letters has $(words $(letters)) words: '$(letters)'
#
#
#

