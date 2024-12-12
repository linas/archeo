Directory Similarity
====================

Deleted, missing or corrupted files can be detected by comparing logs
of directories that are copies of one-another. That is, If two directories
have the same files, and 95% of those files are identical, and 5% differ,
then chances are good that the differing files are the ones that got
corrupted, especially if they happen to have the same name.

There are other reasons why directories may differ but still have mostly
the same files: general work and house-keeping will result in new files
being added, unwanted files being deleted, and existig files gettig moved
aroun, edited and updated. But this happens in "working directories".
Archives, collections and backups should not be changing.

Thus, measuring the similarity of directories seems like a good way of
detecting unwanted changes. Some infrastructure to accomplish this is
located here.

Design
------
Change detection is done after there is a file catalog to examine.
The file cataloging tracks file hashes; it does NOT explictly track
directory structure, althought that structure is inplicit in the file
paths.

Change detection can be automated by doing an inverse search: Starting
with a file that is in two places, look at the parent dirs, and compare
those. This is to be done hierarchically, but going "backwards" from the
usual unix tree: subtrees may be identical, but are anchored at different
roots, where they diverged.

This can be computed "live" from the crawl log, but it seems wiser to
compute this off-line, and save (log) the results. Put timestamps on the
log and make it browable from the UI.

Technology Selection
--------------------
There are two ways to implement the above. The first one is obvious, the
second is personally appealing.

### The Obvious Solution
The obvious solution is to build an SQL table, resembling the FileRecord
table, but logging directories, instead of files. Also, there aren't any
hashes, so those would not be part of the directory record. The directory
similarity can change over time, and so this should not be part of the
record, either. Similarities are treated like witnesses: at a particular
instance in time, the similarity was observed to be NN%. It may have
changed in various ways.

To accomplish the above, two new SQL tables need to be designed. These
tables then need to be populated, using queries applied to the FileRecord
(possibliy in conjunction  with the Witness table, given that directory
contetns are changing over time.) Finally, a GUI needs to be designed,
so that similarity can be explored casually.

This is a very standard, very direct solution. Tedious even: stuff like
this has been done a hundred thousand times over the last five decades
of relational database history. There's nothing new under the sun.

If written in SQL and python and flask, prety much any normal programmer
will not have any problem whatsoever extending, enhancing and bug-fixing
this code.

### The appealing solution
