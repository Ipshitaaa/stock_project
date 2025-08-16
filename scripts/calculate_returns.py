"""
calculate_returns.py
Calculate daily returns for all stocks
Place this in: stock_analysis/scripts/calculate_returns.py
"""

import pandas as pd
import numpy as np

def calculate_daily_returns(symbol):
    """Calculate daily returns for a stock"""
    
    print(f"Calculating returns for {symbol}...")
    
    # Load the data
    filename = f"data/{symbol}.csv"
    data = pd.read_csv(filename, index_col=0, parse_dates=True)
    
    # Calculate daily returns (percentage change)
    data['Daily_Return'] = data['Close'].pct_change()
    
    # Drop the first row (NaN)
    data = data.dropna()
    
    # Calculate some summary statistics
    avg_return = data['Daily_Return'].mean()
    volatility = data['Daily_Return'].std()
    total_return = (data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1
    
    print(f"  📊 Average daily return: {avg_return:.4f} ({avg_return*100:.2f}%)")
    print(f"  📈 Total return (2 years): {total_return:.4f} ({total_return*100:.2f}%)")
    print(f"  📉 Daily volatility: {volatility:.4f} ({volatility*100:.2f}%)")
    print(f"  🎯 Best day: +{data['Daily_Return'].max()*100:.2f}%")
    print(f"  💥 Worst day: {data['Daily_Return'].min()*100:.2f}%")
    
    return data

def compare_all_stocks():
    """Compare returns across all stocks"""
    
    stocks = ['GOOGL', 'JPM', 'PFE', 'AMZN', 'XOM']
    
    print("STOCK RETURNS COMPARISON")
    print("=" * 60)
    
    results = {}
    
    for stock in stocks:
        data = calculate_daily_returns(stock)
        
        # Store key metrics
        results[stock] = {
            'avg_daily_return': data['Daily_Return'].mean(),
            'total_return': (data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1,
            'volatility': data['Daily_Return'].std(),
            'best_day': data['Daily_Return'].max(),
            'worst_day': data['Daily_Return'].min()
        }
        
        print("-" * 40)
    
    # Summary comparison
    print("\n🏆 PERFORMANCE RANKING (2-year total return):")
    sorted_returns = sorted(results.items(), key=lambda x: x[1]['total_return'], reverse=True)
    
    for i, (stock, metrics) in enumerate(sorted_returns, 1):
        total_ret = metrics['total_return']
        print(f"  {i}. {stock}: {total_ret*100:+.1f}%")
    
    print("\n⚡ VOLATILITY RANKING (most to least volatile):")
    sorted_vol = sorted(results.items(), key=lambda x: x[1]['volatility'], reverse=True)
    
    for i, (stock, metrics) in enumerate(sorted_vol, 1):
        vol = metrics['volatility']
        print(f"  {i}. {stock}: {vol*100:.2f}% daily volatility")
    
    return results

if __name__ == "__main__":
    results = compare_all_stocks()