#! /usr/bin/env python3
#
# __main__.py
#
# Main control panel for Archeo
#
from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

# Main application page. Includes various search options
@app.route('/')
def search_form():
	return render_template("index.html")

@app.route('/dup-filenames', methods=['POST'])
def dupe_files():
	return render_template("file-list.html")

@app.route('/', methods=['POST'])
def blarg_post():

	foo = request.form['foo']
	bar = request.form['bar']
	return "You typed " + foo + " and " + bar

#if __name__ == "__main__":
#    server.run(host='0.0.0.0', port=5080)
