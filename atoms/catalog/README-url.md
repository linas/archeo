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

Another way of thinking about the ExecutionLink is as a rewrite rule.
For this, Atomese specifies a `RuleLink`, along with helper links so
that the RuleLink can be used for term rewriting, forward and backward
chaining, etc. It has the `LambdaLink` as a base class, with lambdas
meant to correspond to conventional lambda-calculus lambdas. The
implementation includes niceties like automatic alpha-conversion and
automatic prenex ordering.
