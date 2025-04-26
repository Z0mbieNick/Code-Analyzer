import random

def generate_code():
    return random.randint(1000, 9999)

#Line	Issue
#1	Suspicious import detected: random
#4	Pattern detected: insecure random