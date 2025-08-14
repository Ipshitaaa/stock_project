"""
fetch_data.py
Simple script to download stock data for analysis
Place this in: stock_analysis/scripts/fetch_data.py
"""

import yfinance as yf
import os

def fetch_stock_data():
    """Download 2 years of data for our 5 selected stocks"""
    
    # Your selected companies
    stocks = ['GOOGL', 'JPM', 'PFE', 'AMZN', 'XOM']
    
    # Create data folder if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Created data folder")
    
    print("Fetching stock data...")
    print("-" * 30)
    
    for symbol in stocks:
        print(f"Downloading {symbol}...")
        
        try:
            # Get the data
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="2y")
            
            # Save to CSV
            filename = f"data/{symbol}.csv"
            data.to_csv(filename)
            
            print(f"  ✅ Saved {len(data)} days to {filename}")
            
        except Exception as e:
            print(f"  ❌ Error with {symbol}: {e}")
    
    print("\nData download complete!")

if __name__ == "__main__":
    fetch_stock_data()