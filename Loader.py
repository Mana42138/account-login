import sys
import subprocess

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])

import requests
import os
import sys

files_path = os.path.dirname(os.path.abspath(sys.argv[0]))

file_name = "setup.py"
Item_Path = os.path.join(files_path, file_name)

if os.path.exists(Item_Path):
    os.remove(Item_Path)

print("Installing Setup / requirements.txt")
with open(os.path.join(files_path, file_name), "wb") as file:
    file.write(requests.get("https://raw.githubusercontent.com/Mana42138/Gen-RX/main/setup.py").content)

with open(os.path.join(files_path, "requirements.txt"), "wb") as file:
    file.write(requests.get("https://raw.githubusercontent.com/Mana42138/Gen-RX/main/requirements.txt").content)
