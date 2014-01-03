import random
import string
import hashlib

def make_salt():
    ###Your code here
    #mine
    return ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for x in range(5))
    #instructor's
    #return ''.join(random.choice(string.letters) for x in xrange(5))

# implement the function make_pw_hash(name, pw) that returns a hashed password 
# of the format: 
# HASH(name + pw + salt),salt
# use sha256

def make_pw_hash(name, pw):
    ###Your code here
    #mine
    #salt=make_salt()
    #return str(hashlib.sha256(name + pw + salt).hexdigest())+","+str(salt)
    #instructor's
    salt=make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h, salt)

print make_pw_hash("charles","test_passwo0rd")
