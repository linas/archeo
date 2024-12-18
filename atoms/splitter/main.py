#
# main.py
#
# Bulk split URL's into components

from opencog.atomspace import AtomSpace
from opencog.type_constructors import *
from opencog.exec import execute_atom
from .webui import storage_open, storage_close

# storage_open(storage_url):

# -------------------------------------------------------------------------

def bulk_split()

#	q = QueryLink(
#			EdgeLink(PredicateNode("content xxhash-64"),
#				ListLink(VariableNode ("$URL"), VariableNode("$hash"))),

	e = ExecuttionOutput(
		GroundedPredicate("py:split_url"),
		ListLink(
			ItemNode("file://localhost/usr/lib/foo/bar")))

	r = execute_atom(get_default_atomspace(), e)

	# Unpack the listing, convert it to a python list
	for hi in r.to_list() :
		print("yooo", hi)


# ------------------ End of File. That's all, folks! ----------------------
# -------------------------------------------------------------------------
