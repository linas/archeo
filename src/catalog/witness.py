#! /usr/bin/env python3
#
# witness.py
#
# Witness, aka record the presence of a file in the filesystem.
#

from datetime import datetime
import sqlite3

def file_witness(conn, filename):
	cursor = conn.cursor()
	now = datetime.now()
	print("it is now ", now)
	cursor.execute("INSERT INTO FileRecord(filename, filepath, domain, filesize, filecreate, recordcreate) VALUES ('somefile','/wher/ever','fanny',42,43,44);")

	# Save (commit) the changes
	conn.commit()

conn = sqlite3.connect('file-witness.db')

file_witness(conn, "foobar")

# Close the connection
conn.close()

