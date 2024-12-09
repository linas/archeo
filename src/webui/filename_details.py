#
# filename_details.py
#
# Do flask rendering to show details of a single duplicated filename
#

from flask import render_template
from flask_table import Table, Col, LinkCol

# The dot in front of the name searches the current dir.
from .query import find_filename_details

# ---------------------------------------------------------------------

# Declare table header
class FilenameDetailsTable(Table):
	row = Col('')
	path = Col('File path')
	frecid = Col('Record ID')
	hash = Col('xxHash')

# Find duplicated filenames
def show_filename_details(filename):
	qresult = find_filename_details(filename)

	rowcount = 0
	filelist = []
	for rec in qresult:
		rowcount += 1
		# qresult columns are
		# domain, filepath, filesize, filecreate, filexxh, frecid, protocol

		# SQLite3 has a habit of converting 64-bit hashes into floats.
		# I hae no clue if this corrupts them or not. So what the heck.
		xxhash = rec[4]
		xxhash = int(xxhash)

		filelist.append(dict(row=rowcount, path=rec[1], hash=hex(xxhash), frecid=rec[5]))

	ftable = FilenameDetailsTable(filelist)
	return render_template("filename-details.html", recordcount=rowcount, filetable=ftable)
