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

# Record a phototgraph stored in a directory.
# This has the form of a labelled directed graph edge.
# In ASCII graphics:
#
#                      "some edge label"
#    "from vertex" ------------------------> "to vertex"
#
# which in Atomese, becomes
#
#    (Edge (Predicate "some edge label")
#            (List (Item "from vertex") (Item "to vertex")))
#
# and for python, the parens get re-arranged and commas are inserted:
#
#    Edge (Predicate ("some edge label"),
#          List (Item ("from vertex"), Item ("to vertex")))
#
e = EdgeLink(
	# The relationship between the directory and the file:
	# the file is a "direntry" in the directory.
	PredicateNode("direntry"),
	ListLink(
		# The name of the directory with photos in it.
		ItemNode("my photo album"),

		# The photo itself.
		ItemNode("Fantastic Sunset on Sunday.jpg")))

print("Here's your data:", e)

