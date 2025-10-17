@echo off
echo Starting Billing Software...
echo.

REM Try different Python commands until one works

REM Method 1: Try 'py' command (usually works on Windows)
py Main.py 2>nul
if %errorlevel% == 0 goto :success

REM Method 2: Try 'python' command
python Main.py 2>nul
if %errorlevel% == 0 goto :success

REM Method 3: Try 'python3' command
python3 Main.py 2>nul
if %errorlevel% == 0 goto :success

REM Method 4: Try common Python installation paths
if exist "C:\Python311\python.exe" (
    "C:\Python311\python.exe" Main.py
    goto :success
)

if exist "C:\Python312\python.exe" (
    "C:\Python312\python.exe" Main.py
    goto :success
)

if exist "C:\Python310\python.exe" (
    "C:\Python310\python.exe" Main.py
    goto :success
)

if exist "C:\Python39\python.exe" (
    "C:\Python39\python.exe" Main.py
    goto :success
)

REM Method 5: Try user-specific Python paths
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" Main.py
    goto :success
)

if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" Main.py
    goto :success
)

REM If nothing works, show error
echo ERROR: Python not found!
echo.
echo Please install Python from https://python.org
echo OR edit this batch file and add your Python path
echo.
echo Example: "C:\Your\Python\Path\python.exe" Main.py
echo.
pause
exit /b 1

:success
echo.
echo Billing Software closed.
pause
