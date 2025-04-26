import subprocess

def delete_folder():
    subprocess.run(["rm", "-rf", "/important"])


#Line	Issue
#1	Suspicious import detected: subprocess
#4	Pattern detected: subprocess usage