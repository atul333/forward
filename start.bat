@echo off
echo ================================================
echo Telegram Message Forwarder - Setup Script
echo ================================================
echo.

REM Check if config.py exists
if exist config.py (
    echo [OK] config.py found
) else (
    echo [!] config.py not found. Creating from template...
    copy config.example.py config.py
    echo.
    echo ================================================
    echo IMPORTANT: Please edit config.py and add your:
    echo   - API_ID
    echo   - API_HASH
    echo.
    echo Get these from: https://my.telegram.org
    echo ================================================
    echo.
    pause
    exit /b 1
)

REM Check if API credentials are configured
findstr /C:"YOUR_API_ID" config.py >nul
if %errorlevel% equ 0 (
    echo.
    echo ================================================
    echo ERROR: Please configure your API credentials!
    echo.
    echo Edit config.py and replace:
    echo   - YOUR_API_ID with your actual API ID
    echo   - YOUR_API_HASH with your actual API Hash
    echo.
    echo Get these from: https://my.telegram.org
    echo ================================================
    echo.
    pause
    exit /b 1
)

echo [OK] Configuration looks good
echo.
echo Starting the bot...
echo.
python bot.py

pause
