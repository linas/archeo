--
-- File metadata
--
-- To create a new database, simply say:
--    cat file-metadata.sql | sqlite3 file-metadata.db
--
CREATE TABLE FileMetaData (
   -- Filename component, excluding file path
	filename TEXT NOT NULL,
	fuid INT PRIMARY KEY,
);

-- CREATE INDEX FileHash ON FileMetaData(hash) UNIQUE;

