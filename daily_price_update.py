import argparse
import logging
import yfinance as yf
import json
import datetime
import numpy as np
import pandas as pd
from drawdown_check import check_drawdowns
from moving_average import calculate_moving_average, check_crossing, log_crossing, plot_data  # Importing from moving_average.py
from pathlib import Path

with open('config.json') as config_file:
    config = json.load(config_file)

def setup_logging():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[
                            logging.FileHandler('alerts/latest_alerts.txt', mode='w'),
                            logging.FileHandler('alerts/all_alerts.txt', mode='a')
                        ])
    logging.getLogger('yfinance').setLevel(logging.ERROR)

setup_logging()

def get_tickers():
    with open('tickers.txt') as file:
        return [line.strip() for line in file]

def fetch_current_prices(tickers):
    prices = {}
    for ticker in tickers:
        try:
            data = yf.Ticker(ticker).history(period="1d")
            prices[ticker] = data['Close'].iloc[-1] if not data.empty else None
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            prices[ticker] = None
    return prices

def load_price_history():
    history_path = Path('price_history.json')
    if history_path.exists():
        with open(history_path) as file:
            return json.load(file)
    return {}

def save_price_history(history):
    with open('price_history.json', 'w') as file:
        json.dump(history, file)

def plot_data_from_history(ticker, history, window_size):
    price_data = history.get(ticker, [])
    if price_data:
        prices = [day['Price'] for day in price_data]
        dates = [day['Date'] for day in price_data]
        moving_averages = calculate_moving_average(np.array(prices), window_size)
        plot_data(ticker, prices, moving_averages, dates, window_size)

def main():

    try:
        logging.info("Starting daily price update.")
        print("Starting daily price update.")
        tickers = get_tickers()
        prices = fetch_current_prices(tickers)
        history = load_price_history()

        today = datetime.datetime.now().date()

        for ticker, price in prices.items():
            if price is None:
                logging.warning(f"No price data for {ticker}")
                print(f"No price data for {ticker}") 
                continue

            if ticker not in history:
                history[ticker] = []

            if check_drawdowns(ticker,
                                history,
                                config['check_period_months'],
                                config['drawdown_threshold'],
                                config['recovery_threshold']):
                alert_message = f"ALERT: {ticker} has hit the drawdown criteria."
                logging.info(alert_message)
                print(alert_message)
                if ticker not in alerted_tickers:
                    alerted_tickers.append(ticker)

            price_data = [entry['Price'] for entry in history[ticker]]
            if len(price_data) >= config['moving_average_window']:
                moving_avg = calculate_moving_average(np.array(price_data), config['moving_average_window'])
                if check_crossing(np.array(price_data), moving_avg, config['moving_average_alert_days']):
                    alert_message = f"ALERT: Price and {config['moving_average_window']} days Moving Average crossed for {ticker} in the last {config['moving_average_alert_days']} days."
                    logging.info(alert_message)
                    print(alert_message)
                    log_crossing(ticker)

                    # Add ticker to alerted list if not already present
                    if ticker not in alerted_tickers:
                        alerted_tickers.append(ticker)

            # Remove data older than 4 months
            four_months_ago = today - pd.DateOffset(months=4)
            history[ticker] = [entry for entry in history[ticker] if entry['Date'] >= four_months_ago.isoformat()]

        save_price_history(history)
        logging.info("Daily price update completed successfully.")
        print("Daily price update completed successfully.")

        if args.chart and alerted_tickers:
            print("Would you like to open the chart for the alerted tickers? (close this console if not)")
            print("0. Open all")
            for i, ticker in enumerate(alerted_tickers, start=1):
                print(f"{i}. {ticker}")

            choice = input("Enter your choice (number): ")
            try:
                choice = int(choice)
                if choice == 0:
                    for ticker in alerted_tickers:
                        plot_data_from_history(ticker, history, config['moving_average_window'])
                elif 1 <= choice <= len(alerted_tickers):
                    plot_data_from_history(alerted_tickers[choice - 1], history, config['moving_average_window'])
            except ValueError:
                print("Invalid input. No charts will be opened.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    alerted_tickers = []
    parser = argparse.ArgumentParser(description='Process and plot stock price data.')
    parser.add_argument('--chart', '-y', action='store_true', help='Enable chart display for alerted tickers')
    # Add other arguments as needed
    args = parser.parse_args()
    main()