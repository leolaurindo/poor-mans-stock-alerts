@echo off
:checkInternet
ping -n 1 google.com > NUL 2>&1
if %ERRORLEVEL% neq 0 (
    echo Waiting for internet connection...
    timeout /t 5
    goto checkInternet
)

REM Adjust for activating your environment
REM CALL conda activate stock_alert

REM -y for allowing the script to prompt you choose whether to plot tickers or not
REM cd path/to/script
python daily_price_update.py -y

REM start "" ".\alerts\latest_alerts.txt"

pause