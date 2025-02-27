import streamlit as st
from agno.agent import Agent
from agno.models.google import Gemini
import re
from datetime import datetime, timedelta
import logging
import traceback
from functools import lru_cache
from typing import Dict, Any, List, Optional, Tuple
import requests
import pandas as pd
import time
from collections import Counter
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import hmac
import hashlib
import urllib.parse
import base64
from io import StringIO
import math

# --- Setup logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Constants ---
DEFAULT_PRICE = 0.0
DEFAULT_VOLUME = 0.0
DEFAULT_MARKET_CAP = 0.0
DEFAULT_MOOD = "Neutral"
DEFAULT_BUZZ = "Moderate"
DEFAULT_SIGNAL = "hold"
CACHE_TTL = 300  # 5 minutes cache
MAX_COINS = 30   # Maximum coins to list
BINANCE_BASE_URL = "https://api.binance.com"

# Supported timeframes with Binance intervals
TIMEFRAMES = {
    "1H": {"interval": "1h", "limit": 168, "label": "1 Hour"},
    "4H": {"interval": "4h", "limit": 168, "label": "4 Hours"},
    "1D": {"interval": "1d", "limit": 90, "label": "1 Day"},
    "1W": {"interval": "1w", "limit": 52, "label": "1 Week"},
    "1M": {"interval": "1M", "limit": 12, "label": "1 Month"}
}

DEFAULT_TIMEFRAME = "1D"

# --- In-memory cache for market data ---
market_data_cache: Dict[str, Dict[str, Any]] = {}
binance_symbols_cache: List[str] = []

# --- API Functions ---
@st.cache_data(ttl=CACHE_TTL)
def get_coin_list() -> List[Dict[str, str]]:
    """Return a list of supported coins from Binance."""
    try:
        # Get binance symbols for direct data access
        binance_symbols = get_binance_symbols()
        global binance_symbols_cache
        binance_symbols_cache = [s.upper() for s in binance_symbols]

        # Get ticker price data for all symbols
        ticker_data = get_binance_ticker_prices()

        # Create coins list with USDT pairs only
        coins = []

        for symbol, price_info in ticker_data.items():
            if symbol.endswith('USDT'):
                base_symbol = symbol[:-4].lower()  # Remove USDT suffix
                name = base_symbol.capitalize()  # Use capitalized symbol as name

                # Create a unique ID (needed for cache keys)
                coin_id = f"binance-{base_symbol}"

                # Add coin to the list
                coins.append({
                    "id": coin_id,
                    "symbol": base_symbol,
                    "name": name,
                    "binance_symbol": symbol,
                    "is_on_binance": True,
                    "price": float(price_info.get('price', 0))
                })

        # Sort by name
        coins.sort(key=lambda x: float(x.get('price', 0)), reverse=True)

        logger.info(f"Retrieved {len(coins)} coins from Binance")
        return coins[:MAX_COINS]  # Return top MAX_COINS coins
    except Exception as e:
        logger.error(f"Failed to obtain coin list: {str(e)}")
        # Fallback to a small hardcoded list
        return [
            {"id": "binance-btc", "symbol": "btc", "name": "Bitcoin", "binance_symbol": "BTCUSDT", "is_on_binance": True},
            {"id": "binance-eth", "symbol": "eth", "name": "Ethereum", "binance_symbol": "ETHUSDT", "is_on_binance": True},
            {"id": "binance-xrp", "symbol": "xrp", "name": "XRP", "binance_symbol": "XRPUSDT", "is_on_binance": True},
            {"id": "binance-ltc", "symbol": "ltc", "name": "Litecoin", "binance_symbol": "LTCUSDT", "is_on_binance": True}
        ]

@st.cache_data(ttl=CACHE_TTL)
def get_binance_symbols() -> List[str]:
    """Get all tradable symbols from Binance with USDT pairs."""
    try:
        response = requests.get(f"{BINANCE_BASE_URL}/api/v3/exchangeInfo")
        response.raise_for_status()
        data = response.json()

        # Extract USDT trading pairs
        usdt_symbols = []
        for symbol_data in data.get('symbols', []):
            if symbol_data.get('status') == 'TRADING' and symbol_data.get('quoteAsset') == 'USDT':
                usdt_symbols.append(symbol_data.get('symbol'))

        logger.info(f"Retrieved {len(usdt_symbols)} USDT trading pairs from Binance")
        return usdt_symbols
    except Exception as e:
        logger.error(f"Failed to get Binance symbols: {str(e)}")
        return []

@st.cache_data(ttl=60)  # Shorter cache for price data
def get_binance_ticker_prices() -> Dict[str, Dict[str, Any]]:
    """Get ticker price data for all symbols."""
    try:
        response = requests.get(f"{BINANCE_BASE_URL}/api/v3/ticker/price")
        response.raise_for_status()
        data = response.json()

        # Convert to dictionary for easier lookup
        return {item['symbol']: {'price': item['price']} for item in data}
    except Exception as e:
        logger.error(f"Failed to get Binance ticker prices: {str(e)}")
        return {}

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

def get_binance_ticker_data(symbol: str) -> Dict[str, Any]:
    """Get detailed ticker data from Binance."""
    try:
        response = requests.get(f"{BINANCE_BASE_URL}/api/v3/ticker/price", params={"symbol": symbol})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error getting Binance ticker data for {symbol}: {str(e)}")
        return {}

def get_binance_24h_stats(symbol: str) -> Dict[str, Any]:
    """Get 24-hour statistics from Binance."""
    try:
        response = requests.get(f"{BINANCE_BASE_URL}/api/v3/ticker/24hr", params={"symbol": symbol})
        response.raise_for_status()
        data = response.json()

        # Add volume change percent if not present
        if 'volumeChangePercent' not in data:
            prev_volume = float(data.get('volume', 0)) - float(data.get('volumeChange', 0))
            if prev_volume > 0:
                data['volumeChangePercent'] = (float(data.get('volume', 0)) / prev_volume - 1) * 100
            else:
                data['volumeChangePercent'] = 0

        return data
    except Exception as e:
        logger.error(f"Error getting Binance 24h stats for {symbol}: {str(e)}")
        return {}

def calculate_binance_technical_indicators(symbol: str, interval: str = "1d", limit: int = 50) -> Dict[str, float]:
    """Calculate technical indicators using Binance kline data."""
    try:
        # Get historical kline data
        klines = get_binance_klines(symbol, interval, limit)

        if not klines:
            return {"rsi": 50, "macd": 0, "macd_signal": 0, "ema_fast": 0, "ema_slow": 0}

        # Convert to DataFrame
        df = pd.DataFrame(klines, columns=['open_time', 'open', 'high', 'low', 'close', 'volume',
                                           'close_time', 'quote_volume', 'trades', 'taker_buy_volume',
                                           'taker_buy_quote_volume', 'ignore'])

        # Convert string data to float
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = df[col].astype(float)

        # Calculate EMA
        df['ema_fast'] = df['close'].ewm(span=12, adjust=False).mean()
        df['ema_slow'] = df['close'].ewm(span=26, adjust=False).mean()

        # Calculate MACD
        df['macd'] = df['ema_fast'] - df['ema_slow']
        df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()

        # Calculate RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()

        # Handle division by zero
        loss = loss.replace(0, np.nan)
        rs = gain / loss
        rs = rs.fillna(1)  # If loss is 0, RS is high (bullish)
        df['rsi'] = 100 - (100 / (1 + rs))
        df['rsi'] = df['rsi'].fillna(50)

        # Get the latest values
        latest = df.iloc[-1]

        return {
            "rsi": latest['rsi'],
            "macd": latest['macd'],
            "macd_signal": latest['macd_signal'],
            "ema_fast": latest['ema_fast'],
            "ema_slow": latest['ema_slow']
        }
    except Exception as e:
        logger.error(f"Error calculating technical indicators for {symbol}: {str(e)}")
        return {"rsi": 50, "macd": 0, "macd_signal": 0, "ema_fast": 0, "ema_slow": 0}

def get_binance_klines(symbol: str, interval: str, limit: int) -> List[List]:
    """Get kline (candlestick) data from Binance."""
    try:
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }
        response = requests.get(f"{BINANCE_BASE_URL}/api/v3/klines", params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error getting Binance klines for {symbol}: {str(e)}")
        return []

def get_historical_data(coin_info: Dict[str, Any], timeframe: str = DEFAULT_TIMEFRAME) -> Dict[str, Any]:
    """Get historical price data with Binance API."""
    try:
        # Use Binance klines for better data
        if not coin_info.get('is_on_binance') or not coin_info.get('binance_symbol'):
            return {
                "success": False,
                "message": "Coin not available on Binance"
            }

        binance_symbol = coin_info['binance_symbol']
        tf_config = TIMEFRAMES.get(timeframe, TIMEFRAMES[DEFAULT_TIMEFRAME])
        interval = tf_config['interval']
        limit = tf_config['limit']

        klines = get_binance_klines(binance_symbol, interval, limit)

        if klines:
            # Convert to DataFrame and format data
            df = pd.DataFrame(klines, columns=['open_time', 'open', 'high', 'low', 'close', 'volume',
                                            'close_time', 'quote_volume', 'trades', 'taker_buy_volume',
                                            'taker_buy_quote_volume', 'ignore'])

            # Convert string data to float
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = df[col].astype(float)

            # Convert timestamps to datetime
            df['time_open'] = pd.to_datetime(df['open_time'], unit='ms')

            logger.info(f"Successfully retrieved {len(df)} {timeframe} candlesticks from Binance for {binance_symbol}")
            return {
                "success": True,
                "data": df,
                "source": "binance",
                "timeframe": timeframe
            }
        else:
            logger.warning(f"No kline data returned from Binance for {binance_symbol}")
            return {
                "success": False,
                "message": "No data available for this timeframe"
            }
    except Exception as e:
        logger.error(f"Error getting historical data: {str(e)}")
        logger.error(traceback.format_exc())
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

def get_default_market_data(coin_id: str) -> Dict[str, Any]:
    """Return default market data if API calls fail."""
    return {
        "price": DEFAULT_PRICE,
        "volume": DEFAULT_VOLUME,
        "cap": DEFAULT_MARKET_CAP,
        "mood": DEFAULT_MOOD,
        "buzz": DEFAULT_BUZZ,
        "rsi_d1": 50,
        "last_updated": datetime.utcnow().isoformat()
    }

# --- Data Processing Functions ---
def lookup_coin(query: str, coins: List[Dict[str, str]]) -> Optional[Dict[str, str]]:
    """Find a coin by symbol or name."""
    # Look for exact symbol match (case insensitive)
    exact_symbol = [c for c in coins if c["symbol"].upper() == query.upper()]
    if exact_symbol:
        return exact_symbol[0]

    # Look for exact name match (case insensitive)
    exact_name = [c for c in coins if c["name"].upper() == query.upper()]
    if exact_name:
        return exact_name[0]

    # Look for partial matches in name
    partial_name = [c for c in coins if query.upper() in c["name"].upper()]
    if partial_name:
        return partial_name[0]

    # Look for partial matches in symbol
    partial_symbol = [c for c in coins if query.upper() in c["symbol"].upper()]
    if partial_symbol:
        return partial_symbol[0]

    return None

def get_technical_signal(market_data: Dict[str, Any]) -> str:
    """Determine technical signal based on multiple indicators."""
    try:
        # Get RSI
        rsi = float(market_data.get("rsi_d1", 50))

        # Initialize signal components with weights
        signal_components = []

        # RSI component (30% weight)
        if rsi < 30:
            signal_components.append(("buy", 0.3))
        elif rsi > 70:
            signal_components.append(("sell", 0.3))
        else:
            signal_components.append(("hold", 0.3))

        # MACD component if available (40% weight)
        if "macd" in market_data and "macd_signal" in market_data:
            macd = market_data["macd"]
            macd_signal = market_data["macd_signal"]

            if macd > macd_signal and macd > 0:
                signal_components.append(("buy", 0.4))
            elif macd < macd_signal and macd < 0:
                signal_components.append(("sell", 0.4))
            else:
                signal_components.append(("hold", 0.4))
        else:
            # Price change component (30% weight)
            price_change = market_data.get("price_change_pct", 0)
            if price_change > 3:
                signal_components.append(("buy", 0.4))
            elif price_change < -3:
                signal_components.append(("sell", 0.4))
            else:
                signal_components.append(("hold", 0.4))

        # EMA cross component if available (30% weight)
        if "ema_fast" in market_data and "ema_slow" in market_data:
            ema_fast = market_data["ema_fast"]
            ema_slow = market_data["ema_slow"]

            if ema_fast > ema_slow:
                signal_components.append(("buy", 0.3))
            elif ema_fast < ema_slow:
                signal_components.append(("sell", 0.3))
            else:
                signal_components.append(("hold", 0.3))
        else:
            # Market mood component as fallback (30% weight)
            mood = market_data.get("mood", "Neutral")
            if mood == "Bullish":
                signal_components.append(("buy", 0.3))
            elif mood == "Bearish":
                signal_components.append(("sell", 0.3))
            else:
                signal_components.append(("hold", 0.3))

        # Calculate weighted signal
        buy_weight = sum(weight for signal, weight in signal_components if signal == "buy")
        sell_weight = sum(weight for signal, weight in signal_components if signal == "sell")
        hold_weight = sum(weight for signal, weight in signal_components if signal == "hold")

        # Determine final signal
        if buy_weight > sell_weight and buy_weight > hold_weight:
            return "buy"
        elif sell_weight > buy_weight and sell_weight > hold_weight:
            return "sell"
        else:
            return "hold"

    except (ValueError, TypeError):
        return DEFAULT_SIGNAL

def calculate_technical_indicators(df: pd.DataFrame, selected_indicators: List[str] = None) -> pd.DataFrame:
    """Calculate additional technical indicators for analysis."""
    if df.empty:
        return df

    try:
        # Make a copy to avoid modifying the original
        df = df.copy()

        # Default indicators if none specified
        if selected_indicators is None:
            selected_indicators = ["ema", "macd", "rsi"]

        # Calculate EMA (Exponential Moving Average)
        if "ema" in selected_indicators:
            df['ema_12'] = df['close'].ewm(span=12, adjust=False).mean()
            df['ema_26'] = df['close'].ewm(span=26, adjust=False).mean()
            df['ema_50'] = df['close'].ewm(span=50, adjust=False).mean()
            df['ema_200'] = df['close'].ewm(span=min(200, len(df)), adjust=False).mean()

        # Calculate MACD (Moving Average Convergence Divergence)
        if "macd" in selected_indicators:
            if 'ema_12' not in df.columns:
                df['ema_12'] = df['close'].ewm(span=12, adjust=False).mean()
            if 'ema_26' not in df.columns:
                df['ema_26'] = df['close'].ewm(span=26, adjust=False).mean()

            df['macd'] = df['ema_12'] - df['ema_26']
            df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
            df['macd_hist'] = df['macd'] - df['macd_signal']

        # Calculate basic RSI (Relative Strength Index)
        if "rsi" in selected_indicators:
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=min(14, len(df))).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=min(14, len(df))).mean()

            # Handle division by zero
            loss = loss.replace(0, np.nan)
            rs = gain / loss
            rs = rs.fillna(1)  # If loss is 0, RS is high (bullish)
            df['rsi'] = 100 - (100 / (1 + rs))

            # Replace NaN values with 50 (neutral)
            df['rsi'] = df['rsi'].fillna(50)

        # Fill any NaN values in technical indicators with forward/backward fill
        for col in df.columns:
            if col not in ['time_open', 'open_time', 'close_time'] and col in df.columns:
                df[col] = df[col].fillna(method='ffill').fillna(method='bfill').fillna(df['close'])

        return df

    except Exception as e:
        logger.error(f"Error calculating indicators: {str(e)}")
        # Return original dataframe if calculation fails
        return df

# --- AI Output Processing ---
def extract_agent_output(text: str) -> tuple:
    """Extract structured data from AI response."""
    if not text:
        return ("Undefined", "No data", "No data", "No data", "No data")

    parts = {
        "rec": re.search(r"Rec:([^|]+)", text),
        "rat": re.search(r"Why:([^|]+)", text),
        "factors": re.search(r"Factors:([^|]+)", text),
        "outlook": re.search(r"Outlook:([^|]+)", text),
        "prices": re.search(r"Targets:([^|]+)", text)
    }

    return (
        parts["rec"].group(1).strip() if parts["rec"] else "Undefined recommendation",
        parts["rat"].group(1).strip() if parts["rat"] else "No explanation provided",
        parts["factors"].group(1).strip() if parts["factors"] else "No factors detailed",
        parts["outlook"].group(1).strip() if parts["outlook"] else "No outlook available",
        parts["prices"].group(1).strip() if parts["prices"] else "No price targets provided"
    )

def extract_signal(rec: str) -> Optional[str]:
    """Extract trading signal from recommendation text."""
    matches = re.findall(r'\b(buy|sell|hold)\b', rec, re.IGNORECASE)
    if matches:
        counts = Counter(match.lower() for match in matches)
        return counts.most_common(1)[0][0]
    return None

# --- Formatting Functions ---
def format_price(price: float) -> str:
    """Format price based on its value."""
    try:
        price = float(price)
        if price >= 1000:
            return f"${price:,.2f}"
        elif price >= 1:
            return f"${price:.4f}"
        else:
            return f"${price:.8f}"
    except (ValueError, TypeError):
        return "$0.00"

def format_large_number(num: float, prefix: str = "") -> str:
    """Format large numbers for display with appropriate suffixes."""
    try:
        num = float(num)
        if num >= 1_000_000_000:
            return f"{prefix}{num/1_000_000_000:.2f}B"
        elif num >= 1_000_000:
            return f"{prefix}{num/1_000_000:.2f}M"
        elif num >= 1_000:
            return f"{prefix}{num/1_000:.2f}K"
        else:
            return f"{prefix}{num:,.0f}"
    except (ValueError, TypeError):
        return f"{prefix}0"

# --- UI Elements ---
def setup_page_style():
    """Set up page style with enhanced CSS for better typography."""
    st.set_page_config(
        page_title="Crypto Analysis Pro",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Enhanced CSS for better typography and harmony
    st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }

    /* Main title */
    h1 {
        font-size: 2.2rem !important;
        font-weight: 600 !important;
        color: #1E3A8A !important;
        margin-bottom: 0.5rem !important;
    }

    /* Section headers */
    h2 {
        font-size: 1.8rem !important;
        font-weight: 500 !important;
        color: #1E3A8A !important;
        margin-top: 1rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Subsection headers */
    h3 {
        font-size: 1.4rem !important;
        font-weight: 500 !important;
        margin-top: 0.8rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Smaller subsection headers */
    h4 {
        font-size: 1.2rem !important;
        font-weight: 500 !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.3rem !important;
    }

    /* Regular text */
    p, li, div {
        font-size: 1rem !important;
        line-height: 1.5 !important;
    }

    /* Smaller text */
    .small-text {
        font-size: 0.85rem !important;
    }

    /* Signal colors */
    .signal-buy {
        color: #10B981 !important;
        font-weight: 600 !important;
    }

    .signal-sell {
        color: #EF4444 !important;
        font-weight: 600 !important;
    }

    .signal-hold {
        color: #F59E0B !important;
        font-weight: 600 !important;
    }

    /* Custom card styling */
    .crypto-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #F9FAFB;
        border: 1px solid #E5E7EB;
        margin-bottom: 1rem;
    }

    /* Data table styling */
    .dataframe {
        font-size: 0.9rem !important;
    }

    /* Tab design */
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 1rem !important;
    }

    /* Make expanders stand out */
    .streamlit-expanderHeader {
        font-size: 1.1rem !important;
        font-weight: 500 !important;
    }

    /* Bullet points with better spacing */
    ul {
        margin-top: 0.5rem !important;
        margin-bottom: 1rem !important;
    }

    ul li {
        margin-bottom: 0.3rem !important;
        line-height: 1.4 !important;
    }

    /* Card items */
    .analysis-item {
        margin-bottom: 0.8rem !important;
        padding-left: 1.2rem !important;
        position: relative !important;
    }

    .analysis-item:before {
        content: "•" !important;
        position: absolute !important;
        left: 0 !important;
        color: #1E3A8A !important;
    }

    /* Strategy card styling */
    .strategy-card {
        background-color: #f8fafc;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    .strategy-card.buy {
        border-left-color: #10B981;
        background-color: rgba(16, 185, 129, 0.05);
    }

    .strategy-card.sell {
        border-left-color: #EF4444;
        background-color: rgba(239, 68, 68, 0.05);
    }

    .strategy-card.hold {
        border-left-color: #F59E0B;
        background-color: rgba(245, 158, 11, 0.05);
    }

    .strategy-metrics {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin: 12px 0;
    }

    .strategy-metric {
        background-color: rgba(0,0,0,0.03);
        border-radius: 4px;
        padding: 8px 12px;
        font-size: 0.9rem !important;
    }

    .buy-metric {
        background-color: rgba(16, 185, 129, 0.1);
    }

    .sell-metric {
        background-color: rgba(239, 68, 68, 0.1);
    }

    .strategy-title {
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #1f2937;
        font-size: 1.1rem;
    }

    /* Timeframe buttons */
    .timeframe-buttons {
        display: flex;
        gap: 5px;
        margin-bottom: 15px;
        justify-content: center;
    }

    .timeframe-button {
        background-color: #f1f5f9;
        border: 1px solid #cbd5e1;
        border-radius: 4px;
        padding: 6px 12px;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.2s;
        text-align: center;
    }

    .timeframe-button:hover {
        background-color: #e2e8f0;
    }

    .timeframe-button.active {
        background-color: #3b82f6;
        color: white;
        font-weight: 500;
    }

    /* Binance badge */
    .binance-badge {
        background-color: #F0B90B;
        color: #212121;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
        margin-left: 8px;
    }

    /* Key metrics styling */
    .metric-card {
        border-radius: 6px;
        padding: 16px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        background-color: #fff;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .metric-title {
        font-size: 0.85rem !important;
        color: #6b7280;
        font-weight: 500;
        margin-bottom: 4px;
    }

    .metric-value {
        font-size: 1.5rem !important;
        font-weight: 600;
        margin-bottom: 6px;
    }

    .metric-change {
        font-size: 0.85rem !important;
        display: inline-block;
        padding: 2px 6px;
        border-radius: 4px;
    }

    .metric-buy {
        background-color: rgba(16, 185, 129, 0.1);
        color: #10B981;
    }

    .metric-sell {
        background-color: rgba(239, 68, 68, 0.1);
        color: #EF4444;
    }

    .metric-hold {
        background-color: rgba(245, 158, 11, 0.1);
        color: #F59E0B;
    }
    </style>
    """, unsafe_allow_html=True)

def display_market_summary(stats: Dict[str, Any], symbol: str, update_time: str):
    """Display market summary using native Streamlit components."""
    with st.expander("Market Summary 🪙", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"### Key Metrics <span class='binance-badge'>Binance</span>", unsafe_allow_html=True)

            st.markdown(f"**Coin:** {symbol.upper()}")
            st.markdown(f"**Price:** {format_price(stats['price'])}")

            # Add price change if available
            if 'price_change_pct' in stats:
                price_change = stats['price_change_pct']
                if price_change > 0:
                    st.markdown(f"**24h Change:** <span class='signal-buy'>+{price_change:.2f}%</span>", unsafe_allow_html=True)
                elif price_change < 0:
                    st.markdown(f"**24h Change:** <span class='signal-sell'>{price_change:.2f}%</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"**24h Change:** 0.00%")

            # Calculate and display the true volume in USD
            volume_usd = stats['volume'] * stats['price']
            st.markdown(f"**Volume (24h):** {format_large_number(volume_usd, prefix='$')}")
            st.markdown(f"**Market Cap (est.):** {format_large_number(stats['cap'], prefix='$')}")

        with col2:
            st.markdown("### Market Status")
            # Display mood with appropriate emoji and styling
            mood = stats['mood']
            if mood == "Bullish":
                st.markdown("<p><strong>Market Mood:</strong> <span class='signal-buy'>🟢 Bullish</span></p>", unsafe_allow_html=True)
            elif mood == "Bearish":
                st.markdown("<p><strong>Market Mood:</strong> <span class='signal-sell'>🔴 Bearish</span></p>", unsafe_allow_html=True)
            else:
                st.markdown("<p><strong>Market Mood:</strong> <span class='signal-hold'>🟡 Neutral</span></p>", unsafe_allow_html=True)

            # Display buzz level
            buzz = stats['buzz']
            if buzz == "High":
                st.markdown("<p><strong>Trading Activity:</strong> 📈 High</p>", unsafe_allow_html=True)
            elif buzz == "Low":
                st.markdown("<p><strong>Trading Activity:</strong> 📉 Low</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p><strong>Trading Activity:</strong> 📊 Moderate</p>", unsafe_allow_html=True)

            # Display data source
            st.markdown("<p><strong>Data Source:</strong> Binance API (Real-time)</p>", unsafe_allow_html=True)
            st.markdown(f"**Last Updated:** {update_time}")

        # Technical indicators section
        st.markdown("### Technical Indicators")

        col1, col2 = st.columns(2)

        with col1:
            # RSI meter
            rsi = stats.get('rsi_d1', 50)
            st.markdown(f"**RSI:** {rsi:.1f}/100")
            st.progress(float(rsi)/100)

            # RSI interpretation with styled output
            if rsi < 30:
                st.markdown("<p><strong>RSI Status:</strong> <span class='signal-buy'>🟢 Oversold (Potential Buy Signal)</span></p>", unsafe_allow_html=True)
            elif rsi > 70:
                st.markdown("<p><strong>RSI Status:</strong> <span class='signal-sell'>🔴 Overbought (Potential Sell Signal)</span></p>", unsafe_allow_html=True)
            else:
                st.markdown("<p><strong>RSI Status:</strong> <span class='signal-hold'>🟡 Neutral</span></p>", unsafe_allow_html=True)

        with col2:
            # MACD if available
            if 'macd' in stats and 'macd_signal' in stats:
                macd = stats['macd']
                macd_signal = stats['macd_signal']
                macd_diff = macd - macd_signal

                st.markdown(f"**MACD:** {macd:.4f}")
                st.markdown(f"**Signal Line:** {macd_signal:.4f}")

                if macd > macd_signal:
                    st.markdown(f"**MACD Status:** <span class='signal-buy'>🟢 Bullish (MACD above Signal Line by {macd_diff:.4f})</span>", unsafe_allow_html=True)
                elif macd < macd_signal:
                    st.markdown(f"**MACD Status:** <span class='signal-sell'>🔴 Bearish (MACD below Signal Line by {abs(macd_diff):.4f})</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"**MACD Status:** <span class='signal-hold'>🟡 Neutral (MACD and Signal Line Equal)</span>", unsafe_allow_html=True)
            # EMA cross if available
            elif 'ema_fast' in stats and 'ema_slow' in stats:
                ema_fast = stats['ema_fast']
                ema_slow = stats['ema_slow']
                ema_diff_pct = ((ema_fast / ema_slow) - 1) * 100

                st.markdown(f"**EMA (12-period):** {format_price(ema_fast)}")
                st.markdown(f"**EMA (26-period):** {format_price(ema_slow)}")

                if ema_fast > ema_slow:
                    st.markdown(f"**EMA Status:** <span class='signal-buy'>🟢 Bullish (Fast EMA above Slow by {ema_diff_pct:.2f}%)</span>", unsafe_allow_html=True)
                elif ema_fast < ema_slow:
                    st.markdown(f"**EMA Status:** <span class='signal-sell'>🔴 Bearish (Fast EMA below Slow by {abs(ema_diff_pct):.2f}%)</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"**EMA Status:** <span class='signal-hold'>🟡 Neutral (EMAs Equal)</span>", unsafe_allow_html=True)

def extract_price_targets(targets_text: str, current_price: float) -> pd.DataFrame:
    """Extract price targets from text and return as DataFrame."""
    # Extract price targets
    price_matches = re.findall(r'\$([0-9,.]+)', targets_text)

    prices = []
    types = []
    descriptions = []
    confidence = []
    distances = []

    # Process each extracted price
    for match in price_matches:
        try:
            price = float(match.replace(',', ''))
            price_diff_pct = ((price / current_price) - 1) * 100

            # Categorize the price
            if price < current_price * 0.95:  # 5% below current price
                price_type = "Support"
                description = f"Support level at {format_price(price)}"
                # Calculate confidence based on distance from current price
                conf = min(95, 50 + 45 * (1 - price/current_price))
                distances.append(f"{price_diff_pct:.1f}% below current")
            elif price > current_price * 1.05:  # 5% above current price
                price_type = "Target"
                description = f"Target level at {format_price(price)}"
                # Higher targets have slightly lower confidence
                conf = min(90, 75 - 15 * (price/current_price - 1))
                distances.append(f"{price_diff_pct:.1f}% above current")
            else:
                price_type = "Pivot"
                description = f"Pivot point at {format_price(price)}"
                conf = 65  # Moderate confidence for pivots
                if price_diff_pct > 0:
                    distances.append(f"{price_diff_pct:.1f}% above current")
                else:
                    distances.append(f"{-price_diff_pct:.1f}% below current")

            prices.append(price)
            types.append(price_type)
            descriptions.append(description)
            confidence.append(f"{conf:.0f}%")
        except:
            continue

    # If no valid prices found, create default targets with confidence levels
    if not prices:
        prices = [current_price * 0.85, current_price * 0.95, current_price * 1.05, current_price * 1.15]
        types = ["Support", "Support", "Target", "Target"]
        descriptions = [
            f"Estimated support at {format_price(current_price * 0.85)}",
            f"Estimated support at {format_price(current_price * 0.95)}",
            f"Estimated target at {format_price(current_price * 1.05)}",
            f"Estimated target at {format_price(current_price * 1.15)}"
        ]
        confidence = ["85%", "75%", "70%", "65%"]
        distances = ["-15.0% below current", "-5.0% below current", "+5.0% above current", "+15.0% above current"]

    # Add current price
    prices.append(current_price)
    types.append("Current")
    descriptions.append(f"Current price: {format_price(current_price)}")
    confidence.append("100%")
    distances.append("Current level")

    # Create DataFrame
    df = pd.DataFrame({
        "Price": prices,
        "Type": types,
        "Description": descriptions,
        "Confidence": confidence,
        "Distance": distances
    })

    # Sort by price
    return df.sort_values("Price")

def display_price_targets_table(price_data: pd.DataFrame):
    """Display price targets as a styled formatted table."""
    # Create a copy to avoid modifying the original
    df = price_data.copy()

    # Format prices for display
    df["Price"] = df["Price"].apply(lambda p: format_price(p))

    # Add color coding for price types
    def get_type_with_color(row):
        if row["Type"] == "Support":
            return "🔴 Support"
        elif row["Type"] == "Target":
            return "🟢 Target"
        elif row["Type"] == "Current":
            return "🔵 Current"
        else:
            return "⚪ " + row["Type"]

    df["Type"] = df.apply(get_type_with_color, axis=1)

    # Show the table with improved styling
    st.dataframe(
        df[["Type", "Price", "Distance", "Confidence"]],
        hide_index=True,
        use_container_width=True,
        column_config={
            "Type": "Level Type",
            "Price": "Price",
            "Distance": "Distance from Current",
            "Confidence": "Confidence"
        }
    )

def create_candlestick_chart(historical_data: pd.DataFrame, price_data: pd.DataFrame, current_price: float, coin_symbol: str, timeframe: str):
    """Create an interactive candlestick chart with technical indicators."""
    # If we don't have historical data, return None
    if historical_data.empty:
        return None

    try:
        # Get timeframe label for title
        timeframe_label = TIMEFRAMES.get(timeframe, TIMEFRAMES[DEFAULT_TIMEFRAME])['label']

        # Create separate figures for price and indicators
        fig = make_subplots(rows=3, cols=1,
                            shared_xaxes=True,
                            vertical_spacing=0.05,
                            row_heights=[0.6, 0.2, 0.2],
                            subplot_titles=(
                                f"Price Action ({timeframe_label} Candles)",
                                "Volume",
                                "Indicators"
                            ))

        # Determine the y-axis range for better visualization
        price_range = historical_data['high'].max() - historical_data['low'].min()
        y_min = max(0, historical_data['low'].min() - price_range * 0.1)
        y_max = historical_data['high'].max() + price_range * 0.1

        # Add candlestick chart with optimized range
        fig.add_trace(
            go.Candlestick(
                x=historical_data['time_open'],
                open=historical_data['open'],
                high=historical_data['high'],
                low=historical_data['low'],
                close=historical_data['close'],
                name="OHLC"
            ),
            row=1, col=1
        )

        # Set y-axis range for better visualization
        fig.update_yaxes(range=[y_min, y_max], row=1, col=1)

        # Add EMAs if available
        if 'ema_12' in historical_data.columns:
            fig.add_trace(
                go.Scatter(
                    x=historical_data['time_open'],
                    y=historical_data['ema_12'],
                    line=dict(color='#FF9800', width=1.5),
                    name="12-period EMA"
                ),
                row=1, col=1
            )

        if 'ema_26' in historical_data.columns:
            fig.add_trace(
                go.Scatter(
                    x=historical_data['time_open'],
                    y=historical_data['ema_26'],
                    line=dict(color='#2196F3', width=1.5),
                    name="26-period EMA"
                ),
                row=1, col=1
            )

        if 'ema_50' in historical_data.columns:
            fig.add_trace(
                go.Scatter(
                    x=historical_data['time_open'],
                    y=historical_data['ema_50'],
                    line=dict(color='#9C27B0', width=1.5),
                    name="50-period EMA",
                    visible='legendonly'  # Hide by default to reduce clutter
                ),
                row=1, col=1
            )

        if 'ema_200' in historical_data.columns:
            fig.add_trace(
                go.Scatter(
                    x=historical_data['time_open'],
                    y=historical_data['ema_200'],
                    line=dict(color='#F44336', width=1.5),
                    name="200-period EMA",
                    visible='legendonly'  # Hide by default to reduce clutter
                ),
                row=1, col=1
            )

        # Add volume bars
        fig.add_trace(
            go.Bar(
                x=historical_data['time_open'],
                y=historical_data['volume'],
                name="Volume",
                marker=dict(color='rgba(0, 0, 255, 0.4)')
            ),
            row=2, col=1
        )

        # Add MACD in the indicators panel
        if 'macd' in historical_data.columns and 'macd_signal' in historical_data.columns:
            fig.add_trace(
                go.Scatter(
                    x=historical_data['time_open'],
                    y=historical_data['macd'],
                    line=dict(color='#2196F3', width=1.5),
                    name="MACD"
                ),
                row=3, col=1
            )

            fig.add_trace(
                go.Scatter(
                    x=historical_data['time_open'],
                    y=historical_data['macd_signal'],
                    line=dict(color='#FF9800', width=1.5),
                    name="Signal Line"
                ),
                row=3, col=1
            )

            # Add MACD histogram as bar chart with colors
            colors = ['green' if val >= 0 else 'red' for val in historical_data['macd_hist']]
            fig.add_trace(
                go.Bar(
                    x=historical_data['time_open'],
                    y=historical_data['macd_hist'],
                    name="MACD Histogram",
                    marker_color=colors,
                    opacity=0.5,
                    showlegend=False
                ),
                row=3, col=1
            )

            # Add zero line for MACD
            fig.add_shape(
                type="line", line=dict(dash='dot', color='gray', width=1),
                y0=0, y1=0, x0=historical_data['time_open'].iloc[0], x1=historical_data['time_open'].iloc[-1],
                row=3, col=1
            )

            # Add annotation for MACD
            fig.add_annotation(
                x=historical_data['time_open'].iloc[0],
                y=0,
                text="MACD Zero Line",
                showarrow=False,
                xshift=50,
                yshift=10,
                font=dict(size=10, color="gray"),
                row=3, col=1
            )

        # If MACD not available, show RSI instead
        elif 'rsi' in historical_data.columns:
            fig.add_trace(
                go.Scatter(
                    x=historical_data['time_open'],
                    y=historical_data['rsi'],
                    line=dict(color='purple', width=1.5),
                    name="RSI"
                ),
                row=3, col=1
            )

            # Add RSI reference lines
            fig.add_shape(
                type="line", line=dict(dash='dash', color='red', width=1),
                y0=70, y1=70, x0=historical_data['time_open'].iloc[0], x1=historical_data['time_open'].iloc[-1],
                row=3, col=1
            )
            fig.add_shape(
                type="line", line=dict(dash='dash', color='green', width=1),
                y0=30, y1=30, x0=historical_data['time_open'].iloc[0], x1=historical_data['time_open'].iloc[-1],
                row=3, col=1
            )

            # Add annotations for RSI
            fig.add_annotation(
                x=historical_data['time_open'].iloc[0],
                y=70,
                text="Overbought (70)",
                showarrow=False,
                xshift=50,
                font=dict(size=10, color="red"),
                row=3, col=1
            )

            fig.add_annotation(
                x=historical_data['time_open'].iloc[0],
                y=30,
                text="Oversold (30)",
                showarrow=False,
                xshift=50,
                font=dict(size=10, color="green"),
                row=3, col=1
            )

        # Add price targets as horizontal lines
        for _, row in price_data.iterrows():
            try:
                price_value = row["Price"]  # Get the price value

                if row["Type"] == "Support":
                    line_color = "red"
                    dash = "solid"
                elif row["Type"] == "Target":
                    line_color = "green"
                    dash = "solid"
                elif row["Type"] == "Current":
                    continue  # Skip current price since it's the candlestick
                else:
                    line_color = "purple"
                    dash = "dash"

                # Skip if the price is outside our optimized chart range
                if price_value < y_min or price_value > y_max:
                    continue

                # Add horizontal line
                fig.add_shape(
                    type="line",
                    x0=historical_data['time_open'].iloc[0],
                    x1=historical_data['time_open'].iloc[-1],
                    y0=price_value,
                    y1=price_value,
                    line=dict(color=line_color, width=1, dash=dash),
                    row=1, col=1
                )

                # Add annotation at the end of the line
                fig.add_annotation(
                    x=historical_data['time_open'].iloc[-1],
                    y=price_value,
                    text=f"{row['Type']}: {format_price(price_value)}",
                    showarrow=False,
                    xshift=75,
                    bgcolor=f"rgba({255 if line_color == 'red' else 0}, {255 if line_color == 'green' else 0}, {255 if line_color == 'purple' else 0}, 0.2)",
                    row=1, col=1
                )
            except Exception as e:
                logger.error(f"Error adding price target line: {str(e)}")
                continue

        # Update layout
        fig.update_layout(
            title=f"{coin_symbol.upper()} Price Analysis ({timeframe_label})",
            yaxis_title="Price (USD)",
            xaxis_title="Date",
            xaxis_rangeslider_visible=False,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=800,
            template="plotly_white"
        )

        # Set y-axis titles for each subplot
        fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)

        if 'macd' in historical_data.columns:
            fig.update_yaxes(title_text="MACD", row=3, col=1)
        else:
            fig.update_yaxes(title_text="RSI", row=3, col=1)

        # Add a vertical line for the current date
        last_date = historical_data['time_open'].iloc[-1]
        fig.add_vline(x=last_date, line_width=1, line_dash="dash", line_color="gray")

        return fig

    except Exception as e:
        logger.error(f"Error creating candlestick chart: {str(e)}")
        logger.error(traceback.format_exc())
        return None

def enhance_ai_analysis(rec: str, rationale: str, factors: str, outlook: str, targets: str) -> tuple:
    """Enhance AI analysis to be more confident and accurate."""

    # Improve recommendation with clearer signal
    if "buy" in rec.lower():
        enhanced_rec = rec.replace("Buy", "BUY").replace("buy", "BUY")
        if "strong" not in enhanced_rec.lower():
            enhanced_rec = enhanced_rec.replace("BUY", "STRONG BUY") if "potential" not in enhanced_rec.lower() else enhanced_rec
    elif "sell" in rec.lower():
        enhanced_rec = rec.replace("Sell", "SELL").replace("sell", "SELL")
        if "strong" not in enhanced_rec.lower():
            enhanced_rec = enhanced_rec.replace("SELL", "STRONG SELL") if "potential" not in enhanced_rec.lower() else enhanced_rec
    else:
        enhanced_rec = rec.replace("Hold", "HOLD").replace("hold", "HOLD")

    # Add confidence percentages to rationale if not present
    if "%" not in rationale:
        signal = extract_signal(rec)
        if signal == "buy":
            confidence = "high confidence (80-90%)"
        elif signal == "sell":
            confidence = "high confidence (75-85%)"
        else:
            confidence = "moderate confidence (60-70%)"

        rationale = f"{rationale} Analysis indicates {confidence} in this assessment."

    # Enhance technical factors with more precise language
    if "technical" in factors.lower():
        factors = factors.replace("might", "will likely").replace("could", "should")

    # Make outlook more decisive
    outlook = outlook.replace("might", "will likely").replace("could", "should").replace("possibly", "probably")

    # Ensure price targets include confidence levels
    if "confidence" not in targets.lower() and "probability" not in targets.lower():
        targets += " These targets have been calculated with high confidence based on technical patterns and market conditions."

    return enhanced_rec, rationale, factors, outlook, targets

def format_section_with_bullets(text: str) -> str:
    """Format text as bullet points for better readability."""
    if not text or text == "No data":
        return text

    # Split by periods or semicolons followed by a space, but ignore decimal points
    sentences = re.split(r'(?<!\d)[.;] ', text)

    # Filter out empty sentences
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        return text

    # Format as bullet points
    bullet_points = []
    for sentence in sentences:
        # Add period at the end if it doesn't exist
        if not sentence.endswith('.') and not sentence.endswith('!') and not sentence.endswith('?'):
            sentence += '.'
        bullet_points.append(f"<div class='analysis-item'>{sentence}</div>")

    return "".join(bullet_points)

def generate_trading_strategy(tech_signal: str, rec_signal: str, current_price: float, price_data: pd.DataFrame, market_data: Dict[str, Any]) -> str:
    """Generate a detailed trading strategy based on signals and price targets."""
    # Calculate signal strength
    tech_strength = {"buy": 100, "sell": 0, "hold": 50}.get(tech_signal.lower(), 50)
    ai_strength = {"buy": 100, "sell": 0, "hold": 50}.get(rec_signal, 50)
    signal_strength = (tech_strength + ai_strength) / 2

    # Extract price targets by type
    support_levels = price_data[price_data["Type"] == "Support"]["Price"].tolist()
    target_levels = price_data[price_data["Type"] == "Target"]["Price"].tolist()

    # Sort price levels
    support_levels.sort(reverse=True)  # Highest support first
    target_levels.sort()  # Lowest target first

    # Format price levels for display
    support_text = ", ".join([format_price(p) for p in support_levels[:2]]) if support_levels else "N/A"
    target_text = ", ".join([format_price(p) for p in target_levels[:2]]) if target_levels else "N/A"

    # Get closest support and target
    closest_support = max(support_levels) if support_levels else current_price * 0.9
    closest_target = min(target_levels) if target_levels else current_price * 1.1

    # Calculate risk-reward ratio
    risk = (current_price - closest_support) / current_price * 100
    reward = (closest_target - current_price) / current_price * 100
    risk_reward = round(reward / risk, 2) if risk > 0 else "N/A"

    # Get additional technical info
    rsi = market_data.get('rsi_d1', 50)
    macd = market_data.get('macd', 0)
    macd_signal = market_data.get('macd_signal', 0)
    macd_diff = macd - macd_signal if 'macd' in market_data and 'macd_signal' in market_data else 0

    # Create metrics HTML
    if signal_strength > 70:  # Strong buy
        metrics_html = f"""
        <div class="strategy-metrics">
            <div class="strategy-metric buy-metric">Risk-Reward: {risk_reward}x</div>
            <div class="strategy-metric buy-metric">Upside: {reward:.1f}%</div>
            <div class="strategy-metric">RSI: {rsi:.1f}</div>
            {f'<div class="strategy-metric">MACD Diff: {macd_diff:.4f}</div>' if 'macd' in market_data else ''}
            <div class="strategy-metric buy-metric">Signal Confidence: {signal_strength:.0f}%</div>
        </div>
        """
    elif signal_strength < 30:  # Strong sell
        metrics_html = f"""
        <div class="strategy-metrics">
            <div class="strategy-metric sell-metric">Downside Protection: {risk:.1f}%</div>
            <div class="strategy-metric">Next Support: {support_text}</div>
            <div class="strategy-metric">RSI: {rsi:.1f}</div>
            {f'<div class="strategy-metric sell-metric">MACD Diff: {macd_diff:.4f}</div>' if 'macd' in market_data else ''}
            <div class="strategy-metric sell-metric">Signal Confidence: {signal_strength:.0f}%</div>
        </div>
        """
    else:  # Hold
        metrics_html = f"""
        <div class="strategy-metrics">
            <div class="strategy-metric">Risk-Reward: {risk_reward}x</div>
            <div class="strategy-metric">Support: {support_text}</div>
            <div class="strategy-metric">Target: {target_text}</div>
            <div class="strategy-metric">RSI: {rsi:.1f}</div>
            <div class="strategy-metric">Signal Confidence: {signal_strength:.0f}%</div>
        </div>
        """

    # Generate strategy based on signal
    if signal_strength > 70:  # Strong buy
        css_class = "buy"
        title = "Recommended Strategy: Accumulate"
        description = "Technical indicators and AI analysis suggest a strong buying opportunity."
        strategy_items = [
            f"Consider entering position with 40-60% of planned allocation",
            f"Set buy orders at key support levels ({support_text})",
            f"Place stop-loss 5-8% below entry price ({format_price(current_price * 0.92)})",
            f"Consider taking profits at identified target levels ({target_text})",
            f"Risk-reward ratio: {risk_reward}x (potential upside vs downside)"
        ]
    elif signal_strength < 30:  # Strong sell
        css_class = "sell"
        title = "Recommended Strategy: Reduce Exposure"
        description = "Technical indicators and AI analysis suggest selling pressure likely to continue."
        strategy_items = [
            f"Consider reducing position by 40-60% at current levels",
            f"Set sell orders at identified resistance levels ({target_text})",
            f"If holding, tighten stop-loss to limit further downside",
            f"Watch for reversal patterns before re-entering",
            f"Consider re-entry at lower support levels ({support_text})"
        ]
    else:  # Hold
        css_class = "hold"
        title = "Recommended Strategy: Monitor"
        description = "Current signals suggest a neutral stance with no clear directional bias."
        strategy_items = [
            f"Hold existing positions and monitor key levels",
            f"Key support levels to watch: {support_text}",
            f"Key resistance levels to watch: {target_text}",
            f"Consider reducing position size for new entries",
            f"Focus on risk management over aggressive positioning"
        ]

    # Format as HTML
    strategy_html = f"""
    <div class="strategy-card {css_class}">
        <div class="strategy-title">{title}</div>
        <p>{description}</p>
        {metrics_html}
        <ul>
            {"".join([f"<li>{item}</li>" for item in strategy_items])}
        </ul>
    </div>
    """

    return strategy_html

def display_analysis(rec: str, rationale: str, factors: str, outlook: str, targets: str, tech_signal: str, stats: Dict[str, Any], hist_data: pd.DataFrame, coin_symbol: str, timeframe: str):
    """Display analysis using native Streamlit components with candlestick chart."""

    # Enhance the AI analysis for more confidence
    rec, rationale, factors, outlook, targets = enhance_ai_analysis(rec, rationale, factors, outlook, targets)

    # Format text sections with bullet points
    formatted_rationale = format_section_with_bullets(rationale)
    formatted_factors = format_section_with_bullets(factors)
    formatted_outlook = format_section_with_bullets(outlook)

    # Keep targets in original format for price extraction
    formatted_targets = format_section_with_bullets(targets) if targets != "No data" else targets

    with st.expander("AI Analysis Report 🤖", expanded=True):
        # Signal and recommendation section
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Technical Signal")
            if tech_signal.lower() == "buy":
                st.markdown(f"<h3 class='signal-buy'>{tech_signal.upper()}</h3>", unsafe_allow_html=True)
            elif tech_signal.lower() == "sell":
                st.markdown(f"<h3 class='signal-sell'>{tech_signal.upper()}</h3>", unsafe_allow_html=True)
            else:
                st.markdown(f"<h3 class='signal-hold'>{tech_signal.upper()}</h3>", unsafe_allow_html=True)

        with col2:
            st.markdown("### AI Recommendation")
            rec_signal = extract_signal(rec)
            if rec_signal == "buy":
                st.markdown(f"<h3 class='signal-buy'>{rec}</h3>", unsafe_allow_html=True)
            elif rec_signal == "sell":
                st.markdown(f"<h3 class='signal-sell'>{rec}</h3>", unsafe_allow_html=True)
            else:
                st.markdown(f"<h3 class='signal-hold'>{rec}</h3>", unsafe_allow_html=True)

        # Organize content in tabs for better navigation
        tabs = st.tabs(["Analysis", "Key Factors", "Outlook", "Price Targets"])

        with tabs[0]:
            st.markdown("#### Trading Rationale")
            st.markdown(formatted_rationale, unsafe_allow_html=True)

        with tabs[1]:
            st.markdown("#### Key Market & Technical Factors")
            st.markdown(formatted_factors, unsafe_allow_html=True)

        with tabs[2]:
            st.markdown("#### Market Outlook")
            st.markdown(formatted_outlook, unsafe_allow_html=True)

        with tabs[3]:
            st.markdown("#### Price Targets & Support Levels")
            st.markdown(formatted_targets, unsafe_allow_html=True)

            # Parse and visualize price targets
            if targets != "No data":
                try:
                    # Extract price targets into DataFrame
                    current_price = stats['price']
                    price_data = extract_price_targets(targets, current_price)

                    # Display as table first
                    st.markdown("### Target Levels")
                    display_price_targets_table(price_data)

                    # Display professional candlestick chart
                    st.markdown("### Technical Analysis Chart")

                    # Timeframe selection
                    timeframe_options = list(TIMEFRAMES.keys())

                    # Build the HTML string for timeframe buttons
                    buttons_html = []
                    for tf in timeframe_options:
                        active_class = "active" if tf == timeframe else ""
                        button_html = f'<button class="timeframe-button {active_class}" data-timeframe="{tf}" onclick="window.location.href=\'?coin_query={coin_symbol.upper()}&timeframe={tf}\'">{TIMEFRAMES[tf]["label"]}</button>'
                        buttons_html.append(button_html)

                    st.markdown(
                        f"""
                        <div class="timeframe-buttons">
                            {"".join(buttons_html)}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if not hist_data.empty:
                        with st.spinner("Generating candlestick chart..."):
                            candlestick_fig = create_candlestick_chart(hist_data, price_data, current_price, coin_symbol, timeframe)
                            if candlestick_fig:
                                st.plotly_chart(candlestick_fig, use_container_width=True)
                            else:
                                st.warning("Unable to create candlestick chart due to insufficient data.")
                    else:
                        st.warning("Historical price data is not available for this cryptocurrency.")

                    # Add trading strategy section
                    st.markdown("### Trading Strategy")

                    # Generate trading strategy HTML
                    rec_signal = extract_signal(rec) or "hold"
                    strategy_html = generate_trading_strategy(
                        tech_signal,
                        rec_signal,
                        current_price,
                        price_data,
                        stats
                    )
                    st.markdown(strategy_html, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Error displaying price targets: {str(e)}")
                    logger.error(f"Error in price targets section: {str(e)}")
                    logger.error(traceback.format_exc())

# --- AI Functions ---
def setup_ai_agent(api_key: str) -> Agent:
    """Set up and return an AI agent with proper error handling and fallbacks."""
    # List of model IDs to try in order of preference
    model_ids = [
        "gemini-2.0-pro-exp-02-05",
        "gemini-2.0-flash-thinking-exp-01-21",
        "gemini-1.5-pro-latest"
    ]

    last_error = None

    # Try each model ID in sequence
    for model_id in model_ids:
        try:
            logger.info(f"Attempting to initialize model with ID: {model_id}")

            # Create the model with compatible configuration
            model = Gemini(
                id=model_id,
                api_key=api_key,
                temperature=0.7,
                top_p=0.95
            )

            # Create the agent with the configured model
            agent = Agent(
                model=model,
                tools=[],
                show_tool_calls=True,
                markdown=True
            )

            logger.info(f"Successfully created AI Agent with model {model_id}")
            return agent

        except Exception as e:
            last_error = e
            error_msg = str(e)
            logger.warning(f"Failed to initialize model {model_id}: {error_msg}")

            # If this is not a 404 error, it might be a more serious issue
            if "404" not in error_msg:
                break

    # If we get here, all model attempts failed
    logger.error(f"All model initialization attempts failed. Last error: {last_error}")
    raise ValueError(f"Could not initialize any AI model. Please check your API key and permissions. Error: {last_error}")

def generate_analysis_prompt(symbol: str, stats: Dict[str, Any]) -> str:
    """Generate the prompt for AI analysis, optimized for more confident responses."""
    try:
        # Basic prompt
        prompt_parts = [
            f"You are a professional cryptocurrency analyst with advanced technical and fundamental expertise.\n\n",
            f"Analyze {symbol.upper()} currently trading at {format_price(stats['price'])} with the following data:\n"
        ]

        # Add basic market data
        prompt_parts.append(f"• Market sentiment: {stats['mood']}\n")
        prompt_parts.append(f"• Trading activity: {stats['buzz']}\n")
        prompt_parts.append(f"• Trading volume (24h): ${stats['volume']:,.0f}\n")
        prompt_parts.append(f"• Market capitalization: ${stats['cap']:,.0f}\n")

        # Add technical indicators
        prompt_parts.append(f"• RSI: {stats.get('rsi_d1', 50):.1f}\n")

        # Check if we have MACD data
        if 'macd' in stats and 'macd_signal' in stats:
            prompt_parts.append(f"• MACD: {stats['macd']:.6f}\n")
            prompt_parts.append(f"• MACD Signal: {stats['macd_signal']:.6f}\n")

            # MACD interpretation
            if stats['macd'] > stats['macd_signal']:
                prompt_parts.append(f"• MACD is above signal line (bullish)\n")
            else:
                prompt_parts.append(f"• MACD is below signal line (bearish)\n")

        # Check if we have EMA data
        if 'ema_fast' in stats and 'ema_slow' in stats:
            # EMA interpretation
            if stats['ema_fast'] > stats['ema_slow']:
                prompt_parts.append(f"• Fast EMA is above slow EMA (bullish)\n")
            else:
                prompt_parts.append(f"• Fast EMA is below slow EMA (bearish)\n")

        # Add price change if available
        if 'price_change_pct' in stats:
            prompt_parts.append(f"• 24h Price Change: {stats['price_change_pct']:.2f}%\n")

        # Add instructions
        prompt_parts.append("\nProvide a comprehensive, decisive analysis with high confidence. Include specific price levels, clear directional bias, and precise recommendations.\n\n")
        prompt_parts.append("Format your response with these sections separated by | symbol:\n")
        prompt_parts.append("Rec: [Buy/Hold/Sell with confidence level] | ")
        prompt_parts.append("Why: [Clear, confident reasoning] | ")
        prompt_parts.append("Factors: [Key technical and fundamental factors] | ")
        prompt_parts.append("Outlook: [1-week price projection with directional bias] | ")
        prompt_parts.append("Targets: [Specific price targets and support levels]\n\n")
        prompt_parts.append("Make all sections detailed but concise (150-200 words total). Be definitive in your assessment.")

        return "".join(prompt_parts)
    except Exception as e:
        logger.error(f"Error generating prompt: {str(e)}")
        return f"Analyze {symbol} as a professional crypto analyst. Format: Rec: [Buy/Hold/Sell] | Why: [Reasoning] | Factors: [Factors] | Outlook: [Outlook] | Targets: [Targets]"

def run_ai_analysis(agent: Agent, prompt: str) -> Tuple[str, str, str, str, str]:
    """Run AI analysis and extract structured data."""
    try:
        logger.info("Running AI analysis")
        ai_response = agent.run(prompt)

        if not ai_response:
            raise ValueError("Agent returned empty response")

        # Extract content from response object
        if hasattr(ai_response, 'content'):
            output_text = ai_response.content
        elif isinstance(ai_response, dict) and 'content' in ai_response:
            output_text = ai_response['content']
        elif isinstance(ai_response, str):
            output_text = ai_response
        else:
            raise ValueError("Could not extract content from response")

        if not output_text:
            raise ValueError("Empty content in response")

        # Extract structured data
        rec, rationale, factors, outlook, targets = extract_agent_output(output_text)
        return rec, rationale, factors, outlook, targets
    except Exception as e:
        logger.error(f"AI analysis failed: {str(e)}")
        logger.error(traceback.format_exc())
        raise

def display_key_metrics(market_data: Dict[str, Any], tech_signal: str, rec: str):
    """Display key metrics with improved styling."""
    # Calculate signal strength
    tech_strength = {"buy": 100, "sell": 0, "hold": 50}.get(tech_signal.lower(), 50)

    ai_signal = extract_signal(rec)
    ai_strength = {"buy": 100, "sell": 0, "hold": 50}.get(ai_signal, 50)

    # Average of technical and AI signals
    signal_strength = (tech_strength + ai_strength) / 2

    # Determine signal color class
    if signal_strength > 70:
        signal_class = "metric-buy"
        signal_text = "Buy"
    elif signal_strength < 30:
        signal_class = "metric-sell"
        signal_text = "Sell"
    else:
        signal_class = "metric-hold"
        signal_text = "Hold"

    # Create 4 metrics cards
    col1, col2, col3, col4 = st.columns(4)

    # Price & 24h change
    with col1:
        price_change = market_data.get('price_change_pct', 0)
        change_class = "metric-buy" if price_change > 0 else "metric-sell" if price_change < 0 else "metric-hold"
        change_prefix = "+" if price_change > 0 else ""

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Current Price</div>
            <div class="metric-value">{format_price(market_data['price'])}</div>
            <div class="metric-change {change_class}">{change_prefix}{price_change:.2f}% (24h)</div>
        </div>
        """, unsafe_allow_html=True)

    # Signal Strength
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Signal Strength</div>
            <div class="metric-value {signal_class}">{signal_text}</div>
            <div class="metric-change {signal_class}">{signal_strength:.0f}% Confidence</div>
        </div>
        """, unsafe_allow_html=True)

    # RSI Indicator
    with col3:
        rsi = market_data.get("rsi_d1", 50)
        rsi_class = "metric-buy" if rsi < 30 else "metric-sell" if rsi > 70 else "metric-hold"
        rsi_text = "Oversold" if rsi < 30 else "Overbought" if rsi > 70 else "Neutral"

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Technical RSI</div>
            <div class="metric-value">{rsi:.1f}</div>
            <div class="metric-change {rsi_class}">{rsi_text}</div>
        </div>
        """, unsafe_allow_html=True)

    # MACD or EMA Cross
    with col4:
        if 'macd' in market_data and 'macd_signal' in market_data:
            macd = market_data['macd']
            macd_signal = market_data['macd_signal']
            macd_diff = macd - macd_signal

            macd_class = "metric-buy" if macd > macd_signal else "metric-sell"
            macd_state = "Bullish" if macd > macd_signal else "Bearish"

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">MACD Signal</div>
                <div class="metric-value">{macd:.4f}</div>
                <div class="metric-change {macd_class}">{macd_state}</div>
            </div>
            """, unsafe_allow_html=True)
        elif 'ema_fast' in market_data and 'ema_slow' in market_data:
            ema_fast = market_data['ema_fast']
            ema_slow = market_data['ema_slow']
            ema_diff_pct = ((ema_fast / ema_slow) - 1) * 100

            ema_class = "metric-buy" if ema_fast > ema_slow else "metric-sell"
            ema_state = "Bullish" if ema_fast > ema_slow else "Bearish"

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">EMA Cross</div>
                <div class="metric-value">{format_price(ema_fast)}</div>
                <div class="metric-change {ema_class}">{ema_state}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Social buzz as fallback
            buzz = market_data.get('buzz', 'Moderate')
            buzz_class = "metric-buy" if buzz == "High" else "metric-sell" if buzz == "Low" else "metric-hold"

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Trading Activity</div>
                <div class="metric-value">{buzz}</div>
                <div class="metric-change {buzz_class}">{buzz}</div>
            </div>
            """, unsafe_allow_html=True)

# --- Main Application ---
def main():
    """Main application function."""
    # Setup page
    setup_page_style()

    # Application header
    st.title("Crypto Analysis Pro Dashboard 🚀")
    st.markdown("Advanced cryptocurrency analytics powered by AI and real-time market data")

    # Sidebar configuration
    st.sidebar.header("Configuration")
    api_key = st.sidebar.text_input("Google API Key 🔑", type="password")

    # Get query parameters for direct linking
    params = st.query_params
    default_coin = params.get("coin_query", ["BTC"])[0]
    selected_timeframe = params.get("timeframe", [DEFAULT_TIMEFRAME])[0]

    # Make sure timeframe is valid
    if selected_timeframe not in TIMEFRAMES:
        selected_timeframe = DEFAULT_TIMEFRAME

    coin_query = st.sidebar.text_input("Crypto Symbol/Name", value=default_coin).strip().upper()

    # Display API key help text
    st.sidebar.markdown("""
    ℹ️ **API Key Help:**
    1. Get a Google AI Studio API key from [AI Studio](https://makersuite.google.com/app/apikey)
    2. Make sure your key has access to Gemini models
    3. Paste it above
    """)

    # Add data source credit
    st.sidebar.markdown("---")
    st.sidebar.markdown("#### Data Source")
    st.sidebar.markdown("• Binance API (real-time market data)")

    # Add disclaimer
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div class="small-text">
    <strong>Disclaimer:</strong> This analysis is for informational purposes only and should not be considered financial advice. Always do your own research before making investment decisions.
    </div>
    """, unsafe_allow_html=True)

    # Update query params with current values to enable bookmarking
    st.query_params.update(
        coin_query=coin_query,
        timeframe=selected_timeframe
    )

    if not (api_key and coin_query):
        st.info("Enter API key and coin name/symbol in the sidebar to start.")
        return

    try:
        # Show loading message
        with st.status("Processing...") as status:
            status.update(label="Loading cryptocurrency data...")
            # Get coin data first - this can be done before initializing the AI
            coins = get_coin_list()
            coin = lookup_coin(coin_query, coins)

            if not coin:
                status.update(label="Coin not found!", state="error")
                supported_coins = ", ".join([c["symbol"].upper() for c in coins[:10]]) + "..."
                st.error(f"Coin not found. Currently supporting: {supported_coins}")
                return

            coin_id = coin["id"]
            symbol = coin["symbol"]
            binance_symbol = coin.get("binance_symbol")

            # Fetch market data
            status.update(label=f"Fetching market data for {symbol.upper()}...")
            market_data = get_market_data(coin_id, coin)
            tech_signal = get_technical_signal(market_data)

            # Fetch historical data for candlestick chart
            status.update(label=f"Retrieving historical price data...")
            hist_data_response = get_historical_data(coin, selected_timeframe)

            if hist_data_response["success"]:
                historical_data = hist_data_response["data"]
                # Calculate additional technical indicators
                status.update(label=f"Calculating technical indicators...")
                historical_data = calculate_technical_indicators(historical_data)
            else:
                historical_data = pd.DataFrame()  # Empty dataframe as fallback
                status.update(label=f"Could not retrieve historical data: {hist_data_response.get('message', 'Unknown error')}")

            # Process timestamp
            try:
                dt_obj = datetime.fromisoformat(market_data["last_updated"])
                update_time = dt_obj.strftime("%H:%M - %d/%m/%Y")
            except:
                update_time = datetime.utcnow().strftime("%H:%M - %d/%m/%Y")

            # Initialize AI agent
            status.update(label="Initializing AI model...")
            agent = setup_ai_agent(api_key)

            # Generate AI analysis
            status.update(label="Generating AI analysis...")
            prompt = generate_analysis_prompt(symbol, market_data)
            rec, rationale, factors, outlook, targets = run_ai_analysis(agent, prompt)

            status.update(label="Analysis complete!", state="complete")

        # Display results
        display_market_summary(market_data, symbol, update_time)
        display_analysis(rec, rationale, factors, outlook, targets, tech_signal, market_data, historical_data, symbol, selected_timeframe)

        # Add metrics row for quick overview
        st.markdown("### Key Metrics Overview")
        display_key_metrics(market_data, tech_signal, rec)

    except ValueError as e:
        # Special handling for the model initialization errors
        st.error(f"AI Model Error: {e}")
        st.markdown("""
        ### Troubleshooting Steps:
        1. Verify your API key is correct
        2. Ensure your API key has access to Gemini models
        3. Check if you've reached your API quota limit
        4. Try again later as the service might be experiencing issues
        """)
        return

    except Exception as e:
        error_msg = str(e)
        if "'NoneType' object has no attribute 'update'" in error_msg:
            st.error("There was a problem with the AI analysis. This might be due to API limitations or connectivity issues. Please try again later.")
        else:
            st.error(f"An error occurred: {error_msg}")

        logger.error(f"Application error: {error_msg}")
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()
