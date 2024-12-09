#
# filename_details.py
#
# Do flask rendering to show details of a single duplicated filename
#

from flask import render_template
from flask_table import Table, Col, LinkCol

# The dot in front of the name searches the current dir.
from .query import find_duplicated_names

# ---------------------------------------------------------------------

# Declare table header
class FilenameDetailsTable(Table):
	row = Col('')
	path = Col('File path')
	frecid = Col('Record ID')
	hash = Col('xxHash')

# Find duplicated filenames
def show_filename_details(filename):
	# qresult = find_duplicated_names()

	return "a hey ooo you want " + filename

	# filecount = len(qresult.fetchall())
#	filecount = 0
#	filelist = []
#	for rec in qresult:
#		filecount += 1
#		# Ugly API: columns according to SQL query.
#		fname = rec[0]
#		filelist.append(dict(row=filecount, name=fname, count=rec[2]))
#
#	ftable = DupeTable(filelist)
#	return render_template("file-list.html", filecount=filecount, filetable=ftable)
