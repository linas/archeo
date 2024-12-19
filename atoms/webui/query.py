#
# query.py
#
# Database query shim for the webui for Archeo.

import threading
from datetime import datetime

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
	start = datetime.now()
	load_atomspace()
	end = datetime.now()
	elapsed = end - start
	print("Done loading AtomSpace. Loaded", len(space), "atoms in", elapsed, "secs")

	start = end
	# Size of the incoming set is a quickie indicator of the number of URL's.
	numurls = len(PredicateNode("decoded URL").incoming)
	flatten_all_urls()
	end = datetime.now()
	elapsed = end - start
	print("Flattened all ", numurls, "URLS in", elapsed, "secs")

def storage_close():
	global storage
	cog_close(storage)
	storage = False
	pop_default_atomspace()

# -------------------------------------------------------------------------

# Return a list of files all having the same property (such as the hash,
# the filename, etc.) Properties include:
# * `hashstr` -- multiple files having the same content.
# * `filename` -- multiple files having the same name (but in different locations)
# * `filepath` -- a listing of all files in a directory.
#
# The second argument is a minimum number of duplicates that need to be found,
# in order to make it to the cut.
def find_duplicates(keyword, min_num_dups) :

	q = QueryLink(
			AndLink(
				EdgeLink(PredicateNode(pred_from_key[keyword]),
					ListLink(VariableNode ("$URL"), VariableNode("$prop"))),
				GroupLink(
					VariableNode("$prop"),
					IntervalLink(NumberNode (str(min_num_dups)), NumberNode("-1")))),
				VariableNode("$prop"))

	r = execute_atom(get_default_atomspace(), q)

	# Unpack the listing, convert it to a python list
	proplist = []
	for hi in r.to_list() :
		itemnode = hi.to_list()[0]
		itemname = itemnode.name
		proplist.append(itemname)

	return proplist

# -------------------------------------------------------------------------

# The split URL does not follow the generic
#   (Edge (Predicate key (List url property)))
# structure that the webui expects. This is both good and bad:
# bad as a local design choice, because it forces me to write this
# comment, and the extra code below. As a meta-choice, its ... OK,
# because it forces giving thought to general extra complexity that
# will appear in real life, in general. So, for now, we suffer and write
# the extra code below.
#
# This assumes that the URL decoder has already been run on the data.
# The URL decoder could have, maybe should have written the flat
# structure.
#
# This takes one argument: it should be either
#    ItemNode("file:///some/url/to/flatten")
# which will flatten only one, or
#    VariableNode("$url")
# which will cause *all* of them to be flattened.
#
def flatten_decoded_urls(urlnode) :

	q = QueryLink(
			ExecutionLink(
				PredicateNode("decoded URL"),
				urlnode,
				ListLink(
					EdgeLink(PredicateNode("protocol"), VariableNode("$proto")),
					EdgeLink(PredicateNode("domain"),   VariableNode("$domain")),
					EdgeLink(PredicateNode("filepath"), VariableNode("$path")),
					EdgeLink(PredicateNode("filename"), VariableNode("$name")))),

			# The rewrites to be done
			EdgeLink(PredicateNode("protocol"), ListLink(urlnode, VariableNode("$proto"))),
			EdgeLink(PredicateNode("domain"),   ListLink(urlnode, VariableNode("$domain"))),
			EdgeLink(PredicateNode("filepath"), ListLink(urlnode, VariableNode("$path"))),
			EdgeLink(PredicateNode("filename"), ListLink(urlnode, VariableNode("$name"))))

	execute_atom(get_default_atomspace(), q)

# This function flattens the decoded-URL structure into the simpler
# generic edge form. It flattens *all* of them, in one go.
# The results are not saved to the storage node.
def flatten_all_urls():
	urlnode = VariableNode("$urvar")
	flatten_decoded_urls(urlnode)

# Flatten only one URL, the one provided.
#
# This function flattens the decoded-URL structure into the simpler
# generic edge form.
# The results are not saved to the storage node.
def flatten_url(url) :
	urlnode = ItemNode(url)
	flatten_decoded_urls(urlnode)


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
key_from_pred["protocol"] = 'protocol'
key_from_pred["domain"] = 'domain'
key_from_pred["filepath"] = 'filepath'
key_from_pred["filename"] = 'filename'

pred_from_key = {}
for k,v in key_from_pred.items() :
	pred_from_key[v] = k

# Given a LinkValue containing Atomese edges, convert those
# edges to a python dictionary.
def props_to_dict(listatom) :
	fileinfo = {}
	for props in listatom.to_list() :
		# outlist = props.out
		outlist = props.to_list()
		#print("property", outlist[0], outlist[1])
		pred = outlist[0].name
		if pred in key_from_pred:
			fileinfo[key_from_pred[pred]] = outlist[1].name

	return fileinfo

# -------------------------------------------------------------------------

# Generic query for properties associated with listed keywords
# Example usage:
#   get_fileinfo_from_keywords(domain='foo', filepath='/bar/baz')
# Creates query
#   SELECT * FROM FileRecord WHERE domain='foo' AND filepath='/bar/baz';
#
def get_fileinfo_from_keywords(**kwargs) :

	elist = []
	for k,v in kwargs.items():
		p = pred_from_key[k]
		pn = PredicateNode(p)
		e = EdgeLink(pn, ListLink(VariableNode ("$URL"), ItemNode(v)))
		elist.append(e)

	if 1 < len(elist) :
		pat = AndLink(elist)
	else :
		pat = elist[0]

	q = QueryLink(
		TypedVariableLink(VariableNode("$URL"), TypeNode("ItemNode")),
		pat, VariableNode("$URL"))

	r = execute_atom(get_default_atomspace(), q)
	ndupes = len(r.to_list())
	infolist = []
	for url in r.to_list() :
		fileinfo = get_fileinfo_from_url(url.name)
		fileinfo['filedate'] = float(fileinfo['filedate'])
		fileinfo['count'] = ndupes
		for k,v in kwargs.items():
			fileinfo[k] = v
		infolist.append(fileinfo)

	return infolist

# -------------------------------------------------------------------------

# Given the url, return a dict describing the file at that location.
# XXX FIXME: Filesize should be part of the witness, because the
# filesize can change over time..
def get_fileinfo_from_url(url) :

	flatten_url(url)

	# Find all properties hanging off the URL.
	q = QueryLink(
			# The VariableList declaration is not really needed, but ...
			VariableList(
				TypedVariableLink(VariableNode("$predicate"), TypeNode("PredicateNode")),
				TypedVariableLink(VariableNode("$property"), TypeNode("ItemNode"))),
			# The search pattern
			EdgeLink(VariableNode("$predicate"),
				ListLink(ItemNode (url), VariableNode("$property"))),

			# The results. These will arrive wrapped in a LinkValue.
			VariableNode("$predicate"),
			VariableNode("$property"))

	r = execute_atom(get_default_atomspace(), q)

	# Convert the atomese batch of props hanging off the URL
	# to a python dict.
	fileinfo = props_to_dict(r)
	fileinfo['url'] = url

	return fileinfo

# ------------------ End of File. That's all, folks! ----------------------
# -------------------------------------------------------------------------
