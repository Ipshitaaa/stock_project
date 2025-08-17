"""
create_correlation_heatmap.py
Create a correlation heatmap to see how stocks move together
Place this in: stock_analysis/scripts/create_correlation_heatmap.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def create_correlation_heatmap():
    """Create a correlation heatmap for stock daily returns"""
    
    stocks = ['GOOGL', 'JPM', 'PFE', 'AMZN', 'XOM']
    
    # Collect daily returns for all stocks
    returns_data = {}
    
    for stock in stocks:
        filename = f"data/{stock}.csv"
        data = pd.read_csv(filename, index_col=0, parse_dates=True)
        
        # Calculate daily returns
        daily_returns = data['Close'].pct_change().dropna()
        returns_data[stock] = daily_returns
    
    # Create DataFrame
    returns_df = pd.DataFrame(returns_data)
    
    # Calculate correlation matrix
    correlation_matrix = returns_df.corr()
    
    # Create the heatmap
    plt.figure(figsize=(10, 8))
    
    # Create heatmap with color map
    im = plt.imshow(correlation_matrix, cmap='RdBu', aspect='auto', vmin=-1, vmax=1)
    
    # Add labels
    plt.xticks(range(len(stocks)), stocks, fontsize=12)
    plt.yticks(range(len(stocks)), stocks, fontsize=12)
    
    # Add correlation values as text
    for i in range(len(stocks)):
        for j in range(len(stocks)):
            value = correlation_matrix.iloc[i, j]
            plt.text(j, i, f'{value:.2f}', ha='center', va='center', 
                    color='white' if abs(value) > 0.5 else 'black', fontsize=11)
    
    # Add colorbar
    cbar = plt.colorbar(im)
    cbar.set_label('Correlation Coefficient', fontsize=12)
    
    plt.title('Stock Returns Correlation Matrix', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    
    # Save the chart
    plt.savefig('visuals/correlation_heatmap.png', dpi=300, bbox_inches='tight')
    print("✅ Correlation heatmap saved to visuals/correlation_heatmap.png")
    
    # Print some insights
    print("\n📊 CORRELATION INSIGHTS:")
    print("-" * 40)
    
    # Find highest and lowest correlations (excluding diagonal)
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool), k=1)
    correlations = correlation_matrix.where(mask).stack().sort_values(ascending=False)
    
    print(f"🔗 Highest correlation: {correlations.index[0][0]} & {correlations.index[0][1]} = {correlations.iloc[0]:.3f}")
    print(f"🔗 Lowest correlation: {correlations.index[-1][0]} & {correlations.index[-1][1]} = {correlations.iloc[-1]:.3f}")
    
    plt.show()
    
    return correlation_matrix

if __name__ == "__main__":
    corr_matrix = create_correlation_heatmap()