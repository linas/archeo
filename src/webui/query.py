#
# query.py
#
# Database query shim for the webui for Archeo.

import sqlite3

# -------------------------------------------------------------------------
#
# DB connection as global. This should be a per-thread global,
# but punting on this for now.
#
# This should behave like a closure, but I don't know how to do a
# clusure in python, yet.
global conn;

def query_db_open(dbname):
	global conn
	conn = sqlite3.connect(dbname)

def query_db_close():
	global conn
	conn.close()

# -------------------------------------------------------------------------

# Return a list of duplicted filenames.
# This is fairly normal: the same filename may be used in many places
def find_duplicated_names() :

	# Create a new cursor. Not very efficient but so what.
	cursor = conn.cursor()
	sel = "SELECT filename, frecid, COUNT(*) FROM FileRecord GROUP BY filename HAVING COUNT(*) > 1;"
	return cursor.execute(sel)

# -------------------------------------------------------------------------

# Return filename details
def find_filename_details(filename) :
	cursor = conn.cursor()
	sel = "SELECT domain, filepath, filesize, filecreate, filexxh, frecid, protocol "
	sel += "FROM FileRecord WHERE filename='" + filename + "';"
	return cursor.execute(sel)
