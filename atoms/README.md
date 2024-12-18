AtomSpace Version
-----------------
This directory contains the AtomSpace version of the file witnessing tool.

### Motivation
After prototyping versin 0.0.6 in python+flask+sqlite3, I've decided
to continue the rest of the development using the AtomSpace instead of
sqlite3, but keeping the python+flask tech stack. The reason for this
change is given in the [similarity-README](../src/similarity/README.md).

### Status
Under construction. Still raw, can't yet do what the prototype version
did.

### Structure
There are several parts here:

* The cataloger, which runs over file systems, computes file hashes,
  and logs the resulting filepaths.
  See the [`atoms/catalog` README](catalog) for more.
* The URL splitter, which splits file URL's into components. This
  splitting has the effect of creating indexes that make it much
  faster to perform the assorted WebUI lookups and computations.
* The Web UI, which can be used to browse the catalog above, find
  *identical* files, and see where they are located.
  Its currently under construction.
  See the [`atoms/webui` README](webui) for more.

### HOWTO
Do the following:
* Set up the craw config file. `cd` to `atoms/catalog` and copy
  `crawler.conf-example` to `crawler.conf`. Edit to suit.
* Perform a witnessing run. Run `atoms/catalog/main.py` Wait until done.
* Prepare indexes. This is currently a manual sep, may go away later.
  Run `atoms/splitter/main.py`
* Configure the web interface. `cd` to `atoms/webui` and copy
  `webui.conf-example` to `webui.conf` and edit as appropriate.
  Mostly this is to specify the database location.
* Start the web interface. `cd` to the base project directory, and run
  `gunicorn -w 1 -b 0.0.0.0:5080 atoms.webui.home_page:app`
* Aim your web browser at `http://localhost:5080/` and browse away.
