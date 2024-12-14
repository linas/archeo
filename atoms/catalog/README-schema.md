Atomese schema
--------------
This README documents the Atomese structures that will be used to
track filesystem status. It should be accurate at the time of writing,
but since Atomese allows mutable data structures, it may be outdated
by the time you read this.

The following will be tracked:

### URL
The full string URL, in conventional formats. e.g.
```
   (Item "file://hostname/some/path/to/file.mp3")
```
See [File URI scheme](https://en.wikipedia.org/wiki/File_URI_scheme)
on Wikipedia.

### Content Hash
The file content hash will be encoded as a string. The string will be
"bare" without any further encoding info (such as length, hash type, etc.)
```
   (Item "abcdef123456")
```

### Other Info
All other info (including dates) will also be kept in `ItemNode`, as
strings.  No effort will be made to provide special support for dates
integers or any other primitive data formats. Everything is a string.

Thoughts: Yes, the AtomSpace *could* provide more primitive types.
For example, the current AtomSpace implements a `NumberNode` that
stores a vector of floating-point numbers. This is of only marginal
utility: it does not make the storage size smaller (it does not reduce
disk or RAM usage). It improves performance, only if fed into a
processing pipeline that works with floats.

It appears that the only times that custom Atom types are needed is
when the operations to be carried out are complex (and thus need to
be coded in C++). Primitive types such as "Date" or "Time" do not
(currently) seem to have much utility. So they are not used here.

The meta issue is an old software/hardware engineering issue: which
data types, abstractions and operations are worthy of being bundled
together into a modular unit, and which are not? The current AtomSpace
design made some ad hoc assumptions about what should be bundled, and
this is just like every other piece of hardware or software out there.
There is no automated system for figuring out how modularization should
be performed.

### Relations
All relations will use the conventional `EdgeLink` with `PredicateNode`
to tag the relationship name. Think of the `PredicateNode` as being like
a column name in an SQL table, or an attribute name in a JSON/YAML file.

#### Content hash
A file URI is labelled with its hash:
```
   (Edge (Predicate "content xxhash-64")
      (List (Item "URI...") (Item "abcdef")))
```

#### Other predicates
Other predicates that record file meta-data are:
* `(Predicate "file size")`
* `(Predicate "last modified date")`
These are self-explanatory. Yes, I suppose file UID, GID, attrs
(`ugo+rwxt`) and xattrs should be recorded. And also the file type:
pipe, char device, block device, etc. Disinteresting at the moment.

#### Content witness
The key functional activity is to create a record or "witness" the
existence of a file with some specific metadata at some specific point
in time. This is record can be used to establish a time-line of the
changes seen in a file.  The witness applies a time-stamp to a particular
collection of data (such as file metadata). The prototypical example
would be to witness the file content hash. This would have the form
```
   (Edge (Predicate "witness")
      (List
         (Item "Jan 1, 1970 00:00:00 UTC")
         (Set
            (Edge (Predicate "content xxhash-64")
               (List (Item "URI...") (Item "abcdef"))))))
```
The use of the `SetLink` allows an arbitrary collection of data to be
wrapped up. If this were SQL, then the witness would be recording the
primary key of the SQL table record it was witnessing. But in Atomese,
the simplest way to do this is as above. Of course, a "primary key" or
index could be added into the above, but this kind of defeats the whole
point of hypergraphs: hypergraphs allow you to avoid the hassle and
overhead of maintaining keys in all of your records.

There is a design problem with `SetLink` in the Atomese. Sets don't
scale. It's effectively impossible to add a member to, or remove a
member from a set. To do this, the set needs to be dissolved and
reconstructed.  Dissolution is impossible, if that set is inside of
another `Link`, because Atoms are immutable.

The other issue is searchability and pattern-matching.  Unordered
matching of N items requires N-factorial permutations, and this becomes
unacceptable even at modest values of N.

The way to get around this is to use set membership links instead:
```
   (TagLink
      (TagNode "witness")
      (List
         (Item "Jan 1, 1970 00:00:00 UTC")
         (Edge (Predicate "content xxhash-64")
            (List (Item "URI...") (Item "abcdef"))))))
```
This looks a lot like the above, except the `UnorderedLink` is gone.
