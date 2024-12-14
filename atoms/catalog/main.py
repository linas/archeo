#! /usr/bin/env python3
#
# main.py
#
# Update or create a catalog of files in a file system.
# This crawls a file system specified in the config file,
# and creates or updates a witness record for each file.

from walker import walk_witness

walk_witness("crawler.conf")

