#! /usr/bin/env python3
#
# main.py
#
# Bulk split URL's into components

from opencog.atomspace import AtomSpace
from opencog.type_constructors import *
from opencog.exec import execute_atom

from split_url import split_url

import sys
sys.path.append("..")
from webui.query import storage_open, storage_close

# storage_open(storage_url):

# -------------------------------------------------------------------------

def bulk_split() :

	q = QueryLink(
			EdgeLink(PredicateNode("URL"), VariableNode("$URL")),
			ExecutionOutputLink(
				GroundedSchemaNode("py:split_url"),
				ListLink(VariableNode("$URL"))))

	r = execute_atom(get_default_atomspace(), q)

	print("got", r)
	# Unpack the listing, convert it to a python list
#	for hi in r.to_list() :
#		print("yooo", hi)

space = AtomSpace()
push_default_atomspace(space)

bulk_split()

# ------------------ End of File. That's all, folks! ----------------------
# -------------------------------------------------------------------------
