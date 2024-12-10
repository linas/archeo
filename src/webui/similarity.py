#
# similarity.py
#
# Do flask rendering to show directories with similar content.
#

from .query import select_filerecords
from .utils import prthash, to_sint64

from flask import render_template
from flask_table import Table, Col, DatetimeCol, create_table

# General plan:
# -- Given a hash, find all files having that hash.
# -- Find parent directories of these files.
# -- Look at other files in the parent dirs, and see what fraction
#    the files in there have the same hash. Count.

# Declare table header
class DirTable(Table):
	row = Col('')
	domain = Col('Domain')
	filepath = Col('Path')
	filename = Col('Name')
	filesize = Col('Size (bytes)')
	filecreate = DatetimeCol('Last modified')

# -------------------------------------------------------------------------

# Compare contents of filepaths having at least one file with shared
# content.
#
# The argument is the string that came on the URL GET. It is the hash
# to explore, printed with a leading 0x and is unsigned.
def compare_contents(filehash) :

	# Convert string hash to what sqlite wants.
	uxhash = int(filehash, 16)
	sxhash = to_sint64(uxhash)

	# filerecord column names are
	# protocol, domain, filepath, filename, filesize, filecreate, filexxh, frecid

	# Gather a list of directories in which the hash appears
	qpaths = select_filerecords(filexxh=sxhash)
	dircount = 0
	dirlist = []
	for pa in qpaths:
		dircount += 1
		loc = dict(pa)
		loc['row'] = str(dircount)
		dirlist.append(loc)

	# Report on the one hash, as it appears in the differnt locations.
	dirtable = DirTable(dirlist)

	# Create the summarization table.
	SummaryTable = create_table('boffa')
	SummaryTable.add_column('domain', Col('Domain'))
	SummaryTable.add_column('filepath', Col('Path'))
	SummaryTable.add_column('numfiles', Col('Number of files'))

	# Create a variable-width table.
	DiffTable = create_table('foobar')
	DiffTable.add_column('hashstr', Col('Hash'))
	for pa in dirlist:
		fname = 'filename' + pa['row']
		ftitle = 'Name in ' + pa['row']
		DiffTable.add_column(fname, Col(ftitle))

	# Gather a set of all filehashes that appear in all dirs
	hashset = set()
	for pa in dirlist:
		dentries = select_filerecords(filepath=pa['filepath'], domain=pa['domain'])
		filecount = 0;
		for dentry in dentries:
			filecount += 1
			hashset.add(dentry['filexxh'])
		pa['numfiles'] = filecount

	# Gather names of the files for each hash
	filist = []
	for hash in hashset:
		difro = {}
		difro['filexxh'] = hash
		difro['hashstr'] = prthash(hash)

		# Each dir either has a file with that hash, or not.
		# If it does, report the filename.
		for pa in dirlist:
			dentry = select_filerecords(filepath=pa['filepath'],
				domain=pa['domain'], filexxh=hash)
			defile = dentry.fetchone()
			key = 'filename' + pa['row']
			if defile :
				difro[key] = defile['filename']
			else :
				difro[key] = '-'

		filist.append(difro)

	diff_table = DiffTable(filist)

	summary_table = SummaryTable(dirlist)

	return render_template("similar-dirs.html", xxhash=filehash,
		dirtable=dirtable, difftable=diff_table, summarytable=summary_table)

# ------------------ End of File. That's all, folks! ----------------------
# -------------------------------------------------------------------------
