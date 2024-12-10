#
# crawler.py
#
# Crawl a file system, creating witness records for the files that are found.
# Adhere to crawl guidelines while scanning.

from configparser import ConfigParser
import os
from witness import file_witness, witness_db_open, witness_db_close

# Crawl the indicated directory
def dir_witness(config, dirpath):

	# Errors include `PermissionError: [Errno 13] Permission denied`
	# Not sure what to do about that. Right now, do nothing.
	# XXX FIXME: operation should be determined by the config file.
	try:
		dgen = os.scandir(dirpath)
	except:
		return

	hostname = config['Domain']

	# Files first.
	for fob in dgen :
		if fob.is_file(follow_symlinks=False) :
			fid = file_witness(hostname, fob.path)
			# Debug print. The print throws an error when the filename
			# has non-UTF-8 chars in it. Typically because the file was
			# originally created on MS-Windows. Catch and release.
			try:
				print("reco", fid, fob.path)
			except:
				print("reco", fid, fob.path.encode('utf8', 'surrogateescape'))

	# Directories next. Handle this with a recursive call.
	# Prune directory name patterns. Yes, someday this could
	# be a regex. Not today.

	# If config file doesn't specify these, just ignore.
	try:
		prunenames = config['PruneNames'].split()
	except:
		prunenames = []

	try:
		prunepaths = config['PrunePaths'].split()
	except:
		prunepaths = []

	for fob in os.scandir(dirpath) :
		if fob.is_dir(follow_symlinks=False) :
			if not fob.name in prunenames and not fob.path in prunepaths :
				dir_witness(config, fob.path)
			else:
				print("skip dir ", fob.path)

# Perform a crawl, as specified in the config file.
def crawl_witness(conffile):
	config = ConfigParser()
	config.readfp(open(conffile))

	# Prit info about the crawl
	unit_descr = config.get('Unit', 'Description')

	crawl_stanza = 'Crawler';
	crawl_cfg = config[crawl_stanza]

	crawl_descr = crawl_cfg['Description']
	print("Will crawl: ", crawl_descr)

	# Set the default domain to the hostname, if it's
	# not specified.
	try:
		domain = crawl_cfg['Domain']
	except:
		try:
			domain = os.uname().nodename
		except:
			domain = ''
	crawl_cfg['Domain'] = domain
	print("Domain: ", domain)

	# Get the location to start the crawl.
	rootdir = crawl_cfg['RootDir']
	print("Root dir: ", rootdir)

	# Do the heavy lifting
	dir_witness(crawl_cfg, rootdir)

# ------------------ Enf of File. That's all, folks! ----------------
