#
# dir_list.py
#
# Do flask rendering to show directory contents.
#

from .query import get_fileinfo_from_keywords
from .dir_single import show_single_dir
from .dir_multi import show_multi_dir

# General plan:
# -- Look to see if the provided hash appears in one, or more than one
#    directory. Branch to appropriate listing.

# Print a directory listing.
#
# The argument is the string that came on the URL GET. It is the hash
# to explore, as an ascii hexadecimal string.
def show_dir_listing(hashstr) :

	# Get the directory that this file appears in.
	qdir = get_fileinfo_from_keywords(hashstr=hashstr)

	# This content can appear multiple times in one directory,
	# or in multiple distinct directories. Figure out which.
	multidir = False
	basedom = qdir[0]['domain']
	basedir = qdir[0]['filepath']
	for idx in range (1, len(qdir)) :
		if basedir != qdir[idx]['filepath'] :
			multidir = True
		if basedom != qdir[idx]['domain'] :
			multidir = True

	if multidir :
		return show_multi_dir(hashstr, qdir)
	else :
		return show_single_dir(hashstr, qdir)


# ------------------ End of File. That's all, folks! ----------------------
# -------------------------------------------------------------------------
