#
# show_path.py
#
# Do flask rendering to show directory contents.
#

from flask import render_template
from flask_table import Table, Col, DatetimeCol, LinkCol, create_table

from .property_listing import item_collection

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

# Print a directory listing.
#
# The argument is a filepath.
def show_path_listing(filepath) :

	itco = item_collection()
	filist = itco.build_file_list(filepath=filepath)

	# Generate a detailed report of how the directories dffer
	path_list_table = PathListTable(filist)

	return render_template("path-list.html",
		filepath=filepath,
		pathlisttable=path_list_table)

# ------------------ End of File. That's all, folks! ----------------------
# -------------------------------------------------------------------------
