Catalog Agent
-------------
The catalog agent is a file system crawler that will walk over assorted
filesystems, and catalog what it finds there.

The goal is to log the hostname, the filepath, the content hash and the
date of the crawl.
* The hostname allows the system to look at files scattered over many
  computers. Together with the filepath, this is recorded as a single
  URL.
* The content hash is a file "fingerprint": two files with the same
  content hash are almost surely identical. The hash is not meant to
  be crypto-secure; its meant only to make it easy to find files with
  the same content.
* The crawl date acts as a "witness", testifying that on such a certain
  time and date, the given URL was really there, and really had this
  and such a hash. Multiple witnesses over time can be used to track
  when a file was last seen, where it might be now, whether it got
  corrupted or changed along the way.

This is a rework of an older sqlite3 implementation, to be found in
[src/catalog](../../src/catalog). This version is 10x faster.
Also more flexible and easier to code. And more fun.

Design and Implementation
-------------------------
The system is built on top of the
[AtomSpace](https://wiki.opencog.org/w/AtomSpace) (hyper-)graph database.
Operations on the database are provided by the
[Atomese](https://wiki.opencog.org/w/Atomese) API.
Programmers wishing to modify the code here will need to become familiar
with Atomese.

### AtomSpace Tutorial
Because the AtomSpace is relatively unknown, and is built on some
unusual ideas, an [Atomese tutorial](atomese_tutorial.py) is provided
in this directory. It's a good place to start, if learning system
internals. (There is no need to understand Atomese to use Archeo.)

### Inodes
There are many different design choices available for mapping a
file-system-like hierarchy into Atomese. Perhaps not surprisingly,
one of the better choices resembles a warped version of conventional
POSIX file-system design. Its warped for two reasons: first, Archeo
does not store file content, but rather file hashes. Second, the
AtomSpace is a hypergraph database, and the natural entities are
type, labelled graph edges. There is no (direct) support for
conventional programming constructs like lists, arrays, structures,
pointers or even basic concepts like integers. In Atomese, everything
is a (hyper-)graph.

A detailed design discussion is given in the
[README-Inodes](README-Inodes.md) file.

Implementation Overview
-----------------------
The implementation consists of the following files:
* The `crawler.conf-example`, which configures the directory tree
  to make a record of.
* The `main.py` file, which creates a catalog of a directory tree.
* The `walker.py` file that walks over a directory tree.
* The `witness.py` file that witnesses individual files, and stuffs
  a record of that into the AtomSpace.

TODO
----
* Maybe record the config file in the database. Maybe suck the config
  info out of the database. Buid infrastructure to manage multiple
  crawls.

HOWTO
-----
Only three steps:
* Install the AtomSpace. This is tedious, as there are no up-to-date,
  easily-to-install packages for the AtomSpace. It must be installed
  by hand, from source. The git README's provide details.  Install
  both the [AtomSpace](https://github.com/opencog/atomspace)
  and [AtomSpace-Rocks](http://github.com/opencog/atomspace-rocks),
  which provides an on-disk storage method backed by RockDB.

* Copy `crawler.conf-example` to `crawler.conf`, and edit to specify
  the directories you want crawled.

* Run `main.py`. It can index ballpark dozens of files per second,
  depending on a variety of factors.


