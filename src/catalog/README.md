The File Catalog
----------------
The file catalog creates a searchable index of files,
organized by filename, content hash and other file data.

The search is controlled by a a configuration file, which can be used
to exclude specific file-types, directories or file-system types from
the filesystem crawl. Different config files can be given for differet
crawls.

Issues
------
* The crawler is *slow*. The primary reason for this appears that the
  update of the database is slow. It seems to be bottlenecked on writes.
  Its also possible that inappropriate indexing is creating issues.
* The Web UI cannot be used while the crawler is running. This is
  because SQLite3 is effectively a single-user system. Perhaps it was
  a bad design choice, and should be rectified.
* A list of additional issues included further down.

API Design
----------
Currently uses SQLite3 for storage. Uses a closure-like idea, so that
future changes could use other DB's, as desired.

The crawler control file uses conventional Unix-style stanza-key-value
text formatting.

The crawl control loosely resembles the `/etc/updatedb.conf` file used
by the `locate`, `slocate` and `plocate` file utilities.

File Guide
----------
* crawler.conf-example: An example config file.
* file-witness.sql: database definition
* witness.py: code that can witness one file.
* crawler.py: code that crawls the filesystem

Table Design
------------
SQL tables need to hold this info, and they need to be normalized
so that "things are findable". Some notes about normalization:

* There may be multiple files with the same content hash. They
  may be in different locations. Having the same hash does not
  mean they are the same; there might be hash collisions.

* There may be multiple files with the same name, but with
  different metadata (file creation timestamp, file size,
  directory location)

* Every time a file is witnessed (i.e. seen by this software system)
  it should be logged. This is doen with the RecordWitness table.

Open Questions/Issues
---------------------
* The file witness does *not* currently record the UID and GID of the
  file owner. The problem here is that different hosts map the UID and
  GID to different usernames, and I don't currently understand how to
  deal with this. I need the UID/GID map at the time its observed, as
  it exists on the observing host ... and not some later time.

* This also includes issues like rwx permissions. I don't know how to
  securely track file ownership and permissions in a multi-host setting.
  Fixing this is an important TODO, I guess.

* The file modification date is recorded, but is not currently used for
  anything.

* What to do if "permission denied"? Current plan is to have this run
  by superuser with global filesystem visibility, but general security
  and permissions mapping is unclear. How this is logged should be
  determined by the config file.

  Current impl will log a filename, but return a hash of zero, because
  the contents are unreadable. Directories are currently not logged.

* Should there be a log of a file being searched for, and not found?

* Currently, links are never followed. SHould this be configurable?


HOWTO
-----
Do this to get started:
```
cat file-witness.sql | sqlite3 file-witness.db
cp crawler.conf-example crawler.conf
```
Edit the `crawler.conf` file to config adirectory to be calaoged.
Then run the cataloger, and wait:
```
./main.py
```

Similar projects
----------------
* [Fred Hutch Storage Crawler](https://github.com/FredHutch/storage-crawler)
  Walks filesystem, stores file metadata in Postgres DB. Tiny project,
  abandoned in 2016 after a handful of commits.
