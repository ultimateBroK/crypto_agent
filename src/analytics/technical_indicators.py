"""
Technical indicators calculation for the Crypto Analysis Pro Dashboard.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import traceback

from src.utils.logger import logger
from src.utils.constants import DEFAULT_SIGNAL
from src.data_processing.binance_api import get_binance_klines

def calculate_binance_technical_indicators(symbol: str, interval: str = "1d", limit: int = 50) -> Dict[str, float]:
    """Calculate technical indicators using Binance kline data."""
    try:
        # Get kline data
        klines = get_binance_klines(symbol, interval, limit)
        
        if not klines:
            return {
                'rsi': 50,
                'macd': 0,
                'macd_signal': 0,
                'ema_fast': 0,
                'ema_slow': 0
            }
        
        # Convert to dataframe
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])
        
        # Convert types
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = df[col].astype(float)
        
        # Calculate RSI
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        # Calculate EMAs
        ema_fast = df['close'].ewm(span=12, adjust=False).mean()
        ema_slow = df['close'].ewm(span=26, adjust=False).mean()
        
        # Calculate MACD
        macd = ema_fast - ema_slow
        macd_signal = macd.ewm(span=9, adjust=False).mean()
        
        # Get the latest values
        latest_rsi = rsi.iloc[-1]
        latest_macd = macd.iloc[-1]
        latest_macd_signal = macd_signal.iloc[-1]
        latest_ema_fast = ema_fast.iloc[-1]
        latest_ema_slow = ema_slow.iloc[-1]
        
        return {
            'rsi': latest_rsi,
            'macd': latest_macd,
            'macd_signal': latest_macd_signal,
            'ema_fast': latest_ema_fast,
            'ema_slow': latest_ema_slow
        }
    
    except Exception as e:
        logger.error(f"Error calculating technical indicators for {symbol}: {str(e)}")
        logger.error(traceback.format_exc())
        return {
            'rsi': 50,
            'macd': 0,
            'macd_signal': 0,
            'ema_fast': 0,
            'ema_slow': 0
        }

def calculate_technical_indicators(df: pd.DataFrame, selected_indicators: List[str] = None) -> pd.DataFrame:
    """Calculate additional technical indicators for analysis."""
    if df.empty:
        return df
    
    # Default indicators if none specified
    if not selected_indicators:
        selected_indicators = ['rsi', 'macd', 'ema', 'bollinger']
    
    # Make a copy to avoid modifying the original
    result_df = df.copy()
    
    try:
        # RSI (Relative Strength Index)
        if 'rsi' in selected_indicators:
            delta = result_df['close'].diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            
            avg_gain = gain.rolling(window=14).mean()
            avg_loss = loss.rolling(window=14).mean()
            
            rs = avg_gain / avg_loss
            result_df['rsi'] = 100 - (100 / (1 + rs))
        
        # EMA (Exponential Moving Average)
        if 'ema' in selected_indicators:
            result_df['ema12'] = result_df['close'].ewm(span=12, adjust=False).mean()
            result_df['ema26'] = result_df['close'].ewm(span=26, adjust=False).mean()
            result_df['ema50'] = result_df['close'].ewm(span=50, adjust=False).mean()
            result_df['ema200'] = result_df['close'].ewm(span=200, adjust=False).mean()
        
        # MACD (Moving Average Convergence Divergence)
        if 'macd' in selected_indicators:
            result_df['macd'] = result_df['close'].ewm(span=12, adjust=False).mean() - result_df['close'].ewm(span=26, adjust=False).mean()
            result_df['macd_signal'] = result_df['macd'].ewm(span=9, adjust=False).mean()
            result_df['macd_histogram'] = result_df['macd'] - result_df['macd_signal']
        
        # Bollinger Bands
        if 'bollinger' in selected_indicators:
            result_df['sma20'] = result_df['close'].rolling(window=20).mean()
            result_df['std20'] = result_df['close'].rolling(window=20).std()
            result_df['bollinger_upper'] = result_df['sma20'] + (result_df['std20'] * 2)
            result_df['bollinger_lower'] = result_df['sma20'] - (result_df['std20'] * 2)
        
        # Volume indicators
        if 'volume' in selected_indicators:
            result_df['volume_sma20'] = result_df['volume'].rolling(window=20).mean()
            # Volume Oscillator
            result_df['volume_ema5'] = result_df['volume'].ewm(span=5, adjust=False).mean()
            result_df['volume_ema10'] = result_df['volume'].ewm(span=10, adjust=False).mean()
            result_df['volume_oscillator'] = ((result_df['volume_ema5'] - result_df['volume_ema10']) / result_df['volume_ema10']) * 100
        
        return result_df
    
    except Exception as e:
        logger.error(f"Error calculating additional technical indicators: {str(e)}")
        logger.error(traceback.format_exc())
        return df  # Return original dataframe if calculation fails

def get_technical_signal(market_data: Dict[str, Any]) -> str:
    """Determine technical signal based on multiple indicators."""
    try:
        # Extract indicators
        rsi = market_data.get('rsi_d1', 50)
        macd = market_data.get('macd', 0)
        macd_signal = market_data.get('macd_signal', 0)
        ema_fast = market_data.get('ema_fast', 0)
        ema_slow = market_data.get('ema_slow', 0)
        price_change_pct = market_data.get('price_change_pct', 0)
        
        # Initialize scores
        buy_score = 0
        sell_score = 0
        
        # RSI Analysis (0-100)
        # Oversold condition (buy signal)
        if rsi < 30:
            buy_score += 2
        elif rsi < 40:
            buy_score += 1
        
        # Overbought condition (sell signal)
        if rsi > 70:
            sell_score += 2
        elif rsi > 60:
            sell_score += 1
        
        # MACD Analysis
        # Bullish crossover (buy signal)
        if macd > macd_signal and abs(macd - macd_signal) > 0.00001:
            buy_score += 2
        
        # Bearish crossover (sell signal)
        if macd < macd_signal and abs(macd - macd_signal) > 0.00001:
            sell_score += 2
        
        # EMA Analysis
        # Fast EMA above slow EMA (buy signal)
        if ema_fast > ema_slow and abs(ema_fast - ema_slow) / ema_slow > 0.001:
            buy_score += 1
        
        # Fast EMA below slow EMA (sell signal)
        if ema_fast < ema_slow and abs(ema_fast - ema_slow) / ema_slow > 0.001:
            sell_score += 1
        
        # Price change percentage
        if price_change_pct > 5:
            buy_score += 1
        elif price_change_pct < -5:
            sell_score += 1
        
        # Determine signal based on scores
        if buy_score >= 3 and buy_score > sell_score:
            return "buy"
        elif sell_score >= 3 and sell_score > buy_score:
            return "sell"
        else:
            return "hold"
    
    except Exception as e:
        logger.error(f"Error determining technical signal: {str(e)}")
        return DEFAULT_SIGNAL
