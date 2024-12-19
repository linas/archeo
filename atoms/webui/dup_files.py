#
# dup_files.py
#
# Do flask rendering to show duplicated files.
#

from flask import render_template
from flask_table import Table, Col, DatetimeCol, LinkCol

# The dot in front of the name searches the current dir.
from .property_listing import build_duplicates

# ---------------------------------------------------------------------

# Declare table header
class DupeFileTable(Table):
	row = Col('')
	# endpoint must be the name of a flask function that already exists
	# and is associated to a given URL. The kwargs are passed as a GET
	# param (which just repeats the filename). The attr MUST name an
	# item in the row dictionary. It is the string that will be displayed
	# in the generated `a href` link.
	filename = LinkCol('File Name', attr='filename', endpoint='filename_detail',
		url_kwargs=dict(filename='filename'))
	count = Col('Count')
#	hashstr = Col('xxHash')
	hashstr = LinkCol('xxHash', attr='hashstr', endpoint='directory_detail',
		url_kwargs=dict(hashstr='hashstr'))
#	url = Col('URL')
#	domain = Col('Domain')
#	filepath = Col('Path')
	filepath = LinkCol('Path', attr='filepath', endpoint='directory_detail',
		url_kwargs=dict(filepath='filepath'))
	filesize = Col('Size (bytes)')
	filedate = DatetimeCol('Last modified')

# Find duplicated filenames
def show_dup_files():

	rowlist = build_duplicates('filename', 2)
	ftable = DupeFileTable(rowlist)
	return render_template("file-list.html", filecount=itemcount, filetable=ftable)
