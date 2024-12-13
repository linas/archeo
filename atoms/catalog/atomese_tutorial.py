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
from opencog.storage_rocks import *

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

# AtomSpace contents can be loaded, stored and send over the net.
# Below, a StorageNode is used save selected AtomSpace contents
# to a RocksDB database. Rocks is nice, because it requires no
# config to use.

# Create a RocksDB StorageNode, and open a connection to it.
# The rocks:// URL specifies a directory in the local filesystem.
storage = RocksStorageNode("rocks:///tmp/foo")
cog_open(storage)

# Store the one and only edge created above.
store_atom(e)

# Close the connection to storage.
cog_close(storage)
print("Closed the connection to storage")

print("\nWill now clear the AtomSpace.")
print("Before clearing, it contains a total of " + str(len(space)) + " atoms")
print("These are:")

for atom in space:
	print(atom)

space.clear()
print("The AtomSpace after clearing: ", len(space))


print("Good bye!")
