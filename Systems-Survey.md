Systems Survey
==============
What else is out there? What does it do? The survey below will be
limited to open-source, free software.

COPTR
-----
This is a tools registery. Browse for appropriate tools.

Piecemeal data recovey tools
----------------------------
* [Top 20 Best Linux Data Recovery Tools to Recover Deleted/Corrupted Files](https://www.digitalocean.com/community/tutorials/top-best-linux-data-recovery-tools)
  This list includes tools for disk recovery (dealing with failing
  or filed disk drives with bad sectors, etc.
  -- TestDisk - Partition and Disk Recovery Tool
  -- Mondo Rescue - Network Drive Recovery Utility
  -- ddrescue - GNU Data Recovery Utility
. -- Redo Backup and Recovery - Easiest GUI Recovery Utility
  -- SafeCopy - One of The Best Linux Data Recovery Tools

  Recovery tools for specific file formats
  -- Foremost - A Forensic Data Recovery Tool
     PDF, jpeg recovery from various media types (usb sticks, iphones...)
  -- Scalpel - A Cross-Platform File Carving Utility
     Based on Foremost, can find/extract data from corrupted disks.
  -- [PhotoRec](https://www.cgsecurity.org/wiki/PhotoRec) - Photo Recovery Utility

  Boot rescue systems-- rescue Linux systems that won't boot any more.
  -- Boot Repair - Live CD File Recovery
  -- SystemRescue CD - An AIO Rescue Package Live CD
  -- Ultimate Boot CD - A Collection of Almost All Data Recovery Tools
  -- Knoppix - A Daily-Driver Capable Recovery Distribution
  -- GParted Live - The GUI Tool for GNU Parted

  File undelete tools
  -- ext4magic - One of the Best Linux Data Recovery Tools for ext4
  -- extundelete - An ext3grep Successor
  -- ext3undel - A Custom Script to Simplify File Recovery

  Forensic tools
  -- The Sleuth Kit - Forensic Evidence
     Crawl web surfing history, emails, recently accessed files,
     deleted files. Build timeline of user activity.

Data Integrity
--------------
* Tripwire --
  It works by creating a baseline database, and then regularly comparing
  the state of the file system with the database. If it detects changes
  (e.g. addition or modification of some files), it includes these changes
  in its report, so that the security administrators could check these changes.
* [FIM File Integrity Monitor](https://github.com/Achiefs/fim)
  Tracks any event over your files. It is capable of keeping historical data
  of your files. It checks the filesystem changes in the background.
  [Can FIM be adapted for Archeo?](https://github.com/Achiefs/fim/discussions/178)

File characterization
---------------------
* [Apache Tika](https://tika.apache.org/) - Content analysis toolkit.
  Detects and extracts metadata and text from over a thousand different
  file types (such as PPT, XLS, and PDF). Java. Active project.
* [DROID](https://www.nationalarchives.gov.uk/information-management/manage-information/policy-process/digital-continuity/file-profiling-tool-droid/)
  Digital Record Object Identification. File identification tool.
  See [github source](https://github.com/digital-preservation/droid)
  Appears to be inactive. Windows-focused, GUI. Hass command line too.
* [C3PO](https://openpreservation.org/blogs/c3po-content-profiling-tool-preservation-analysis/)
  content profiling tool for preservation analysis.
  See also [github repo](https://github.com/peshkira/c3po) Abandoned.

* FIDO
* [JHOVE](https://jhove.openpreservation.org/)
  Open source file format identification, validation & characterisation.
  Validates a dozen different file formats to make sure they pass basic
  integrity checks. Java. Seems stagnant, last update 2019.
* FITS

Moving Data
-----------
Moving data from here to there.
* [Airbyte](https://github.com/airbytehq/airbyte) has 300+ connectors
  to move data from here to there. Talking about "big data" mostly.

* HEVO

* Many others.

Saving stuff
------------
* [ArchiveBox](https://github.com/ArchiveBox/ArchiveBox)
  ArchiveBox is a powerful, self-hosted internet archiving solution
  to collect, save, and view websites offline.

Data Quality Tools
------------------
"Data Quality" is a code-word for the aggregating vast amounts of data
from giant websites. This includes data on marketing campaigns, click-thru,
A/B testing, browsing histories, browsing patterns. The focus is on dealing
with a fire-hose of click and mouse-movement data streaming in from thousands
or millions of users.

This is not about the quality of archival data, but about streams of fresh
data coming in.

* [6 Popular Open Source Data Quality Tools To Know in 2024: Overview, Features & Resources](https://atlan.com/open-source-data-quality-tools/)

Provides a review of:
 * Deequ
 * dbt Core
 * MobyDQ
 * Great Expectations
 * Soda Core
 * Cucumber


Information Management Systems
------------------------------
And content management systems (CMS). Aimed at libraries, archives,
archivists. Do not seem to include tools aimed at content integrity.

* Archivematica
* RODA
* DSpace
* Fedora
* Eprints
* Samvera (Hyku)

* [CollectiveAccess](https://www.collectiveaccess.org/)
  CollectiveAccess is free, open-source software for cataloguing
  and publishing museum and archival collections.

* [AccessToMemeory](https://www.accesstomemory.org/en/)

* [AchiveSpace](https://archivesspace.org/)
  -- Sharply aimed at traditional archive/library activities.
  -- Aimed at organizations that have professional full-time staff.
  -- Tech follow on to Archon & Archivists Toolkit
  -- Contact: ArchivesSpaceHome@lyrasis.org
  -- Getting Started with ArchivesSpace:
     https://archivesspace.org/resources/user-resources/getting-started/
