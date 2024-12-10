#
# filename_details.py
#
# Do flask rendering to show details of a single duplicated filename
#

from flask import render_template
from flask_table import Table, Col, DatetimeCol

# The dot in front of the name searches the current dir.
from .utils import prthash
from .query import find_filename_details

# ---------------------------------------------------------------------

# Declare table header
class FilenameDetailsTable(Table):
	row = Col('')
	host = Col('Domain')
	path = Col('File path')
	size = Col('Size (bytes)')
	date = DatetimeCol('Last modified')
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
		# protocol, domain, filepath, filename, filesize, filecreate, filexxh, frecid
		filelist.append(dict(row=rowcount, host=rec[1], path=rec[2],
			size=rec[4], date=rec[5], hash=prthash(rec[6]), frecid=rec[7]))

	ftable = FilenameDetailsTable(filelist)
	return render_template("filename-details.html", filename=filename,
		recordcount=rowcount, filetable=ftable)
