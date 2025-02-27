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
import time

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
COINPAPRIKA_BASE_URL = "https://api.coinpaprika.com/v1"

# --- In-memory cache for market data ---
market_data_cache: Dict[str, Dict[str, Any]] = {}

# --- API Functions ---
@st.cache_data(ttl=CACHE_TTL)
def get_coin_list() -> List[Dict[str, str]]:
    """Return a list of supported coins using Coinpaprika API."""
    try:
        # Use Coinpaprika API to fetch available coins
        response = requests.get(f"{COINPAPRIKA_BASE_URL}/coins")
        response.raise_for_status()
        data = response.json()

        # Filter active coins only
        active_coins = [coin for coin in data if coin.get('is_active') is True]

        # Sort by rank to get the most important coins first
        active_coins.sort(key=lambda x: int(x.get('rank', 9999)))

        # Convert to our standard format
        coins = []
        for coin in active_coins[:MAX_COINS]:  # Limit to top MAX_COINS coins
            coin_id = coin['id']
            symbol = coin['symbol'].lower()
            name = coin['name']

            coins.append({
                "id": coin_id,
                "symbol": symbol,
                "name": name
            })

        logger.info(f"Retrieved {len(coins)} coins from Coinpaprika")
        return coins
    except Exception as e:
        logger.error(f"Failed to obtain coin list: {str(e)}")
        # Fallback to a small hardcoded list
        return [
            {"id": "btc-bitcoin", "symbol": "btc", "name": "Bitcoin"},
            {"id": "eth-ethereum", "symbol": "eth", "name": "Ethereum"},
            {"id": "xrp-xrp", "symbol": "xrp", "name": "XRP"},
            {"id": "ltc-litecoin", "symbol": "ltc", "name": "Litecoin"}
        ]

# --- Market data functions ---
def get_market_data(coin_id: str) -> Dict[str, Any]:
    """Get market data for a specific coin using Coinpaprika API."""
    try:
        # Check cache first
        if coin_id in market_data_cache:
            cached_data = market_data_cache[coin_id]
            last_updated = datetime.fromisoformat(cached_data.get('last_updated', ''))
            if (datetime.utcnow() - last_updated).total_seconds() < CACHE_TTL:
                logger.info(f"Using cached data for {coin_id}")
                return cached_data

        # Get ticker data from Coinpaprika
        response = requests.get(f"{COINPAPRIKA_BASE_URL}/tickers/{coin_id}")
        response.raise_for_status()
        data = response.json()

        # Extract relevant information
        price = float(data.get('quotes', {}).get('USD', {}).get('price', DEFAULT_PRICE))
        volume_24h = float(data.get('quotes', {}).get('USD', {}).get('volume_24h', DEFAULT_VOLUME))
        market_cap = float(data.get('quotes', {}).get('USD', {}).get('market_cap', DEFAULT_MARKET_CAP))

        # Generate sentiment data
        sentiment = get_market_sentiment(coin_id, price, data)

        # Create the market data object
        result = {
            "price": price,
            "volume": volume_24h,
            "cap": market_cap,
            "mood": sentiment["market_mood"],
            "buzz": sentiment["social_buzz"],
            "rsi_d1": sentiment["rsi_d1"],
            "last_updated": datetime.utcnow().isoformat()
        }

        # Update cache
        market_data_cache[coin_id] = result
        return result

    except Exception as e:
        logger.error(f"Error getting market data for {coin_id}: {str(e)}")
        logger.error(traceback.format_exc())
        return get_default_market_data(coin_id)

def get_market_sentiment(coin_id: str, current_price: float, ticker_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Generate market sentiment data based on ticker trends."""
    try:
        # If we have ticker data, use it to determine real sentiment
        if ticker_data:
            # Calculate daily change percentage
            percent_change_24h = ticker_data.get('quotes', {}).get('USD', {}).get('percent_change_24h', 0)

            # Determine mood based on 24h movement
            if percent_change_24h > 5:
                mood = "Bullish"
            elif percent_change_24h < -5:
                mood = "Bearish"
            else:
                mood = "Neutral"

            # Calculate "buzz" based on volume and market cap ratio
            volume_24h = ticker_data.get('quotes', {}).get('USD', {}).get('volume_24h', 0)
            market_cap = ticker_data.get('quotes', {}).get('USD', {}).get('market_cap', 1)

            # Volume to market cap ratio as a percentage
            volume_to_cap_ratio = (volume_24h / market_cap) * 100 if market_cap > 0 else 0

            if volume_to_cap_ratio > 15:
                buzz = "High"
            elif volume_to_cap_ratio > 5:
                buzz = "Moderate"
            else:
                buzz = "Low"

            # Calculate pseudo-RSI based on recent price movements
            # This is a simplified approximation
            percent_change_7d = ticker_data.get('quotes', {}).get('USD', {}).get('percent_change_7d', 0)
            percent_change_24h = ticker_data.get('quotes', {}).get('USD', {}).get('percent_change_24h', 0)
            percent_change_1h = ticker_data.get('quotes', {}).get('USD', {}).get('percent_change_1h', 0)

            # Weight recent changes more heavily
            weighted_change = (percent_change_1h * 3 + percent_change_24h * 2 + percent_change_7d) / 6

            # Convert to a pseudo-RSI scale (0-100)
            # RSI = 100 - (100 / (1 + RS)) where RS = avg gain / avg loss
            # We'll use a simplified calculation based on our weighted change
            rsi = 50 + (weighted_change * 1.5)  # Simple linear transform
            rsi = max(0, min(100, rsi))  # Clamp to 0-100 range

            return {
                "market_mood": mood,
                "social_buzz": buzz,
                "rsi_d1": rsi
            }

        # Fallback to the random but consistent method if no ticker data
        import random

        # Seed random with coin_id and current day to keep sentiment consistent for a day
        day_of_year = datetime.utcnow().timetuple().tm_yday
        random.seed(f"{coin_id}-{day_of_year}")

        # Generate pseudo-random sentiment values
        moods = ["Bearish", "Neutral", "Bullish"]
        buzz_levels = ["Low", "Moderate", "High"]

        mood = random.choices(moods, weights=[0.3, 0.4, 0.3])[0]
        buzz = random.choices(buzz_levels, weights=[0.2, 0.5, 0.3])[0]
        rsi = max(0, min(100, random.normalvariate(50, 15)))

        return {
            "market_mood": mood,
            "social_buzz": buzz,
            "rsi_d1": rsi
        }
    except Exception as e:
        logger.error(f"Error generating sentiment data: {str(e)}")
        return {
            "market_mood": DEFAULT_MOOD,
            "social_buzz": DEFAULT_BUZZ,
            "rsi_d1": 50
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
    """Determine technical signal based on RSI."""
    rsi = market_data.get("rsi_d1", 50)
    try:
        rsi = float(rsi)
        if rsi < 30:
            return "buy"
        elif rsi > 70:
            return "sell"
        else:
            return "hold"
    except (ValueError, TypeError):
        return DEFAULT_SIGNAL

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
    from collections import Counter
    matches = re.findall(r'\b(buy|sell|hold)\b', rec, re.IGNORECASE)
    if matches:
        counts = Counter(match.lower() for match in matches)
        return counts.most_common(1)[0][0]
    return None

# --- Formatting Functions ---
def format_recommendation(rec: str, inline: bool = False) -> str:
    """Format recommendation text with color based on signal."""
    signal = extract_signal(rec)

    color_map = {
        "buy": "#28a745",  # Richer green
        "sell": "#dc3545",  # Richer red
        "hold": "#6c757d",  # Darker gray
        None: "#343a40"     # Near black
    }

    color = color_map.get(signal, "#343a40")

    if inline:
        return f"<span style='font-size:1.5em; font-weight:bold; color:{color}; margin-left:10px; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);'>{rec}</span>"
    else:
        return f"<div style='font-size:2em; font-weight:bold; color:{color}; text-shadow: 1px 1px 3px rgba(0,0,0,0.15); padding: 10px; border-left: 5px solid {color};'>{rec}</div>"

def create_bullet_list(text: str) -> str:
    """Create HTML bullet list from text with improved formatting."""
    if not text or text == "No data":
        return "<ul class='custom-bullets'><li>No data available.</li></ul>"

    sentences = re.split(r'(?<!\d)\.(?!\d)', text)
    items = [sentence.strip() for sentence in sentences if sentence.strip()]

    # Add different bullet icons for variety
    icons = ["💎", "📊", "📈", "🔍", "⚡"]

    html_list = "<ul class='custom-bullets' style='line-height: 1.6; margin-top: 10px;'>"
    for i, item in enumerate(items):
        icon = icons[i % len(icons)]
        html_list += f"<li style='margin-bottom: 8px;'><span style='margin-right: 10px;'>{icon}</span>{item}.</li>"
    html_list += "</ul>"

    return html_list

# --- UI Elements ---
def setup_page_style():
    """Set up page style and CSS."""
    st.set_page_config(page_title="Crypto Analysis", layout="centered")
    st.markdown("""
    <style>
    /* Reset default margins and paddings */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    /* Enforce a uniform font across all elements */
    html, body, [class*="css"] {
        font-family: 'Helvetica', sans-serif !important;
    }
    /* Custom heading box with transparent background */
    .heading-box {
        border: 1px solid #ddd;
        padding: 8px;
        margin-bottom: 10px;
        background-color: transparent;
        font-family: 'Helvetica', sans-serif;
    }
    /* Content box to control typography for section content */
    .content-box {
        border: 1px dashed #ddd;
        padding: 8px;
        margin-bottom: 10px;
        background-color: transparent;
        font-family: 'Helvetica', sans-serif;
    }
    ul.custom-bullets {
        list-style: none;
        padding-left: 0;
    }
    ul.custom-bullets li::before {
        content: "🔹";
        margin-right: 5px;
    }
    /* Loading animation */
    .loading {
        display: inline-block;
        width: 30px;
        height: 30px;
        border: 3px solid rgba(0, 0, 0, 0.2);
        border-radius: 50%;
        border-top-color: #3498db;
        animation: spin 1s ease-in-out infinite;
    }
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    </style>
    """, unsafe_allow_html=True)

def display_market_summary(stats: Dict[str, Any], symbol: str, update_time: str):
    """Display market summary section with improved formatting."""
    with st.expander("Market Summary 🪙", expanded=True):
        price_display = format_price(stats['price'])

        # Format market cap and volume
        cap_display = format_large_number(stats['cap'], prefix="$")
        volume_display = format_large_number(stats['volume'], prefix="$")

        # Create mood indicator with appropriate color
        mood_colors = {"Bullish": "#28a745", "Neutral": "#ffc107", "Bearish": "#dc3545"}
        mood_color = mood_colors.get(stats['mood'], "#6c757d")

        # Create buzz indicator
        buzz_scale = {"Low": "25%", "Moderate": "50%", "High": "90%"}
        buzz_width = buzz_scale.get(stats['buzz'], "50%")

        st.markdown(f"""
        <div style='background-color: #f8f9fa; border-radius: 10px; padding: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <table style='width: 100%; border-collapse: collapse;'>
                <tr>
                    <td style='padding: 8px; font-weight: bold;'>Coin:</td>
                    <td style='padding: 8px;'>{symbol}</td>
                </tr>
                <tr style='background-color: rgba(0,0,0,0.03);'>
                    <td style='padding: 8px; font-weight: bold;'>Price:</td>
                    <td style='padding: 8px;'>{price_display}</td>
                </tr>
                <tr>
                    <td style='padding: 8px; font-weight: bold;'>Volume (24h):</td>
                    <td style='padding: 8px;'>{volume_display}</td>
                </tr>
                <tr style='background-color: rgba(0,0,0,0.03);'>
                    <td style='padding: 8px; font-weight: bold;'>Market Cap:</td>
                    <td style='padding: 8px;'>{cap_display}</td>
                </tr>
                <tr>
                    <td style='padding: 8px; font-weight: bold;'>Last Updated:</td>
                    <td style='padding: 8px;'>{update_time}</td>
                </tr>
                <tr style='background-color: rgba(0,0,0,0.03);'>
                    <td style='padding: 8px; font-weight: bold;'>Market Mood:</td>
                    <td style='padding: 8px;'><span style='color: {mood_color}; font-weight: bold;'>{stats['mood']}</span></td>
                </tr>
                <tr>
                    <td style='padding: 8px; font-weight: bold;'>Social Buzz:</td>
                    <td style='padding: 8px;'>
                        <div style='background-color: #e9ecef; border-radius: 5px; height: 10px; width: 100%;'>
                            <div style='background-color: #007bff; border-radius: 5px; height: 10px; width: {buzz_width};'></div>
                        </div>
                        <span style='font-size: 0.8em;'>{stats['buzz']}</span>
                    </td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

def format_large_number(num: float, prefix: str = "") -> str:
    """Format large numbers for display with appropriate suffixes."""
    if num >= 1_000_000_000:
        return f"{prefix}{num/1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"{prefix}{num/1_000_000:.2f}M"
    elif num >= 1_000:
        return f"{prefix}{num/1_000:.2f}K"
    else:
        return f"{prefix}{num:,.0f}"

def create_price_target_chart(current_price: float, targets_text: str):
    """Create a visual representation of price targets."""
    import matplotlib.pyplot as plt
    import numpy as np
    from io import BytesIO
    import base64

    # Extract price targets
    price_matches = re.findall(r'\$([0-9,.]+)', targets_text)
    prices = []
    for match in price_matches:
        try:
            price = float(match.replace(',', ''))
            prices.append(price)
        except:
            pass

    # If no valid prices found, use estimated values
    if not prices:
        # Create sample prices 20% up and down from current
        prices = [current_price * 0.8, current_price * 1.2]

    # Sort and deduplicate
    prices = sorted(set(prices))

    # Create a simple horizontal chart
    fig, ax = plt.subplots(figsize=(8, 3))

    # Plot price range
    min_price = min(min(prices), current_price) * 0.9
    max_price = max(max(prices), current_price) * 1.1

    # Current price marker
    ax.axvline(x=current_price, color='blue', linestyle='-', alpha=0.7)
    ax.text(current_price, 0.5, f"Current: ${current_price:.2f}",
            ha='center', va='center', rotation=90, color='blue')

    # Price targets
    for price in prices:
        if price < current_price:
            color = 'red'
            label = f"Support: ${price:.2f}"
        else:
            color = 'green'
            label = f"Target: ${price:.2f}"

        ax.axvline(x=price, color=color, linestyle='--', alpha=0.7)
        ax.text(price, 0.8, label, ha='center', va='center', rotation=90, color=color)

    # Configure chart
    ax.set_xlim(min_price, max_price)
    ax.set_ylim(0, 1)
    ax.set_title("Price Targets")
    ax.grid(True, alpha=0.3)
    ax.set_yticks([])
    plt.tight_layout()

    # Convert plot to base64 for embedding in HTML
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=100)
    plt.close(fig)
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    return f"<img src='data:image/png;base64,{data}' style='width:100%;'/>"

def display_analysis(rec: str, rationale: str, factors: str, outlook: str, targets: str, tech_signal: str):
    """Display AI analysis section with improved card layout."""
    with st.expander("AI Analysis Report 🤖", expanded=True):
        # Section card styling
        card_style = """
        <style>
        .analysis-card {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .card-header {
            border-bottom: 1px solid #dee2e6;
            padding-bottom: 10px;
            margin-bottom: 15px;
            font-weight: bold;
        }
        </style>
        """
        st.markdown(card_style, unsafe_allow_html=True)

        # Technical Signal
        st.markdown(f"<div class='analysis-card'><div class='card-header'>Technical Signal 💻</div>{format_recommendation(tech_signal, inline=True)}</div>", unsafe_allow_html=True)

        # Recommendation
        st.markdown("<div class='analysis-card'><div class='card-header'>Recommendation 📊</div>", unsafe_allow_html=True)
        st.markdown(format_recommendation(rec), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Remaining sections with the card layout
        sections = [
            ("Rationale 📜", rationale),
            ("Key Factors 🧩", factors),
            ("1-Week Outlook 🔮", outlook),
            ("Price Targets 🎯", targets)
        ]

        for title, content in sections:
            st.markdown(f"<div class='analysis-card'><div class='card-header'>{title}</div>", unsafe_allow_html=True)
            st.markdown(create_bullet_list(content), unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        if targets != "No data":
            chart_html = create_price_target_chart(stats['price'], targets)
            st.markdown(f"<div class='analysis-card'><div class='card-header'>Visual Price Range</div>{chart_html}</div>", unsafe_allow_html=True)

# --- AI Functions ---
def setup_ai_agent(api_key: str) -> Agent:
    """Set up and return an AI agent with proper error handling and fallbacks."""
    # List of model IDs to try in order of preference
    model_ids = [
        "gemini-2.0-pro-exp-02-05",
        "gemini-2.0-flash-thinking-exp-01-21"
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
    """Generate the prompt for AI analysis."""
    try:
        prompt = (
            f"Analyze {symbol} now at {format_price(stats['price'])}.\n"
            f"Market mood is: {stats['mood']} and social buzz: {stats['buzz']}.\n"
            f"Volume: ${stats['volume']:,.0f}, Cap: ${stats['cap']:,.0f}.\n\n"
            "Provide your analysis in a single response with these parts separated by | symbol in order:\n"
            "Rec: [Buy/Hold/Sell] | Why: [Explain your reasoning] | Factors: [List key factors] | "
            "Outlook: [Provide 1-week outlook] | Targets: [Supply price targets]\n"
            "Ensure none of the fields are empty and keep your answer around 150 words."
        )
        return prompt
    except Exception as e:
        logger.error(f"Error generating prompt: {str(e)}")
        return f"Analyze {symbol}. Provide analysis in format: Rec: [Buy/Hold/Sell] | Why: [Reasoning] | Factors: [Factors] | Outlook: [Outlook] | Targets: [Targets]"

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

# --- Main Application ---
def main():
    """Main application function."""
    # Setup page
    setup_page_style()

    # Application header
    st.title("Crypto Reimagined Dashboard 🚀")
    st.markdown("A fresh perspective on your crypto analysis – powered by AI and Coinpaprika data. 🌐")

    # Sidebar configuration
    st.sidebar.header("Configuration")
    api_key = st.sidebar.text_input("Google API Key 🔑", type="password")
    coin_query = st.sidebar.text_input("Crypto Symbol/Name", value="BTC").strip().upper()

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
    st.sidebar.markdown("Market data provided by [Coinpaprika](https://coinpaprika.com/)")

    if not (api_key and coin_query):
        st.info("Enter API key and coin name/symbol in the sidebar to start.")
        return

    try:
        # Show loading message
        with st.spinner("Loading cryptocurrency data..."):
            # Get coin data first - this can be done before initializing the AI
            coins = get_coin_list()
            coin = lookup_coin(coin_query, coins)

            if not coin:
                supported_coins = ", ".join([c["symbol"].upper() for c in coins[:10]]) + "..."
                st.error(f"Coin not found. Currently supporting: {supported_coins}")
                return

            coin_id = coin["id"]
            symbol = coin["symbol"].upper()

            # Fetch market data
            market_data = get_market_data(coin_id)
            tech_signal = get_technical_signal(market_data)

            # Process timestamp
            try:
                dt_obj = datetime.fromisoformat(market_data["last_updated"].replace("Z", "+00:00"))
                dt_obj += timedelta(hours=7)  # UTC+7
                update_time = dt_obj.strftime("%H:%M - %d/%m/%Y")
            except:
                update_time = datetime.utcnow().strftime("%H:%M - %d/%m/%Y")

        # Initialize AI agent with improved error handling
        with st.spinner("Initializing AI model..."):
            agent = setup_ai_agent(api_key)

        # Generate AI analysis
        with st.spinner("Generating AI analysis..."):
            prompt = generate_analysis_prompt(symbol, market_data)
            rec, rationale, factors, outlook, targets = run_ai_analysis(agent, prompt)

        # Display results
        display_market_summary(market_data, symbol, update_time)
        display_analysis(rec, rationale, factors, outlook, targets, tech_signal)

        st.success("Analysis complete! Review the sections above for full details. ✅")

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
