#
# query.py
#
# Database query shim for the webui for Archeo.

import sqlite3
# from .utils import to_sint64

# -------------------------------------------------------------------------
#
# DB connection as global. This should be a per-thread global,
# but punting on this for now.
#
# This should behave like a closure, but I don't know how to do a
# closure in python, yet.
global conn;

def query_db_open(dbname):
	global conn
	conn = sqlite3.connect(dbname)
	# The row factory allows access to query results by column name.
	conn.row_factory = sqlite3.Row

def query_db_close():
	global conn
	conn.close()

# -------------------------------------------------------------------------

# Return a list of duplicated filenames.
# This is fairly normal: the same filename may be used in many places
def find_duplicated_names() :
	cursor = conn.cursor()
	sel = "SELECT filename, frecid, COUNT(*) FROM FileRecord GROUP BY filename HAVING COUNT(*) > 1;"
	return cursor.execute(sel)

# -------------------------------------------------------------------------

# Return a list of duplicated hashes.
# This is fairly normal: the same file contents, different locations/names
def find_duplicated_hashes() :
	cursor = conn.cursor()
	sel = "SELECT filexxh, COUNT(*) FROM FileRecord GROUP BY filexxh HAVING COUNT(*) > 1;"
	return cursor.execute(sel)

# -------------------------------------------------------------------------

# Generic select on the FileRecord table.
# Example usage:
#   select_filerecords(domain='foo', filepath='/bar/baz')
# Creates query
#   SELECT * FROM FileRecord WHERE domain='foo' AND filepath='/bar/baz';
#
def select_filerecords(**kwargs) :
	cursor = conn.cursor()
	sel = "SELECT * FROM FileRecord WHERE "
	more = False
	vlist = []
	for k,v in kwargs.items():
		if more :
			sel += " AND "
		sel += k + " =? "
		more = True;
		vlist.append(v)
	sel += ";"
	return cursor.execute(sel, vlist)

# ------------------ End of File. That's all, folks! ----------------------
# -------------------------------------------------------------------------
