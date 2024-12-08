#! /usr/bin/env python3
#
# main.py
#
# Do stuff.

import os
import sqlite3
from witness import file_witness, witness_db_open, witness_db_close

hostname = "phony"

witness_db_open('file-witness.db')

r = file_witness(hostname, "/tmp/xxx")
print("I got fileid ", r)
r = file_witness("funny", "/tmp/zzz")
print("I got fileid ", r)

# Close the connection
witness_db_close()
