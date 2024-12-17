#
# dup_hashes.py
#
# Do flask rendering to show distinct file records having the same
# content hash.
#

from flask import render_template
from flask_table import Table, Col, DatetimeCol, LinkCol

# The dot in front of the name searches the current dir.
from .utils import prthash, to_uint64
from .query import find_duplicated_hashes, select_filerecords

# ---------------------------------------------------------------------

# Declare table header
class DupeHashTable(Table):
	row = Col('')
	hash = LinkCol('xxHash', attr='hashstr', endpoint='directory_detail',
      url_kwargs=dict(signedhash='xxhash'))
	count = Col('Count')
	domain = Col('Domain')
	filepath = Col('Path')
	filename = LinkCol('Name', attr='filename', endpoint='filename_detail',
		url_kwargs=dict(filename='filename'))
	filesize = Col('Size (bytes)')
	filecreate = DatetimeCol('Last modified')

# Find duplicated filenames
def show_dup_hashes():

	# argument is min number of dupes.
	dup_hashes = find_duplicated_hashes(2)

	itemcount = 0
	rowlist = []
	for hashstr in dup_hashes:

		# We use this to construct a second query, for all files with
		# a given hash. Returned columns are
		# URL, filesize, filecreate
		first = True
		fresult = select_filerecords(filexxh=hashstr)
		for frow in fresult:
			itemcount += 1
			frow['row'] = itemcount
			if first:
				first = False
				frow['hashstr'] = hashstr
				frow['count'] = 42
				frow['xxhash'] = 123
			else :
				frow['hashstr'] = ''
				frow['count'] = ''
				frow['xxhash'] = ''

			rowlist.append(frow)

		# Blank line. Maybe there's some prettier way; I can't be bothered.
		rowlist.append(dict(row='', hashstr='', count='', xxhash='',
			domain='', filepath='', filename='', filesize='', filecreate=''))


	ftable = DupeHashTable(rowlist)
	return render_template("dup-hash-list.html", itemcount=itemcount, filetable=ftable)
