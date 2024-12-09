Web UI
------
This directory implements a basic web-UI control panel into the system.

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
and eventually, there has to be accomodation for that. Just not today.

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

Other maybe useful things:
* SQLAlchemy -- Should probably use this if/when things get complicated.


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
As a regular user, copy `webui.conf-example` to `webui.conf` and edit
to indicate the location of the file catalog. Then start the webserver:
```
cd /this/project/home/dir
python3 -m venv .venv
. .venv/bin/activate
gunicorn -w 4 -b 0.0.0.0:5080 src.webui.home_page:app
```
The above creates a python "virtual environment" (provviding a degree
of isolation from the rest of the operating ssytem) It then starts a
a webserver located at `http://localhost:5080/` The `0.0.0.0` exposes
it to the local network, and so the pages become accessible on other
(local) machines.

Reference Material
------------------
* [Flask Deploying to Production](https://flask.palletsprojects.com/en/stable/deploying/)
* [Flask Deployong to Apache Httpd](https://flask.palletsprojects.com/en/stable/deploying/apache-httpd/)
  Notes about deploying Flask on Apache.
