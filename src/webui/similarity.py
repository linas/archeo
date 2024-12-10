#
# similarity.py
#
# Ad hoc code to find directories with similar content.

import sqlite3
from .query import find_filehash_details
from .utils import prthash, to_sint64

from flask import render_template
from flask_table import Table, Col, LinkCol

# General plan:
# -- Given a hash, find all files having that hash.
# -- Find parent directories of these files.
# -- Look at other files in the parent dirs, and see what fraction
#    the files in there have the same hash. Count.

# -------------------------------------------------------------------------

# Compare contents of filepaths having at least one file with shared
# content.
#
# The argument is the string that came on the URL GET. It is the hash
# to explore, printed with a leading 0x and is unsigned.
def compare_contents(filehash) :

	# Convert string hash to what sqlite wants.
	uxhash = int(filehash, 16)
	sxhash = to_sint64(uxhash)
	qpaths = find_filehash_details(sxhash)

	itemcount = 0
	for pa in qpaths:
		itemcount += 1
		# columns are protocol, domain, filepath, filename, filesize, filecreate, filexxh, frecid
		#	host=fi[1], path=fi[2], name=fi[3], size=fi[4], date=fi[5]))

	print("hello simy ", itemcount);
	return render_template("similar-dirs.html", xxhash=filehash)

#	cursor = conn.cursor()
#	sel = "SELECT protocol, domain, filepath, filename, frecid "
#	sel += "FROM FileRecord WHERE filexxh=?;"
#	return cursor.execute(sel, (filehash,))

# ------------------ End of File. That's all, folks! ----------------------
# -------------------------------------------------------------------------
