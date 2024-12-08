#! /usr/bin/env python3
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
	f = open(filename, "rb")
	hasher = xxhash.xxh64()
	while True:
		chunk = f.read(4096)
		if not chunk:
			break
		hasher.update(chunk)
	# return hasher.hexdigest()
	return hasher.intdigest()

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

	# Search for a matching witness, if any
	sel = "SELECT frecid FROM FileRecord WHERE "
	sel += "filename = '" + filename + "';"
	w = cursor.execute(sel)
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

	# Split the full filepathname into a filepath and the filename
	(filepath, filename) = os.path.split(fullname)

	fstat = fh.stat()
	fsize = str(fstat.st_size)

	# Get the file hash
	fhash = str(get_xxhash(fullname))

	# Do we already have a witness for this file? If so, return that
	frecid = find_file_record(conn, domain, filepath, filename, fhash, fsize)
	if frecid:
		return frecid

	# If we are here, we create a new witness record.
	# Create a new cursor. Not very efficient but so what.
	cursor = conn.cursor()

	# Stuff a bunch of data into the DB
	insrec = "INSERT INTO FileRecord(filename, filepath, domain, filexxh, filesize, filecreate) VALUES "
	insrec += "('" + filename + "','" + filepath + "','" + domain + "',"
	insrec += fhash + "," + fsize + "," + str(fstat.st_mtime) + ")"
	insrec += " RETURNING frecid;"
	cursor.execute(insrec)

	# We could get the rowid from the cursor.lastrowid
	# but RETURNING gives me warm fuzzies.
	# rowid = cursor.lastrowid
	(rowid,) = cursor.fetchone()

	# Save (commit) the changes
	conn.commit()

	return rowid

# Record date of witnessing
def witness_date(fileid) :
	# Get the current time, right now.
	now = datetime.now()
	# insrec =  "," + str(now.timestamp()) + ");"

# Be a witness to the existence of a file.
#
# Arguments:
#   conn the sqlite3 connection
#   fullname: the full file pathname
#   domain: the hostname
def file_witness(conn, domain, fullname):
	frecid = get_file_record(conn, domain, fullname)
	print("yo freci ", frecid)
	witness_date(frecid)


conn = sqlite3.connect('file-witness.db')

r = file_witness(conn, "funny", "/tmp/xxx")
r = file_witness(conn, "funny", "/tmp/zzz")

# Close the connection
conn.close()

