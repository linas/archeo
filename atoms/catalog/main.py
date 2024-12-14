#! /usr/bin/env python3
#
# main.py
#
# Update or create a catalog of files in a file system.
# This crawls a file system specified in the config file,
# and creates or updates a witness record for each file.

from witness import witness_db_open, witness_db_close
from crawler import crawl_witness

witness_db_open('file-witness.db')

crawl_witness("crawler.conf")

# Close the connection
witness_db_close()
