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
		return 0

	hasher = xxhash.xxh64()
	while True:
		chunk = f.read(4096)
		if not chunk:
			break
		hasher.update(chunk)
	return hasher.hexdigest()

# Build the desired ItemNode for a file
def make_file_url(domain, fullname):
	url = "file://" + domain + fullname
	return Item(url)

# Witness data about a file. This includes the content hash and the size.
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
	fsize = fstat.st_size

	# Get the file hash
	fhash = get_xxhash(fullname)

	# Get the current time, right now.
	now = Item(str(datetime.now()))

	print("its now", now)

	# File Atom
	fa = make_file_url(domain, fullname)

	fc = Edge (Predicate ("content xxhash-64"),
		List (fa, Item (fhash)))

	w = Predicate ("witness")

   Edge (w, List (now, fc))

	# cursor.execute(insrec, (fhash, fsize, fstat.st_mtime))


# functions above are "private" to this module
# -------------------------------------------------------------------------
#

storage = False

# Create a default AtomSpace, and open a connection to storage.
# the storage_url must be "rocks:///some/path/to/location"
def witness_store_open(storage_url):
	space = AtomSpace()
	set_default_atomspace(space)

	global storage
	storage = RocksStorageNode(storage_url)
	cog_open(storage)

def witness_store_close():
	global storage
	cog_close(storage)
	storage = False

# Be a witness to the existence of a file.
# This is the primary, main public API implemented in this file.
# Return the id number of the witnessed object
#
# Arguments:
#   fullname: the full file pathname
#   domain: the hostname
def file_witness(domain, fullname):
	global con
	frecid = get_file_record(domain, fullname)
	witness_date(conn, frecid)
	return frecid

# ------------------- That's all! End of file! ------------------
