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
