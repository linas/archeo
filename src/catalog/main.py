#! /usr/bin/env python3
#
# main.py
#
# Do stuff.

import sqlite3
from witness import file_witness

conn = sqlite3.connect('file-witness.db')

r = file_witness(conn, "funny", "/tmp/xxx")
print("I got fileid ", r)
r = file_witness(conn, "funny", "/tmp/zzz")
print("I got fileid ", r)

# Close the connection
conn.close()

