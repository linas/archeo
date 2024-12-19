#
# walker.py
#
# Walk over a file system, creating witness records for the files that
# are found. Adhere to crawl guidelines while scanning.

from configparser import ConfigParser
import os
from witness import file_witness, witness_store_open, witness_store_close

# Crawl the indicated directory
# The first argument, fwit, is an instance of the file_witness class.
# The second is a config file that governs the crawl.
# The third is he current directory; there will be a depth-first
# descent into the directory.
def dir_witness(fwit, config, dirpath):

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
			fwit.witness_file(hostname, fob.path)
			# Debug print. The print throws an error when the filename
			# has non-UTF-8 chars in it. Typically because the file was
			# originally created on MS-Windows. Catch and release.
			try:
				print("witness", fob.path)
			except:
				print("witness", fob.path.encode('utf8', 'surrogateescape'))

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
				dir_witness(fwit, config, fob.path)
			else:
				print("skip dir ", fob.path)

# Perform a crawl, as specified in the config file.
def walk_witness(conffile):
	config = ConfigParser()
	config.readfp(open(conffile))

	# Print info about the crawl
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

	# Where to record results
	storage_url = crawl_cfg['Storage']
	print("Storage: ", storage_url)
	witness_store_open(storage_url)

	# Use a crawl witness class. This uses a single, uniform timestamp
	# so that all observations get tagged with the same timestamp.
	with file_witness() as fkwit:
		dir_witness(fkwit, crawl_cfg, rootdir)

	witness_store_close()

# ------------------ End of File. That's all, folks! ----------------
