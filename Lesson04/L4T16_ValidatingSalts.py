import random
import string
import hashlib

def make_salt():
    #return ''.join(random.choice(string.letters) for x in xrange(5))
    return ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for x in range(5))

# Implement the function valid_pw() that returns True if a user's password 
# matches its hash. You will need to modify make_pw_hash.

def make_pw_hash(name, pw, s=None):
    if s:
        salt=s
    else:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h, salt)

def valid_pw(name, pw, h):
    ###Your code here
    try:
        salt=h.split(',')[1]
    except:
        return False
    return True if make_pw_hash(name,pw,salt)==h else False
    

h = make_pw_hash('spez', 'hunter2')
print h
print valid_pw('spez', 'hunter2', h)

