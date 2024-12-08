The File Catalog
----------------
The file catalog attempts to create a searchable index of files,
organized by filename, content hash and other file data.

SQL tables need to hold this info, and they need to be normalized
so that "things are finable". Some normalization notes:

* There may be multiple files with the same content hash. They
  may be in different locations.

* There may be multiple files with the same name, but with
  different metadata (file creation timestamp, file size,
  directory location

* Every time a file is witnessed (i.e. seen by this software system)
  it should be logged.

The file witness does *not* currently record the UID and GID of the
file owner. The problem here is that different hosts map the UID and
GID to different usernames, and I don't currently understand how to
deal with this. I need the UID/GID map at the time its observed, as
it exists on the observing host ... and not some later time.

This also includes issues like rwx permissions. I don't know how to
securely track file ownership and permissions in a multi-host setting.
Fixing this is an important TODO, I guess.


HOWTO
-----
Do this to get started:
```
cat file-witness.sql | sqlite3 file-witness.db
```
