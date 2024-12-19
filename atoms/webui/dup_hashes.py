#
# dup_hashes.py
#
# Do flask rendering to show distinct file records having the same
# content hash.
#

from flask import render_template
from flask_table import Table, Col, DatetimeCol, LinkCol

# The dot in front of the name searches the current dir.
from .query import find_duplicates, get_fileinfo_from_keywords

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
	filepath = LinkCol('Path', attr='filepath', endpoint='directory_detail',
		url_kwargs=dict(filepath='filepath'))
#	filename = Col('Name')
	filename = LinkCol('Name', attr='filename', endpoint='filename_detail',
		url_kwargs=dict(filename='filename'))
	filesize = Col('Size (bytes)')
	filedate = DatetimeCol('Last modified')

# Find duplicated hashes
def show_dup_hashes():

	# argument is min number of dupes.
	dup_hashes = find_duplicates('hashstr', 2)

	itemcount = 0
	rowlist = []
	for hashstr in dup_hashes:

		# We use this to construct a second query, for all files with
		# a given hash. Returned columns ar properties associated with
		# that hash, including url, filesize, filedate
		first = True
		fresult = get_fileinfo_from_keywords(hashstr=hashstr)
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

	#if 0 == itemcount :
	#	rowlist.append(dict(row='', hashstr='', count='', url='',
	#		domain='', filepath='', filename='', filesize='', filedate=''))

	ftable = DupeHashTable(rowlist)
	return render_template("dup-hash-list.html", itemcount=itemcount, filetable=ftable)
