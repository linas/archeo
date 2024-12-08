#
# crawler.py
#
# Crawl a file system, creating witness records for the files that are found.
# Adhere to crawl guidelines while scanning.

from configparser import ConfigParser
import os
from witness import file_witness, witness_db_open, witness_db_close

# Crawl the indicated directory
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

def crawl_witness(conffile):
	config = ConfigParser()
	config.readfp(open(conffile))

	unit_descr = config.get('Unit', 'Description')

	crawl_stanza = 'Crawler';

	crawl_descr = config.get(crawl_stanza, 'Description')

	print("Will crawl: ", crawl_descr)
	try:
		domain = config.get(crawl_stanza, 'xDomain')
	except:
		try:
			domain = os.uname().nodename
		except:
			domain = ''

	print("Domain: ", domain)

