#
# dir_list.py
#
# Do flask rendering to show directory contents.
#

from .query import select_filerecords
from .dir_single import show_single_dir
from .dir_multi import show_multi_dir

# General plan:
# -- Look to see if the provided hash appears in one, or more than one
#    directory. Branch to appropriate listing.

# Print a directory listing.
#
# The argument is the string that came on the URL GET. It is the hash
# to explore, printed with a leading 0x and is unsigned.
def show_dir_listing(filehash) :

	# Convert string hash to what sqlite wants.
	uxhash = int(filehash, 16)
	sxhash = to_sint64(uxhash)

	# Get the directory that this file appears in.
	qpath = select_filerecords(filexxh=sxhash)
	qdir = qpath.fetchall()
	if 1 < len(qdir) :
		return show_multi_dir(qdir)
	else :
		return show_single_dir(qir[0])


# ------------------ End of File. That's all, folks! ----------------------
# -------------------------------------------------------------------------
