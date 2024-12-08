#
# dir-scan.py
#
# Perform a scan of a directory.
# Adhere to crawl guidelines while scanning.

import os
from witness import file_witness, witness_db_open, witness_db_close

def dir_witness(hostname, dirpath):

	# Errors include `PermissionError: [Errno 13] Permission denied`
	# Not sure what to do about that. RIght now, do nothing.
	try:
		dgen = os.scandir(dirpath)
	except:
		return

	# Files first
	for fob in dgen :
		if fob.is_file(follow_symlinks=False) :
			fid = file_witness(hostname, fob.path)
			print("reco", fid, fob.path)

	# Directories next. Handle this with a recursive call.
	for fob in os.scandir(dirpath) :
		if fob.is_dir(follow_symlinks=False) :
			dir_witness(hostname, fob.path)
