--
-- File metadata witness
--
-- Make a record of having seen some file at some point in time, having
-- some associated data, such as a location, size and content hash.
--
-- To create a new database, simply say:
--    cat file-witness.sql | sqlite3 file-witness.db
--
-- Dates will be stored as Unix timestampes (seconds since Jan 1, 1970)
-- This is because unix files conventionally have unix timestamps, so
-- no conversion is required. Although most machines will run NTP, and
-- thus have an "accurate" clock, I'm not convinced UTC issues haven't
-- mess up file timestamps.
--
-- Foreign keys will be used.
PRAGMA foreign_keys = ON;

-- DB version. I anticipate future changes to the DB, and I anticipate
-- that rescanning the file system to rebuild the DB may not be viable,
-- e.g. for cold storage. Thus, data may need to be migrated to a later
-- version. This records the version number of the file-witnessing tableset.
CREATE TABLE Version (
	dbname TEXT NOT NULL,
	version INTEGER
);
INSERT INTO Version (dbname, version) VALUES ('FileWitness', 1);

-- Log of a file object, including name, size, location, and content hash.
-- None of this data is unique: there may be multiple files of the given
-- name, but with different sizes, contents, locations.
CREATE TABLE FileRecord (
   -- Filename component, excluding file path.
	filename TEXT NOT NULL,

	-- File path (location in filesystem), excluding filename.
	filepath TEXT NOT NULL,

	-- Domain (hostname) Domains might also be cold storage (offline
	-- disks) or otherwise unreachable at any given point in time.
	domain TEXT NOT NULL,

	-- Protocol. Usually will be `file:` unless its `nfs:` or `ceph:`
	-- or similar access method. Note that this might lead to confusion
	-- for mounted filesystems, bind-mounts and similar.  If blank,
	-- assume local filesystem or local mount point.
	protocol TEXT,

	-- File hash. xxh seems like a good choice. 64-bit.
	filexxh INTEGER,

	-- File size, in bytes.
	filesize INT,

	-- File creation timestamp.
	filecreate INT,

	-- Unique ID for this particular file record.
	-- SQLite wants INTEGER so that this can function as a primary key.
	-- This will autoincrement when not supplied.
	frecid INTEGER PRIMARY KEY
);

CREATE INDEX record_hash_idx ON FileRecord (filexxh);

-- Record of when a file with the indicated FileRecord was last seen
-- and validated as having the metadata as recorded in the FileRecord
CREATE TABLE RecordWitness (

	-- File record ID, references primary key in FileRecord
	frecid INTEGER,

	-- Date last seen and verified.
	witnessdate INT,

	-- Foreign keys must be last in sqlite3 table defs.
	FOREIGN KEY (frecid) REFERENCES FileRecord(frecid)
);

-- Record of two files having identical content. They may have different
-- timestamps, names and filepaths, but must have the same size and hash.
CREATE TABLE IdenticalContent (
	frecid_a INTEGER,
	frecid_b INTEGER,

	-- Date of comparison
	comparedate IT,

	FOREIGN KEY (frecid_a) REFERENCES FileRecord(frecid),
	FOREIGN KEY (frecid_b) REFERENCES FileRecord(frecid)
);


-- CREATE INDEX FileHash ON FileMetaData(hash) UNIQUE;

