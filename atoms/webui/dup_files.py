#
# dup_files.py
#
# Do flask rendering to show duplicated files.
#

from flask import render_template
from flask_table import Table, Col, DatetimeCol, LinkCol

# The dot in front of the name searches the current dir.
from .query import find_duplicates, get_fileinfo_from_keywords

# ---------------------------------------------------------------------

# Declare table header
class DupeFileTable(Table):
	row = Col('')
	# endpoint must be the name of a flask function that already exists
	# and is associated to a given URL. The kwargs are passed as a GET
	# param (which just repeats the filename). The attr MUST name an
	# item in the row dictionary. It is the string that will be displayed
	# in the generated `a href` link.
	name = LinkCol('File Name', attr='name', endpoint='filename_detail',
		url_kwargs=dict(filename='name'))
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

	# argument is min number of dupes.
	dup_files = find_duplicates('filename', 2)

	itemcount = 0
	rowlist = []
	for fname in dup_files:
		itemcount += 1

		# We use this to construct a second query, for all files with
		# a given hash. Returned columns ar properties associated with
		# that hash, including url, filesize, filedate
		first = True
		fresult = get_fileinfo_from_keywords(filename=fname)
		for frow in fresult:
			itemcount += 1
			frow['row'] = itemcount
			if first:
				first = False
			else :
				frow['hashstr'] = ''
				frow['count'] = ''

			rowlist.append(frow)

		# Blank line. Maybe there's some prettier way; I can't be bothered.
		rowlist.append(dict(row='', hashstr='', count='', url='',
			domain='', filepath='', filename='', filesize='', filedate=''))

	ftable = DupeFileTable(rowlist)
	return render_template("file-list.html", filecount=itemcount, filetable=ftable)
