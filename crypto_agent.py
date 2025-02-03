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

# --- Main Application ---
def main():
    st.set_page_config(page_title="Crypto Reimagined", layout="centered")
    st.title("Crypto Reimagined Dashboard")
    st.markdown("A fresh perspective on your crypto analysis – powered by AI and consolidated market data.")

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
    with st.expander("Market Summary", expanded=True):
        st.write(f"**Coin:** {symbol}")
        price_display = f"${stats['price']:,.2f}" if stats['price'] >= 1 else f"${stats['price']:,.8f}"
        st.write(f"**Price:** {price_display}")
        st.write(f"**Volume (24h):** ${stats['volume']:,.0f}")
        st.write(f"**Market Cap:** ${stats['cap']:,.0f}")
        st.write(f"**Last Updated (UTC+7):** {update_time}")
        st.write(f"**Mood:** {stats['mood']}")
        st.write(f"**Social Buzz:** {stats['buzz']}")

    with st.expander("AI Analysis Report", expanded=True):
        st.markdown("### Recommendation")
        st.info(f"{rec}")
        st.markdown("### Rationale")
        st.write(rationale)
        st.markdown("### Key Factors")
        st.write(factors)
        st.markdown("### 1-Week Outlook")
        st.write(outlook)
        st.markdown("### Price Targets")
        st.write(targets)

    st.success("Analysis complete! Review the sections above for full details.")

if __name__ == "__main__":
    main()
