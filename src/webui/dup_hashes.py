#
# dup_hashes.py
#
# Do flask rendering to show distinct file records having the same
# content hash.
#

from flask import render_template
from flask_table import Table, Col, DatetimeCol

# The dot in front of the name searches the current dir.
from .utils import prthash
from .query import find_duplicated_hashes, find_filehash_details

# ---------------------------------------------------------------------

# Declare table header
class DupeHashTable(Table):
	row = Col('')
	hash = Col('xxHash')
	count = Col('Count')
	host = Col('Domain')
	path = Col('Path')
	name = Col('Name')
	size = Col('Size (bytes)')
	date = DatetimeCol('Last modified')

# Find duplicated filenames
def show_dup_hashes():
	qresult = find_duplicated_hashes()

	itemcount = 0
	rowlist = []
	for rec in qresult:
		# Ugly API: columns according to SQL query.  The columns are:
		# filexxh, COUNT(*)

		# We use this to construct a second query, for all files with
		# a given hash.
		first = True
		fresult = find_filehash_details(rec[0])
		for fi in fresult:
			itemcount += 1
			if first:
				first = False
				# columns are protocol, domain, filepath, filename, filesize, filecreate, filexxh, frecid
				rowlist.append(dict(row=itemcount, hash=prthash(rec[0]), count=rec[1],
					host=fi[1], path=fi[2], name=fi[3], size=fi[4], date=fi[5]))
			else :
				rowlist.append(dict(row=itemcount, hash='', count='',
					host=fi[1], path=fi[2], name=fi[3], size=fi[4], date=fi[5]))


	ftable = DupeHashTable(rowlist)
	return render_template("dup-hash-list.html", itemcount=itemcount, filetable=ftable)
