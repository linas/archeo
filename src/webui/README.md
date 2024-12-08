Web UI
------
This directory implements a basic web-UI control panel into the system.

Design
------
The user interface needs to be able to run python scripts. In some
cases, these might have to be as root or some powerful user. Maybe.
The security design is curently unclear.

A long-term goal is to allow custom modules written e.g. in rust or java
and so the framwork needs to accomadate these. The current design choices
are:

* Flask -- ideal for python microservices, i.e. projects like this.
* FastAPI -- New, ideal for scalable services. Almost as easy as flask,
  but perhaps forces an async architecture that might cause issues.
  Async flask is supposed to be just as fast.
* Webpy -- ???
* `mod_wsgi` -- Apache module (Web Server Gateway Interface)
* `mod_python` -- Apache module
* Django -- Large complex deployment framework.
* SQLAlchemy -- use with flask


HOWTO
-----
These instructions are for a novice webserver admin. This sets up a
webserver on your local host, and aims it at the Archeo control panel.

As the root user:
```
apt install python3-flask
apt install apache2
service apache2 start
mv /var/www/html /var/www/html-otherstuff
ln -s /where/ever/src/archeo/src/webui /var/www/html
```
