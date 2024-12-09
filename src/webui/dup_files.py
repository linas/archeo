#
# dup_files.py
#
# Do flask rendering to show duplicated files.
#

from flask import render_template
from flask_table import Table, Col

# The dot in front of the name searches the current dir.
from .query import find_duplicated_names

# ---------------------------------------------------------------------

# Declare table header
class DupeTable(Table):
	row = Col('')
	name = Col('File Name')
	count = Col('Count')
	fid = Col('fid')

# Find duplicated filenames
def show_dup_files():
	hm = find_duplicated_names()

	# filecount = len(hm.fetchall())
	filecount = 0
	filelist = []
	for rec in hm:
		filecount += 1
		# Ugly API: columns according to SQL query.
		filelist.append(dict(row=filecount, name=rec[0], count=rec[2], fid=rec[1]))
		# print("donkers", rec)

	ftable = DupeTable(filelist)
	return render_template("file-list.html", filecount=filecount, filetable=ftable)
