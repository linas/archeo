
Hypergraphs and Filesystems
---------------------------
The AtomSpace is a hypergraph database. A filesystem is, well, a
filesystem. These two are quite different, and so the question arises:
what is the best way to represent the one with the other? For the
Archeo project, there is no need to store file contents; only content
hashes. However, the general abstract idea of a filesystem structure
must be preserved. It has to be represented with (labelled, directed,
hyper-) graph edges. The final, ideal form, presented below, will
loosely resemble an [inode](https://en.wikipedia.org/wiki/inode)
structure.

To get to there, Some basics need to be reviewed, together with some
simple but inadequate designs.

Edges and hyperedges
--------------------
