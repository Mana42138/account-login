import secrets
import string
import time
import os
import sys
from datetime import date
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from auth import AccountManager
import requests
import json
import psutil

# import ctypes
# ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1) # Run as admin if needed

def status(text):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[1;34m" + text + "\033[0m")

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
        with open(os.path.join(files_path, datafile), "w") as file:
            json.dump(data, file, indent=4)
    except json.decoder.JSONDecodeError:
        files_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        with open(os.path.join(files_path, datafile), "w") as file:
            file.write(data)

def terminate_process(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            proc.kill()
            print(f"Process {process_name} terminated.")
            return True
    print(f"No process named {process_name} found.")
    return False

program_name = "RobloxPlayerBeta.exe"

# URLs
first_names_url = "https://raw.githubusercontent.com/Mana42138/Gen-RX/main/firstnames.txt"
last_names_url = "https://raw.githubusercontent.com/Mana42138/Gen-RX/main/lastnames.txt"
codes = requests.get("https://raw.githubusercontent.com/Mana42138/Gen-RX/main/codes.txt")
proxies = requests.get("https://raw.githubusercontent.com/Mana42138/Gen-RX/main/proxy-list")
roblox_url = "https://www.roblox.com/"

status("Getting first names...")
first_names_response = requests.get(first_names_url)
status("Getting last names...")
last_names_response = requests.get(last_names_url)

# Check if name loading was successful
if first_names_response.status_code == 200 and last_names_response.status_code == 200:
    first_names = list(set(first_names_response.text.splitlines()))
    last_names = list(set(last_names_response.text.splitlines()))
else:
    status("Name loading failed. Re-Execute the script.")
    sys.exit()

if codes.status_code != 200:
    status("Code request failed. Re-Executing")
    sys.exit()

if proxies.status_code != 200:
    status("proxies request failed. Re-Executing")
    sys.exit()


# File paths
files_path = os.path.dirname(os.path.abspath(sys.argv[0]))
text_files_folder = os.path.join(files_path, "Accounts")
text_file = os.path.join(text_files_folder, f"Accounts.txt")
text_file2 = os.path.join(text_files_folder, f"AltManagerLogin.txt")

settings_file = os.path.join(files_path, "settings.json")

codes_list = list(set(codes.text.splitlines()))


# Create folder if it does not exist
if not os.path.exists(text_files_folder):
    os.makedirs(text_files_folder)

if not os.path.exists(settings_file):
    status("Initializing first time setup...")
    AUTO_LAUNCH = input("## Auto Launch ##\nWould you like to enable this feature? \n (y/n)")
    if AUTO_LAUNCH=="y":AUTO_LAUNCH=True
    else:AUTO_LAUNCH=False

    SHOW_CODES = input("## Show Codes ##\nWould you like to enable this feature? \n (y/n)")

    if SHOW_CODES=="y":SHOW_CODES=True
    else:SHOW_CODES=False

    AUTO_COPY_CODES = input("## Auto Copy Codes ##\nWould you like to enable this feature? \n (y/n)")

    if AUTO_COPY_CODES=="y":AUTO_COPY_CODES=True
    else:AUTO_COPY_CODES=False

    AUTO_CLOSE_ROBLOX = input("## Auto Close Roblox ##\nWould you like to enable this feature? \n (y/n)")

    if AUTO_CLOSE_ROBLOX=="y":AUTO_CLOSE_ROBLOX=True
    else:AUTO_CLOSE_ROBLOX=False

    COPY_CODES_KEY = input("## Copy Codes Key ##\n Please press the key you want to use: ")

    PASSWORD = input("## PASSWORD ##\n Please type your password: ")

    GAME_ID = input("## GAME_ID ##\n Please type the game id you want to join: ")


    data = {
        "AUTO_LAUNCH": AUTO_LAUNCH,
        "SHOW_CODES": SHOW_CODES,
        "AUTO_COPY_CODES": AUTO_COPY_CODES,
        "COPY_CODES_KEY": COPY_CODES_KEY.lower(),
        "PASSWORD": PASSWORD,
        "GAME_ID": GAME_ID,
        "AUTO_CLOSE_ROBLOX": AUTO_CLOSE_ROBLOX
    }
    writefile("settings.json", data)

# Lists of days, months and years
days = [str(i + 1) for i in range(10, 28)]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
years = [str(i + 1) for i in range(1980, 2004)]

# Password generator
def gen_password(length):
    status("Generating a password...")
    chars = string.ascii_letters + string.digits + "Ññ¿?¡!#$%&/()=\/¬|°_-[]*~+"
    password = ''.join(secrets.choice(chars) for _ in range(length))
    return password

#Username generator
def gen_user(first_names, last_names):
    status("Generating a username...")
    first = secrets.choice(first_names)
    last = secrets.choice(last_names)
    full = f"{first}{last}_{secrets.choice([i for i in range(1, 999)]):03}"
    return full

def create_account(url, first_names, last_names):
        # Config
        settings = readfile("settings.json")
        AUTO_LAUNCH = settings["AUTO_LAUNCH"]
        PASSWORD = settings["PASSWORD"]
        SHOW_CODES = settings["SHOW_CODES"]
        GAME_ID = settings["GAME_ID"]
        AUTO_CLOSE_ROBLOX = settings["AUTO_CLOSE_ROBLOX"]

        if AUTO_CLOSE_ROBLOX:
            terminate_process(program_name)

        status("Starting to create an account...")
        cookie_found = False
        username_found = False
        elapsed_time = 0
        status("Initializing webdriver...")
        driver = webdriver.Edge()
        driver.set_window_size(1200, 800)
        driver.set_window_position(0, 0)
        # driver.minimize_window()
        driver.get(url)
        time.sleep(2)
        
        # HTML items
        status("searching for items on the website")
        try:
            accept_button = driver.find_element(By.CLASS_NAME, "btn-cta-lg")
            accept_button.click()
        except:
            pass

        username_input = driver.find_element("id", "signup-username")
        username_error = driver.find_element("id", "signup-usernameInputValidation")
        password_input = driver.find_element("id", "signup-password")
        day_dropdown = driver.find_element("id", "DayDropdown")
        month_dropdown = driver.find_element("id", "MonthDropdown")
        year_dropdown = driver.find_element("id", "YearDropdown")
        male_button = driver.find_element("id", "MaleButton")
        female_button = driver.find_element("id", "FemaleButton")
        register_button = driver.find_element("id", "signup-button")

        status("Selecting day...")
        Selection = Select(day_dropdown)
        Selection.select_by_value(secrets.choice(days))
        time.sleep(0.3)

        status("Selecting month...")
        Selection = Select(month_dropdown)
        Selection.select_by_value(secrets.choice(months))
        time.sleep(0.3)

        status("Selecting year...")
        Selection = Select(year_dropdown)
        Selection.select_by_value(secrets.choice(years))
        time.sleep(0.3)

        while not username_found:
            status("Selecting username...")
            username = f"{gen_user(first_names, last_names)}Inc"
            username_input.clear()
            username_input.send_keys(username)
            time.sleep(1)
            if username_error.text.strip() == "":
                username_found = True
        
        status("Selecting password...")
        password = PASSWORD
        password_input.send_keys(password)
        time.sleep(0.3)

        status("Selecting gender...")
        gender = secrets.choice([1,2])
        if gender == 1:
            male_button.click()
        else:
            female_button.click()
        time.sleep(0.5)

        status("Registering account...")
        register_button.click()
        time.sleep(3)

        # Wait until the account creation limit is reset
        try:
            driver.find_element("id", "GeneralErrorText")
            # driver.quit()
            for i in range(360):
                status(f"Limit reached, waiting... {i+1}/{360}")
                time.sleep(1)
        except:
            pass
            
        # Wait until the cookie is found or the maximum time has passed
        while not cookie_found and elapsed_time < 180:
            status("Waiting for the cookie...")
            time.sleep(3)
            elapsed_time += 3
            for cookie in driver.get_cookies():
                if cookie.get('name') == '.ROBLOSECURITY':
                    cookie_found = True
                    break
        if cookie_found:
            status("Cookie found...")
            result = [cookie.get('value'), username, password]
            save_account_info(result)
            
            if result is not None:
                status("Successfully created!")
                time.sleep(.2)
                if AUTO_LAUNCH:
                    Manager = AccountManager(result[0])
                    ticket = Manager.get_authentication_ticket()
                    job_id = Manager.job_id()
                    
                    Manager.launch_roblox(ticket, str(GAME_ID), job_id)

        if SHOW_CODES:
            status(f"##Codes## \n\n")
            for v in codes_list:
                print(v)
        return result

# Save account information to text file
def save_account_info(account_info):
    status("Saving account info...")
    with open(text_file, 'a') as file:
        file.write(f"Username: {account_info[1]}\nPassword: {account_info[2]}\nCookie: {account_info[0]}\n\n\n")

# Save login information for AltManager
def save_altmanager_login(account_info, item):
    with open(text_file2, 'a') as file:
        status("Saving account login (for alt manager)...")
        file.write(f"{account_info[1]}:{account_info[2]}: Item {item}\n")

# Create accounts
def main():
    stuff = create_account(roblox_url, first_names, last_names)
    item = input("Item: ")
    status("Adding item!")
    save_altmanager_login(stuff, item)
    
    if readfile("settings.json")["AUTO_CLOSE_ROBLOX"]:
        terminate_process(program_name)
