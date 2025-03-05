"""
Constants for the Crypto Analysis Pro Dashboard.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
DEFAULT_COIN = "BTC"  # Default cryptocurrency
DEFAULT_TIMEFRAME = "1D"  # Default timeframe

# Define available timeframes with their labels and parameters
TIMEFRAMES = {
    "1d": {
        "label": "1 Day",
        "interval": "1h",
        "period": "1d",
        "limit": 24  # 24 hours in a day
    },
    "1w": {
        "label": "1 Week",
        "interval": "4h",
        "period": "1w",
        "limit": 42  # 7 days * 6 (4-hour intervals per day)
    },
    "1m": {
        "label": "1 Month",
        "interval": "1d",
        "period": "1m",
        "limit": 30  # ~30 days in a month
    },
    "3m": {
        "label": "3 Months",
        "interval": "1d",
        "period": "3m",
        "limit": 90  # ~90 days in 3 months
    },
    "6m": {
        "label": "6 Months",
        "interval": "1d",
        "period": "6m",
        "limit": 180  # ~180 days in 6 months
    },
    "1y": {
        "label": "1 Year",
        "interval": "1d",
        "period": "1y",
        "limit": 365  # 365 days in a year
    }
}

# Technical indicator thresholds
TECH_INDICATOR_THRESHOLDS = {
    "rsi": {
        "overbought": 70,
        "oversold": 30,
        "neutral_low": 45,
        "neutral_high": 55
    },
    "macd": {
        "signal_threshold": 0
    },
    "bollinger": {
        "band_threshold": 0.8
    }
}

# Styling color constants
COLORS = {
    # Main colors
    "buy": "#10B981",     # Green
    "sell": "#EF4444",    # Red
    "hold": "#FBBF24",    # Yellow
    "neutral": "#94A3B8", # Gray
    
    # Accent colors
    "primary": "#3B82F6",     # Blue
    "secondary": "#8B5CF6",   # Purple
    "background": "#1E293B",  # Dark blue
    "card": "#1E1E1E",        # Dark gray
    "text": "#F1F5F9",        # Light gray
    "muted": "#94A3B8"        # Medium gray
}

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "dummy_key")
