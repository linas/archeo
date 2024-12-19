#
# show_path.py
#
# Do flask rendering to show directory contents.
#

from flask import render_template
from flask_table import Table, Col, DatetimeCol, LinkCol, create_table

from .query import get_fileinfo_from_keywords

# General plan:
# -- Print the directory contents.

# Declare table header
class PathListTable(Table):
	row = Col('')
	hashstr = LinkCol('xxHash', attr='hashstr',
		endpoint='directory_detail',
		url_kwargs=dict(hashstr='hashstr'))
	filename = LinkCol('Name', attr='filename', endpoint='filename_detail',
		url_kwargs=dict(filename='filename'))
	filesize = Col('Size (bytes)')
	filedate = DatetimeCol('Last modified')

# -------------------------------------------------------------------------

# Create a list of dictionaries describing files.
# The list to be created is specified via the key-value arguements
#
# The  argument is a property.
def build_file_list(**kwargs) :

	dentries = get_fileinfo_from_keywords(**kwargs)

	# Get a list of all distinct hashes in this directory
	hashset = set()
	for dentry in dentries:
		hashset.add(dentry['hashstr'])

	# Gather names of the files for each hash
	filist = []
	totcount = 0;
	for hash in hashset:
		totcount += 1

		# Get the file(s) with this hash.
		kwargs['hashstr'] = hash
		dentries = get_fileinfo_from_keywords(**kwargs)

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

	return filist

# -------------------------------------------------------------------------

# Print a directory listing.
#
# The argument is a filepath.
def show_path_listing(filepath) :

	filist = build_file_list(filepath=filepath)

	# Generate a detailed report of how the directories dffer
	path_list_table = PathListTable(filist)

	return render_template("path-list.html",
		filepath=filepath,
		pathlisttable=path_list_table)

# ------------------ End of File. That's all, folks! ----------------------
# -------------------------------------------------------------------------
