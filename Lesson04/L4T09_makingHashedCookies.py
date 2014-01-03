import hashlib

def hash_str(s):
    return hashlib.md5(s).hexdigest()

# -----------------
# User Instructions
# 
# Implement the function make_secure_val, which takes a string and returns a 
# string of the format: 
# s,HASH

def make_secure_val(s):
    #mine
    newS=hash_str(s)
    return str(s)+","+str(newS)
    #instructor's
    return "%s,%s" % (s,hash_str(s))
    

print make_secure_val("hello")
