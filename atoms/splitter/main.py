#! /usr/bin/env python3
#
# main.py
#
# Bulk split URL's into components

from opencog.atomspace import AtomSpace
from opencog.type_constructors import *
from opencog.exec import execute_atom
from opencog.storage import store_atom

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

	# Report on what we've done
	print("Number of URL's split:", len(r.to_list()))

	# Store into the database
	for splt in r.to_list() :
		store_atom(splt)

# Just do it
storage_open("rocks:///tmp/foo")
bulk_split()
storage_close()

# ------------------ End of File. That's all, folks! ----------------------
# -------------------------------------------------------------------------
