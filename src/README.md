Tools
-----
Not much here yet. Directories:

* `catalog`: the crawler, for populating the initial database.
* `webui`: the main control panel.

TODO
----
Some general ideas.
* If a directory has files with hash miscompares, and that directory
  is under git control, then perhaps git can offer an explanation of
  what is happening to that file.

* Is there any point at all for coupling this into any kind of
  intrustion-detection framework? After all, we are generating file
  hashes, which are weak file fingerprints.
