import json
import sys
import matplotlib.pyplot as plt
import pandas as pd

def load_price_history():
    with open('price_history.json', 'r') as file:
        return json.load(file)

def plot_stock_chart(ticker, history):
    if ticker not in history or not history[ticker]:
        print("Ticker not found")
        return

    data = pd.DataFrame(history[ticker])
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    plt.figure(figsize=(10, 6))
    plt.plot(data['Price'], label=ticker)
    plt.title(f'Stock Price Chart for {ticker}')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

def main(ticker):
    history = load_price_history()
    plot_stock_chart(ticker, history)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <TICKER>")
    else:
        main(sys.argv[1])
