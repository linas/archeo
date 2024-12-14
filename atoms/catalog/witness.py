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

# Attempt to locate a known file record, based on the filename, filepath
# size and hash. This does not guarantee that its "really the same file".
# because there could be hash collisions, because we're not using crypto-
# strong hashes. But I think that's OK, for present purposes.
#
# This is meant to be a "private routine only", a helper for the internal
# use of the witness, below. Thus, it has a "hard to use" but more(?)
# efficient API
def find_file_record(conn, domain, filepath, filename, fhash, fsize) :

	return False


# Find or create a file record. This is not the same as "witnessing"
# the file; a witness also records the date when the file was seen.
# This, by contrast, merely creates a tracking id for a file.
#
# Arguments:
#   fullname: the full file pathname
#   domain: the hostname
def get_file_record(domain, fullname):

	# Try to find the file in the filesystem
	fh = pathlib.Path(fullname, follow_symlinks=False)

	# Throw an exception if the file doesn't exist.
	if not fh.is_file():
		raise ValueError("No such file")

	# Split the full filepathname into a filepath and the filename
	(filepath, filename) = os.path.split(fullname)

	fstat = fh.stat()
	fsize = fstat.st_size

	# Get the file hash
	fhash = get_xxhash(fullname)

	# Do we already have a witness for this file? If so, return that
	frecid = find_file_record(conn, domain, filepath, filename, fhash, fsize)
	if frecid:
		return frecid

	insrec = "INSERT INTO FileRecord "
	cursor.execute(insrec, (filename, filepath, domain, fhash, fsize, fstat.st_mtime))

	return rowid

# Record date of witnessing
def witness_date(conn, fileid) :
	# Get the current time, right now.
	now = datetime.now()

	# Stuff a bunch of data into the DB
	insrec = "INSERT INTO RecordWitness(frecid, witnessdate) VALUES (?, ?);"
	cursor.execute(insrec, (fileid, now.timestamp()))

	# Save (commit) the changes
	conn.commit()

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
	frecid = get_file_record(conn, domain, fullname)
	witness_date(conn, frecid)
	return frecid

# ------------------- That's all! End of file! ------------------
