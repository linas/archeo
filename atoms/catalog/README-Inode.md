
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
A directed, labelled graph edge can be drawn, using ascii-art, as
follows:
```
                  edge-label
    named-tail ----------------> head-with-name
```
In [Atomese](https://wiki.opencog.org/w/Atomese), this is written as
```
    (Edge
       (Predicate "edge-label")
       (List (Item "named-tail") (Item "head-with-name")))
```
The native form for Atomese is s-expressions, but the above can be
written in python syntax, simply by rearranging the parenthesis and
adding some commas in strategic places:
```
    Edge (
       Predicate ("edge-label"),
       List (Item ("named-tail"), Item ("head-with-name")))
```
A hyper-edge has the clunky ascii-art:
```
                link-label       +------------------------+
    tail-node ------------\      |         link           |
                           \-->  |  anode -------> bnode  |
                                 |                        |
                                 +------------------------+
```
The box is meant to show a hierarchical arrangement. The arrow to the
left is pointing to the box and everything in it. This arrow is called
a hyperedge, only ecause the box is not a simple vertex, but a compound
object.  The hierarchical structure is much much more obvious when
written out as an s-expression:
```
    (Edge
       (Predicate "link-label")
       (List
           (Item "tail-node")
           (Edge
               (Predicate "link")
               (List
                   (Item "anode")
                   (Item "bnode")))))
```

Representing Directory Trees
----------------------------
The obvious hierarchical structure suggests an easy, simple and poor
idea for representing a filepath. For example, the path `/usr/lib/X11`
can be represented as
```
   (Edge (Predicate "dirent")
      (List
         (Item "/")
         (Edge (Predicate "dirent")
             (List
                (Item "/usr")
                (Edge (Predicate "dirent")
                   (List
                      (Item "/lib")
                      (Item "/X11")))))
```
Perhaps a bit verbose, but having an obvious structure. The flaw with
this design becomes evident when contemplating a directory `/usr/lib`
with a thousand entries. It would require a thousand of the above
s-expressions. Now, s-expressions can be represented fairly compactly,
but still, each Atom in the s-expression does use RAM. (An Atom is an
s-expression with balanced parenthesis, where the name immediately
following an open-paren is a type, the Atom type.)

### DAGs
One can simplify the above by just using ordinary arrows (and not
hyperedges), and creating a graph that way: a directed acyclic graph
or DAG. Sounds great! What can go wrong?

Plenty. Imagine the DAG for `/usr/lib/X11` and `/var/lib/ceph`. These
are obviously different and unrelated directories in a file system,
but if we try to draw an arrow from `usr` to `lib` and from `var` to
`lib` ... uh-oh. The two `lib`s are not the same. If a string name is
used, there's trouble.

### Inodes
One way to get around this is to issue a unique ID number for each
directory. This number is conventionally called an
[i-number](https://en.wikipedia.org/wiki/inode) One way to issue
i-numbers is to simply count up. This causes problems in
multi-threaded, distributed (decentralized) apps: the `i++`
must be performed atomically, under a lock, in exactly one place
in the entire universe.

### Decent
A different idea is to generate a strong cryptographic hash, say SHA-256,
and use that to uniquely identify every directory. The large hash is
needed to avoid the birthday paradox. Sounds good, but storing 256 bytes
for ever directory is ... not efficient.

### URL's
There's a fourth way. It's comical, its stupid, its clever, its deranged,
its magic, its obvious, its efficient and easy and compact and it works.
Use a URL.

You read that right. The U in URL stands for Unique, and that's exactly
what is needed. We can know that the `lib` in `/usr/lib/X11` is a
***different*** `lib` from the one in `/var/lib/ceph` because everything
in the `string` that came before `lib` is ... different. Unique. Also
its compact, only 4 bytes in this example, human-readable (unlike SHA-256)
and, uhhh, heh, "decentralized": any thread or process can easily (trivially)
and uniqely compute it in parallel, without any collisions. Quite remarkable.

Hypergraph representation of URL's
----------------------------------
The above states that the best hypergraph representation for a file is
the trivial one, as a single node:
```
         (Item "/string/path/to/with/slashes/to/the/file.mp3")
```
The issue with this representation is searchability. To fine all
instances if `file.mp3`, we need the following representation:
```
   (Edge (Predicate "dirpath")
      (List
         (Item "/string/path/to/with/slashes/to/the/")
         (Item "file.mp3")))

   (Edge (Predicate "dirpath")
      (List
         (Item "/a/different/path/to/the/")
         (Item "file.mp3")))
```
The AtomSpace in-RAM representation of the above two hypergraphs are
such that if you have the node `(Item "file.mp3")`, you can trivially and
immediately find *everything* pointing it it, such as the two paths
shown. The Atomese query for this is trivial. (This is why Atomese
beats the pants off of SQL, at least for usability.)

In the above example, there's a common subdirectory: `/to/the/file.mp3`
appears under distinct roots. This happened presumably because one
location is the "original", and the other is a "backup copy" that
someone made sometime in the past. The goal of the Archeo project is
to find not just common files, but common subdirectories. This
suggests that the hypergraph representation should also include the
following:
```
   (Edge (Predicate "dirpath")
      (List
         (Item "/string/path/to/with/slashes/")
         (Item "/to/the/file.mp3")))

   (Edge (Predicate "dirpath")
      (List
         (Item "/a/different/path/")
         (Item "/to/the/file.mp3")))
```
As before, the query to find all parent dirs for
`(Item "/to/the/file.mp3")` is trivial and extremely fast. The price for
this is more memory usage. A file listed N directories deep requires N
different splits, if all possible subdirectories are to be found. This
is somewhat wasteful of space, but perhaps not all that bad.

To save space (and trade it for time), these multiple splits of a path
do not need to be permanently stored in the file records. Just one split
(or the unsplit version) needs to be stored; all the others can be
generated as needed, on the fly. The algo to generate them is effectively
trivial. All metadata (timestamps, content hashes, witnesses, etc.) can
be stored with the one copy.

Conclusion
----------
The final proposal, discussed at the end, seems to provide the best
hypergraph representation that fits the needs of the Archeo project.
Its easy, its fast, its obvious. We'll see how well it works.

Of course, now that we've discovered a simple and magical representation,
there's no particulare reason to use the Atomspace for this. The
representation is so simple that it could easily be implemented in SQL,
and would probably be more compact. Atomese was designed for complex,
mutable and rapidly changing graphs. This is not not complex, and is
effectively static, completely unchanging. Statically-defined SQL tables
set up at the dawn of time would probably work just fine. I guess.
Since no one is reading this text anyway, it probably doesn't matter.
