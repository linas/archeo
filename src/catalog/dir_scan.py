#
# dir-scan.py
#
# Perform a scane of a directory.
# Adhere to crawl guidelines will scanning

import os
from witness import file_witness, witness_db_open, witness_db_close

def dir_witness(hostname, dirpath):
	diter = os.scandir(dirpath)
	for fob in diter:
		print("yoo", fob)

# r = file_witness(hostname, "/tmp/xxx")
# print("I got fileid ", r)
