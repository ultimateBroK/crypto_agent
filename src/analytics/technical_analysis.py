"""
Technical analysis functions for cryptocurrency data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple

def perform_technical_analysis(df: pd.DataFrame) -> Dict[str, float]:
    """
    Extract technical indicators from a DataFrame with price history.
    Returns a dictionary of indicator values.
    """
    if df.empty:
        return {}
    
    # Get the most recent values
    latest = df.iloc[-1]
    
    # Extract indicators
    indicators = {
        'price': latest['close'],
        'open': latest['open'],
        'high': latest['high'],
        'low': latest['low'],
        'volume': latest['volume']
    }
    
    # Add technical indicators if available
    indicator_names = [
        'sma20', 'sma50', 'sma200', 
        'ema12', 'ema26', 'ema50', 'ema200', 
        'macd', 'macd_signal', 'macd_histogram',
        'rsi', 'bollinger_upper', 'bollinger_lower', 'bb_width'
    ]
    
    for name in indicator_names:
        if name in df.columns:
            indicators[name] = latest[name]
    
    # Calculate additional derived indicators
    if 'bollinger_upper' in indicators and 'bollinger_lower' in indicators:
        current_price = indicators['price']
        upper = indicators['bollinger_upper']
        lower = indicators['bollinger_lower']
        
        # Calculate percentB (position within Bollinger Bands)
        indicators['bb_percentB'] = (current_price - lower) / (upper - lower) if upper != lower else 0.5
        
        # Distance from bands
        indicators['dist_from_upper'] = (upper / current_price - 1) * 100
        indicators['dist_from_lower'] = (current_price / lower - 1) * 100
    
    # Calculate price momentum
    if len(df) >= 14:
        indicators['momentum_1d'] = (latest['close'] / df.iloc[-2]['close'] - 1) * 100
        indicators['momentum_1w'] = (latest['close'] / df.iloc[-7]['close'] - 1) * 100 if len(df) >= 7 else None
        indicators['momentum_1m'] = (latest['close'] / df.iloc[-30]['close'] - 1) * 100 if len(df) >= 30 else None
    
    return indicators

def get_technical_signal(indicators: Dict[str, float]) -> str:
    """Get overall technical signal with improved error handling."""
    try:
        bullish = 0
        bearish = 0
        total_signals = 0

        # Validate input data
        if not indicators or not isinstance(indicators, dict):
            return "Neutral"

        # Check RSI with safe access
        rsi = indicators.get('rsi')
        if rsi is not None:
            if rsi > 70:
                bearish += 1
            elif rsi < 30:
                bullish += 1
            total_signals += 1

        # Check MACD
        if 'macd' in indicators and 'macd_signal' in indicators:
            macd = indicators['macd']
            signal = indicators['macd_signal']
            
            if macd > signal:
                bullish += 1
                if macd > 0 and signal > 0:
                    bullish += 1  # Strong bullish if both above zero
                total_signals += 2
            else:
                bearish += 1
                if macd < 0 and signal < 0:
                    bearish += 1  # Strong bearish if both below zero
                total_signals += 2
        
        # Check EMA crossovers
        if 'ema50' in indicators and 'ema200' in indicators:
            ema50 = indicators['ema50']
            ema200 = indicators['ema200']
            
            if ema50 > ema200:
                bullish += 2  # Golden cross situation
                total_signals += 2
            else:
                bearish += 2  # Death cross situation
                total_signals += 2
        
        # Check price vs EMAs
        if 'price' in indicators and 'ema50' in indicators:
            price = indicators['price']
            ema50 = indicators['ema50']
            
            if price > ema50:
                bullish += 1  # Price above short-term trend
                total_signals += 1
            else:
                bearish += 1  # Price below short-term trend
                total_signals += 1
        
        # Check Bollinger Bands
        if 'bb_percentB' in indicators:
            percent_b = indicators['bb_percentB']
            
            if percent_b < 0.2:
                bullish += 1  # Near lower band - potential bounce
                total_signals += 1
            elif percent_b > 0.8:
                bearish += 1  # Near upper band - potential reversal
                total_signals += 1
        
        # Check momentum
        if 'momentum_1w' in indicators:
            momentum = indicators['momentum_1w']
            if momentum is not None:
                if momentum > 5:
                    bullish += 1  # Strong upward momentum
                    total_signals += 1
                elif momentum < -5:
                    bearish += 1  # Strong downward momentum
                    total_signals += 1
        
        # Safe calculation of final signal
        if total_signals == 0:
            return "Neutral"

        bullish_ratio = bullish / max(total_signals, 1)  # Prevent division by zero
        bearish_ratio = bearish / max(total_signals, 1)

        if bullish_ratio > 0.7:
            return "Strong Buy"
        elif bullish_ratio > 0.5:
            return "Buy"
        elif bearish_ratio > 0.7:
            return "Strong Sell"
        elif bearish_ratio > 0.5:
            return "Sell"
        return "Neutral"

    except Exception as e:
        logger.error(f"Error in technical signal calculation: {str(e)}")
        return "Neutral"  # Safe fallback
