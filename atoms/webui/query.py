#
# query.py
#
# Database query shim for the webui for Archeo.

import threading

from opencog.atomspace import AtomSpace
from opencog.type_constructors import *
from opencog.exec import execute_atom
from opencog.storage import *
from opencog.storage_rocks import *

# -------------------------------------------------------------------------

storage = False

def storage_open(storage_url):
	global storage

	# If already open, do nothing.
	threading.Lock()
	if storage :
		return

	space = AtomSpace()
	push_default_atomspace(space)

	storage = RocksStorageNode(storage_url)
	cog_open(storage)

	# We're just going to bulk-load everything. This won't scale
	# for large DB's, but its OK for now.
	load_atomspace()
	print("Done loading AtomSpace. Size=", len(space))

def storage_close():
	global storage
	cog_close(storage)
	storage = False
	pop_default_atomspace()

# -------------------------------------------------------------------------

# Return a list of duplicated filenames.
# This is fairly normal: the same filename may be used in many places
def find_duplicated_names() :
	#sel = "SELECT filename, frecid, COUNT(*) FROM FileRecord GROUP BY filename HAVING COUNT(*) > 1;"
	#return cursor.execute(sel)
	return {}

# -------------------------------------------------------------------------

# Return a list of duplicated hashes.
# This is fairly normal: the same file contents, different locations/names
# Argument is a minimum number of duplicates that need to be found,
# in order to make it to the cut.
def find_duplicated_hashes(min_num_dups) :

	q = QueryLink(
			AndLink(
				EdgeLink(PredicateNode("content xxhash-64"),
					ListLink(VariableNode ("$URL"), VariableNode("$hash"))),
				GroupLink(
					VariableNode("$hash"),
					IntervalLink(NumberNode (str(min_num_dups)), NumberNode("-1")))),
				VariableNode("$hash"))

	r = execute_atom(get_default_atomspace(), q)

	# Unpack the listing, convert it to a python list
	hashlist = []
	for hi in r.to_list() :
		itemnode = hi.to_list()[0]
		itemname = itemnode.name
		hashlist.append(itemname)

	return hashlist

# -------------------------------------------------------------------------
# The WebUI uses (key,value) pairs to display tables. The keys cannot
# contain spaces, and when used in kwargs, cannot be strings. Meanwhile
# The AtomSpace names are ... strings with spaces. So build a dictionary
# converting from the AtomSpace conventions to the WebUI conventions.
# Do it here, with the off-chance that other subsystems need the restricted
# naming conventions.

key_from_pred = {}
key_from_pred["content xxhash-64"] = 'hashstr'
key_from_pred["file size"] = 'filesize'
key_from_pred["last modified"] = 'filedate'

# Given the url, return a dict describing the file at that location.
def get_fileinfo_from_url(url) :

	# Find all properties hanging off the URL.
	q = QueryLink(
			# The VariableList declaration is not really needed, but ...
			VariableList(
				TypedVariableLink(VariableNode("$predicate"), TypeNode("PredicateNode")),
				TypedVariableLink(VariableNode("$property"), TypeNode("ItemNode"))),
			EdgeLink(VariableNode("$predicate"),
				ListLink(ItemNode (url), VariableNode("$property"))),
			ListLink(VariableNode("$predicate"), VariableNode("$property")))

	r = execute_atom(get_default_atomspace(), q)
	fileinfo = {}
	fileinfo['url'] = url
	for props in r.to_list() :
		# print("property", props.out[0], props.out[1])
		fileinfo[key_from_pred[props.out[0].name]] = props.out[1].name

	return fileinfo

# -------------------------------------------------------------------------

# Given the filehash, return a list of dicts describing the files
# having that hash.
def get_fileinfo_from_hash(hashstr) :

	q = QueryLink(
			EdgeLink(PredicateNode("content xxhash-64"),
				ListLink(VariableNode ("$URL"), ItemNode(hashstr))),
			VariableNode("$URL"))

	r = execute_atom(get_default_atomspace(), q)
	ndupes = len(r.to_list())
	infolist = []
	for url in r.to_list() :
		fileinfo = get_fileinfo_from_url(url.name)
		fileinfo['hashstr'] = hashstr
		fileinfo['count'] = ndupes
		infolist.append(fileinfo)

	return infolist

# -------------------------------------------------------------------------

def select_filerecords(**kwargs) :
	return []

# ------------------ End of File. That's all, folks! ----------------------
# -------------------------------------------------------------------------
