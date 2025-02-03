import streamlit as st
from agno.agent import Agent
from agno.models.google import Gemini
import re
from datetime import datetime, timedelta
import requests
from pycoingecko import CoinGeckoAPI
import logging

# --- Setup logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Utility Functions ---
@st.cache_data(ttl=3600)
def get_coin_list():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/coins/list")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to obtain coin list: {e}")
        return []

def extract_agent_output(text):
    # Extract fields using new delimiters in agent's response
    rec = re.search(r"Rec:([^|]+)", text)
    rat = re.search(r"Why:([^|]+)", text)
    factors = re.search(r"Factors:([^|]+)", text)
    outlook = re.search(r"Outlook:([^|]+)", text)
    prices = re.search(r"Targets:([^|]+)", text)
    return (
        rec.group(1).strip() if rec else "Undefined recommendation",
        rat.group(1).strip() if rat else "No explanation provided",
        factors.group(1).strip() if factors else "No factors detailed",
        outlook.group(1).strip() if outlook else "No outlook available",
        prices.group(1).strip() if prices else "No price targets provided",
    )

def lookup_coin(query, coins):
    exact = [c for c in coins if c["symbol"].upper() == query or c["name"].upper() == query]
    if exact:
        return exact[0]
    partial = [c for c in coins if query in c["name"].upper()]
    return partial[0] if partial else None

def pull_extra_data(coin_id):
    try:
        # Dummy extra data call – replace with real API if available
        url = f"https://api.example.com/crypto/{coin_id}/stats"
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logging.warning("Extra data request failed: %s", e)
        return {}

def merge_market_stats(gecko, extra):
    return {
        "price": gecko.get("current_price", {}).get("usd", 0),
        "volume": gecko.get("total_volume", {}).get("usd", 0),
        "cap": gecko.get("market_cap", {}).get("usd", 0),
        "mood": extra.get("market_mood", "Neutral"),
        "buzz": extra.get("social_buzz", "No buzz")
    }

def create_bullet_list(text):
    # Split on periods not part of a decimal number.
    sentences = re.split(r'(?<!\d)\.(?!\d)', text)
    items = [sentence.strip() for sentence in sentences if sentence.strip()]
    # Append period at end of each sentence.
    return "<ul class='custom-bullets'>" + "".join(f"<li>{item}.</li>" for item in items) + "</ul>"

def extract_signal(rec):
    # Extract all trading signals and return the most frequently mentioned one.
    from collections import Counter
    matches = re.findall(r'\b(buy|sell|hold)\b', rec, re.IGNORECASE)
    if matches:
        counts = Counter(match.lower() for match in matches)
        return counts.most_common(1)[0][0]
    return None

def format_recommendation(rec):
    signal = extract_signal(rec)
    if signal == "buy":
        color = "green"
    elif signal == "sell":
        color = "red"
    elif signal == "hold":
        color = "gray"
    else:
        color = "black"
    return f"<div style='font-size:2em; font-weight:bold; color:{color};'>{rec}</div>"

def format_recommendation_inline(rec):
    signal = extract_signal(rec)
    if signal == "buy":
        color = "green"
    elif signal == "sell":
        color = "red"
    elif signal == "hold":
        color = "gray"
    else:
        color = "black"
    return f"<span style='font-size:1.5em; font-weight:bold; color:{color}; margin-left:10px;'>{rec}</span>"

def get_technical_signal(extra_data):
    # Use D1 timeframe indicator; for example, using the daily RSI ("rsi_d1")
    rsi = extra_data.get("rsi_d1")
    if rsi is not None:
        try:
            rsi = float(rsi)
            if rsi < 30:
                return "buy"
            elif rsi > 70:
                return "sell"
            else:
                return "hold"
        except Exception:
            pass
    # Fallback signal if no D1 indicator available.
    return "hold"

# --- Main Application ---
def main():
    st.set_page_config(page_title="Crypto Reimagined", layout="centered")
    # Updated global CSS including styles for heading and content boxes
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
    </style>
    """, unsafe_allow_html=True)
    
    st.title("Crypto Reimagined Dashboard 🚀")
    st.markdown("A fresh perspective on your crypto analysis – powered by AI and consolidated market data. 🌐")

    # Sidebar inputs
    st.sidebar.header("Configuration")
    api_key = st.sidebar.text_input("Google API Key 🔑", type="password")
    coin_query = st.sidebar.text_input("Crypto Symbol/Name", value="BTC").strip().upper()
    
    if not (api_key and coin_query):
        st.info("Enter API key and coin name/symbol in the sidebar to start.")
        return

    # Initialize Agent
    try:
        agent = Agent(
            model=Gemini(id="gemini-2.0-flash-exp", api_key=api_key),
            tools=[], show_tool_calls=True, markdown=True
        )
        logging.info("AI Agent created.")
    except Exception as e:
        st.error(f"Agent failed initialization: {e}")
        return

    # Fetch coin details
    coins = get_coin_list()
    coin = lookup_coin(coin_query, coins)
    if not coin:
        st.error("Coin not found in CoinGecko database.")
        return
    coin_id = coin["id"]
    symbol = coin["symbol"].upper()

    # Retrieve primary market data
    cg = CoinGeckoAPI()
    coin_info = cg.get_coin_by_id(
        id=coin_id, localization='false', tickers='false',
        market_data='true', community_data='false', developer_data='false', sparkline='false'
    )
    market = coin_info.get("market_data", {})
    extra_data = pull_extra_data(coin_id)
    stats = merge_market_stats(market, extra_data)
    # Compute technical signal based on extra_data indicators.
    tech_signal = get_technical_signal(extra_data)
    
    # Process timestamp info
    last_updated_raw = coin_info.get("last_updated", "")
    try:
        dt_obj = datetime.fromisoformat(last_updated_raw.replace("Z", "+00:00"))
    except Exception:
        dt_obj = datetime.utcnow()
    dt_obj += timedelta(hours=7)
    update_time = dt_obj.strftime("%H:%M - %d/%m/%Y")
    
    # Build refreshed AI prompt with new delimiters (| used for separation)
    prompt = (f"Analyze {symbol} now at ${stats['price']:.8f}.\n"
              f"Market mood is: {stats['mood']} and social buzz: {stats['buzz']}.\n"
              f"Volume: ${stats['volume']:,.0f}, Cap: ${stats['cap']:,.0f}.\n\n"
              "Provide your analysis in a single response with these parts separated by | symbol in order:\n"
              "Rec: [Buy/Hold/Sell] | Why: [Explain your reasoning] | Factors: [List key factors] | "
              "Outlook: [Provide 1-week outlook] | Targets: [Supply price targets]\n"
              "Ensure none of the fields are empty and keep your answer around 150 words.")
    
    # Query the agent
    try:
        ai_response = agent.run(prompt)
        output_text = ai_response.content
        rec, rationale, factors, outlook, targets = extract_agent_output(output_text)
    except Exception as e:
        st.error(f"Agent query failed: {e}")
        return

    # New output style using expanders for each section
    with st.expander("Market Summary 🪙", expanded=True):
        # Replace individual st.write calls with a markdown bullet list using emoji
        price_display = f"${stats['price']:,.2f}" if stats['price'] >= 1 else f"${stats['price']:,.8f}"
        st.markdown(f"""
        - 🔹 **Coin:** {symbol}
        - 🔹 **Price:** {price_display}
        - 🔹 **Volume (24h):** ${stats['volume']:,.0f}
        - 🔹 **Market Cap:** ${stats['cap']:,.0f}
        - 🔹 **Last Updated (UTC+7):** {update_time}
        - 🔹 **Mood:** {stats['mood']}
        - 🔹 **Social Buzz:** {stats['buzz']}
        """)

    with st.expander("AI Analysis Report 🤖", expanded=True):
        # Combine heading and inline recommendation signal in one line using HTML
        st.markdown(f"<h3 style='display:inline'>Technical Signal 💻</h3>{format_recommendation_inline(tech_signal)}", unsafe_allow_html=True)
        st.markdown("### Rationale 📜")
        st.markdown(create_bullet_list(rationale), unsafe_allow_html=True)
        st.markdown("### Key Factors 🧩")
        st.markdown(create_bullet_list(factors), unsafe_allow_html=True)
        st.markdown("### 1-Week Outlook 🔮")
        st.markdown(create_bullet_list(outlook), unsafe_allow_html=True)
        st.markdown("### Price Targets 🎯")
        st.markdown(create_bullet_list(targets), unsafe_allow_html=True)

    st.success("Analysis complete! Review the sections above for full details. ✅")

if __name__ == "__main__":
    main()
