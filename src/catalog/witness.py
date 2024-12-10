#
# witness.py
#
# Witness, aka record the presence of a file in the filesystem.
# Given a filepath, this will record the existence of such a file
# into the SQL db holding filedata.

from datetime import datetime
import os
import pathlib
import sqlite3
import xxhash

# Get the xxhash of a file at the given location.
# Returns a 64-bit int.
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
	# return hasher.hexdigest()

	# Half the time, the sign bit will be set. But sqlite3 chokes
	# on this case. So explictly convert to signed 64-bit
	uinthash = hasher.intdigest()
	if uinthash > 2**63-1 :
		return uinthash - 2**64
	else :
		return uinthash

# Attempt to locate a known file record, based on the filename, filepath
# size and hash. This does not guarantee that its "really the same file".
# because there could be hash collisions, because we're not using crypto-
# strong hashes. But I think that's OK, for present purposes.
#
# This is meant to be a "private routine only", a helper for the internal
# use of the witness, below. Thus, it has a "hard to use" but more(?)
# efficient API
def find_file_record(conn, domain, filepath, filename, fhash, fsize) :

	# Create a new cursor. Not very efficient but so what.
	cursor = conn.cursor()

	# Avoid computing the filehash if we already know that the
	# the file is not in the catalog. This is the most common case,
	# when cataloging brand-new, previously-unseen files.
	sel = "SELECT frecid FROM FileRecord WHERE filename = ?;"
	w = cursor.execute(sel, (filename,))
	ro = w.fetchone()
	if not ro:
		return 0

	# Search for a matching witness, if any
	sel = "SELECT frecid FROM FileRecord WHERE filename = ? AND "
	sel += "filepath = ? AND domain = ? AND filexxh = ? AND filesize = ?;"
	w = cursor.execute(sel, (filename, filepath, domain, fhash, fsize))
	ro = w.fetchone()
	if not ro:
		return 0
	(rowid,) = ro
	return rowid


# Find or create a file record. This is not the same as "witnessing"
# the file; a witness also records the date when the file was seen.
# This, by contrast, merely creates a tracking id for a file.
#
# Arguments:
#   conn the sqlite3 connection
#   fullname: the full file pathname
#   domain: the hostname
def get_file_record(conn, domain, fullname):

	# Try to find the file in the filesystem
	fh = pathlib.Path(fullname, follow_symlinks=False)

	# Throw an exception if the file doesn't exist.
	if not fh.is_file():
		raise ValueError("No such file")

	# On Linux, filenames are just "a bunch of bytes", maybe
	# an iso8859 encoding, maybe utf8, maybe microsoft-crazy.
	# The database can only deal with strings that are taken to be
	# bytestrings of valid utf8 chars. Meanwhile, in python3,
	# strings are strings of chars, which may or may not be
	# representable (or "encodable") as utf8.
	#
	# Thus, we test. If the filename can be "encoded" into utf8,
	# *then* just pass the python string to sqlite3, and let sqlite3
	# call encode() on it. Which it will, because when it fails, it
	# throws an exception. We want to anticipate this exception, before
	# it happens, and avoid it. We want to avoid it because its nasty
	# to handle at that point; its too late.
	#
	# So we test by trying the encode ourselves. If no error, then
	# do nothing, and pass the python string to sqlite as-is. But if
	# it throws, then we encode ourselves, using the 'surrogateescape'
	# option. This gives us a byte string, which sqlite can deal with.
	#
	# We don't want to do this for all strings, because then the plain
	# old SELECT blah FROM blah WHERE foo='bar'; fails in the native
	# sqlite3 command shell, because foo is a byte string and 'bar' is
	# a cough cough "character string". Yes, this is screwy and
	# non-sensical, but so it goes.
	try:
		fullname.encode('utf8')
	except:
		fullname = fullname.encode('utf8', 'surrogateescape')

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

	# If we are here, we create a new witness record.
	# Create a new cursor. Not very efficient but so what.
	cursor = conn.cursor()

	# Stuff a bunch of data into the DB
	insrec = "INSERT INTO FileRecord "
	insrec += "(filename, filepath, domain, filexxh, filesize, filecreate) "
	insrec += "VALUES (?, ?, ?, ?, ?, ?) RETURNING frecid;"
	cursor.execute(insrec, (filename, filepath, domain, fhash, fsize, fstat.st_mtime))

	# We could get the rowid from the cursor.lastrowid
	# but RETURNING gives me warm fuzzies.
	# rowid = cursor.lastrowid
	(rowid,) = cursor.fetchone()

	# Save (commit) the changes
	conn.commit()

	return rowid

# Record date of witnessing
def witness_date(conn, fileid) :
	# Get the current time, right now.
	now = datetime.now()

	# Create a new cursor. Not very efficient but so what.
	cursor = conn.cursor()

	# Stuff a bunch of data into the DB
	insrec = "INSERT INTO RecordWitness(frecid, witnessdate) VALUES (?, ?);"
	cursor.execute(insrec, (fileid, now.timestamp()))

	# Save (commit) the changes
	conn.commit()

# functions above are "private" to this module
# -------------------------------------------------------------------------
#
# DB connection as global. This should be a per-thread global,
# but multi-threading is low on the priority list right now.
# Basically, the connection will be a part of the DB context
# I don't want to drag this through the whole API just to get
# at the context. Think of this as a (lisp) closure.
global conn;

def witness_db_open(dbname):
	global conn
	conn = sqlite3.connect(dbname)

def witness_db_close():
	global conn
	conn.close()

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
