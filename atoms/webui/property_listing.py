#
# property_listing.py
#
# Convert Atomese item properites to python lists-of-dictionaries.
# Each Atomese item is mapped to a python dictionary. Multiple
# dictionaries are places into a python list (could have been a set,
# there is no particular ordering that matters.)

# The dot in front of the name searches the current dir.
from .query import find_duplicates, get_fileinfo_from_keywords

# ---------------------------------------------------------------------

# Items can be filenames, content hashes, filepaths, etc.
# This class builds a list of such items.
class item_collection :

	itemcount = 0

	def __init__(self) :
		return

	# Build a list of duplicated items.
	# First argument: the property that is duplicated
	# Second argument: min number of duplications to rise above.
	#
	# Returned value: a list of items having that duplicated property.
	# The returned list contains a complete description of the item, in the
	# form of a dictionary with the item properties in the dict.
	# That is, the returned value is a list of dictionaries.
	#
	# This is a query shim, translating the result of queries to the
	# AtomSpace, into python dicts that python API's are expecting to get.
	#
	def build_duplicates(self, property, min_num_dups):

		dup_items = find_duplicates(property, min_num_dups)

		itemcount = 0
		rowlist = []
		for item in dup_items:
			itemcount += 1

			# We use this to construct a second query, for all files with
			# a given hash. Returned columns ar properties associated with
			# that hash, including url, filesize, filedate
			first = True
			fresult = get_fileinfo_from_keywords(**{property:item})
			for frow in fresult:
				itemcount += 1
				frow['row'] = itemcount
				if first:
					first = False
				else :
					frow['hashstr'] = ''
					frow['count'] = ''

				rowlist.append(frow)

			# Blank line. Maybe there's some prettier way; I can't be bothered.
			# viz. There needs to be a CSS for the displayed table, indicating
			# a grouping break. Not sure how to convey this grouping.
			rowlist.append(dict(row='', hashstr='', count='', url='',
				domain='', filepath='', filename='', filesize='', filedate=''))

		self.itemcount = itemcount
		return rowlist
