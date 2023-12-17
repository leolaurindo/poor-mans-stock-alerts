import yfinance as yf
import json
import datetime
import pandas as pd
import sys
from pathlib import Path

def fetch_historical_data_for_ticker(ticker):
    try:
        end_date = datetime.datetime.now()
        start_date = end_date - pd.DateOffset(months=4)
        data = yf.Ticker(ticker).history(start=start_date, end=end_date)
        if not data.empty:
            return [{'Date': str(date.date()), 'Price': price} for date, price in data['Close'].items()]
        else:
            return None
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def update_price_history(ticker, historical_data, history):
    if ticker not in history:
        history[ticker] = historical_data
    else:
        # Append new data and remove duplicates
        existing_dates = {entry['Date'] for entry in history[ticker]}
        new_data = [entry for entry in historical_data if entry['Date'] not in existing_dates]
        history[ticker].extend(new_data)

    # Remove data older than 4 months
    four_months_ago = datetime.datetime.now().date() - pd.DateOffset(months=4)
    history[ticker] = [entry for entry in history[ticker] if entry['Date'] >= four_months_ago.isoformat()]

    return history

def save_price_history(history):
    with open('price_history.json', 'w') as file:
        json.dump(history, file)

def update_tickers_file(ticker):
    with open('tickers.txt', 'r+') as file:
        tickers = {line.strip() for line in file}
        if ticker not in tickers:
            file.write(f"\n{ticker}")

def main(ticker):
    historical_data = fetch_historical_data_for_ticker(ticker)
    if historical_data is not None:
        history = load_price_history()
        updated_history = update_price_history(ticker, historical_data, history)
        save_price_history(updated_history)
        update_tickers_file(ticker)
        print(f"Updated price history for {ticker}.")
    else:
        print(f"Failed to fetch historical data for {ticker}.")

def load_price_history():
    history_path = Path('price_history.json')
    if history_path.exists():
        with open(history_path) as file:
            return json.load(file)
    return {}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a ticker symbol. Usage: python update_single_ticker.py <TICKER>")
    else:
        main(sys.argv[1])
