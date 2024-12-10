#
# utils.py
#
# Minor common utils

# Convert a signed 64-bit int into an unsigned int.
# The unsigned 64-bit xxhash'es are stored in sqlite3 as signed ints.
# Before printing, convert them back.
def to_uint64(signed_int64):

	if signed_int64 < 0 :
		return signed_int64 + 2**64
	else :
		return signed_int64


# Print the signed 64-bit mangled hash as an unsigned hash.
# Again, this is because sqlite3 stores only signed 64-bit ints.
# Common utility so that all web pages print in the same format.
# TODO: fix this to get rid of the leading 0x
def prthash(signed_int64):
	return hex(to_uint64(signed_int64))

# ------------------- That's all! End of file! ------------------
