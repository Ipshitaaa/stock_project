"""
moving_average_prediction.py
Simple prediction model using moving average crossover strategy
Place this in: stock_analysis/scripts/moving_average_prediction.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def moving_average_strategy(symbol):
    """
    Simple moving average crossover strategy
    Signal: BUY when short MA crosses above long MA
            SELL when short MA crosses below long MA
    """
    
    print(f"\n📈 Moving Average Strategy for {symbol}")
    print("=" * 50)
    
    # Load data
    filename = f"data/{symbol}.csv"
    data = pd.read_csv(filename, index_col=0, parse_dates=True)
    
    # Calculate moving averages
    data['MA_20'] = data['Close'].rolling(window=20).mean()  # Short term
    data['MA_50'] = data['Close'].rolling(window=50).mean()  # Long term
    
    # Generate signals
    data['Signal'] = 0  # 0 = Hold, 1 = Buy, -1 = Sell
    data['Position'] = 0  # Track current position
    
    # Buy signal: MA_20 crosses above MA_50
    # Sell signal: MA_20 crosses below MA_50
    for i in range(1, len(data)):
        if data['MA_20'].iloc[i] > data['MA_50'].iloc[i] and data['MA_20'].iloc[i-1] <= data['MA_50'].iloc[i-1]:
            data['Signal'].iloc[i] = 1  # Buy
        elif data['MA_20'].iloc[i] < data['MA_50'].iloc[i] and data['MA_20'].iloc[i-1] >= data['MA_50'].iloc[i-1]:
            data['Signal'].iloc[i] = -1  # Sell
    
    # Calculate strategy returns
    data['Daily_Return'] = data['Close'].pct_change()
    data['Strategy_Return'] = 0
    
    position = 0  # 0 = no position, 1 = long position
    for i in range(len(data)):
        if data['Signal'].iloc[i] == 1:  # Buy signal
            position = 1
        elif data['Signal'].iloc[i] == -1:  # Sell signal
            position = 0
        
        data['Position'].iloc[i] = position
        
        # Strategy return = daily return * position (only make money when holding stock)
        if i > 0:
            data['Strategy_Return'].iloc[i] = data['Daily_Return'].iloc[i] * data['Position'].iloc[i-1]
    
    # Calculate cumulative returns
    data['Buy_Hold_Cumulative'] = (1 + data['Daily_Return']).cumprod() - 1
    data['Strategy_Cumulative'] = (1 + data['Strategy_Return']).cumprod() - 1
    
    # Performance summary
    buy_hold_return = data['Buy_Hold_Cumulative'].iloc[-1]
    strategy_return = data['Strategy_Cumulative'].iloc[-1]
    
    print(f"📊 PERFORMANCE RESULTS:")
    print(f"   Buy & Hold Return: {buy_hold_return*100:.2f}%")
    print(f"   Strategy Return: {strategy_return*100:.2f}%")
    print(f"   Difference: {(strategy_return - buy_hold_return)*100:.2f}%")
    
    # Count signals
    buy_signals = len(data[data['Signal'] == 1])
    sell_signals = len(data[data['Signal'] == -1])
    print(f"   Buy Signals: {buy_signals}")
    print(f"   Sell Signals: {sell_signals}")
    
    return data

def plot_strategy(symbol, data):
    """Plot the moving average strategy"""
    
    plt.figure(figsize=(15, 10))
    
    # Plot 1: Price and Moving Averages
    plt.subplot(2, 1, 1)
    plt.plot(data.index, data['Close'], label='Close Price', linewidth=1.5, alpha=0.7)
    plt.plot(data.index, data['MA_20'], label='MA 20', linewidth=1.5)
    plt.plot(data.index, data['MA_50'], label='MA 50', linewidth=1.5)
    
    # Mark buy/sell signals
    buy_signals = data[data['Signal'] == 1]
    sell_signals = data[data['Signal'] == -1]
    
    plt.scatter(buy_signals.index, buy_signals['Close'], 
               color='green', marker='^', s=100, label='Buy Signal', zorder=5)
    plt.scatter(sell_signals.index, sell_signals['Close'], 
               color='red', marker='v', s=100, label='Sell Signal', zorder=5)
    
    plt.title(f'{symbol} - Moving Average Strategy (20/50 day)', fontsize=14, fontweight='bold')
    plt.ylabel('Price ($)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 2: Cumulative Returns Comparison
    plt.subplot(2, 1, 2)
    plt.plot(data.index, data['Buy_Hold_Cumulative'] * 100, 
             label='Buy & Hold', linewidth=2)
    plt.plot(data.index, data['Strategy_Cumulative'] * 100, 
             label='Moving Average Strategy', linewidth=2)
    
    plt.title('Strategy Performance Comparison', fontsize=14, fontweight='bold')
    plt.ylabel('Cumulative Return (%)')
    plt.xlabel('Date')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(f'visuals/{symbol}_moving_average_strategy.png', dpi=300, bbox_inches='tight')
    print(f"✅ Strategy chart saved to visuals/{symbol}_moving_average_strategy.png")
    plt.show()

def test_all_stocks():
    """Test the strategy on all stocks"""
    
    stocks = ['GOOGL', 'JPM', 'PFE', 'AMZN', 'XOM']
    results = {}
    
    print("🚀 TESTING MOVING AVERAGE STRATEGY ON ALL STOCKS")
    print("=" * 60)
    
    for stock in stocks:
        data = moving_average_strategy(stock)
        plot_strategy(stock, data)
        
        # Store results
        buy_hold = data['Buy_Hold_Cumulative'].iloc[-1]
        strategy = data['Strategy_Cumulative'].iloc[-1]
        results[stock] = {
            'buy_hold': buy_hold,
            'strategy': strategy,
            'difference': strategy - buy_hold
        }
    
    # Summary ranking
    print(f"\n🏆 STRATEGY PERFORMANCE RANKING:")
    print("-" * 50)
    sorted_results = sorted(results.items(), key=lambda x: x[1]['difference'], reverse=True)
    
    for i, (stock, perf) in enumerate(sorted_results, 1):
        emoji = "🎯" if perf['difference'] > 0 else "📉"
        print(f"{i}. {stock}: Strategy beat Buy&Hold by {perf['difference']*100:.2f}% {emoji}")
    
    return results

if __name__ == "__main__":
    # Test on all stocks
    results = test_all_stocks()