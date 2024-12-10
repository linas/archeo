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
# SQL table column names are
# protocol, domain, filepath, filename, filesize, filecreate, filexxh, frecid
class FilenameDetailsTable(Table):
	row = Col('')
	domain = Col('Domain')
	filepath = Col('File path')
	filesize = Col('Size (bytes)')
	filecreate = DatetimeCol('Last modified')
	frecid = Col('Record ID')
	hash = Col('xxHash')

# Find duplicated filenames
def show_filename_details(filename):
	qresult = select_filerecords(filename=filename)

	rowcount = 0
	filelist = []
	for rec in qresult:
		row = dict(rec)
		rowcount += 1
		row['row'] = rowcount
		row['hash'] = prthash(rec['filexxh'])
		filelist.append(row)

	ftable = FilenameDetailsTable(filelist)
	return render_template("filename-details.html", filename=filename,
		recordcount=rowcount, filetable=ftable)
