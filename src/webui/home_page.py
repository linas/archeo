#! /usr/bin/env python3
#
# __main__.py
#
# Main control panel for Archeo
#
import sys, errno
from configparser import ConfigParser

from flask import Flask
from flask import request
from flask import render_template

# The dot in front of the name searches the current dir.
from .query import query_db_open, query_db_close

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

# Main application page. Includes various search options
@app.route('/')
def search_form():
	return render_template("index.html")

@app.route('/dup-filenames', methods=['POST'])
def dupe_files():
	return render_template("file-list.html")

@app.route('/', methods=['POST'])
def blarg_post():
	global foobar
	bop = op()

	foo = request.form['foo']
	bar = request.form['bar']
	return "You typed " + foo + " and " + bar + " and foobar=" + str(foobar) + bop

#if __name__ == "__main__":
#    server.run(host='0.0.0.0', port=5080)
