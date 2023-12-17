import json
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
import matplotlib.dates as mdates
from datetime import datetime

with open('config.json') as config_file:
    config = json.load(config_file)
    
def calculate_moving_average(prices, window_size):
    """Calculate the moving average using a specified window size."""
    return np.convolve(prices, np.ones(window_size), 'valid') / window_size

def check_crossing(prices, moving_averages, alert_days):
    """Check if the price and moving average crossed in the last alert_days."""
    for i in range(1, alert_days + 1):
        if (prices[-i] > moving_averages[-i] and prices[-i-1] <= moving_averages[-i-1]) or \
           (prices[-i] < moving_averages[-i] and prices[-i-1] >= moving_averages[-i-1]):
            return True
    return False

def log_crossing(ticker):
    """Log the crossing event to a file."""
    with open("alerts/ma_alerts.txt", "a") as log_file:
        log_file.write(f"Crossing detected for {ticker}\n")

def process_data(file_path, tickers, window_size, alert_days=10):
    """Process the data from the JSON file and plot for specified tickers."""
    if not os.path.exists(file_path):
        print("File not found:", file_path)
        return

    with open(file_path, 'r') as file:
        data = json.load(file)

    for ticker in tickers:
        if ticker in data:
            price_data = data[ticker]
            prices = [day['Price'] for day in price_data]
            dates = [day['Date'] for day in price_data]

            if len(prices) >= window_size:
                moving_averages = calculate_moving_average(prices, window_size)
                plot_data(ticker, prices, moving_averages, dates, window_size)

                if check_crossing(prices, moving_averages, alert_days):
                    print(f"Alert: Price and Moving Average crossed for {ticker} in the last {alert_days} days.")
                    log_crossing(ticker)
        else:
            print(f"Ticker {ticker} not found in data.")


def plot_data(ticker, prices, moving_averages, dates, window_size):
    """Plot the prices and moving averages for a ticker."""
    plt.figure(figsize=(17,8))

    # Convert string dates to datetime objects
    dates = [datetime.strptime(date, '%Y-%m-%d') for date in dates]

    plt.plot(dates, prices, label='Price')
    plt.plot(dates[-len(moving_averages):], moving_averages, label=f'{window_size}-day Moving Average')
    plt.title(f"Price and {window_size}-day Moving Average for {ticker}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()

    # Adjust the locator for less frequent ticks (e.g., every two weeks or every month)
    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))  # Adjust the interval as needed
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))

    # Improve readability of x-axis (dates)
    plt.xticks(rotation=45)
    plt.tight_layout() # Adjust layout to prevent clipping of tick-labels

    plt.show()

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Process and plot stock price data.')
    parser.add_argument('--chart', nargs='+', help='Tickers to plot')
    parser.add_argument('--ma', '--moving_average', type=int, default=config['moving_average_window'], help='Window size for moving average')
    parser.add_argument('--alert', type=int, default=config['moving_average_alert_days'], help='Days to check for crossing')
    args = parser.parse_args()

    # Check if tickers are provided for charting
    if args.chart:
        file_path = "price_history.json"
        process_data(file_path, args.chart, args.ma, args.alert)
