
import requests
import os
import sys
import json

def readfile(datafile):
    try:
        files_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        with open(os.path.join(files_path, datafile), "r") as file:
            data = json.load(file)
        return data
    except:
        files_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        with open(os.path.join(files_path, datafile), "r") as file:
            return file.read()
        
def writefile(datafile, data):
    try:
        files_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        with open(os.path.join(files_path, datafile), "wb") as file:
            file.write(data)  # Write binary data directly
    except Exception as e:
        print(f"Error occurred: {e}")

files_path = os.path.dirname(os.path.abspath(sys.argv[0]))

def Main():
    print("Starting...")
    Request_Links = {
        "register.py": "https://raw.githubusercontent.com/Mana42138/account-login/main/register.py",
        "auth.py": "https://raw.githubusercontent.com/Mana42138/account-login/main/auth.py",
        "auto_copy.py": "https://raw.githubusercontent.com/Mana42138/account-login/main/auto_copy.py",
        "main.py": "https://raw.githubusercontent.com/Mana42138/account-login/main/main.py"
        }
    
    for item, value in Request_Links.items():
        Item_Path = os.path.join(files_path, item)
        if os.path.exists(Item_Path):
            os.remove(Item_Path)
        writefile(item, requests.get(value).content)


Main()
