#
# dir_single.py
#
# Do flask rendering to show directory contents.
#

from datetime import datetime

from flask import render_template
from flask_table import Table, Col, DatetimeCol, LinkCol, create_table

from .query import select_filerecords
from .utils import prthash, to_sint64, to_uint64

# General plan:
# -- If we are here, assume that the hash appears in only *one*
#    directory (its an error if more than one.)
# -- Print the directory contents.

# Declare table header
class DirListTable(Table):
	row = Col('')
	hashstr = LinkCol('xxHash', attr='hashstr',
		endpoint='directory_detail',
		url_kwargs=dict(signedhash='filexxh'))
	filename = Col('Name')
	filesize = Col('Size (bytes)')
	filecreate = DatetimeCol('Last modified')


class FileTable(Table):
	prop = Col('')
	val = Col('')

# -------------------------------------------------------------------------

# Print a directory listing.
#
# The first argument is a signed int content hash (of some file).
# The second argument is the FileRecord query result of length one.
# It will be used to display all other files having the same
# domain and filepath.
def show_single_dir(sxhash, dirinfo) :

	dirinfo = dict(dirinfo)
	dirinfo['hashstr'] = prthash(sxhash)

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

		# Get the file(s) with this hash.
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
			difro = dict(allfiles[idx])
			difro['row'] = ''
			difro['hashstr'] = ''
			filist.append(difro)

	# Generate a detailed report of how the directories dffer
	dir_list_table = DirListTable(filist)

	ftime = datetime.fromtimestamp(dirinfo['filecreate'])
	finfolist = []
	finfolist.append({'prop': "Domain:", 'val': dirinfo['domain']})
	finfolist.append({'prop': "Path:", 'val': dirinfo['filepath']})
	finfolist.append({'prop': "File name:", 'val': dirinfo['filename']})
	finfolist.append({'prop': "Size:", 'val': dirinfo['filesize']})
	finfolist.append({'prop': "Last modified:", 'val': str(ftime)})
	file_table = FileTable(finfolist)

	return render_template("dir-list.html", hashstr=prthash(sxhash),
		fileinfo=file_table, dirlisttable=dir_list_table)

# ------------------ End of File. That's all, folks! ----------------------
# -------------------------------------------------------------------------
