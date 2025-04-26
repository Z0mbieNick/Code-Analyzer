



📖 Explanation of all security problems your analyzer can detect
1. Dangerous use of eval()
eval() executes any string as Python code.

If a hacker controls the string, they can run malicious code inside your program.

Example:
  user_input = "os.system('rm -rf /')"
  eval(user_input)  # BAD! Hacker controls this!
Your analyzer detects if eval() is used.

2. Dangerous use of exec()
exec() also runs arbitrary Python code from a string.

It’s just as dangerous as eval().

Example:
  exec("open('passwords.txt').read()")
Your analyzer detects exec() usage too.

3. Hardcoded passwords or secrets
Storing passwords, API keys, tokens directly in code is a big mistake.

If someone gets your code, they steal the secrets.

Example:
  password = "admin123"
  api_key = "SECRET_API_KEY"
Your analyzer detects when secret-looking words are hardcoded.

4. Insecure hash functions (md5, sha1)
md5 and sha1 hashing algorithms are broken (they can be cracked easily).

You should use strong hashes like bcrypt, argon2, sha256.

Example:
  hashlib.md5("password".encode()).hexdigest()
Your analyzer detects md5 and sha1 usage.

5. Insecure randomness (random)
Python’s random is not secure for cryptography (it’s predictable).

You should use secrets module instead.

Example (bad):
  random.randint(1000, 9999)  # Not safe for passwords or tokens
Your analyzer detects use of random in security-sensitive places.

6. Unsafe subprocess execution
subprocess.run(), subprocess.Popen(), etc. can execute system commands.

If the command includes user input, it can be command injection.

Example:
  subprocess.run(["rm", "-rf", "/"])  # Danger!
Your analyzer detects usage of subprocess functions.

7. Unsafe object deserialization (pickle.load())
pickle can load dangerous Python objects from files.

Hackers can create a file that, when loaded, executes code.

Example:
  pickle.load(open("malicious_file.pkl", "rb"))  # Can execute code!
Your analyzer detects pickle.load() usage.

8. Potential division by zero
If you divide by a value without checking, the program crashes.

Example:
  result = 10 / user_input
  If user_input == 0, it crashes.
Your analyzer detects divisions and warns you.

9. Suspicious imports
Certain Python libraries are dangerous if used wrong.

Example:
  import pickle
  import subprocess
  import random
  import hashlib
Your analyzer warns when code imports these libraries (because they are risky).