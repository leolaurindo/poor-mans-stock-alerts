import yfinance as yf
import json
import datetime
import pandas as pd
import argparse

def get_tickers():
    with open('tickers.txt') as file:
        return [line.strip() for line in file]

def fetch_price_history(tickers, duration_months=4):
    end_date = datetime.datetime.now()
    start_date = end_date - pd.DateOffset(months=duration_months)
    price_history = {}

    for ticker in tickers:
        try:
            data = yf.Ticker(ticker).history(start=start_date, end=end_date)
            price_history[ticker] = [{'Date': str(date.date()), 'Price': price} for date, price in data['Close'].items()]
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            price_history[ticker] = []

    return price_history

def save_price_history(history):
    with open('price_history.json', 'w') as file:
        json.dump(history, file)

def main():
    parser = argparse.ArgumentParser()  # Create an argument parser
    parser.add_argument("-m", "--months", type=int, default=4, help="Duration in months")  # Add argument for months
    args = parser.parse_args()  # Parse arguments

    print(f"Fetching data for {args.months} months")  # Debug print

    tickers = get_tickers()
    history = fetch_price_history(tickers, args.months)  # Pass the months argument to fetch_price_history
    save_price_history(history)

if __name__ == "__main__":
    main()
