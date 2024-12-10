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
	SummaryTable.add_column('row', Col(''))
	SummaryTable.add_column('domain', Col('Domain'))
	SummaryTable.add_column('filepath', Col('Path'))
	# SummaryTable.add_column('common', Col('Files in common'))
	# SummaryTable.add_column('numfiles', Col('Tot files'))
	# SummaryTable.add_column('overlapstr', Col('% common'))
	SummaryTable.add_column('ratio', Col('Common ratio'))

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
	commoncount = 0;
	for hash in hashset:
		difro = {}
		difro['filexxh'] = hash
		difro['hashstr'] = prthash(hash)

		# Each dir either has a file with that hash, or not.
		# If it does, report the filename.
		same_everywhere = True
		for pa in dirlist:
			dentry = select_filerecords(filepath=pa['filepath'],
				domain=pa['domain'], filexxh=hash)
			defile = dentry.fetchone()
			key = 'filename' + pa['row']
			if defile :
				difro[key] = defile['filename']
			else :
				difro[key] = '-'
				same_everywhere = False

		# Increment commonality count, if the hash is found in all
		# the different paths
		if same_everywhere :
			commoncount += 1

		filist.append(difro)

	# Generate a detailed report of how the directories dffer
	diff_table = DiffTable(filist)

	# Generate a summary report
	for pa in dirlist:
		pa['common'] = commoncount
		overlap = commoncount / pa['numfiles']
		pa['overlap'] = overlap
		overlapstr = str(int (1000.0 * overlap) / 10.0) + " %"
		pa['overlapstr'] = overlapstr
		pa['ratio'] = str(commoncount) + " / " + str(pa['numfiles']) \
			+ " = " + overlapstr

	summary_table = SummaryTable(dirlist)

	return render_template("similar-dirs.html", xxhash=filehash,
		dirtable=dirtable, difftable=diff_table, summarytable=summary_table)

# ------------------ End of File. That's all, folks! ----------------------
# -------------------------------------------------------------------------
