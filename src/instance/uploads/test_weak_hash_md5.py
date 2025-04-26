import hashlib

def hash_password(pw):
    return hashlib.md5(pw.encode()).hexdigest()

#Line	Issue
#1	Suspicious import detected: hashlib
#4	Pattern detected: insecure hashing

