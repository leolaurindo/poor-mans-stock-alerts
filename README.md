# Stock Price Alert

## Project Overview
This project consists of scripts for tracking the stock prices of specified tickers. It includes functionalities for fetching historical data, daily updates and setting price alerts according to some monitoring rules.

## Disclaimers
This project is for (my) educational purposes. I do not take any financial insights or take any decisions from this project and I do not encourage you to do so. I wrote this for praciting and testing simple coding functionalities. I encourage you to view it this way rather than a financial instrument of some sort.

This is still in a very basic stage and, although it probably won't be more than basic when fully made, I intent to modify some parts, add new alert indicators, organize it into folder properly and document it better.

Today, the script is hardcoded to handle data from 4 months old. It deletes data older than that. This should later be modularized to handle data from any period amount.

## Setup requirements
- Python 3.x
- Clone this repository
- Required libraries: `yfinance`, `pandas`, `numpy`, `matplotlib`
    - You can `pip install -r requirements.txt`
- A `tickers.txt` file for initial ticker setup. Write the tickers as in the `tickers.txt.sample`, with line breaks, and following Yahoo Finance's standard (i.e. the ticker must appear as it appear on Yahoo's website).
- A `config.json` as in the `config.json.sample`. It should have the keys
    - "check_period_months": which sets how many months the code will check for drawdowns (don't set higher than 4 months yet, as the script is hardcoded to erase data older than four months)
    - "drawdown_threshold": which should be a negative float or interger value indicating the amount of drawdown percentage the code will search
    - "recovery_threshold": which should be a positive float or integer value  indicating the amount percentage growth in price will be considered "recovered"
    - "moving_average_window": which should be an integer of days on top of which the script will calculate the moving averages
    - "moving_average_alert_days": which should be an integer of days that the script will consider when alerting about the moving average and price lines crossing (e.g.: if the lines crossed in the last 3 days, it will alert)

- (Optional): configure `run_daily_update.bat` (for Windows) or `run_daily_update.sh` (for Linux) to activate your python environment and schedule it on workings days using Windows Task Scheduler or Linux cron.

## Features

- Fetch 4-month historical data for a list of stock tickers.
- Perform daily updates of those ticker's prices
- Monitor and alert for significant price drawdowns and recoveries from those drawdowns
- Monitor and alert for additional indicators, such as the movement of moving averages in relation to the stock's price.

## Basic Usage and scripts arguments breakdown

### Initial data fetch

Run `initial_data_fetch.py` to collect the past 4 months of price data for the tickers listed in `tickers.txt`
- `python initial_data_fetch.py`

If any time after setting up the tickers you want to add another ticker, you can run `add_single_ticker.py` and pass the ticker following yahoo finance's standard. This script will fetch the price history for this ticker, add to `price_history.json` and will also add to `tickers.txt`.

### Daily updates and monitoring

The script `daily_price_update.py` is intended to run on working days via task scheculer or cron. This repository already contains `run_daily_update.bat` and `run_daily_update.sh`, which can be configured to call the script on task scheduler/cron respectively.

The script updates `price_history.json` and then iterates over the price history and checks if any of the alert rules set on the indicators and `config.json` are true. If so, it prints to the console and/or writes on `alerts/latest_alerts.txt` and `alerts/all_alerts.txt`.

If you pass the argument `-y` (`python daily_price_update.py -y`), the script will also prompt at the end of the execution if you want to open the price chart for any of the tickers alerted with it's configured moving average.


### Indicators and ad-hoc analysis

For now, we only have two basic indicators that will be monitored by the script.

1. **Drawdowns and recoveries** (`drawdown_check.py`): First, configure the amount of drawdown in percentage you want to monitor and the amount of recovery (also in percentage). The script will monitor if any of the tickers had any drawdown in any period of time. It will, then, check if the stock had recovered from this drawdown for a set amount. It will alert if it had either had a drawdown and/or recovered.

    The script can also be run separatedly and it accepts the following args when doing so:
    - `--ticker`: to select a single ticker you may want to check
    - `--check_period_months`: modify how much months it checks for the drawdown, instead of the four default months.
    - `--drawdown_threshold`: modify the drawndown threshold for the execution
    - `--recovery_threshold`: modify the recovery amount threshold for the execution

2. **Moving average and price cross** (`moving_average.py`): First, configure the `config.json` values (check the **setup requirements**). This script will monitor if a ticker's set moving average crossed it's price value had crossed either up or down in the last `n` days.

    This piece can also be run separatedly, and it accepts the following args when doing so:
    - `--chart`: you can pass multiple tickers and it will plot charts with its moving averages for you to check.
            E.g.: `python moving_averapy.py ITUB3.SA MSFT`
    - `--ma` or `moving_average`: you can pass an integer to modify the moving average window for the execution
    - `--alert`: you can pass an integer to modify how may days the script will search for after the moving average and the price line had crossed.


3. `ticker_plot.py`: It accepts a ticker in yahoo finance's standard as argument and creates a line plot.
