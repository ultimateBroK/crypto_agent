"""
Market data processing for the Crypto Analysis Pro Dashboard.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
import traceback

from src.utils.constants import DEFAULT_PRICE, DEFAULT_VOLUME, DEFAULT_MARKET_CAP, DEFAULT_MOOD, DEFAULT_BUZZ, CACHE_TTL
from src.utils.logger import logger
from src.data_processing.binance_api import (
    get_binance_ticker_data, 
    get_binance_24h_stats, 
    get_default_market_data
)
from src.analytics.technical_indicators import calculate_binance_technical_indicators

# --- In-memory cache for market data ---
market_data_cache: Dict[str, Dict[str, Any]] = {}

def get_market_data(coin_id: str, coin_info: Dict[str, Any]) -> Dict[str, Any]:
    """Get market data for a specific coin using Binance API."""
    try:
        # Check cache first
        if coin_id in market_data_cache:
            cached_data = market_data_cache[coin_id]
            last_updated = datetime.fromisoformat(cached_data.get('last_updated', ''))
            if (datetime.utcnow() - last_updated).total_seconds() < CACHE_TTL:
                logger.info(f"Using cached data for {coin_id}")
                return cached_data

        # For Binance coins
        if coin_info.get('is_on_binance'):
            binance_symbol = coin_info.get('binance_symbol')

            # Get detailed ticker data
            binance_data = get_binance_ticker_data(binance_symbol)

            # Get 24-hour stats
            stats_24h = get_binance_24h_stats(binance_symbol)

            # Initialize result
            result = {
                "price": float(binance_data.get('lastPrice', coin_info.get('price', DEFAULT_PRICE))),
                "volume": float(stats_24h.get('volume', DEFAULT_VOLUME)),
                "cap": float(stats_24h.get('quoteVolume', DEFAULT_VOLUME * 10)),  # Use quote volume as proxy
                "last_updated": datetime.utcnow().isoformat()
            }

            # Price change percentage
            price_change_pct = float(stats_24h.get('priceChangePercent', 0))
            result["price_change_pct"] = price_change_pct

            # Get detailed technical indicators
            tech_indicators = calculate_binance_technical_indicators(binance_symbol, "1d", 50)

            # Add technical indicators
            result.update({
                "rsi_d1": tech_indicators.get('rsi', 50),
                "macd": tech_indicators.get('macd', 0),
                "macd_signal": tech_indicators.get('macd_signal', 0),
                "ema_fast": tech_indicators.get('ema_fast', 0),
                "ema_slow": tech_indicators.get('ema_slow', 0)
            })

            # Set market mood based on indicators
            if price_change_pct > 5 or (tech_indicators.get('rsi', 50) > 65 and price_change_pct > 2):
                result["mood"] = "Bullish"
            elif price_change_pct < -5 or (tech_indicators.get('rsi', 50) < 35 and price_change_pct < -2):
                result["mood"] = "Bearish"
            else:
                result["mood"] = "Neutral"

            # Determine social buzz based on volume
            volume_change_percent = float(stats_24h.get('volumeChangePercent', 0))
            if volume_change_percent > 50:
                result["buzz"] = "High"
            elif volume_change_percent > 10:
                result["buzz"] = "Moderate"
            else:
                result["buzz"] = "Low"

            # Update cache
            market_data_cache[coin_id] = result
            return result
        else:
            # Fallback for non-Binance coins (shouldn't happen with new implementation)
            return get_default_market_data(coin_id)

    except Exception as e:
        logger.error(f"Error getting market data for {coin_id}: {str(e)}")
        logger.error(traceback.format_exc())
        return get_default_market_data(coin_id)

def lookup_coin(query: str, coins: List[Dict[str, str]]) -> Optional[Dict[str, str]]:
    """Find a coin by symbol or name."""
    if not query or not coins:
        return None
    
    # Normalize query
    query = query.strip().lower()

def update_market_data_cache(coin_id: str, data: Dict[str, Any]) -> None:
    """Update the market data cache for a specific coin."""
    try:
        # Add timestamp if not present
        if 'last_updated' not in data:
            data['last_updated'] = datetime.utcnow().isoformat()
            
        # Update the cache
        market_data_cache[coin_id] = data
        logger.info(f"Updated market data cache for {coin_id}")
    except Exception as e:
        logger.error(f"Error updating market data cache for {coin_id}: {str(e)}")
        logger.error(traceback.format_exc())
    
    # First try exact symbol match
    for coin in coins:
        if coin.get('symbol', '').lower() == query:
            return coin
    
    # Then try exact name match
    for coin in coins:
        if coin.get('name', '').lower() == query:
            return coin
    
    # Then try partial symbol match
    for coin in coins:
        if query in coin.get('symbol', '').lower():
            return coin
    
    # Then try partial name match
    for coin in coins:
        if query in coin.get('name', '').lower():
            return coin
    
    # No match found
    return None
