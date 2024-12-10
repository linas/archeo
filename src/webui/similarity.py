#
# similarity.py
#
# Ad hoc code to find directories with similar content.

import sqlite3
from .query import find_filehash_details

# General plan:
# -- Given a hash, find all files having that hash.
# -- Find parent directories of these files.
# -- Look at other files in the parent dirs, and see what fraction
#    the files in there have the same hash. Count.

# -------------------------------------------------------------------------

# Compare contents of filepaths having at least one file with shared
# content.
#
# As always, the argument is assumed to be a file hash, encoded as a
# 64-bit signed int, previously returned by sqlite3, so that no further
# conversion/massaging is required.
def compare_contents(filehash) :

	qpaths = find_filehash_details(filehash)

	itemcount = 0
	for pa in qpaths:
		itemcount += 1
		# columns are protocol, domain, filepath, filename, filesize, filecreate, filexxh, frecid
		#	host=fi[1], path=fi[2], name=fi[3], size=fi[4], date=fi[5]))

	print("hello simy ", itemcount);
	return "foobarbaz"

#	cursor = conn.cursor()
#	sel = "SELECT protocol, domain, filepath, filename, frecid "
#	sel += "FROM FileRecord WHERE filexxh=?;"
#	return cursor.execute(sel, (filehash,))

# ------------------ End of File. That's all, folks! ----------------------
# -------------------------------------------------------------------------
