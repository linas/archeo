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
