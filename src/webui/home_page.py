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
from .query import query_db_open, query_db_close
from .dup_files import show_dup_files
from .dup_hashes import show_dup_hashes
from .filename_details import show_filename_details
from .similar_dirs import show_similar_dirs

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
	dbfile = db_stanza['Location']
	print("Will use db located at: " + dbfile)
	query_db_open(dbfile)

# Perform initialization. This is called once per worker thread.
# Some of the init does not require per-worker config
def create_app() :
	app = Flask(__name__)

	config_db("./src/webui/webui.conf")
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
@app.route('/similar-dirs', methods=['POST'])
def sim_dirs():
	return show_similar_dirs()

# ----------------------------------------------------------------------
# File-detail sub-page
# Display details for a given filename.
@app.route('/filename.detail', methods=['GET'])
def filename_detail():
	return show_filename_details(request.args['filename'])

# ----------------------------------------------------------------------
# Testing
@app.route('/', methods=['POST'])
def blarg_post():

	foo = request.form['foo']
	bar = request.form['bar']
	return "You typed " + foo + " and " + bar

#if __name__ == "__main__":
#    server.run(host='0.0.0.0', port=5080)
