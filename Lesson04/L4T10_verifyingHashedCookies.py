import hashlib

def hash_str(s):
    return hashlib.md5(s).hexdigest()

def make_secure_val(s):
    #mine
    #newS=hash_str(s)
    #return str(s)+","+str(newS)
    #instructor's
    return "%s,%s" % (s,hash_str(s))

# -----------------
# User Instructions
# 
# Implement the function check_secure_val, which takes a string of the format 
# s,HASH
# and returns s if hash_str(s) == HASH, otherwise None 

def check_secure_val(h):
    ###Your code here
    #mine
    hSplit=h.split(',')
    return hSplit[0] if make_secure_val(hSplit[0])==h else None
    #instructor's
    val = h.split(',')[0]
    if h == make_secure_val(val):
        return val


test=make_secure_val("Hello World!")
print check_secure_val(test)

