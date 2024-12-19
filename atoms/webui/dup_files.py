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

# Show duplicated items.
# First argument: the property that is duplicated
# Secnd argument: min number of duplications to rise above.
def show_duplicates(property, min_num_dups):

	dup_items = find_duplicates(property, min_num_dups)

	itemcount = 0
	rowlist = []
	for item in dup_items:
		itemcount += 1

		# We use this to construct a second query, for all files with
		# a given hash. Returned columns ar properties associated with
		# that hash, including url, filesize, filedate
		first = True
		fresult = get_fileinfo_from_keywords(filename=item)
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

# Find duplicated filenames
def show_dup_files():

	return show_duplicates('filename', 2)
