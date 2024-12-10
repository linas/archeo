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
	dirtable = DirTable(dirlist)

	# Create a variable-width table.
	DiffTable = create_table('foobar')
	DiffTable.add_column('filexxh', Col('Hash'))
	for pa in dirlist:
		fname = 'filename' + pa['row']
		ftitle = 'Name in ' + pa['row']
		DiffTable.add_column(fname, Col(ftitle))

	# Gather a set of all filehashes that appear in all dirs
	hashset = set()
	for pa in dirlist:
		dentries = select_filerecords(filepath=pa['filepath'], domain=pa['domain'])
		for dentry in dentries:
			hashset.add(dentry['filexxh'])

	# Gather names of the files for each hash
	filist = []
	for hash in hashset:
		difro = {}
		difro['filexxh'] = hash

		for pa in dirlist:
			dentry = select_filerecords(filepath=pa['filepath'],
				domain=pa['domain'], filexxh=hash)
			print("yoo ", dentry.fetchone())

		difro['filename1'] = 'asf'
		difro['filename2'] = 'ert'
		filist.append(difro)

	diff_table = DiffTable(filist)

	return render_template("similar-dirs.html", xxhash=filehash,
		dirtable=dirtable, difftable=diff_table)

# ------------------ End of File. That's all, folks! ----------------------
# -------------------------------------------------------------------------
