#
# dup_hashes.py
#
# Do flask rendering to show distinct file records having the same
# content hash.
#

from flask import render_template
from flask_table import Table, Col, DatetimeCol, LinkCol

# The dot in front of the name searches the current dir.
from .property_listing import item_collection

# ---------------------------------------------------------------------

# Declare table header
class DupeHashTable(Table):
	row = Col('')
#	hashstr = Col('xxHash')
	hashstr = LinkCol('xxHash', attr='hashstr', endpoint='directory_detail',
		url_kwargs=dict(hashstr='hashstr'))
	count = Col('Count')
#	url = Col('URL')
#	domain = Col('Domain')
#	filepath = Col('Path')
	filepath = LinkCol('Path', attr='filepath', endpoint='path_detail',
		url_kwargs=dict(filepath='filepath'))
#	filename = Col('Name')
	filename = LinkCol('Name', attr='filename', endpoint='filename_detail',
		url_kwargs=dict(filename='filename'))
	filesize = Col('Size (bytes)')
	filedate = DatetimeCol('Last modified')

# Find duplicated hashes
def show_dup_hashes():

	itco = item_collection()
	rowlist = itco.build_duplicates('hashstr', 2)

	ftable = DupeHashTable(rowlist)
	return render_template("dup-hash-list.html", itemcount=itco.itemcount, filetable=ftable)
