--
-- File metadata
--
-- To create a new database, simply say:
--    cat file-metadata.sql | sqlite3 file-metadata.db
--
-- Dates will be stored as Unix timestampes (seconds since Jan 1, 1970)
-- This is because unix files conventionally have unix timestamps, so
-- no conversion is required. Although most machines will run NTP, and
-- thus have an "accurate" clock, I'm not convinced UTC issues haven't
-- mess up file tiemstamps.
--
-- Log of a file object, including name, size, location, and content hash.
-- None of this data is unique: there may be multiple files of the given
-- name, but with different sizes, contents, locations.
CREATE TABLE FileRecord (
   -- Filename component, excluding file path.
	filename TEXT NOT NULL,

	-- File path (location in filesystem), excluding filename.
	filepath TEXT NOT NULL,

	-- Domain (hostname) Domains might also be cold storage (offline
	   disks) or otherwise unreachable at any given point in time.
	domain TEXT NOT NULL,

	-- Protocol. Usually will be `file:` unless its `nfs:` or `ceph:`
	   or similar access method. Note that this might lead to confusion
	   for mounted filesystems, bind-mounts and similar.  If blank,
	   assume local filesystem or local mount point.
	protocol TEXT,

	-- File hash. xxh3 seems like a good choice. 64-bit.

	-- File size, in bytes.
	filesize INT,

	-- File creation timestamp.
	filecreate INT,

	-- Date this record was created.
	recordcreate INT,

	-- Unique ID for this particular file record.
	-- SQLite wants INTEGER so that this can function as a primary key.
	frecid INTEGER PRIMARY KEY AUTOINCREMENT
);

-- Record of when a file with the indicated FileRecord was last seen
   and validated as having the metadata as recorded in the FileRecord
CREATE TABLE RecordWitness (

	-- File record ID, references primary key in FileRecord
	frecid INTEGER,
	FOREIGN KEY (frecid) REFERENCES FileRecord(frecid),

	-- Date last seen and verified.
	witnessdate INT
);

-- Record of two files having identical content. They may have different
-- timestamps, names and filepaths, but must have the same size and hash.
CREATE TABLE IdenticalContent (
	frecid_a INTEGER,
	FOREIGN KEY (frecid_a) REFERENCES FileRecord(frecid),
	frecid_b INTEGER,
	FOREIGN KEY (frecid_b) REFERENCES FileRecord(frecid),

	-- Date of comparison
	comparedate IT
);


-- CREATE INDEX FileHash ON FileMetaData(hash) UNIQUE;

