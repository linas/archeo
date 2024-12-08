The File Catalog
----------------
The file catalog attempts to create a searchable index of files,
organized by filename, content hash and other file data.

SQL tables need to hold this info, and they need to be normalized
so that "things are finable". Some normalization notes:

* There may be multiple files with the same content hash. They
  may be in different locations.

* There may be multiple files with the same name, but with
  different metadata (file creation timestamp, file size,
  directory location

* Every time a file is witnessed (i.e. seen by this software system)
  it should be loged.
