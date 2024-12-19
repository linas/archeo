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

# Build a list of duplicated items.
# First argument: the property that is duplicated
# Second argument: min number of duplications to rise above.
#
# Returned value: a list of items having that duplicated property.
# The returned list contains a complete description of the item, in the
# form of a dictionary with the item properties in the dict.
# That is, the returned value is a list of dictionaries.
#
# This is a query shim, translating the result of queries to the
# AtomSpace, into python dicts that python API's are expecting to get.
#
def build_duplicates(property, min_num_dups):

	dup_items = find_duplicates(property, min_num_dups)

	itemcount = 0
	rowlist = []
	for item in dup_items:
		itemcount += 1

		# We use this to construct a second query, for all files with
		# a given hash. Returned columns ar properties associated with
		# that hash, including url, filesize, filedate
		first = True
		fresult = get_fileinfo_from_keywords(**{property:item})
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
		# viz. There needs to be a CSS for the displayed table, indicating
		# a grouping break. Not sure how to convey this grouping.
		rowlist.append(dict(row='', hashstr='', count='', url='',
			domain='', filepath='', filename='', filesize='', filedate=''))

	return rowlist

# Find duplicated filenames
def show_dup_files():

	rowlist = build_duplicates('filename', 2)
	ftable = DupeFileTable(rowlist)
	return render_template("file-list.html", filecount=itemcount, filetable=ftable)
