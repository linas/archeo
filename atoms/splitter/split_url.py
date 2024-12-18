#
# split_url.py
#
# Split URL's into components

from opencog.atomspace import AtomSpace
from opencog.type_constructors import *
from opencog.exec import execute_atom
# from .webui import storage_open, storage_close

from urllib.parse import urlparse

def split_url(itemnode) :

	# We expect itemnode to really be a node
	if not itemnode.is_node() :
		raise RuntimeError("Not a node!")

	o = urlparse(itemnode.name)
	print("hey", o)

	rc = Node("asdf")
	return rc



# ------------------ End of File. That's all, folks! ----------------------
# -------------------------------------------------------------------------
