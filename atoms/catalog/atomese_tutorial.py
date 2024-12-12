#! /usr/bin/env python3
#
# atomese_tutorial.py
#
"""
A basic tutorial showing some of the basic concepts from the OpenCog
AtomSpace. The final implementation is an expansion of the basic idea
shown in this demo. Read this first, if you are new to OpenCog.
"""

from opencog.atomspace import AtomSpace
from opencog.type_constructors import *
from opencog.storage import *

space = AtomSpace()
set_default_atomspace(space)

# Record a photograph stored in a directory.
#
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
# Photographs are "stored" (or can be found at) URL locations.
# The relationship between the URL location and the file name can
# be indicated with an arrow. (This is one of many ways.)
e = EdgeLink(
	# Here, "URL" is just some string. Any string will do.
	PredicateNode("URL"),
	ListLink(
		# The name of the directory with photos in it.
		ItemNode("file:///Home Computer/folders/My photo album"),

		# The photo itself.
		ItemNode("Fantastic Sunset on Sunday.jpg")))

print("Here's your data:", e)

# -------------------------------------------

storage = RocksStorageNode("rocks://tmp/foo")
