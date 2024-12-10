#
# utils.py
#
# Minor common utils

# Convert a signed 64-bit int into an unsigned int.
# The unsigned 64-bit xxhash'es are stored in sqlite3 as signed ints.
# Before printing, convert them back.
def to_uint64(signed_int64_val):

	if signed_int64_val < 0 :
		return signed_int64_val + 2**64
	else :
		return signed_int64_val

# Half the time, a 64-bit unsigned hash will have the sign bit set.
# But sqlite3 chokes on this case. So explictly convert to signed 64-bit
def to_sint64(uint_val):
	if uint_val > 2**63-1 :
		return uint_val - 2**64
	else :
		return uint_val

# Print the signed 64-bit mangled hash as an unsigned hash.
# Again, this is because sqlite3 stores only signed 64-bit ints.
# Common utility so that all web pages print in the same format.
# hex() prints a leading 0x
def prthash(signed_int64_val):
	# return hex(to_uint64(signed_int64_val))
	return "%0.8X" % to_uint64(signed_int64_val)

# ------------------- That's all! End of file! ------------------
