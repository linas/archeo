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
from .query import find_duplicated_hashes, find_filehash_details

# ---------------------------------------------------------------------

# Declare table header
class DupeHashTable(Table):
	row = Col('')
	hash = LinkCol('xxHash', attr='hashstr', endpoint='path_similarity',
      url_kwargs=dict(signedhash='xxhash'))
	count = Col('Count')
	host = Col('Domain')
	path = Col('Path')
	name = Col('Name')
	size = Col('Size (bytes)')
	date = DatetimeCol('Last modified')

# Find duplicated filenames
def show_dup_hashes():
	qresult = find_duplicated_hashes()

	itemcount = 0
	rowlist = []
	for rec in qresult:
		# Ugly API: columns according to SQL query.  The columns are:
		# filexxh, COUNT(*)

		# We use this to construct a second query, for all files with
		# a given hash.
		first = True
		fresult = find_filehash_details(rec[0])
		for fi in fresult:
			itemcount += 1
			if first:
				first = False
				# columns are protocol, domain, filepath, filename, filesize, filecreate, filexxh, frecid
				rowlist.append(dict(row=itemcount,
					# prthash is used for display on the web page and is
					# subject to change. The hex conversion is used in the
					# link URL GET method and must be decodable at the other
					# end, and thus must not change on a whim.
					xxhash = hex(to_uint64(rec[0])),
					hashstr=prthash(rec[0]), count=rec[1],
					host=fi[1], path=fi[2], name=fi[3], size=fi[4], date=fi[5]))
			else :
				rowlist.append(dict(row=itemcount, xxhash = '', hashstr='', count='',
					host=fi[1], path=fi[2], name=fi[3], size=fi[4], date=fi[5]))

		# Blank line. Maybe there's some prettier way; I cna't be bothered.
		rowlist.append(dict(row='', xxhash = '', hashstr='', count='',
			host='', path='', name='', size='', date=''))


	ftable = DupeHashTable(rowlist)
	return render_template("dup-hash-list.html", itemcount=itemcount, filetable=ftable)
