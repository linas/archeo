#! /usr/bin/env python3
#
# hello_world.py
#
"""
A basic demo for how to use the OpenCog AtomSpace together with python,
to store and retreive data. A great place to start for beginners.
"""

from opencog.atomspace import AtomSpace
from opencog.atomspace import types
from opencog.type_constructors import *


space = AtomSpace()
set_default_atomspace(space)

# Record a phototgraph stored in a directory
s = Section(
	# The relationship between the directory and the file:
	# the file is a "direntry" in the directory.
	PredicateNode("direntry"),
	Link(
		# The name of the directory with photos in it.
		ItemNode("my photo album"),

		# The photo itself.
		ItemNode("Fantastic Sunset on Sunday.jpg")))

print("Hey yo its", s)

