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

# Functions above are "private" to this module
# -------------------------------------------------------------------------
# Class below is the public API

# The file witness class. This is implemented as a class for two reasons.
# One is that it allows a bunch of constant Atoms to be set up; this saves
# some small amount of python overhead. Another reason is that this gives
# the same exact timestamp to one observation run. Thus, one run can be
# thought of as a space-like slice through the environmental data (the
# filesystem). Of course, if the file data is actively changing while
# observations are going on, then the timestamps could be off, since the
# crawls can take seconds, minutes or hours. The goal here is not to have
# some relativisticly-accurate timestamp, but instead to mark a
#
# Conceptually, the walker and the storage open-close could also be made
# a part of this class. But at this time, there is no burning need to
# consolidate all these functions under one class. This is in contrast to
# a single setup of the predicates, which is a real benefit.
class file_witness:
	def __init__(self):
		# Predicates of all kinds
		self.w = PredicateNode ("witness")
		self.phash = PredicateNode ("xxhash-64")
		self.purl = PredicateNode ("URL")
		self.conth = PredicateNode ("content xxhash-64")
		self.csize	= PredicateNode ("file size")
		self.cmod = PredicateNode ("last modified")

		# Get the current time, right now.
		self.now = ItemNode(str(datetime.now()))

		# Type-tag the date as being a date-dype.
		pwd = PredicateNode("witness date")
		store_atom(EdgeLink (pwd, self.now))

	# Be a witness to the existence of a file.
	# This is the primary, main public API implemented in this file.
	#
	# Arguments:
	#   fullname: the full file pathname
	#   domain: the hostname
	def witness_file(self, domain, fullname):

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
		fh = ItemNode(fhash)

		# File Atom
		fa = make_file_url(domain, fullname)

		store_atom(EdgeLink (self.phash, fh))   # Type-tag hashes as being hashes
		store_atom(EdgeLink (self.purl, fa))    # Type-tag URLS as being URL's

		# Witness
		fc = EdgeLink (self.conth, ListLink (fa, fh))
		store_atom(EdgeLink (self.w, ListLink (self.now, fc)))

		store_atom(EdgeLink (self.w, ListLink (self.now,
			EdgeLink (self.csize, ListLink (fa, ItemNode (str(fstat.st_size)))))))

		store_atom(EdgeLink (self.w, ListLink (self.now,
			EdgeLink (self.cmod, ListLink (fa, ItemNode (str(fstat.st_mtime)))))))

# -------------------------------------------------------------------------
# Open and close

# Global pointer to currently open StorageNode
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
