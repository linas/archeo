#! /usr/bin/env python3
#
# main.py
#
# Do stuff.

import os
import sqlite3
from witness import witness_db_open, witness_db_close
from crawler import dir_witness

hostname = "phony"

witness_db_open('file-witness.db')

dir_witness(hostname, "/tmp")

# Close the connection
witness_db_close()
