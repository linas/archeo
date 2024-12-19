SQLite3 prototype
=================
This directory contains a now-abandoned prototype of the system,
written using a conventional software stack of sqlite3+python+flask
This prototype "works", but was abandoned due to limitations imposed
by the very nature of SQL. The
[AtomSpace](https://github.com/opencog/atomspace)
provides a superior data processing infrastructure for this kind of
problem. Addtional details on this tech selection are in the
[similarity README](similarity/README.md) file.

HOWTO
-----
There are two parts to this prototype:
* The cataloger, which runs over file systems, computes file hashes,
  and logs the resulting filepaths.
  See the [`src/catalog` README](catalog) for more.
* The Web UI, which can be used to browse the catalog above, find
  *identical* files, and see where they are located.
  See the [`src/webui` README]webui) for more.

Both parts work just fine, and are "done".

Please review each README above for addtional install, config and
operation details.

Both parts need some basic python infrastructure. As root:
```
apt install python3 python3-flask python3-venv python3-xxhash
apt install sqlite3
apt install gunicorn
```

TODO
----
Some specfic coding tasks:
* Create CSS sytlesheets for everything. Currently, this is fugly.

* Create a file browser, resembling a conventional file browser. This
  would be a bit different though, because the file records in the
  DB might be in cold storage (so we can "see" what's there, without
  actually booting it and plugging it in.) The display should also
  offer how many times the file has been witnessed (seen, recorded in
  the DB) and it should allow browsing by similar/identical names
  and browsing by content hash (showing other files, file locations,
  with the same hash.)  So, a regular file browser, but with some
  extra super-powers.  This is already half-way done; but only half-way.

* Utility to mark a file that disappeared: was present in earlier scans
  but is now gone.

* There are more TODO items scattered about in other README's.

Some general ideas.
* If a directory has files with hash miscompares, and that directory
  is under git control, then perhaps git can offer an explanation of
  what is happening to that file.

* Is there any point at all for coupling this into any kind of
  intrustion-detection framework? After all, we are generating file
  hashes, which are weak file fingerprints.
