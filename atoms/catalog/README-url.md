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

Practical Examples
------------------
Lets try these, each in turn, and see what happens. The starting point
is a single node:
```
   (ItemNode "file://example.com/etc/X11/Xsession")
```
Note that `ItemNode` is used, and not `URLNode`, so the type is not known
a priori. The AtomSpace will contain  ItemNodes that are not URL's. This
creates problems with type identification and type matching that could be
avoided by using `URLNode`. For this text, its better to do things "the
hard way", because having explict type encodings is a luxury that perhaps
we can live without.

The below looks at the execution-style, the jigsaw-style, and the unix-style
for decoding this URL.

### ExecutionLink
The conventional Atomese for decoding would be to construct
```
   ExecutionOutput
      GroundedPredicate "py:decode_a_url"
      List
         Item "file://example.com/etc/X11/Xsession"
```
where "py:decode_a_url" calls some blob of python code that imports
some off-the-shelf python URL decoding library to split the URL.
Calling `cog-execute!` on the above would return
```
   ExecutionLink
      Predicate "decoded URL"
      List
         Item "file://example.com/etc/X11/Xsession"
      List
         Edge
            Predicate "protocol"
            Item "file"
         Edge
            Predicate "domain"
            Item "example.com"
         Edge
            Predicate "path"
            Item "/etc/X11"
         Edge
            Predicate "filename"
            Item "Xsession"
```
The output is a collection of key-value pairs. These are explicitly
written out as Atoms, as opposed to Values, because we want these
to be explcitly searcahble during similarity calculations. That is,
it must be possible to write a query that asks for all URL's that have
"example.com" as the domain name. Such queries are not possible if the
key-value pairs are stored as Values.

The primary issue with the above design is that URL's need to be split
before the query is performed. That means that there must be a preliminary
step that loops over *all* URL's in the AtomSpace, and splits them.
Splitting generrates about ten atoms for each URL, (ignoring overhead
associated with incoming sets, etc.) Thus, this splitting step risks
blowing up the size of the AtomSpace. Storing the splits as Values
doesn't really help; it shaves off the incoming sets, but that's all)

To add injury to insult, sloppy use of Storage risks saving this redundant
data to the database. So we blew up RAM usage, and risk blowing up storage,
just because the query engine cannot perform searches on "compactified" URL's.
Can we redisng the query engine to do better?

### String Regex
The query engine performs matching based on Node type and Node string,
and that's it. Given that we know that the Node name is a string, perhaps
we could do some sort of regex string compare?  The regex is a very compact
notation for specifying complex string patterns. It is certainly far more
compact than Atomese (and this has benefits for RAM and storage). There
are well-developed and well-maintained regex libraries out there, so having
a regex compare on the Node name during the pattern query is not an
outrageous ask. How might this look?

The regex to select the domain name is
```
.+\:\/\/(:alphanum:+,$1)\/.+
```
Or something like that. I might have a bug in the above.  Writing regexes
is hard. They are often buggy.  There is a risk of accidental matches to
things that are not URL's.  The biggest issue is that, well, regexes are
not Atomese! That is, we very much want a unified framework where all
computation is done in Atomese. Regexes break this, unless a module to
convert Atomese to regexes and back is provided. Heh. And how should the
encode/decode of regex to/from Atomese look like? Maybe like a URL
encode/decode?  See, the problem is generic.

Anyway, lets suppose there was regex support in the query engine. What would
that look like? It would need to be
```
   TypedVariable
       VariableNode "$X"
       TyepNode "ItemNode"
       RegexNode ".+\:\/\/(:alphanum:+,$1)\/.+"
```
This would accept as a match any node that was an `ItemNode`, and matched
the regex. What should the grounding be? It could be either the original
matched ItemNode, or it could be a new ItemNode that has the matches $1 as
its string name. i.e. a rewrite is performed upon grounding. Yuck. With
the query engine, we've been careful to split out term rewriting as a
distinct step, and backing off on this now seems like a bad idea. Thus,
the grounding needs to be the original node, with the above being an
accept/reject pattern, and then a distinct rewrite step at the end.

I don't like where this is going, so I'm going to set this down for now.

### Expansion during query
The current query engine uses two types of predicates to determine
matches: concrete Atoms, using the `PresentLink` and virtual Atoms,
which come in two types: the built-in virtuals, such as `GreaterThanLink`
and the `EvaulationLink` used in combination with the `GroundedPredicate`.

How might this look, if we wanted to search only for those URL's that
had "example.com" as the domain name?  The following would work:

```
   EvaluationLink
      GroundedPredicate "py:url_decoder"
      List
         Variable "$url"
         Predicate "domain"
         Item "example.com"
```
Perhaps better would be this:
```
   EqualLink
      Item "example.com"
      ExecutionOutputLink
         GroundedPredicate "py:url_decoder"
         List
            Variable "$url"
            Predicate "domain"
```
The above is nice, because it explicitly exposes the equality compare
to where it can be seen by other algos (and thus manipulated by any
algos that know what equality actually means.)

If the predicate was built in, it would have the compact form
```
   EqualLink
      Item "example.com"
      UrlDecoderLink
         Variable "$url"
         Predicate "domain"
```

Expansion during query has a huge performance penalty: to determine
if some URL contains "example.com", *every* URL must be examined. By
contrast, the pre-decoded form has a nearly instant, trivial solution:
just look at the incoming set of `(Item "example.com")` and every such
URL is instantly available. This is because incoming sets behave as
de facto built-in indexes, and just like SQL DB's, if you have an index,
then a lookup in the index is nearly trivial.

The situation is even worse if doing a join through an unknown domain:
in this case, one risks N-squared decodes to perform the compare, vs.
a log N index lookup.

Dynamics
--------
The above sketches two performance-space tradeoffs; are there other ways
to split the problem?

One possibility is to create a child AtomSpace (or "frame"), treat this
as a temporary scratch space, do computations, and discard when done.
The expansion of URL's into components is done in this scratch space.

How is this expansion done? The conventional answer is blunt-force
trauma: create a black box that does the expansion, and make yourself
feel good about this violation by calling it an "agent".

The Atomese way of doing this is to apply a single-pass query and
rewrite. Best to be explicit. Lets assume all URL's are tagged in some
way; for example
```
   Edge
      Predicate "URL"
      Item "file://example.com/etc/X11/Xsession"
```

The Atomese to apply a rewrite to all URL's in the current AtomSpace
is
```
   Query
      Present
         Edge
            Predicate "URL"
            Variable "$X"
      ExecututionOutput
         GroundedProceedure "py:split_a_url"
         List
            Variable "$X"
```
That's it. Executing this will traverse all URL's in the current
AtomSpace and apply the proceedure to the search results, one by one,
as they are encountered.

The point of writing this as Atomese is that this allows some
hypothetical meta-level algorithm to perform reasoning on what this
query does.

The above performs a bulk rewrite. This is fine if the goal is to do it
once on a static dataset, but is sub-optimal if new URL's are constantly
flowing into the system. In this case, the bulk query is to be replaced
by a stream process. There are multiple demos and explanations of how to
do streaming in Atomese. Is it worth reviewing these?

