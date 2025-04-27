import random
import subprocess
import hashlib

password = "super_secret_123"

def run_user_code(user_input):
    eval(user_input)  # Dangerous use of eval

def divide(a, b):
    return a / b  # Possible division by zero

def hash_password(pw):
    return hashlib.md5(pw.encode()).hexdigest()

def get_random_number():
    return random.randint(1, 10)

def delete_folder():
    subprocess.run(["rm", "-rf", "/important/data"]) # dangeorous because subprocess.run([...]) tells Python to directly run a command on the operating system.
    #It’s like opening the terminal manually and typing
