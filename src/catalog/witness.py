#
# witness.py
#
# Witness, aka record the presence of a file in the filesystem.
#

import sqlite3

conn = sqlite3.connect('file-witness.db')
