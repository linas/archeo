#
# dir_list.py
#
# Do flask rendering to show directory contents.
#

from .query import select_filerecords
from .utils import prthash, to_sint64, to_uint64

from flask import render_template
from flask_table import Table, Col, DatetimeCol, LinkCol, create_table

# General plan:
# -- If we are here, assume that the hash appears in only *one*
#    directory (its an error if more than one.)
# -- Print the directory contents.

# Declare table header
class DirListTable(Table):
	row = Col('')
	hashstr = Col('Hash')
	filename = Col('Name')
	filesize = Col('Size (bytes)')
	filecreate = DatetimeCol('Last modified')

#	DiffTable.add_column('hashstr', LinkCol('xxHash', attr='hashstr',
#		endpoint='path_similarity',
#      url_kwargs=dict(signedhash='xxhash')))

# -------------------------------------------------------------------------

# Print a directory listing.
#
# The argument is the string that came on the URL GET. It is the hash
# to explore, printed with a leading 0x and is unsigned.
def show_dir_listing(filehash) :

	# Convert string hash to what sqlite wants.
	uxhash = int(filehash, 16)
	sxhash = to_sint64(uxhash)

	# filerecord column names are
	# protocol, domain, filepath, filename, filesize, filecreate, filexxh, frecid

	# Get the directory that this file appears in.
	qpath = select_filerecords(filexxh=sxhash)
	qdir = qpath.fetchall()
	if (1 < len(qdir))
		return "Error: There's a bug in the code!!!"

	dirinfo = qdir[0]

	# Get a list of all distinct hashes in this directory
	dentries = select_filerecords(filepath=dirinfo['filepath'], domain=dirinfo['domain'])
	hashset = set()
	for dentry in dentries:
		hashset.add(dentry['filexxh'])

	# Gather names of the files for each hash
	filist = []
	totcount = 0;
	for hash in hashset:
		totcount += 1

		% Get the file(s) with this hash.
		dentry = select_filerecords(filepath=dirinfo['filepath'],
			domain=dirinfo['domain'], filexxh=hash)

		allfiles = dentry.fetchall()
		nfiles = len(allfiles)

		difro = dict(allfiles[0])
		difro['row'] = totcount

		# prthash is used for display on the web page and is
		# subject to change. The hex conversion is used in the
		# link URL GET method and must be decodable at the other
		# end, and thus must not change on a whim. And the
		# straight-up hash is needed for SQL queries.
		difro['filexxh'] = hash
		difro['hashstr'] = prthash(hash)
		difro['xxhash'] = hex(to_uint64(hash))

		filist.append(difro)

		# The hash may appear more than once in this directory.
		# That is, there may be more than one file, having a different
		# name, but with the same contents. Group these together.
		# Blank out the hash to avoid clutter.
		for idx in range (1, nfiles) :
			difro = dict(allfiles[id])
			difro['row'] = ''
			difro['hashstr'] = ''
			filist.append(difro)

	# Generate a detailed report of how the directories dffer
	diff_table = DiffTable(filist)

	return render_template("dir-list.html", hashstr=prthash(sxhash),
		dirtable=dirtable, difftable=diff_table, summarytable=summary_table)

# ------------------ End of File. That's all, folks! ----------------------
# -------------------------------------------------------------------------
