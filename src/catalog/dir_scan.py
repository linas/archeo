#
# dir-scan.py
#
# Perform a scan of a directory.
# Adhere to crawl guidelines while scanning.

import os
from witness import file_witness, witness_db_open, witness_db_close

def dir_witness(hostname, dirpath):
	# Files first
	for fob in os.scandir(dirpath) :
		if fob.is_file() :
			fid = file_witness(hostname, fob.path)
			print("reco", fid, fob.path)

	# Directories next
	for fob in os.scandir(dirpath) :
		if fob.is_dir() :
			print("yoo", fob.path)
