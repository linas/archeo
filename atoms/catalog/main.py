#! /usr/bin/env python3
#
# main.py
#
# Update or create a catalog of files in a file system.
# This crawls a file system specified in the config file,
# and creates or updates a witness record for each file.

import sys
from walker import walk_witness

if 2 != len(sys.argv):
	print("Usage: " + sys.argv[0] + " <config file>")
	print("\tThe config file specifies which directories to crawl,")
	print("\tand where crawl results will be stored.")
	sys.exit(1)

# Expecting crawler.conf
walk_witness(sys.argv[1])
