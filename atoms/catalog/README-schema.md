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
would be to witness the file content hash. This could have the form
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
This looks a lot like the above, except the `SetLink` is gone.

Tags are non-centralized, in that one thread (process) can be adding
one tag at the same time that another process is adding another: there
is no need to pull all set members into a centralized location before
the set can be minted. Tags can be added in a decentralized fashion.

The downside to this is that tags can also be removed at any time; thus
they are not secure. For the present use-cases, this means that witnesses
can be tampered with. This is far out of bounds, but collections of Atoms
can be cryptographically signed, and the signatures be built into a block
chain.

Meta issues
-----------
The engineering/design meta-issue rises again.  How do I know that it is
important to have file witnesses? How do I know that file content hashes
are the things that need to be recorded? How do I know that the objects
I'm dealing with are files? How do I know what a file system is, and how
do I know the characteristics that it has? How do I know that these
abstractions are the appropriate ones to make, and that this is the
correct design?

The answers to these questions are all obvious to the (software) engineer,
because the creation of software designs are the primary activity that
software engineers engage in. But how does the engineer "do" these things?
How does the engineer accomplish them?

The obvious answer is that the engineer goes to school, gets trained and
learns from experience on how to convert verbal descriptions of software
artifacts into functional computer code. The engineer reads lots of specs,
remembers how things work. The engnieer measures performance, and thus
knows what designs are performant. The engineer factors and refactors code,
and thus develops a taste for what things "go together", what a module
should be like, and what a good API is. These are all learned from
experience.

It is perhaps incorrect to think that there is some simple magic wand to
be waved around, thus obtaining modular design and API wisdom. It is
tempting to think that perhaps there is some Bayesian similarity factor,
or perhaps some Ising model that can be applied to software systems, and
that by letting this model percolate, an ideal module and API pops out.
Perhaps there is such a system. It would be very un-human-like in how it
arrives at optimal solutions.

Perhaps I could even design an Ising-model-inspired lambda-calculus
combinator and optimizer. But this just shifts the location of the
problem: how do I know that Ising models and lambda calculus are the
appropriate abstractions?


The End
-------
That's it. I think I'm done. What else is there?
