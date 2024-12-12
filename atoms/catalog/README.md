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

HOWTO
-----
Step one: install the AtomSpace.


