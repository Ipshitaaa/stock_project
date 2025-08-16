"""
create_price_chart.py
Create price charts for all stocks
Place this in: stock_analysis/scripts/create_price_charts.py
"""

import pandas as pd
import matplotlib.pyplot as plt

def create_price_comparison():
    """Create a simple price comparisonc hart for all stocks"""
    stocks = ['GOOGL', 'JPM', 'PFE', 'AMZN', 'XOM']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']  # Nice colors
    plt.figure(figsize=(14, 8))

    for i, stock in enumerate(stocks):
        filename = f"data/{stock}.csv"
        data = pd.read_csv(filename, index_col=0, parse_dates=True)
        
        # Plot the closing price
        plt.plot(data.index, data['Close'], label=stock, color=colors[i], linewidth=2)
    
    plt.title("Stock Price Comparison (Last 2 Years)", fontsize=16, fontweight='bold')
    plt.xlabel("Date", fontsize=14)
    plt.ylabel("Price (USD)", fontsize=14)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    #Save the chart 
    plt.savefig('visuals/price_comparison.png',dpi=300,bbox_inches='tight')
    print("Price comparison chart saved as visuals/price_comparison.png")
    plt.show()

if __name__ == "__main__":
    create_price_comparison()

    