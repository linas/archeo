#
# query.py
#
# Database query shim for the webui for Archeo.

import threading

from opencog.atomspace import AtomSpace
from opencog.type_constructors import *
from opencog.exec import execute_atom
from opencog.storage import *
from opencog.storage_rocks import *

# -------------------------------------------------------------------------

storage = False

def storage_open(storage_url):
	global storage

	# If already open, do nothing.
	threading.Lock()
	if storage :
		return

	space = AtomSpace()
	push_default_atomspace(space)

	storage = RocksStorageNode(storage_url)
	cog_open(storage)

	# We're just going to bulk-load everything. This won't scale
	# for large DB's, but its OK for now.
	load_atomspace()
	print("Done loading AtomSpace. Size=", len(space))

def storage_close():
	global storage
	cog_close(storage)
	storage = False
	pop_default_atomspace()

# -------------------------------------------------------------------------

# Return a list of duplicated filenames.
# This is fairly normal: the same filename may be used in many places
def find_duplicated_names() :
	#sel = "SELECT filename, frecid, COUNT(*) FROM FileRecord GROUP BY filename HAVING COUNT(*) > 1;"
	#return cursor.execute(sel)
	return {}

# -------------------------------------------------------------------------

# Return a list of duplicated hashes.
# This is fairly normal: the same file contents, different locations/names
# Argument is a minimum number of duplicates that need to be found,
# in order to make it to the cut.
def find_duplicated_hashes(min_num_dups) :

	q = QueryLink(
			AndLink(
				EdgeLink(PredicateNode("content xxhash-64"),
					ListLink(VariableNode ("$URL"), VariableNode("$hash"))),
				GroupLink(
					VariableNode("$hash"),
					IntervalLink(NumberNode (str(min_num_dups)), NumberNode("-1")))),
				VariableNode("$hash"))

	r = execute_atom(get_default_atomspace(), q)

	# Unpack the listing, convet it to a python list
	hashlist = []
	for hi in r.to_list() :
		itemnode = hi.to_list()[0]
		itemname = itemnode.name
		hashlist.append(itemname)

	return hashlist

# -------------------------------------------------------------------------

# Generic select on the FileRecord table.
# Example usage:
#   select_filerecords(domain='foo', filepath='/bar/baz')
# Creates query
#   SELECT * FROM FileRecord WHERE domain='foo' AND filepath='/bar/baz';
#
def select_filerecords(**kwargs) :
#	sel = "SELECT * FROM FileRecord WHERE "
#	more = False
#	vlist = []
#	for k,v in kwargs.items():
#		if more :
#			sel += " AND "
#		sel += k + " =? "
#		more = True;
#		vlist.append(v)
#	sel += ";"
#	return cursor.execute(sel, vlist)
	return {}

# ------------------ End of File. That's all, folks! ----------------------
# -------------------------------------------------------------------------
