@echo off
title File Mama — Build to EXE
color 0A
echo.
echo  ================================================
echo   FILE MAMA — Auto Build Script
echo  ================================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Python not found!
    echo  Download from: https://www.python.org/downloads/
    echo  Make sure to check "Add Python to PATH" during install.
    pause
    exit /b 1
)

echo  [OK] Python found
echo.

:: Install pyinstaller + comtypes
echo  Installing required packages...
pip install pyinstaller comtypes --quiet
if %errorlevel% neq 0 (
    echo  [ERROR] pip install failed. Check your internet connection.
    pause
    exit /b 1
)
echo  [OK] Packages installed
echo.

:: Cleanup old builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

:: Build
echo  Building FileMama.exe ...
echo.
pyinstaller FileMama.spec

if %errorlevel% neq 0 (
    echo.
    echo  [ERROR] Build failed. See error above.
    pause
    exit /b 1
)

echo.
echo  ================================================
echo   BUILD SUCCESSFUL!
echo   Your EXE is at:  dist\FileMama.exe
echo  ================================================
echo.
echo  Copy  dist\FileMama.exe  anywhere you want.
echo  Drop it into a messy folder and double-click!
echo.
pause
