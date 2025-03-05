"""
Mock data functions for cryptocurrency data.
This would be replaced with actual API calls in a production environment.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

def get_coin_data(symbol: str) -> Dict[str, Any]:
    """Get current data for a coin. Mock implementation."""
    # Dictionary of sample data
    sample_data = {
        "BTC": {
            "price": 65420.37,
            "price_change_pct": 2.47,
            "volume": 48293857492,
            "cap": 1275893745928,
            "mood": "Bullish",
            "buzz": "High"
        },
        "ETH": {
            "price": 3645.21,
            "price_change_pct": -1.23,
            "volume": 23857439275,
            "cap": 437892563412,
            "mood": "Neutral",
            "buzz": "Moderate"
        },
        "SOL": {
            "price": 143.67,
            "price_change_pct": 5.82,
            "volume": 7294582938,
            "cap": 62498372634,
            "mood": "Bullish",
            "buzz": "High"
        },
        "ADA": {
            "price": 0.58,
            "price_change_pct": -0.75,
            "volume": 845739284,
            "cap": 20576928374,
            "mood": "Bearish",
            "buzz": "Low"
        },
        "BNB": {
            "price": 608.24,
            "price_change_pct": 1.15,
            "volume": 2895734982,
            "cap": 93482734982,
            "mood": "Bullish",
            "buzz": "Moderate"
        },
        # Default for any other symbol
        "DEFAULT": {
            "price": 100.00,
            "price_change_pct": 0.5,
            "volume": 1000000000,
            "cap": 10000000000,
            "mood": "Neutral",
            "buzz": "Moderate"
        }
    }
    
    return sample_data.get(symbol, sample_data["DEFAULT"])

def get_historical_data(symbol: str, timeframe: str) -> pd.DataFrame:
    """
    Get historical price data for a coin.
    Mock implementation that generates synthetic data.
    """
    # Parse timeframe to determine number of data points
    points = {
        "1d": 24,      # 1 day with hourly data
        "1w": 42,      # 1 week with 4-hour data
        "1m": 30,      # 1 month with daily data
        "3m": 90,      # 3 months with daily data
        "6m": 180,     # 6 months with daily data
        "1y": 365      # 1 year with daily data
    }
    
    n_points = points.get(timeframe, 100)
    
    # Get current price as reference
    current_price = get_coin_data(symbol)["price"]
    
    # Generate synthetic time series data
    np.random.seed(hash(symbol) % 100000)  # Use symbol as seed for consistency
    
    # Generate timestamps
    end_date = datetime.now()
    if timeframe == "1d":
        start_date = end_date - timedelta(days=1)
        date_range = pd.date_range(start=start_date, end=end_date, periods=n_points)
    elif timeframe == "1w":
        start_date = end_date - timedelta(weeks=1)
        date_range = pd.date_range(start=start_date, end=end_date, periods=n_points)
    elif timeframe == "1m":
        start_date = end_date - timedelta(days=30)
        date_range = pd.date_range(start=start_date, end=end_date, periods=n_points)
    elif timeframe == "3m":
        start_date = end_date - timedelta(days=90)
        date_range = pd.date_range(start=start_date, end=end_date, periods=n_points)
    elif timeframe == "6m":
        start_date = end_date - timedelta(days=180)
        date_range = pd.date_range(start=start_date, end=end_date, periods=n_points)
    else:  # 1y
        start_date = end_date - timedelta(days=365)
        date_range = pd.date_range(start=start_date, end=end_date, periods=n_points)
    
    # Generate price data with trend and volatility based on symbol
    if symbol == "BTC":
        trend = 0.0003
        volatility = 0.015
    elif symbol == "ETH":
        trend = 0.0002
        volatility = 0.02
    elif symbol == "SOL":
        trend = 0.0004
        volatility = 0.03
    elif symbol == "ADA":
        trend = 0.0001
        volatility = 0.025
    elif symbol == "BNB":
        trend = 0.0002
        volatility = 0.018
    else:
        trend = 0.0002
        volatility = 0.02
    
    # Start with current price and work backwards
    price = current_price
    prices = [price]
    
    for i in range(1, n_points):
        # Random walk with drift
        price = price * (1 + np.random.normal(trend, volatility))
        prices.append(price)
    
    # Reverse to get chronological order
    prices.reverse()
    
    # Calculate OHLC data
    data = []
    for i in range(n_points):
        base_price = prices[i]
        high_factor = 1 + np.random.uniform(0, volatility)
        low_factor = 1 - np.random.uniform(0, volatility)
        
        if i < n_points - 1:
            close = prices[i + 1]
            open_price = base_price
        else:
            open_price = prices[i - 1]
            close = current_price
        
        high = max(open_price, close) * high_factor
        low = min(open_price, close) * low_factor
        
        # Ensure logical OHLC values
        high = max(high, open_price, close)
        low = min(low, open_price, close)
        
        volume = np.random.uniform(0.5, 1.5) * get_coin_data(symbol)["volume"] / n_points
        
        data.append({
            "open": open_price,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume
        })
    
    # Create DataFrame
    df = pd.DataFrame(data, index=date_range)
    
    # Add technical indicators
    df = add_technical_indicators(df)
    
    return df

def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Add technical indicators to historical data."""
    if df.empty:
        return df
    
    # Copy DataFrame to avoid modifying the original
    df_tech = df.copy()
    
    # Calculate SMA
    df_tech['sma20'] = df_tech['close'].rolling(window=20).mean()
    df_tech['sma50'] = df_tech['close'].rolling(window=50).mean()
    df_tech['sma200'] = df_tech['close'].rolling(window=200).mean()
    
    # Calculate EMA
    df_tech['ema12'] = df_tech['close'].ewm(span=12, adjust=False).mean()
    df_tech['ema26'] = df_tech['close'].ewm(span=26, adjust=False).mean()
    df_tech['ema50'] = df_tech['close'].ewm(span=50, adjust=False).mean()
    df_tech['ema200'] = df_tech['close'].ewm(span=200, adjust=False).mean()
    
    # Calculate MACD
    df_tech['macd'] = df_tech['ema12'] - df_tech['ema26']
    df_tech['macd_signal'] = df_tech['macd'].ewm(span=9, adjust=False).mean()
    df_tech['macd_histogram'] = df_tech['macd'] - df_tech['macd_signal']
    
    # Calculate RSI
    delta = df_tech['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    
    rs = avg_gain / avg_loss
    df_tech['rsi'] = 100 - (100 / (1 + rs))
    
    # Calculate Bollinger Bands
    df_tech['bollinger_middle'] = df_tech['sma20']
    std_dev = df_tech['close'].rolling(window=20).std()
    df_tech['bollinger_upper'] = df_tech['bollinger_middle'] + (std_dev * 2)
    df_tech['bollinger_lower'] = df_tech['bollinger_middle'] - (std_dev * 2)
    df_tech['bb_width'] = (df_tech['bollinger_upper'] - df_tech['bollinger_lower']) / df_tech['bollinger_middle']
    
    return df_tech
