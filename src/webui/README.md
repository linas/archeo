Web UI
------
This directory implements a basic web-UI control panel into the system.

HOWTO
-----
These instructions are for a novice webserver admin. This sets up a
webserver on your local host, and aims it at the Archeo control panel.

As the root user:
```
apt install apache2
service apache2 start
mv /var/www/html /var/www/html-otherstuff
ln -s /where/ever/src/archeo/src/webui /var/www/html
```
