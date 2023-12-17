#!/bin/bash
checkInternet() {
    ping -c 1 google.com > /dev/null 2>&1
    return $?
}
while ! checkInternet; do
    echo "Waiting for internet connection..."
    sleep 5
done

# Uncomment and adjust to activate your environment if needed
# source activate stock_alert

# Change 'path/to/script' to the actual path of your script
# cd path/to/script
# -y for allowing the script to prompt you choose whether to plot tickers or not
python daily_price_update.py -y

# Uncomment to open the latest alerts text file
# xdg-open ./alerts/latest_alerts.txt

read -p "Press enter to continue"
