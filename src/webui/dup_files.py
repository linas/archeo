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

# Declare your table
class ItemTable(Table):
	name = Col('Name')
	description = Col('Description')

# Get some objects
class Item(object):
	def __init__(self, name, description):
		self.name = name
		self.description = description
items = [Item('Name1', 'Description1'),
		 Item('Name2', 'Description2'),
		 Item('Name3', 'Description3')]
# Or, equivalently, some dicts
items = [dict(name='Name1', description='Description1'),
		 dict(name='Name2', description='Description2'),
		 dict(name='Name3', description='Description3')]

# Populate the table
ftable = ItemTable(items)

# Find duplicated filenames
def show_dup_files():
	hm = find_duplicated_names()
	filecount = len(hm.fetchall())
	print("oh yeah", filecount)
	#for rec in hm:
	#	print("donkers", rec)

	return render_template("file-list.html", filecount=filecount, filetable=ftable)
