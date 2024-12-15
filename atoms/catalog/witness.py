#
# witness.py
#
# Witness, aka record the presence of a file in the filesystem.
# Given a filepath, this will record the existence of such a file
# into an AtomSpace.

from datetime import datetime
import os
import pathlib
import xxhash

from opencog.atomspace import AtomSpace
from opencog.type_constructors import *
from opencog.storage import *
from opencog.storage_rocks import *

# Get the xxhash of a file at the given location.
# Returns a hash, encoded as a hex string.
def get_xxhash(filename):

	# A typical exception is "Access denied". In this case, we return
	# a hash of zero, and so the existence of the file will be noted,
	# but not of it's contents.
	# XXX FIXME: this logging should be controlled by the config file.
	try:
		f = open(filename, "rb")
	except:
		return '0'

	hasher = xxhash.xxh64()
	while True:
		chunk = f.read(4096)
		if not chunk:
			break
		hasher.update(chunk)
	return str(hasher.hexdigest())

# Build the desired ItemNode for a file
def make_file_url(domain, fullname):
	url = "file://" + domain + fullname
	return ItemNode(url)

# functions above are "private" to this module
# -------------------------------------------------------------------------
#

# Be a witness to the existence of a file.
# This is the primary, main public API implemented in this file.
#
# Arguments:
#   fullname: the full file pathname
#   domain: the hostname
def witness_file(domain, fullname):

	# Try to find the file in the filesystem
	fh = pathlib.Path(fullname, follow_symlinks=False)

	# Throw an exception if the file doesn't exist.
	if not fh.is_file():
		raise ValueError("No such file")

	# Stat the file before touching te atomspace. This might
	# cause more exceptions to be thrown, I guess.
	fstat = fh.stat()

	# Get the file hash
	fhash = get_xxhash(fullname)

	# Get the current time, right now.
	now = ItemNode(str(datetime.now()))

	# File Atom
	fa = make_file_url(domain, fullname)
	w = PredicateNode ("witness")

	fc = EdgeLink (PredicateNode ("content xxhash-64"),
		ListLink (fa, ItemNode (fhash)))
	store_atom(EdgeLink (w, ListLink (now, fc)))

	store_atom(EdgeLink (w, ListLink (now,
		EdgeLink (PredicateNode ("file size"),
			ListLink (fa, ItemNode (str(fstat.st_size)))))))

	store_atom(EdgeLink (w, ListLink (now,
		EdgeLink (PredicateNode ("last modified"),
			ListLink (fa, ItemNode (str(fstat.st_mtime)))))))

storage = False

# Create a default AtomSpace, and open a connection to storage.
# the storage_url must be "rocks:///some/path/to/location"
def witness_store_open(storage_url):
	space = AtomSpace()
	push_default_atomspace(space)

	global storage
	storage = RocksStorageNode(storage_url)
	cog_open(storage)

def witness_store_close():
	global storage
	cog_close(storage)
	storage = False
	pop_default_atomspace()

# ------------------- That's all! End of file! ------------------
