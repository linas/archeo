
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
The box is meant to show a hierarchical arrangement. This is much much
more obvious when written out as an s-expression:
```
    (Edge
       (Predicate "link-label")
       (List
           (Item "tail-node")
           (Edge
               (Predicate "link"),
               (List
                   (Item "anode")
                   (Item "bnode")))))
```
