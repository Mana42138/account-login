import subprocess
import sys

def check_installed_packages():
    completed_process = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True)
    installed_packages = completed_process.stdout.splitlines()

    return installed_packages

def install_packages(requirements_file):
    installed_packages = check_installed_packages()

    with open(requirements_file) as file:
        packages = file.readlines()
        for package in packages:
            package_name = package.strip()
            if any(package_name.lower() in installed.lower() for installed in installed_packages):
                print(f"{package_name} is already installed.")
            else:
                print(f"Installing {package_name}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
