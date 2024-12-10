#
# dup_hashes.py
#
# Do flask rendering to show distinct file records having the same
# content hash.
#

from flask import render_template
from flask_table import Table, Col, LinkCol

# The dot in front of the name searches the current dir.
from .query import find_duplicated_hashes

# ---------------------------------------------------------------------

# Declare table header
class DupeHashTable(Table):
	row = Col('')
	# endpoint must be the name of a flask function that already exists
	# and is associated to a given URL. The kwargs are passed as a GET
	# param (which just repeats the filename). The attr MUST name an
	# item in the row dictionary. It is the string that will be displayed
	# in the generated `a href` link.
	name = LinkCol('File Name', attr='name', endpoint='filename_detail',
		url_kwargs=dict(filename='name'))
	count = Col('Count')

# Find duplicated filenames
def show_dup_hashes():
	qresult = find_duplicated_hashes()

	itemcount = 0
	filelist = []
	for rec in qresult:
		itemcount += 1
		# Ugly API: columns according to SQL query.  The columns are:
		# protocol, domain, filepath, filename, filesize, filecreate, frecid, COUNT(*)
		fname = rec[3]
		filelist.append(dict(row=itemcount, name=fname, count=rec[7]))

	ftable = DupeHashTable(filelist)
	return render_template("dup-hash-list.html", itemcount=itemcount, filetable=ftable)
