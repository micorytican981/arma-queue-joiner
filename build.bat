@echo off
cd /d "%~dp0"
echo ============================================
echo   Building Arma Reforger Queue Joiner
echo ============================================
echo.

echo [1/3] Installing dependencies...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)

echo [2/3] Installing PyInstaller...
pip install pyinstaller --quiet

echo [3/3] Building executable...
pyinstaller --onefile --windowed --name "ArmaQueueJoiner" --icon=icon.ico --hidden-import=mss --add-data "icon.ico;." app.py

echo.
echo Done! Executable is in the dist\ folder.
echo.
pause