--
-- File metadata
--
-- To create a new database, simply say:
--    cat file-metadata.sql | sqlite3 file-metadata.db
--
-- Log of a file object, including name, size, location, and content hash.
-- None of this data is unique: there may be multiple files of the given
-- name, but with different sizes, contents, locations.
CREATE TABLE FileRecord (
   -- Filename component, excluding file path.
	filename TEXT NOT NULL,

	-- File path (location in filesystem), excluding filename.
	filepath TXT NOT NULL,

	-- Domain (hostname) Domains might also be cold storage (offline
	   disks) or otherwise unreachable at any given point in time.
	domain TXT NOT NULL,

	-- Protocol. Usually will be `file:` unless its `nfs:` or `ceph:`
	   or similar access method. Note that this might lead to confusion
	   for mounted filesystems, bind-mounts and similar.  If blank,
	   assume local filesystem or local mount point.
	protocol TXT,

	-- File hash. xxh3 seems like a good choice. 64-bit.

	-- File size, in bytes.
	filesize INT,

	-- File creation timestamp.

	-- Date this record was created.

	-- Unique ID for this particular file record.
	frecid INT PRIMARY KEY
);

-- Record of when a file with the indicated FileRecord was last seen
   and validated as having the metadata as recorded in the FileRecord
CREATE TABLE RecordWitness (

	-- FIle record ID
	frecid INT FOREIGN KEY
);

-- CREATE INDEX FileHash ON FileMetaData(hash) UNIQUE;

