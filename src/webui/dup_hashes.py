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
from .query import find_duplicated_hashes

# ---------------------------------------------------------------------

# Declare table header
class DupeHashTable(Table):
	row = Col('')
	hash = Col('xxHash')
	count = Col('Count')

# Find duplicated filenames
def show_dup_hashes():
	qresult = find_duplicated_hashes()

	itemcount = 0
	filelist = []
	for rec in qresult:
		itemcount += 1
		# Ugly API: columns according to SQL query.  The columns are:
		# filexxh, COUNT(*)
		filelist.append(dict(row=itemcount, hash=prthash(rec[0]), count=rec[1]))

	ftable = DupeHashTable(filelist)
	return render_template("dup-hash-list.html", itemcount=itemcount, filetable=ftable)
