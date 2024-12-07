
Archeo -- Data Recovery
=======================
Repairing lost, corrupted, damaged data. The Archivist's Freind.
Data Hoarders Welcome.  Data Archeology. Forensics. Longevity.
A Unified View of Data.

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
finished counting. Wife & kids have more. I panicked. My panick is
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
  version can be created.
* Search my old backups and archives for a good copy.
* Consolidate all my old archives and copies. They are everywhere,
  I don't even know what I have, if its any good, and its all taking up
  disk space. Where is it? What is it? Is it rotten? Is it good?
* Start small, for home users. Expand to archives, libraries. Support
  databases and complex data. Allow data forensics and data recovery.
  Do things that data archivists need. Handle medical data, business data,
  science data. Scale to exabytes.
* Build the foundations for AI.

Don't laugh at that last bullet. Yes, you and I both are tired of the
AI hype and the rather underwhelming results. But I'm being serious, here.
If you'll let me, I want to write a short essay about AI and longevity.

The Process of Living
---------------------
Living organisms heal themselves. A collection of data should be
self-healing. Living organisms know things and remember things.
A collection of data should know what's in it, what it's made out
of, when some blob of data was last seen online, or in cold storage.

There should be ways of exploring, finding, searching, discovering.
Knowing who you are, by knowing what you remember. Living organisms
have eyes for looking, for seeing. An AI/AGI needs sensory organs,
too, but for "seeing" collections of data. For finding and exploring
data, for living in a world not of tiger hiding in grass and rocks
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
their data. Perhaps one day, this project wiil be useful to archivists
or librarians. Maybe even scientists or business owners. But lets not
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

Version 0.0.0
-------------
No code yet.


Boiling the ocean
Archivists
Backups
Big Ten accounting firms -- who has what?
wireshark packet sniffing
intrusion detction says files have changed. System knows what you have. Sort of.
splunk error log exploration

ceph, mdrain, ext4fs, btrfs, xfs metadata
File explorers & file browsers
