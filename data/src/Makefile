# Possible arguments
# DEBUG=1               [ 0 | 1 ],         default 0
# COMPILER              [ g++ | clang++ ], default: g++ on Linux
#

DEBUG ?= 0

# platform
PLATFORM := $(shell uname -s)
$(info PLATFORM: $(PLATFORM))

# compiler
COMPILER ?= g++
CC = $(COMPILER)
$(info COMPILER: $(CC))

# directories
BINDIR:=bin
ifeq ($(DEBUG),1)
  BINDIR=$(BINDIR)-dbg
endif
$(info BINDIR: $(BINDIR))

# file extensions
ifeq ($(PLATFORM), Linux)
  OBJ=.o
  EXE=.out
  DLL=.so
  LIB=.a
else
# cygwin or mingw
  OBJ=.obj
  EXE=.exe
  DLL=.dll
  LIB=.lib
endif
$(info EXTENSIONS:  $(OBJ) $(EXE) $(DLL) $(LIB))


CPPFILES := $(patsubst ./%,%,$(shell find . -name "*.cpp"))
$(info CPP:     $(CPPFILES))

DEPFILES := $(patsubst %.cpp,$(BINDIR)/%.d,$(CPPFILES))
$(info DEPFILES:     $(DEPFILES))


OBJFILES := $(patsubst %.cpp,$(BINDIR)/%$(OBJ),$(CPPFILES))
$(info OBJFILES:     $(OBJFILES))


HEADER := $(patsubst ./%,%,$(shell find . -name "*.h"))
$(info HEADER:     $(HEADER))


MAINS := $(shell grep -l "int main" *.cpp)
$(info MAINS:   $(MAINS))

NONMAINS := $(filter-out $(MAINS),$(CPPFILES))
$(info NONMAINS:   $(NONMAINS))

NONMAINSOBJ := $(patsubst %.cpp,$(BINDIR)/%$(OBJ),$(NONMAINS))
$(info NONMAINOBJS: $(NONMAINSOBJ))

TARGETS := $(patsubst %.cpp,$(BINDIR)/%$(EXE),$(MAINS))
$(info TARGETS: $(TARGETS))

DEPFLAGS=-MT $@ -MMD -MP -MF $(BINDIR)/$*.d
CFLAGS:=-c -std=c++20 -march=native -Wall -Werror

LFLAGS=
LIBS=

ifeq ($(DEBUG),1)
   CFLAGS += -g -DDEBUG
else
   CFLAGS += -O3
endif


all : $(TARGETS)

.SECONDARY: $(OBJFILES) $(DEPFILES)


$(BINDIR)/%$(OBJ) : %.cpp
$(BINDIR)/%$(OBJ) : %.cpp Makefile $(BINDIR)/%.d | $(BINDIR)
	$(CC) $(CFLAGS) $(DEPFLAGS) $< -o $@

$(BINDIR)/%$(EXE) : $(BINDIR)/%$(OBJ) $(NONMAINSOBJ)
	$(CC) $(LFLAGS) $^ -o $@


$(DEPFILES):

include $(wildcard $(DEPFILES))

# clean
.PHONY: clean
clean:
	rm -rf $(BINDIR)


# use -p for multithreading
$(BINDIR):
	mkdir -p $@
