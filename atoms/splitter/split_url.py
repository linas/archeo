#
# split_url.py
#
# Split URL's into components

from opencog.atomspace import AtomSpace
from opencog.type_constructors import *
from opencog.exec import execute_atom
from .webui import storage_open, storage_close

from urllib.parse import urlparse

def split_url(url) :
	print("hey", url)
	return Node('foo')



# ------------------ End of File. That's all, folks! ----------------------
# -------------------------------------------------------------------------
