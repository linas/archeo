#
# dup_files.py
#
# Do flask rendering to show duplicated files.
#

from flask import render_template
# from flask_table import Table, Col

# The dot in front of the name searches the current dir.
from .query import find_duplicated_names

# ---------------------------------------------------------------------

# Find duplicated filenames
def show_dup_files():
	hm = find_duplicated_names()
	filecount = len(hm.fetchall())
	print("oh yeah", filecount)
	#for rec in hm:
	#	print("donkers", rec)
	return render_template("file-list.html", filecount=filecount)
