@echo off
echo Building Smart Sticky Notes...

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install required packages
echo Installing required packages...
pip install -r requirements.txt
pip install pyinstaller

REM Remove pathlib if it exists
echo Removing pathlib package...
pip uninstall pathlib -y

REM Copy icon file
echo Copying icon file...
copy "D:\Development\Personal\SmartStickyNotes\assets\icons\SmartStickyNotes.ico" "SmartStickyNotes.ico"

REM Build the executable
echo Building executable...
pyinstaller SmartStickyNotes.spec

echo Build complete!
echo The executable is in the 'dist' folder.
pause 