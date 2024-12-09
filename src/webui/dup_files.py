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

# Find duplicated filenames
def show_dup_files():
	qresult = find_duplicated_names()

	# filecount = len(qresult.fetchall())
	filecount = 0
	filelist = []
	for rec in qresult:
		filecount += 1
		# Ugly API: columns according to SQL query.
		fname = rec[0]
		fmore = "<a href=\"show-name-dupes.html?name=" + fname + "\">"
		fmore += fname + "</a>"
		filelist.append(dict(row=filecount, name=fmore, count=rec[2]))

	ftable = DupeTable(filelist)
	return render_template("file-list.html", filecount=filecount, filetable=ftable)
