#
# similar_dirs.py
#
# Do flask rendering to show similar directories.
#

from flask import render_template
from flask_table import Table, Col

# The dot in front of the name searches the current dir.
# from .query import find_duplicated_names

# ---------------------------------------------------------------------

# Find directories with similar content.
def show_similar_dirs():
	return render_template("similar-dirs.html")
