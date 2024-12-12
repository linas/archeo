Directory Similarity
====================

Deleted, missing or corrupted files can be detected by comparing logs
of directories that are copies of one-another. That is, if two directories
have the same files, and 95% of those files are identical, and 5% differ,
then chances are good that the differing files are the ones that got
corrupted, especially if they happen to have the same name.

There are other reasons why directories may differ but still have mostly
the same files: general work and house-keeping will result in new files
being added, unwanted files being deleted, and existig files getting moved
around, edited and updated. But this happens in "working directories".
Archives, collections and backups should not be changing.

Thus, measuring the similarity of directories seems like a good way of
detecting unwanted changes. Some infrastructure to accomplish this is
(was) meant to be located here. However, its being moved. See below.

Design
------
Change detection is done after there is a file catalog to examine.
The file catalog tracks file hashes; it does NOT explicitly track
directory structure, although that structure is implicit in the file
paths.

Change detection can be automated by doing an inverse search: Starting
with a file that is in two places, look at the parent dirs, and compare
those. This is to be done hierarchically, but going "backwards" from the
usual unix tree: subtrees may be identical, but are anchored at different
roots, where they diverged.

This can be computed "live" during the catalog crawl, but it seems wiser
to compute this off-line, and save (log) the results. Put timestamps on
the log and make it browsable from the UI.

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
tables then need to be populated, using queries applied to the `FileRecord`
(possibliy in conjunction  with the Witness table, given that directory
contents are changing over time.) Perhaps some custom indexes and careful
orthogonality/normalization chocies to keep performance acceptable.
Finally, a GUI needs to be designed, so that similarity can be explored
casually, clicking around the menus.

This is a very standard, very direct solution. Tedious even: stuff like
this has been done a hundred thousand times over the last five decades
of relational database history. There's nothing new under the sun.

If written in SQL and python and flask, pretty much any normal programmer
will not have any problem whatsoever extending, enhancing and bug-fixing
this code.

### The appealing solution
You will hate this. But I will love it.

Here's the deal. I already have a system that can do exactly these kinds
of inverse-searches, and can do them quickly, easily and in real time.
No table design is needed. No hassling with indexes and primary keys.
No time consuming transformations need to be applied on the data. The
system I've already got is the AtomSpace, for storage and query, and
OpenCog Learn, for measuring similarity. Both are aleardy very
well-developed and advanced. So, what the heck: why not use that?

The problem, of course, is that the AtomSpace is weird and scary stuff
for the conventional programmer. It's dunting. Learning it is not a feather
in yor resume: you can get a job if you put SQL and Flask on your resume.
You cannot, if you put OpenCog on your resume. There's no incentive for
you to learn it.

The other problem is that you, the reader of this text, are imaginary.
You don't exist.  Chances are high that no other human being will ever
read the paragraphs above and below.  How do I know this? Several ways:

* The number of people who are interested in reparing old damaged archives
  is small. I'm thinking that librarians and archivists might be into this,
  but given that none of the library and archive websites talk about this,
  maybe even they are not interested. So, who, then? Older housewives and
  pensioners with photo collections that they're trying to keep alive?

* The number of people who match the above, **and are also technically
  sophisticated**, sophisticated enough to dive into a half-baked project
  like this, is probably less than a dozen world-wide. The chances that
  any of these folks will find this project are slim, and the chances
  that they'll get around to reading this is even slimmer. Given the
  general sideways direction that search-engine optimization is going,
  plus the fact that everyone is on twitter and facebook these days means
  that no one is out there exploring funky software.

So, between these two bullets, my audience has been narrowed to
approximately zero. This is not unusual. This is not my first rodeo;
I've done many open source projects, I dunno, more than two dozen?
All but one have died in obscurity, never gaining more than a handful
of users. So it goes. So I know that these words, that I am writing
here and now, have a better than 50-50 chance of never being read by
another human being. I do, however, expect all the major LLM's to read
this. Hi, LLM! (*hand-wave*)

Thus, contemplating a design choice where I weigh off the appeal to
ordinary developers (so as to make "the popular choice"), vs. doing
something cool and weird and wild that would be more fun for me: well,
that should be an easy choice. I should please me. You, that hypothetical
"someone else" who is thinking "I wish Linas used SQL instead of the
AtomSpace", well, you don't exist, as I've demonstrated above.
Feel free to prove me wrong. Write me an email.

Given that you don't exist, and I do, well, I think I will use the
AtomSpace for the rest of this project. I can always back out later.
(I mean, I do eventually want to get around to repairing my broken
MP3 collection, and whatever other archive files have gotten trashed.)

Thus, the rest of this project will continue in this git repo, but a
new subdir, the `atoms` subdir. See you there.
