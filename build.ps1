Write-Host "Building Smart Sticky Notes..."

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install required packages
Write-Host "Installing required packages..."
pip install -r requirements.txt
pip install pyinstaller

# Install PyQt6 with all components
Write-Host "Installing PyQt6 components..."
pip install --upgrade PyQt6 PyQt6-Qt6 PyQt6-sip

# Remove pathlib if it exists
Write-Host "Removing pathlib package..."
pip uninstall pathlib -y

# Create a simple icon file if it doesn't exist
if (-not (Test-Path "icon.ico")) {
    Write-Host "Creating icon file..."
    # Create a simple icon using Pillow
    python -c "
from PIL import Image, ImageDraw
img = Image.new('RGBA', (256, 256), (255, 255, 255, 0))
draw = ImageDraw.Draw(img)
draw.rectangle([50, 50, 206, 206], fill='#4CAF50')
draw.rectangle([70, 70, 186, 186], fill='#FFFFFF')
img.save('icon.ico', format='ICO', sizes=[(256, 256)])
"
}

# Clean previous build
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
}
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
}

# Build the executable
Write-Host "Building executable..."
pyinstaller SmartStickyNotes.spec

Write-Host "Build complete!"
Write-Host "The executable is in the 'dist' folder."
Read-Host "Press Enter to continue..." 