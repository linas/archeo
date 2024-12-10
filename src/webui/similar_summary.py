#
# similar_summary.py
#
# Do flask rendering to show summary of similar directories.
#

from flask import render_template
from flask_table import Table, Col

# The dot in front of the name searches the current dir.
# from .query import find_duplicated_names

# ---------------------------------------------------------------------

# Find directories with similar content.
def show_similar_summary():
	return render_template("similar-summary.html")
