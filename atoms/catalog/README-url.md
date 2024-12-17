URL Splitting
=============
The WWW has taught the world that the URL is a compact and easy-to-use
unique locator for a resource. As a string, its got a fixed format, it's
easy to parse, it contains structured info about domain names, port
numbers, filepaths and more.  Given that Atomese Nodes are also strings,
its a natural fit to store a file location as a URL.

However, it is also nice to extract the pieces-parts from the URL: the
domain name, the filepath, the filename itself. How should this be done?

The conventional answer is blunt: just do it. This is python. Just import
some URL-splitting python module, read the documentation, use it. Done.

That's a reasonable answer, but incorrect for the present application.
Again, the (meta-)goal is to uncover structural similarity. The toolset
is meant to be built on Atomese, and so the structures have to be
representable as Atomese, and accessible as Atomese.

So the question becomes: how should URL splitting (and reconstruction)
be handled in Atomese? As always, there are several alternatives.

### ExecutionLink
Atomese has an old and under-documented, effectively unused link type
called ExecutionLink. It can be repurposed for the present task. The
structure of the ExecutionLink was originally meant to resemble the
following:
```
   ExecutionLink
      PrediceNode "name of function"
      ListLink
         Atom "input argument 1"
         Atom "input argument 2"
         ...
      ListLink
         Atom "output result 1"
         Atom "output result 2"
         ...
```
In this form, it can be interpreted as a record of a named function,
showing the statically-mapped function values for the input. Indeed,
the `ExecutionOutputLink` replaces the `Predicate` by at
`GroundedPredicate`, and omits the output, because this is dynamically
generated. The `ExecutionOutputLink` is specified in detail and strongly
implemented in the AtomSpace. It's used in many places for many things.

### RuleLink, LambdaLink
Another way of thinking about the ExecutionLink is as a rewrite rule.
For this, Atomese specifies a `RuleLink`, along with helper links so
that the RuleLink can be used for term rewriting, forward and backward
chaining, etc. It has the `LambdaLink` as a base class, with lambdas
meant to correspond to conventional lambda-calculus lambdas. The
implementation includes niceties like automatic alpha-conversion and
automatic prenex ordering.

### Jigsaw pieces
The jigsaw-piece and connector concept is similar, but it attempts to
explictly eliminate the directionality of input/output, and replace
that with a generalized conception of mating rules specified by
`SexNode`s. The `SexNode` allows for more than just the binary types
(input/output, read/write, true/false, plus/minus) and their
conventional heterosexual mating rules.

URL encoding/decoding would be bi-directional (input and output are
flipped for encoding vs. decoding) but is still otherwise heterosexual
(there is a producer and a consumer).

### Unix open/close
Finally, there is the unix convetion of open, close, read, write. Unix
objects cannot be read or written until after they are opened. The open
and close functions can be interpreted ("given a semantics") of
establishing a connection, and then, once that connection is established,
data can flow across it. Atomese does not currently have a strongly
specified open/close semantics.

Another way to think of open/close is as a chance to run pre- and
post-operation hooks. Pre and post processing is generic in computer
science; this suggests that Atomese should have some semantic conception
for this.
