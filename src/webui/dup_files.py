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
	name = Col('File Name')
	count = Col('Count')
	fid = Col('fid')

# Get some objects
class Item(object):
	def __init__(self, name, count, fid):
		self.name = name
		self.count = count
		self.fid = fid

# Or, equivalently, some dicts
items = [dict(name='foo', count=44, fid=3),
		 dict(name='bar', count=66, fid=5)]

# Find duplicated filenames
def show_dup_files():
	hm = find_duplicated_names()

	# filecount = len(hm.fetchall())
	filecount = 0
	filelist = []
	for rec in hm:
		filecount += 1
		filelist.append(dict(name='foo', count=filecount, fid=99))
		print("donkers", rec)

	print("oh yeah", filecount)
	ftable = DupeTable(filelist)
	return render_template("file-list.html", filecount=filecount, filetable=ftable)
