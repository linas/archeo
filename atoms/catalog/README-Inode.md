
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
The obvious hierarcical structure suggests an easy, simple and poor
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
Perhasp a bit verbose, but having an obvious structure. The flaw with
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
`lib` ... uh-oh. The two `lib`s are not the same. 
