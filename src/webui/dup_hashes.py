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
	hash = LinkCol('xxHash', attr='hashstr', endpoint='path_similarity',
      url_kwargs=dict(signedhash='xxhash'))
	count = Col('Count')
	domain = Col('Domain')
	filepath = Col('Path')
	filename = Col('Name')
	filesize = Col('Size (bytes)')
	filecreate = DatetimeCol('Last modified')

# Find duplicated filenames
def show_dup_hashes():
	qresult = find_duplicated_hashes()

	itemcount = 0
	rowlist = []
	for rec in qresult:
		# Ugly API: columns according to SQL query.  The columns are:
		# filexxh, COUNT(*)

		# We use this to construct a second query, for all files with
		# a given hash. Returned columns are
		# protocol, domain, filepath, filename, filesize, filecreate, filexxh, frecid
		first = True
		fresult = select_filerecords(filexxh=rec['filexxh'])
		for fi in fresult:
			itemcount += 1
			frow = dict(fi)
			frow['row'] = itemcount
			if first:
				first = False
				# prthash is used for display on the web page and is
				# subject to change. The hex conversion is used in the
				# link URL GET method and must be decodable at the other
				# end, and thus must not change on a whim.
				frow['xxhash'] = hex(to_uint64(rec[0]))
				frow['hashstr'] = prthash(rec[0])
				frow['count'] = rec[1]
			else :
				frow['xxhash'] = ''
				frow['hashstr'] = ''
				frow['count'] = ''

			rowlist.append(frow)

		# Blank line. Maybe there's some prettier way; I can't be bothered.
		rowlist.append(dict(row='', xxhash = '', hashstr='', count='',
			domain='', filepath='', filename='', filesize='', filecreate=''))


	ftable = DupeHashTable(rowlist)
	return render_template("dup-hash-list.html", itemcount=itemcount, filetable=ftable)
