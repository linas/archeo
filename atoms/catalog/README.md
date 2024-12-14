Catalog Agent
-------------
The catalog agent is a file system crawler that will walk over assorted
filesystems, and catalog what it finds there. See the older
[catalog README](../../src/catalog/) for a better, more comprehensive
description.

In short, the goal is to log the hostname, the filepath, the content
hash and the crawl date.
* The hostname allows the system to look at data scattered over many
  computers. Together with the filepath, this is more or less a URL.
* The content hash is a file "fingerprint": two files with the same
  content hash are almost surely identical. The hash is not meant to
  be crypto-secure; its meant only to make it easy to find files with
  the same content.
* The crawl date acts as a "witness", testifying that on such a certain
  time and date, the given URL was really there, and really had this
  and such a hash. Multiple witnesses over time can be used to track
  when a file was last seen, where it might be now, whether it got
  corrupted or changed along the way.

By using the AtomSpace instead of sqlite3, the pain of designing good
SQL tables, creating indexes, designing queries, and worrying about
future expansions and data migrations can be avoided. Less hassle,
more fun.

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
The implementation consists of teh following files:
* The `crawler.conf-example`, which is identical to the one in
  [src/catalog](../../src/catalog).
* The `crawler.py` file that does the walking.
* The `main.py` file.

TODO
----
* Maybe record the config file in the database. Maybe suck the config
  info out of the database. Buid infrastructure to manage multiple
  crawls.

HOWTO
-----
The use of this code is made difficult by the fact that there are no
up-to-date, easily-to-install packages for the AtomSpace. It must be
installed by hand, from source. The git README's provide details.
Install both the [AtomSpace](https://github.com/opencog/atomspace)
and [AtomSpace-Rocks](http://github.com/opencog/atomspace-rocks),
which provides  an on-disk storage method backed by RockDB. In
addition to Rocks, there is an entire distributed storage and
communications architecture. That is, you can do more, than just
store to disk.


