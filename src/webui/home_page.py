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

@app.route('/')
def ola():
	return "hello worrld"

#@app.route('/')
#def bonkers_form():
#	return render_template("index.html")

@app.route('/', methods=['POST'])
def blarg_post():
	foo = request.form['foo']
	bar = request.form['bar']
	if foo == 'bla' :
		return "<h1>Binkers ...</h1>"
	else :
		return "<h1>Bonkers !</h1>"

#if __name__ == "__main__":
#    server.run(host='0.0.0.0', port=5080)
