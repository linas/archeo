Directory Similarity
--------------------

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
