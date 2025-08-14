"""
explore_data.py
Quick script to load and explore our stock data
Place this in: stock_analysis/scripts/explore_data.py
"""

import pandas as pd

def explore_stock_data(symbol):
    """Load and explore data for one stock"""
    
    print(f"Exploring {symbol} data...")
    print("=" * 40)
    
    # Load the CSV file
    filename = f"data/{symbol}.csv"
    
    try:
        data = pd.read_csv(filename)
        
        print(f"✅ Loaded {symbol} data successfully!")
        print(f"📊 Shape: {data.shape[0]} rows, {data.shape[1]} columns")
        
        # Show column names
        print(f"📋 Columns: {list(data.columns)}")
        
        # Show first few rows
        print(f"\n🔝 First 5 rows:")
        print(data.head())
        
        # Show last few rows
        print(f"\n🔚 Last 5 rows:")
        print(data.tail())
        
        # Basic stats for Close price
        print(f"\n📈 Close Price Statistics:")
        print(f"   Current Price: ${data['Close'].iloc[-1]:.2f}")
        print(f"   Highest Price: ${data['Close'].max():.2f}")
        print(f"   Lowest Price: ${data['Close'].min():.2f}")
        print(f"   Average Price: ${data['Close'].mean():.2f}")
        
        return data
        
    except Exception as e:
        print(f"❌ Error loading {symbol}: {e}")
        return None

if __name__ == "__main__":
    # All your stocks
    stocks = ['GOOGL', 'JPM', 'PFE', 'AMZN', 'XOM']
    
    for stock in stocks:
        explore_stock_data(stock)
        print("\n" + "="*50 + "\n")
