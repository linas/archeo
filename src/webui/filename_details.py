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
# SQL table column names are
# protocol, domain, filepath, filename, filesize, filecreate, filexxh, frecid
class FilenameDetailsTable(Table):
	row = Col('')
	hash = LinkCol('xxHash', attr='hashstr', endpoint='directory_detail',
      url_kwargs=dict(signedhash='xxhash'))
	domain = Col('Domain')
	filepath = Col('File path')
	filesize = Col('Size (bytes)')
	filecreate = DatetimeCol('Last modified')
	# frecid = Col('Record ID')

# Find duplicated filenames
def show_filename_details(filename):
	qresult = select_filerecords(filename=filename)

	rowcount = 0
	filelist = []
	for rec in qresult:
		row = dict(rec)
		rowcount += 1
		row['row'] = rowcount

		# prthash is used for display on the web page and is
		# subject to change. The hex conversion is used in the
		# link URL GET method and must be decodable at the other
		# end, and thus must not change on a whim.
		row['hashstr'] = prthash(row['filexxh'])
		row['xxhash'] = hex(to_uint64(row['filexxh']))

		filelist.append(row)

	ftable = FilenameDetailsTable(filelist)
	return render_template("filename-details.html", filename=filename,
		recordcount=rowcount, filetable=ftable)
