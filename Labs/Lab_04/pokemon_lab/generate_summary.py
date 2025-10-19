#!/usr/bin/env python3
# ...existing code...
import os
import sys
import pandas as pd

def generate_summary(portfolio_file):
    if not os.path.exists(portfolio_file):
        print(f"Error: {portfolio_file} not found.", file=sys.stderr)
        sys.exit(1)
    df = pd.read_csv(portfolio_file)
    if df.empty:
        print("Portfolio file is empty.")
        return
    total_portfolio_value = df["card_market_value"].sum()
    idx = df["card_market_value"].idxmax()
    most_valuable = df.loc[idx]
    print(f"Total Portfolio Value: ${total_portfolio_value:,.2f}")
    print("Most Valuable Card:")
    print(f"  Name: {most_valuable.get('card_name','N/A')}")
    print(f"  ID: {most_valuable.get('card_id','N/A')}")
    print(f"  Value: ${most_valuable.get('card_market_value',0.0):,.2f}")

def main():
    generate_summary("card_portfolio.csv")

def test():
    generate_summary("test_card_portfolio.csv")

if __name__ == "__main__":
    test()
# ...existing code...