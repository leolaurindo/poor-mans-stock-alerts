import pandas as pd
import json
import sys
import argparse

with open('config.json') as config_file:
    config = json.load(config_file)

def check_drawdowns(ticker, history, check_period_months, drawdown_threshold, recovery_threshold):
    if ticker not in history or not history[ticker]:
        return False
    df = pd.DataFrame(history[ticker])
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df.sort_index(inplace=True)

    end_date = df.index[-1]
    start_date = end_date - pd.DateOffset(months=check_period_months)
    drawdown_detected = False

    for date, row in df.loc[start_date:end_date].iterrows():
        for past_date, past_row in df.loc[start_date:date].iterrows():
            drawdown = (row['Price'] - past_row['Price']) / past_row['Price'] * 100

            if drawdown <= drawdown_threshold:
                drawdown_detected = True
            elif drawdown_detected and drawdown > recovery_threshold:
                return True

    return drawdown_detected

def check_all_tickers(history, check_period_months, drawdown_threshold, recovery_threshold):
    results = {}
    for ticker in history.keys():
        result = check_drawdowns(ticker, history, check_period_months, drawdown_threshold, recovery_threshold)
        if result:  # Only store results where drawdown is detected and not recovered
            results[ticker] = result
    return results

def parse_args():
    parser = argparse.ArgumentParser(description='Check stock drawdowns.')
    parser.add_argument('--ticker', help='Ticker symbol to check', default=None)
    parser.add_argument('--check_period_months', help='Period for checking drawdowns in months', type=int, default=config['check_period_months'])
    parser.add_argument('--drawdown_threshold', help='Threshold for drawdown detection', type=float, default=config['drawdown_threshold'])
    parser.add_argument('--recovery_threshold', help='Threshold for recovery detection', type=float, default=config['recovery_threshold'])
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    # Load history from a file or other source
    with open('price_history.json') as file:
        history = json.load(file)

    if args.ticker:
        # Check a specific ticker
        result = check_drawdowns(args.ticker, history, args.check_period_months, args.drawdown_threshold, args.recovery_threshold)
        print(f"Drawdown check for {args.ticker}: {result}")
    else:
        # Check all tickers and display only those with drawdowns not recovered
        results = check_all_tickers(history, args.check_period_months, args.drawdown_threshold, args.recovery_threshold)
        for ticker, result in results.items():
            print(f"Drawdown detected for {ticker}")