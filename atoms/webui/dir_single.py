#
# dir_single.py
#
# Do flask rendering to show directory contents.
#

from flask import render_template
from flask_table import Table, Col, DatetimeCol, LinkCol, create_table

from .query import get_fileinfo_from_keywords

# General plan:
# -- If we are here, assume that the hash appears in only *one*
#    directory (its an error if more than one.)
# -- Print the directory contents.

# Declare table header
class FileTable(Table):
	filename = LinkCol('Name', attr='filename', endpoint='filename_detail',
		url_kwargs=dict(filename='filename'))
	filesize = Col('Size (bytes)')
	filedate = DatetimeCol('Last modified')

class DirListTable(Table):
	row = Col('')
	hashstr = LinkCol('xxHash', attr='hashstr',
		endpoint='directory_detail',
		url_kwargs=dict(hashstr='hashstr'))
	filename = LinkCol('Name', attr='filename', endpoint='filename_detail',
		url_kwargs=dict(filename='filename'))
	filesize = Col('Size (bytes)')
	filedate = DatetimeCol('Last modified')

# -------------------------------------------------------------------------

# Print a directory listing.
#
# The first argument is the content hash (of some file).
# The second argument is a FileRecord query result. If it has a length
# of more than one, then all of these should have the same domain and
# filepath. That is, the content might be appearing multiple times in
# just one directory.
def show_single_dir(hashstr, dirlist) :

	# How many times does it appear there?
	if 1 == len(dirlist) :
		ntimes = "once"
		ess = ''
	else :
		ntimes = "several times"
		ess = 's'

	# List the one or more names under which it appears.
	file_table = FileTable(dirlist)

	# Get a list of all distinct hashes in this directory
	dirinfo = dirlist[0]
	dentries = get_fileinfo_from_keywords(filepath=dirinfo['filepath'], domain=dirinfo['domain'])
	hashset = set()
	for dentry in dentries:
		hashset.add(dentry['hashstr'])

	# Gather names of the files for each hash
	filist = []
	totcount = 0;
	for hash in hashset:
		totcount += 1

		# Get the file(s) with this hash.
		dentries = get_fileinfo_from_keywords(filepath=dirinfo['filepath'],
			domain=dirinfo['domain'], hashstr=hash)

		nfiles = len(dentries)

		difro = dentries[0]
		difro['row'] = totcount

		filist.append(difro)

		# The hash may appear more than once in this directory.
		# That is, there may be more than one file, having a different
		# name, but with the same contents. Group these together.
		# Blank out the hash to avoid clutter.
		for idx in range (1, nfiles) :
			difro = dentries[idx]
			difro['row'] = ''
			difro['hashstr'] = ''
			filist.append(difro)

	# Generate a detailed report of how the directories dffer
	dir_list_table = DirListTable(filist)

	# Where is this content located?
	location = dirinfo['domain'] + ":" + dirinfo['filepath']

	return render_template("dir-list.html", hashstr=hashstr,
		ntimes=ntimes, location=location, ess=ess,
		fileinfo=file_table, dirlisttable=dir_list_table)

# ------------------ End of File. That's all, folks! ----------------------
# -------------------------------------------------------------------------
