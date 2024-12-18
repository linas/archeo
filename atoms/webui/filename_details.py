#
# filename_details.py
#
# Do flask rendering to show details of a single duplicated filename
#

from flask import render_template
from flask_table import Table, Col, DatetimeCol, LinkCol

# The dot in front of the name searches the current dir.
from .utils import prthash, to_uint64
from .query import select_filerecords

# ---------------------------------------------------------------------

# Declare table header
# Available properties:
# protocol, domain, filepath, filename, filesize, filedate, hashstr
class FilenameDetailsTable(Table):
	row = Col('')
	hash = LinkCol('xxHash', attr='hashstr', endpoint='directory_detail',
      url_kwargs=dict(hashstr='hashstr'))
	domain = Col('Domain')
	filepath = Col('File path')
	filesize = Col('Size (bytes)')
	filedate = DatetimeCol('Last modified')

# Find duplicated filenames
def show_filename_details(filename):
	qresult = select_filerecords(filename=filename)

	print("file sres", qresult)

	rowcount = 0
	filelist = []
	for row in qresult:
		rowcount += 1
		row['row'] = rowcount

		filelist.append(row)

	ftable = FilenameDetailsTable(filelist)
	return render_template("filename-details.html", filename=filename,
		recordcount=rowcount, filetable=ftable)
