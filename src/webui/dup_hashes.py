#
# dup_hashes.py
#
# Do flask rendering to show distinct file records having the same
# content hash.
#

from flask import render_template
from flask_table import Table, Col, LinkCol

# The dot in front of the name searches the current dir.
from .utils import prthash
from .query import find_duplicated_hashes, find_filehash_details

# ---------------------------------------------------------------------

# Declare table header
class DupeHashTable(Table):
	row = Col('')
	hash = Col('xxHash')
	count = Col('Count')
	name = Col('Name')

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
				rowlist.append(dict(row=itemcount, hash=prthash(rec[0]), count=rec[1], name=fi[3]))
			else :
				rowlist.append(dict(row=itemcount, hash='', count='', name=fi[3]))


	ftable = DupeHashTable(rowlist)
	return render_template("dup-hash-list.html", itemcount=itemcount, filetable=ftable)
