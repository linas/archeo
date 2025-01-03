Web UI
------
This directory implements a basic web-UI control panel into the system.

*** UNDER CONSTRUCTION !! Kinda bogus !! ***

Design
------
The implementation in this directory uses the Python3 `gunicorn`
web server to expose a web app written in the python `flask` web
app framework.

Flask was selected because it is quick and easy to develop for.
Other choices are possible (listed below). The gunicorn server
was selected because it requires less configuration than a fresh
Apache install would require, and thus can get you up and running
more quickly.

A long-term goal is to allow custom modules written e.g. in rust or java
and eventually, there has to be accommodation for that. Just not today.

Alternative frameworks and servers:
* Flask -- ideal for python microservices, i.e. projects like this.
* FastAPI -- New, ideal for scalable services. Almost as easy as flask,
  but perhaps forces an async architecture that might cause issues.
  Async flask is supposed to be just as fast.
* Webpy -- ???
* Django -- Large complex python server deployment framework.

Different ways to serve python apps:
* `gunicorn` -- web server for python.
* `waitress` -- web server for python.
* `mod_wsgi` -- Web Server Gateway Interface. (?)
* `mod_python` -- Apache module (?)

AtomSpace
---------
If in doubt, consult the [Atomese tutorial](../catalog/atomese_tutorial.py).

HOWTO
-----
These instructions are for a novice webserver admin. This sets up a
webserver on your local host, and aims it at the Archeo control panel.

As the root user:
```
apt install python3-flask
apt install python3-venv
apt install gunicorn
```
As a regular user, finish install of python:
```
cd /this/project/home/dir
python3 -m venv .venv
. .venv/bin/activate
pip install flask-table
```

As a regular user, copy `webui.conf-example` to `webui.conf` and edit
to indicate the location of the file catalog. Then start the webserver.
```
cd /this/project/home/dir
. .venv/bin/activate  # Not needed, if you already did it above
gunicorn --timeout 900 -w 1 -b 0.0.0.0:5080 atoms.webui.home_page:app
```
The above creates a python "virtual environment" (providing a degree
of isolation from the rest of the operating system) It then starts a
a webserver located at `http://localhost:5080/` The `0.0.0.0` exposes
it to the local network, and so the pages become accessible on other
(local) machines.

The timeout is set to 900 seconds; you may need to adjust. The AtomSpace
uses RocksDB; sometimes RocksDB reorganizes itself, this can lead to
longer stalls. Sometimes AtomSpace needs to compute something complex;
currntly it does this inline, instead of a special thead.

Reference Material
------------------
* [Flask Deploying to Production](https://flask.palletsprojects.com/en/stable/deploying/)
* [Flask Deployong to Apache Httpd](https://flask.palletsprojects.com/en/stable/deploying/apache-httpd/)
