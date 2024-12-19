
Archeo -- Data Recovery
=======================
Finding and repairing lost, corrupted, damaged data. The Archivist's
Friend.  Data Hoarders Welcome.  Data Archeology. Forensics. Longevity.
A Unified View of File System Data.

A Humble Start
--------------
Fifteen years ago, I copied 3376 MP3 files from one computer to another.
Where they sat, untouched, all this time. Today, I noticed that 683 of
these files differ. I looked at a couple. One was 2146766 bytes long.
The other was 2147789 bytes long. A difference of a thousand-something
bytes, but you know, identical files are supposed to be identical. Not
different. Maybe one is corrupted? But which one?

They both load just fine into `audacity`. They both play, just fine,
till the end. One had a tiny squeal, lasting a heartbeat. Barely. Both
files have fairly long stretches of zero bytes: file data which is zero,
for a bunch of bytes in a row. Is this normal?

This ain't good. I have maybe 1.5 million files. Not sure, haven't
finished counting. Wife & kids have more. I panicked. My panic is
justified. Out of those 1.5 million files, 1440 of them consist of
nothing but zeros (they shouldn't; they're photos, tar files...)

A quick search on the net indicates that ... what the heck, everybody
and their kid brother have this problem. More quick searching indicates
that there are lots of mini-tools, dribs & drabs that repair this and
that, usually specialized, maybe command-line, maybe graphical, maybe
obsolete. There are discussions on reddit, quora and stack exchange.
There's even AI-generated hallucinations. But there is no unified data
recovery tool. At least for Linux.  At least free, open-source, GPL'ed.

And so now I am writing these paragraphs. And I'm thinking of creating
software to help me with my recovery efforts. And I'd like you to help
me do this.

Goals
-----
Projects must have goals. A scope. A vision. A motivating dream which
inspires developers and sustains users. So here:
* Must solve my personal data corruption problem.
* Must be very easy to use, so I guess graphical, pull-down menu & all.
* Must allow plugins and modules for custom repair. There are already
  tools that fix MP3's, and other tools that fix photos. Use those.
* Use copies, when available. Figure out if one of the copies is good,
  and use that. But if there are two broken copies, maybe a single good
  version can be created by splicing these together.
* Search my old backups and archives for a good copy.
* Consolidate all my old archives and copies. They are everywhere,
  I don't even know what I have, or if its any good, and its all taking
  up disk space. Where is it? What is it? Is it rotten? Is it good?
* Provide "some level of" content integrity assurances.
* Start small, for home users. Expand to archives, libraries. Support
  databases and complex data. Allow data forensics and data recovery.
  Do things that data archivists need. Handle medical data, business data,
  science data. Scale to exabytes. Big-Ten accounting firms offer
  asset tracking for large accounts. IBM offers information management
  systems for large corporations. How do they deal with this?
* Build the foundations for AI.

Don't laugh at that last bullet. Yes, you and I both are tired of the
AI hype and the rather underwhelming results. But I'm being serious, here.
If you'll let me, I want to write a short essay about AI and longevity.

The Process of Living
---------------------
Living organisms heal themselves. A collection of data should be
self-healing. Living organisms know things and remember things.
A collection of data should know what's in it, what it's made out
of. It should know when some blob of data was last seen online,
or whether its now in cold storage.

There should be ways of exploring, finding, searching, discovering.
Knowing who you are, by knowing what you remember. Living organisms
have eyes for looking, for seeing. An AI/AGI needs sensory organs,
too, but for "seeing" collections of data. For finding and exploring
data, for living in a world not of tigers hiding in grass and rocks
falling from cliffs, but archives of social media posts.

Is this kind of software useful?
--------------------------------
Everyone is moving to the cloud anyway. Photos live on cell phones,
and are automatically synced to Google's cloud. If you run out of
storage, you can buy more for $X/month. This is an easy choice for
most users: why futz with a desktop computer, or worse, a Linux desktop,
when everything runs on the cloud? Of course, if you don't pay your
monthly fee, your data disappears.

Plan B is to buy a NAS storage box, and keep your stuff there. These
are expensive, but very very easy for most users: plug 'em in and go.
Is there secret, silent data corruption on a NAS box? Who knows? Are
you keeping backup copies? "Who needs backup", you might think, "I've
got RAID." This kind of thinking is fine, until "operator error" results
in a deleted file that maybe you really should not have deleted.

So the idea here is for the FSF purist: someone who wants fine-grained
freedoms to control their data, rather then being beholden to some cloud
provider who will wipe your data soon as you miss a monthly bill or two.
Someone who might be willing to use a proprietary NAS box, but would
like some way of double-checking.

This project is for the finicky and technically sophisticated user
(hobbyist?) who runs a Linux desktop or three at home, and worries about
their data. Perhaps one day, this project will be useful to archivists
or librarians. Maybe housewives and pensioners with family photo albums
and genealogy trees that they are safe-guarding. Perhaps even scientists
protecting their data, or business owners, who ... ???. But lets not
get ahead of ourselves. Let's take a closer look.


Data types
-----------
The issue, the meta-issue is that google, and many other on-line
social media and networking services (MySpace, anyone?) have a habit
of shutting down services that are not profitable. If you are lucky,
you might get a copy of your data.

More generally, you can't. When Meta/Facebook ditches you, you do not
have the option of downloading all your old posts and photos. Those are
gone forever. The insult is lack of due process: Facebook is judge, jury
and hangman. The injury is loss of connection, loss of data.

Some sources are just hard to backup. Chats on Discord. SMS and WhatsApp
messages (and photos, videos, sounds) Perhaps valueless for a younger
crowd. Perhaps more interesting if its from grandma, or a deceased loved
one.  There's nothing wrong with building a digital shrine for a lost loved
one. This is what love and cherished memories are about.  Perhaps one
day, the weight of the past will be too much. That is not today.

Version 0.0.8
-------------
Based on a few days of searching the net, I can't find anything even
vaguely close to what I want. And so, perhaps stupidly, I've started
writing a system. I've done this because this is kind of a blocker for
my migrating data from here to there, and specifically, from off my RAID
arrays and onto Ceph.

The current system architecture is minimal, and the implementation
was started two weeks ago. A basic filesystem crawler/cataloger has been
set up, and it works. A web UI has been prototyped.  See the *HOWTO*
below.

There are two prototypes. The first was written in highly conventional
SQL plus Python plus Flask for the Web UI. It was easy. It's not
complicated. Any ordinary developer can read and understand this code,
and hack on it.

The second is the same as the first, but replaces sqlite3 by the
[AtomSpace](https://github.com/opencog/atomspace). This was forced by
the general systemic shortcomings of SQL: its just not really the
appropriate tool for this particular job. The AtomSpace is much faster,
and much easier to use, and much more flexible. However, it took the
first prototype to (re-)discover this. The design decisions that lead
to this are reviewed in the
[similarity README](src/similarity/README.md) file.

Systems Survey
--------------
The [Systems Survey](Systems-Survey.md) is a lame attempt to list and
review related systems, or systems that could provide tools, or a
framework, or otherwise be deployed. Anyone out there care to move
this page to the project wiki?

Questions and Ideas
-------------------
Ideally, the system envisioned here "plays nice" with existing systems.
Perhaps its a module on existing systems. Perhaps the impleemntation
can make use of existing frameworks. How would this work?

* What do archivists and digital librarians do today? If they import
  a new data set, do they scrub it? How do they track multiple copies
  of what they have? Short answer: no, they do not. If they do, they
  do not talk about it, and it is not mentioned on their project
  websites. The assumption is, I assume, that they can trust their
  storage systems to not screw up.

* How do backup systems keep track of what's where? When the last backup
  was made? If the backup is corrupted? What are the existing open source
  backup systems?

* Intrusion detection systems store hashes of files, and detect corruption
  based on those hashes. If you don't have hashes of your old data, you are
  SOL. Are there systems or frameworks for tracking file hashes and other
  file metadata? Can these be used in data archival systems?
  Examples include Tripwire and FIM (File Integrity Monitor).

* File explorers and (graphical) file browsers... show files. Do any of
  them provide a framework for tracking data health? A meta-system for
  tracking backup copies? Some plugin framework?

* Systems like splunk are designed for admins who need to track error logs
  for hundreds of machines. Can the splunk dashboard and framework be
  repurposed for tracking archive health?

* Systems like wireshark can do low-level network packet inspection.
  Wirsehark includes a packet disasembly and formatting language. This
  has been used to create thousands of packet disassemblers, since each
  byte and bit in a packet can be named and labelled. Could this be used
  to disassemble and repair MP3 files? Tar files? Corrupted git archives?

* Disk drive forensics tools can pull apart corrupted disk images. Is
  there any kind of generic framework that can be used?

* How does one prevent damage, moving forward, into the future?
  Clearly, off-the-shelf mdraid+ext4fs plus consumer-grade PC's, disk
  drives and controllers are inadequate (because that's the setup I used
  for the last few decades, and now I have data corruption.) Stacked
  combinations of LVM, Btrfs, XFS are not obviously better. Ceph is a
  distributed storage system. The very first time I used it, I found data
  corruption errors. Perhaps Ceph is to blame, perhaps a disk controller
  is to blame.  Maybe a cosmic ray hit the system during file copy. Ceph
  is aimed at large clusters, not small users. Fully debugged if you have
  1000 OSD's on 100 hosts. But not so much if you have 3 OSD's on two hosts.
  There's no home-user Ceph community. There should be.

Design requirements
-------------------
In my current modest setup, I need these things:

* Log of which directories were copied from where to where, and when.
* Directory metadata: how many files? How many bytes?
* If the original version is still there, does the new copy agree
  with the old one?
* Can a compare of new and old be run on some peridoic basis?
  e.g. once a month? Twice a year? What was the result?
* Checksums. Compute and store checksums. Compare file contents
  by checksum.  Find files by checksum.
* Limit checksum collection to specific file types, similar to how
  locate, mlocate, plocate and updatedb work.
* When were these last computed? What was the matching file
  name? What was the file metadata at that time?
* Allow file validation plugins. e.g. JHOVE, Apache Tika or DROID
  can be used to determine if a file passes basic integrity checks.

Tech selection
--------------
* Should be possible for ordinary coders to modify and extend this
  project. Thus, python seems like a reasonable choice. Java seems
  overkill/awkward, and rust not popular enough. (And rust requires
  compiling).
* Data has to be kept somewhere. Ideally, configurable, in some
  database. Postgres, MariaDB and SQLite all seem viable. The first
  two feel like overkill. SQLite seems small, simple, easy for now.
* High performance is not a requirement. High usability is.

Tech re-selection
-----------------
The prototype version 0.0.6 was written in a very conventional stack
of sqlite3 for the SQL db, python for the programming language, and
python flask for the web ui. This stuff is widely used, widely
understood, and quite easy for ordinary developers to get into and use.

The prototype consists of a crawler that creates a file catalog, and
a web UI that can walk directories and explore the locations of similar
files. It works just fine.

For version 0.2, I want to add some rather sophisticated similarity
detection tools, described in the [similarity README](src/similarity/README.md).
While designing that, I realized that my sqlite3+python+flask stack is
not going to cut it, and that I already have much better tools: namely,
the [AtomSpace](https://github.com/opencog/atomspace).

The problem is that almost no one has heard of the AtomSpace, almost
no one uses it, and its a strange weird beast for ordinary programmers.
However, I've also realized that the number of ordinary programmers who
are going to join this project is approximately zero. So why should I
cater to them, these people who will never arriv and assist, anyway,
when there is something way more fun and useful to work with? So I'm
restarting this project on the OpenCog AtomSpace.

HOWTO (AtomSpace)
-----------------
The current version AtomSpace+python+flask code is in the
[`atoms`](atoms) directory.  Refer to the README there for how to
set up and operate.

The current implementation "works", but has many shortcomings.
That is, it "works", but is woefully incomplete.

HOWTO (Prototype)
-----------------
The earlier version 0.0.6 sqlite3+python+flask prototype is in the
[`src`](src) directory. See the README there for HOWTO instructions.
