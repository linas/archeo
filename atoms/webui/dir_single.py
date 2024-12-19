#
# dir_single.py
#
# Do flask rendering to show directory contents.
#

from flask import render_template
from flask_table import Table, Col, DatetimeCol, LinkCol, create_table

from .property_listing import item_collection

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

	itco = item_collection()
	filist = itco.build_file_list(filepath=dirinfo['filepath'], domain=dirinfo['domain'])

	# Generate a detailed report of how the directories dffer
	dir_list_table = DirListTable(filist)

	# Where is this content located?
	location = dirinfo['domain'] + ":" + dirinfo['filepath']

	return render_template("dir-list.html", hashstr=hashstr,
		ntimes=ntimes, location=location, ess=ess,
		fileinfo=file_table, dirlisttable=dir_list_table)

# ------------------ End of File. That's all, folks! ----------------------
# -------------------------------------------------------------------------
