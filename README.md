# Stock Price Alert

## Project Overview
This project consists of scripts for tracking the stock prices of specified tickers. It includes functionalities for fetching historical data, daily updates and setting price alerts according to some rules.

## Disclaimers
This project is for (my) educational purposes. I do not take any financial insights or take any decisions from this project and I do not encourage you to do so. I wrote this for praciting and testing simple coding functionalities. I encourage you to view it this way rather than a financial instrument of some sort.

This is still in a very basic stage and, although it probably won't be more than basic when fully made, I intent to modify some parts, add new alert indicators, organize it into folder properly and document it better.

Today, the script is hardcoded to handle data from 4 months old. It deletes data older than that. This should later be modularized to handle data from any period amount.

## Setup requirements
- Python 3.x
- Required libraries: `yfinance`, `pandas`, `numpy`, `matplotlib`
    - You can `pip install -r requirements.txt`
- A `tickers.txt` file for initial ticker setup. Write the tickers as in the `tickers.txt.sample`, with line breaks, and following yahoo finance's standard.
- A `config.json` as in the `config.json.sample`. It should have the keys

"check_period_months": 4,
"drawdown_threshold": -22.5,
"recovery_threshold": 10,
"moving_average_window": 20,
"moving_average_alert_days": 3