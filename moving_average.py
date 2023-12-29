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
    if len(prices) < window_size:
        return []  # Not enough data to calculate moving average
    return np.convolve(prices, np.ones(window_size), 'valid') / window_size

def check_crossing(prices, moving_averages, alert_days):
    """
    Check if the price and moving average crossed at any point within the last alert_days.
    A crossing is defined as the price moving from one side of the MA to the other between two consecutive days.
    """
    # Ensure we have enough data points
    if len(prices) < alert_days + 1 or len(moving_averages) < alert_days:
        return False

    # Starting index for the moving averages considering their shorter length due to the window size
    ma_start_index = len(prices) - len(moving_averages)

    # Loop through the specified number of alert_days
    for i in range(alert_days, 0, -1):
        # Indices for the price and moving average on the current and previous day
        price_today_idx = -i
        price_yesterday_idx = price_today_idx - 1
        ma_today_idx = price_today_idx + ma_start_index
        ma_yesterday_idx = price_yesterday_idx + ma_start_index

        # Ensure the indices are within the range of the moving averages list
        if ma_yesterday_idx < 0:
            continue

        # Check for crossing
        price_today = prices[price_today_idx]
        price_yesterday = prices[price_yesterday_idx]
        ma_today = moving_averages[ma_today_idx]
        ma_yesterday = moving_averages[ma_yesterday_idx]

        crossed = (price_today > ma_today) != (price_yesterday > ma_yesterday)
        if crossed:
            return True  # A crossing has occurred

    return False  # No crossing occurred within the alert_days

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
