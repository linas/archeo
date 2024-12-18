#
# split_url.py
#
# Split URL's into components

import os

from opencog.atomspace import AtomSpace
from opencog.type_constructors import *
from opencog.exec import execute_atom
# from .webui import storage_open, storage_close

from urllib.parse import urlparse

def split_url(itemnode) :

	# We expect itemnode to really be a node
	if not itemnode.is_node() :
		raise RuntimeError("Not a node!")

	# Use an off-the-shelf python tool to split
	o = urlparse(itemnode.name)

	rc = ExecutionLink(
		PredicateNode("decoded URL"),
		itemnode,
		ListLink(
			EdgeLink(PredicateNode("protocol"), ItemNode(o.scheme)),
			EdgeLink(PredicateNode("domain"), ItemNode(o.netloc)),
			EdgeLink(PredicateNode("filepath"), ItemNode(os.path.dirname(o.path))),
			EdgeLink(PredicateNode("filename"), ItemNode(os.path.basename(o.path)))))

	return rc

# ------------------ End of File. That's all, folks! ----------------------
# -------------------------------------------------------------------------
