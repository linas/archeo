#! /usr/bin/env python3
#
# home_page.py
#
# Main control panel for Archeo
#
import sys, errno
from configparser import ConfigParser

from flask import Flask
from flask import request
from flask import render_template

# XXX FIXME Super ultra mega Hack alert!
# My friend Dario likes to drive a super ultra mega car.
# Drives too fast, drives to flash, doesn't care about the crash.
# The import of flask_tables (in various other files) fails if this
# is not added to the system path. Beats me why. Clearly something is
# broken, because this is just plain wrong.
import sys
sys.path.append('./.venv/lib/python3.11/site-packages')

# The dot in front of the name searches the current dir.
from .query import storage_open, storage_close
from .dup_files import show_dup_files
from .dup_hashes import show_dup_hashes
from .filename_details import show_filename_details
from .dir_list import show_dir_listing
from .similar_summary import show_similar_summary

# Read config file to discover DB location.
def config_db(conffile) :
	global done_setup

	print("Looking for WebUI config file at: " + conffile)
	config = ConfigParser()

	try:
		config.readfp(open(conffile))
	except:
		print("Fatal error: cannot find config file: " + conffile)
		sys.exit(errno.EINTR);

	db_stanza = config['WitnessDB']
	storage = db_stanza['Storage']
	print("Will use StorageNode located at: " + storage)
	storage_open(storage)

# Perform initialization. This is called once per worker thread.
# Some of the init does not require per-worker config
def create_app() :
	app = Flask(__name__)

	config_db("./atoms/webui/webui.conf")
	return app

app = create_app()

# ---------------------------------------------------------------------

# Main application page. Includes various search options
@app.route('/')
def search_form():
	return render_template("index.html")

# Find duplicated filenames, display them.
@app.route('/dup-filenames', methods=['POST'])
def dupe_files():
	return show_dup_files()

# Find duplicated hashes, display them.
@app.route('/dup-hashes', methods=['POST'])
def dupe_hashes():
	return show_dup_hashes()

# Find similar dirs.
@app.route('/similar-summary', methods=['POST'])
def sim_summary():
	return show_similar_summary()

# ----------------------------------------------------------------------
# File-detail sub-page
# Display details for a given filename.
@app.route('/filename.detail', methods=['GET'])
def filename_detail():
	return show_filename_details(request.args['filename'])

# ----------------------------------------------------------------------
# Directory-listing sub-page
# Display all directories that might hold a given hash.
@app.route('/directory.detail', methods=['GET'])
def directory_detail():
	return show_dir_listing(request.args['hashstr'])

# ----------------------------------------------------------------------
# Testing
@app.route('/', methods=['POST'])
def blarg_post():

	foo = request.form['foo']
	bar = request.form['bar']
	return "You typed " + foo + " and " + bar

#if __name__ == "__main__":
#    server.run(host='0.0.0.0', port=5080)
