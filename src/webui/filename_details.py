#
# filename_details.py
#
# Do flask rendering to show details of a single duplicated filename
#

from flask import render_template
from flask_table import Table, Col, DatetimeCol

# The dot in front of the name searches the current dir.
from .utils import prthash
from .query import select_filerecords

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
	qresult = select_filerecords(filename=filename)

	# Available columns are
	# protocol, domain, filepath, filename, filesize, filecreate, filexxh, frecid
	rowcount = 0
	filelist = []
	for rec in qresult:
		rowcount += 1
		filelist.append(dict(row=rowcount, host=rec['domain'], path=rec['filepath'],
			size=rec['filesize'], date=rec['filecreate'], hash=prthash(rec['filexxh']),
			frecid=rec['frecid']))

	ftable = FilenameDetailsTable(filelist)
	return render_template("filename-details.html", filename=filename,
		recordcount=rowcount, filetable=ftable)
