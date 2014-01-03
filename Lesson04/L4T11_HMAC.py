import hashlib
import hmac

# Implement the hash_str function to use HMAC and our SECRET instead of md5
SECRET = 'imsosecret'
def hash_str(s):
    ###Your code here
    return hmac.new(SECRET,s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    hSplit=h.split('|')
    return hSplit[0] if make_secure_val(hSplit[0])==h else None




test=make_secure_val("Hello World!")
print check_secure_val(test)
