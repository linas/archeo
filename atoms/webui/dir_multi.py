#
# dir_multi.py
#
# Do flask rendering to show multiple directories, each having
# at least one file in common.
#

from .query import select_filerecords
from .utils import prthash, to_sint64, to_uint64

from flask import render_template
from flask_table import Table, Col, DatetimeCol, LinkCol, create_table

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
	filename = LinkCol('Name', attr='filename', endpoint='filename_detail',
		url_kwargs=dict(filename='filename'))
	filesize = Col('Size (bytes)')
	filecreate = DatetimeCol('Last modified')

# -------------------------------------------------------------------------

# Compare contents of filepaths having at least one file with shared
# content.
#
# The first arg is the signed in hash for which the listing is being
# expanded on. The second are is the reqult of the DB query, containing
# a collection of directories in which this hash appears
def show_multi_dir(sxhash, qpaths) :

	# Stash the list of directories. We'll walk this list repeatedly.
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
	# SummaryTable.add_column('numunique', Col('Tot unique hashes'))
	# SummaryTable.add_column('overlapstr', Col('% common'))
	SummaryTable.add_column('ratio', Col('Common ratio'))

	# Create a variable-width table.
	DiffTable = create_table('foobar')
	DiffTable.add_column('row', Col(''))
	DiffTable.add_column('hashstr', LinkCol('xxHash', attr='hashstr',
		endpoint='directory_detail',
		url_kwargs=dict(signedhash='xxhash')))

	for pa in dirlist:
		fname = 'filename' + pa['row']
		ftitle = 'Name in ' + pa['row']
		DiffTable.add_column(fname,
			LinkCol(ftitle, attr=fname, endpoint='filename_detail',
				url_kwargs=dict(filename=fname)))

	# Gather a set of all filehashes that appear in all dirs
	hashset = set()
	for pa in dirlist:
		dentries = select_filerecords(filepath=pa['filepath'], domain=pa['domain'])
		hlocal = set()
		for dentry in dentries:
			hashset.add(dentry['filexxh'])
			hlocal.add(dentry['filexxh'])

		# How many of these files are unique?
		pa['numunique'] = len(hlocal)

	# Gather names of the files for each hash
	filist = []
	commoncount = 0;
	totcount = 0;
	for hash in hashset:
		totcount += 1
		difro = {}
		difro['row'] = totcount

		# prthash is used for display on the web page and is
		# subject to change. The hex conversion is used in the
		# link URL GET method and must be decodable at the other
		# end, and thus must not change on a whim. And the
		# straight-up hash is needed for SQL queries.
		difro['filexxh'] = hash
		difro['hashstr'] = prthash(hash)
		difro['xxhash'] = hex(to_uint64(hash))

		# Each dir either has one or more files with that hash,
		# or none. Report all files having the same hash.
		same_everywhere = True
		maxfiles = 0
		for pa in dirlist:
			dentry = select_filerecords(filepath=pa['filepath'],
				domain=pa['domain'], filexxh=hash)
			allfiles = dentry.fetchall()
			nfiles = len(allfiles)
			if maxfiles < nfiles:
				maxfiles = nfiles;

			key = 'filename' + pa['row']
			if 0 < nfiles :
				difro[key] = allfiles[0]['filename']
			else :
				difro[key] = ''
				same_everywhere = False

		# Increment commonality count, if the hash is found in all
		# the different paths
		if same_everywhere :
			commoncount += 1

		filist.append(difro)

		# One (or more) of the directories have more than one
		# file with the given hash. Report these on distinct rows.
		# Blank out the hash to avoid clutter.
		for idx in range (1, maxfiles) :
			difro = {}
			difro['row'] = ''
			difro['hashstr'] = ''
			difro['xxhash'] = ''

			# We could save the query results above, or we can just
			# rerun the query. I'm lazy, the performance hit is tiny.
			# Just rerun the query. Pick up where we left off.
			for pa in dirlist:
				dentry = select_filerecords(filepath=pa['filepath'],
					domain=pa['domain'], filexxh=hash)
				allfiles = dentry.fetchall()
				nfiles = len(allfiles)
				key = 'filename' + pa['row']
				if idx < nfiles :
					difro[key] = allfiles[idx]['filename']
				else :
					difro[key] = '-'

			# Add this to the list
			filist.append(difro)

	# Generate a detailed report of how the directories dffer
	diff_table = DiffTable(filist)

	# Generate a summary report
	for pa in dirlist:
		pa['common'] = commoncount
		overlap = commoncount / pa['numunique']
		pa['overlap'] = overlap
		overlapstr = str(int (1000.0 * overlap) / 10.0) + " %"
		pa['overlapstr'] = overlapstr
		pa['ratio'] = str(commoncount) + " / " + str(pa['numunique']) \
			+ " = " + overlapstr

	summary_table = SummaryTable(dirlist)

	return render_template("similar-dirs.html", hashstr=prthash(sxhash),
		dirtable=dirtable, difftable=diff_table, summarytable=summary_table)

# ------------------ End of File. That's all, folks! ----------------------
# -------------------------------------------------------------------------
