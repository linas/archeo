#! /usr/bin/env python3
#
# witness.py
#
# Witness, aka record the presence of a file in the filesystem.
#

from datetime import datetime
import os
import pathlib
import sqlite3

# Be a witness to the existence of a file.
#
# Arguments:
#   conn the sqlite3 connection
#   fullname: the full file pathname
#   domain: the hostname
def file_witness(conn, domain, fullname):

	# Try to find the file in the filesystem
	fh = pathlib.Path(fullname, follow_symlinks=False)

	# Hmm. Should probably throw an error, here
	if not fh.is_file():
		return False

	print("yo its " + str(fh))

	fstat = fh.stat()
	print("its this " + str(fstat.st_size))
	print("its this " + str(fstat.st_mtime))

	# Split the full filepathname into a filepath and the filename
	(filepath, filename) = os.path.split(fullname)

	# Create a new cursor. Not very efficient but so what.
	cursor = conn.cursor()

	# Get the current time, right now.
	now = datetime.now()
	insrec = "INSERT INTO FileRecord(filename, filepath, domain, filesize, filecreate, recordcreate) VALUES "
	insrec += "('" + filename + "','" + filepath + "','" + domain + "',"
	insrec += str(fstat.st_size) + "," + str(fstat.st_mtime) + "," + str(now.timestamp()) + ");"
	cursor.execute(insrec)

	# Save (commit) the changes
	conn.commit()

conn = sqlite3.connect('file-witness.db')

file_witness(conn, "funny", "/tmp/xxx")

# Close the connection
conn.close()

