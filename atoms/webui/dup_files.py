#
# dup_files.py
#
# Do flask rendering to show duplicated files.
#

from flask import render_template
from flask_table import Table, Col, LinkCol

# The dot in front of the name searches the current dir.
from .query import find_duplicates

# ---------------------------------------------------------------------

# Declare table header
class DupeTable(Table):
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
def show_dup_files():
	qresult = find_duplicates('filename', 2)

	filecount = 0
	filelist = []
	for fname in qresult:
		filecount += 1
		filelist.append(dict(row=filecount, name=fname, count=333))

	ftable = DupeTable(filelist)
	return render_template("file-list.html", filecount=filecount, filetable=ftable)
