Tools
-----
Not much here yet. Directories:

* `catalog`: the crawler, for populating the initial database.
* `webui`: the main control panel.
* `similarity`: infrstructure for finding similar directories.

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
