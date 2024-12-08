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
def find_witness(conn, domain, filepath, filename, fhash, fsize) :
	return 0


# Be a witness to the existence of a file.
#
# Arguments:
#   conn the sqlite3 connection
#   fullname: the full file pathname
#   domain: the hostname
def file_witness(conn, domain, fullname):

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
	find_witness(conn, domain, filepath, filename, fhash, fsize)

	# Create a new cursor. Not very efficient but so what.
	cursor = conn.cursor()

	# Stuff a bunch of data into the DB
	insrec = "INSERT INTO FileRecord(filename, filepath, domain, filexxh, filesize, filecreate) VALUES "
	insrec += "('" + filename + "','" + filepath + "','" + domain + "',"
	insrec += fhash + "," + fsize + "," + str(fstat.st_mtime) + ");"
	cursor.execute(insrec)
	rowid = cursor.lastrowid

	# Save (commit) the changes
	conn.commit()

	return rowid

# Record date of witnessing
def witness_date(fileid) :
	# Get the current time, right now.
	now = datetime.now()
	# insrec =  "," + str(now.timestamp()) + ");"


conn = sqlite3.connect('file-witness.db')

r = file_witness(conn, "funny", "/tmp/xxx")
print("yo insert " + str(r))
r = file_witness(conn, "funny", "/tmp/zzz")
print("yo insert " + str(r))

# Close the connection
conn.close()

