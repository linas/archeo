Meta: Sensory systems
---------------------
This README contains a meandering discussion of sensory systems.

If not already clear, this project is very much about the development of
a sensory system in Atomese. Conventional human sensory systems are sound
and vision, but of course, science offers many more: wind velocity,
temperature, density and composition. These are fields, usually in 3D
space. But there are also phylogenetics, movement of human populations
and the intermingling of their genetic content, their cultural content,
the local spoken dialect, customs, beleifs in gods. The later are all
complex relationship networks that change over time, and their
characterization and understanding is a modern scientific undertaking.

### A simple, concrete network
A filesstem, especially a filesystem changing over time, offers a simple,
immediate, direct example of a complex network whose structure can be
explored. Conventionally, this is done with file browsers, or command
line tools like `cd` and `ls`. More recently, web browsers allow point
by point inspection of individual web pages. Social networks, such as
facebook or twitter, allow point-by-point inspection of more abstract
data.

The task for an AGI is how to intake, onboard and process sensory
information from an exterior world, and thereby "understand" what is
going on "out there". The relation between "self" and "outside world"
is mediated by the sensations. The meta question that I would like to
explore here is the process and act of sensing the environment.

To do this, I can blather on abstractly. Or I can write code to actually
do it. The goal of using the file system as an "external environment"
that can be observed is that it avoids the pitfalls of know-it-all AI
approaches. Vision and sound are too obvious, and too easily dismissed.
Natural langauge text is susceptible to LLM approaches all to easily;
and so "reading" is not conventinoally understood to be a sensory act.
The filesystem provides the small, simple, direct and easy-to-work-with
example of a network that can be sensed.

### The engineering trap
The filesystem is a well-understood concept, and so it is all to easy
to fall into the enginering trap: we already know what we want, so all
we have to do is to write some shims, some connectors, some file crawlers
and content digesters, and bingo, done! This is a trap, because I am
doing all the thinking, not the AGI: I decide what is important, how
things fit together, how to represent file structures in Atomese. The
"I" here is the software-writing engineer and developer. The goal here
is to discover a colleciton of sensory algorithms that can process
network information in the abstract, without my intervention as designer.

Sadly, I am falling into that trap. I do not yet understand the generic
sensory process sufficiently to just write generic code. So I am very
much in the middle of hand-crafting a very specific system, targeting
the filesystem. Someday, it can be replicated and generalized to social
networks, genetic networks, economic networks, and the like. But right
now, I don't yet understand the general principles, so I have to muddle
along.

As far as I know, no one has done this. We don't have some generic
network analyzer that can be deployed for electrical circuits,
protein-gene reactomes, financial transactions and historical events.

Eventually, I hope to have some pearls of wisdom here about neural nets,
but not yet. I have the vague inkling that neural nets do provide a
means for building a generic network analyzer, but I don't know anything
about that, yet.

### Current design
Some notes about the current design.

* The URL has been selected as the primary, unique coordinate on the
  abstract space of the network. This is because it really is "unique":
  at a fixed instance in time, there can only be one "thing" that the
  URL refers to.

* Items at the endpoint of URL's have "properties": a filesize, a
  content hash, a date-last-modified. Perhaps more, say, mime-type.
  The properties appear to be "flat" and unstructured. The filesize
  and modification time are numeric scalars. A mime-type is a one-of-N
  selection, but still a scalar. There is no network connectivity
  encoded in the properties, other than that collections of URL's
  may have shared properties.

* The primary goal of analysis is to arrive at an understanding of the
  sets of URL's that have shared properties. What, exactly, does this
  entail? Lets list some of these.

  -- The sets of URL's all having the same value for some given property
     (e.g. all URL's having the same filesize)
  -- The set-theoretic intersection and union of such single-property
     collections.
  -- The set of all possible intersections and unions itself forms a
     network, called a "lattice". The standard math tools for lattices
     are boolean algebras, frames, locales.
  -- The measure of similarity of such sets, including simple overlaps,
     conditional probabilities, mutual information.
  -- Syntactical structure among these sets. For example, given a clique
     of N sets, there is a spanning tree that can be deduced by selecting
     only those links with maximal mutual information.
  -- Recursive syntactical structure, obtained by re-applying the above
     segmentation at the next abstraction level.
  -- Things that LLM's can do. I'm not sure what those things are.

* Time has been selected as the primary, unique linear dimension along
  which the network can be observed. Observations consist of snapshots
  of the network at given points in time. The primacy of time seems
  overwhelming. General relativity aside, time seems to be something
  that flows, separating past an future. Sensory systems are necessarily
  in the "here and now". Of course, a sensory system could just analyze
  a single snapshot of some dataset taken at some point in time. But the
  overall passage of time is a sensory inevitability.

* The current design captures the passage of time by "witnessing" a
  set of properties associated to a URL at a given instant in time. This
  forms a snapshot of the network, from which timelike dynamics can be
  observed.

### Atomese Technical Issues
Despite almost a decade of development, Atomese still has a variety of
shortcomings, exposed by the analysis above. Lets ponder these.

There's a lack of generic similarity tools. Yes, the `learn` project
has a collection of tools for computing mutual information, and
classifying and clustering. However, these lack a generic API. Adapting
these to observe structure in a file system requires a lot of by-hand
engineering (and redesign, re-implementation).

The reason that re-design, re-engineering is needed is because the
abstraction level is somehow wrong. I can't say "here's a bunch of URL's
with a bunch of associated flat properties, have at it".  So I guess
one of the goals here is to obtain the appropriate abstraction level.

I have a deeply-held beleif that the recursive application of structure
extraction is a key to AGI, but this remains unproven because its
unimplemented, because the structural abstractions needed to perform
similarity measurements and syntactical reltions on generic networks
remain uncaptured. The correct API is groped at, but is challenging
to create.

Meanwhile, I've failed to ponder neural nets sufficiently. I do not
understand how to apply a neural net to solve the narrow scope of
issues in this project (the narrow scope being to identify corrupted
files.)

### Nuts & Bolts
What am I actually doing?

I've hand-designed an Atomese representation for file system data and
snapshots of properties. This is because I know that URL's are suitable
object identifiers (OID), and what file properites are. I'd like to have
AI automation for property discovery and for the discovery of OID's.

I'm hand-converting the Atomese representation into a python representation.
This is beccause the python flask webui system expects python dictionaries
and not Atomese. Both the python dicts and the Atomese contain "the same
info", just in different systems. I would like for this to be automated.

Automation of Atomese->python dict conversion requires a very uniform API
to be given to the Atomese properties: they really do have to be "flat",
or else the conversion fails.  This converter is again hand-engineered,
and it is not clear how to use AI automation to generate the required
code. Any kind of hand-built automation tool suffers from multiple
defects:
* It is hard to build, because the abstraction levels ar high up and hard
  to master.
* It is hard to debug, because mistakes at high abstraction layers cause
  failures whose signatures are hard to trace back to the failing code.
* It is fragile, in that minor changes can create hard-to-debug bugs.
* It is intellectually isolated. No human is reading what I write here,
  It is even less likelikely that anyone will look at the automated
  converter, understand why it is needed, what it does, and how to use it
  to solve their own special problem using this generic tool.
  That is, the audience is too small. The audience is of one: me.

I have poor control of search and siplay parameters. For example:
duplicates are shown, when there are 2 or more of something. The number
2 is a paramter and its hard-coded. Exposing it in the web page is a
pain in the neck: one moer thing to wire up and connect, one more thing
to explain.  I'd like to have AI automated wiring.

Another example is the max number of items to display. Right now, this
is unbounded, leading to poor performance when there are thousands of
objects to display. Again, this is a control parameter that needs to be
wired into place.

It needs to be wired in two different ways: narrowly, into the GUI, and
generically, as part of the control system for performing AtomSpace
queries. This is again the "engineering trap": I am carefully hand-crafting
a specific system, having specific controls. There are two parts to this
engineering:

* I have to think of what I want (e.g. control the max number of displayed
  files in a table)
* I have to implement the code to add this control.

The second bullet is interesting, because the implementation of this code
is a mostly mechanical process. I have to know what files to edit, what
structures to touch, but, to a large degree, its "do it the same way that
the other controls are done".

The second bullet is already abstracted in the MVC Model-View-Controller
paradigm. I don't want to hand-implement the desired MVC at each stage,
I want to automated the production of the MVC linkage.



