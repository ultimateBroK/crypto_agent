import streamlit as st
from agno.agent import Agent
from agno.models.google import Gemini
import re  # Import regex to parse response content
from datetime import datetime, timedelta
import requests  # Used to fetch data from CoinMarketCap
from pycoingecko import CoinGeckoAPI  # Import CoinGecko API wrapper
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Cache the coin list from CoinGecko for 1 hour to reduce API calls and errors
@st.cache_data(ttl=3600)
def fetch_coin_list():
    try:
        url = "https://api.coingecko.com/api/v3/coins/list"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to fetch coin list: {e}")
        return []

# Updated: Parse additional "rationale" field from agent's analysis response
def parse_agent_response(decoded_content):
    recommendation_match = re.search(r"Recommendation:\s*(.*)", decoded_content, re.IGNORECASE)
    rationale_match = re.search(r"Reason(?:ing)?:\s*(.*)", decoded_content, re.IGNORECASE)
    key_factors_match = re.search(r"Key factors:\s*([\s\S]*?)\n\n", decoded_content, re.IGNORECASE)
    short_term_outlook_match = re.search(r"Short-term outlook:\s*([\s\S]*?)\n\n", decoded_content, re.IGNORECASE)
    price_targets_match = re.search(r"Price targets:\s*([\s\S]*?)\n\n", decoded_content, re.IGNORECASE)
    recommendation = recommendation_match.group(1).strip() if recommendation_match else "N/A"
    rationale = rationale_match.group(1).strip() if rationale_match else "No rationale provided."
    key_factors = key_factors_match.group(1).strip() if key_factors_match else "No detailed factors available."
    short_term_outlook = short_term_outlook_match.group(1).strip() if short_term_outlook_match else "No specific outlook available."
    price_targets = price_targets_match.group(1).strip() if price_targets_match else "No specific price targets available."
    return recommendation, rationale, key_factors, short_term_outlook, price_targets

# Function to get coin details based on the crypto query
def get_coin_details(crypto_query, coin_list):
    matched_coins = [coin for coin in coin_list if coin["symbol"].upper() == crypto_query or coin["name"].upper() == crypto_query]
    if not matched_coins:
        matched_coins = [coin for coin in coin_list if crypto_query in coin["name"].upper()]
    return matched_coins[0] if matched_coins else None

# New: Fetch additional market data from another source (dummy implementation)
def fetch_additional_market_data(coin_id):
    # Replace URL and parsing logic with actual API call if available
    try:
        url = f"https://api.example.com/crypto/{coin_id}/data"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()  # Expected to return a dict with extra info
    except Exception as e:
        logging.warning("Additional data not available: %s", e)
        return {}

# New: Aggregate market data from CoinGecko and additional data source
def aggregate_market_data(gecko_data, additional_data):
    aggregated = {}
    # Example: Merge sentiment score if available, else default value.
    aggregated['sentiment'] = additional_data.get("sentiment", "Neutral")
    aggregated['news_score'] = additional_data.get("news_score", "No news data")
    # Also include key details from gecko_data
    aggregated['current_price'] = gecko_data.get("current_price", {}).get("usd", 0)
    aggregated['volume_24h'] = gecko_data.get("total_volume", {}).get("usd", 0)
    aggregated['market_cap'] = gecko_data.get("market_cap", {}).get("usd", 0)
    return aggregated

def main():
    # Set up the basic layout of the Streamlit app
    st.title("Escape the matrix agent 📈🤖")
    st.caption("This app allows you to analyze cryptocurrencies and generate detailed reports. 🚀")

    # Prompt user for their Google API key
    google_api_key = st.text_input("Google API Key 🔑", type="password")
    if google_api_key:
        try:
            # Initialize the AI agent using the Google Gemini model
            agent = Agent(
                model=Gemini(id="gemini-2.0-flash-exp", api_key=google_api_key),
                tools=[],
                show_tool_calls=True,
                markdown=True,
            )
            logging.info("AI agent initialized.")
        except Exception as e:
            logging.error("Error initializing AI agent: %s", e)
            st.error(f"Error initializing AI agent: {e}")
            st.stop()

        # Prompt user for cryptocurrency name or symbol
        crypto_input = st.text_input("Enter the crypto name or symbol (e.g., Bitcoin or BTC) 💰").strip()
        if crypto_input:
            try:
                # Convert user input to uppercase for standard search matching
                crypto_query = crypto_input.upper()
                # Retrieve the cached list of coins from CoinGecko
                coin_list = fetch_coin_list()
                if not isinstance(coin_list, list) or not coin_list:
                    st.error("Error fetching coin list from CoinGecko.")
                    st.stop()
                selected_coin = get_coin_details(crypto_query, coin_list)
                if not selected_coin:
                    st.error("Crypto not found on CoinGecko.")
                    st.stop()
                coin_id = selected_coin["id"]
                proper_symbol = selected_coin["symbol"].upper()
                logging.info("Selected coin: %s", proper_symbol)

                # Fetch primary market data using CoinGecko API
                cg = CoinGeckoAPI()
                coin_data = cg.get_coin_by_id(id=coin_id, localization='false', tickers='false', 
                                                market_data='true', community_data='false', 
                                                developer_data='false', sparkline='false')
                market_data = coin_data.get("market_data", {})
                # Fetch additional data from another source
                additional_data = fetch_additional_market_data(coin_id)
                aggregated_data = aggregate_market_data(market_data, additional_data)
                current_price = aggregated_data['current_price']
                volume_24h = aggregated_data['volume_24h']
                market_cap = aggregated_data['market_cap']
                sentiment = aggregated_data['sentiment']
                news_score = aggregated_data['news_score']
                last_updated_str = coin_data.get("last_updated")
                try:
                    # Convert the last updated string to a datetime object
                    last_updated_dt = datetime.fromisoformat(last_updated_str.replace("Z", "+00:00"))
                except Exception:
                    last_updated_dt = datetime.utcnow()
                # Adjust last updated time to UTC+7
                last_updated_vn = last_updated_dt + timedelta(hours=7)
                last_updated = last_updated_vn.strftime("%H:%M - %d/%m/%Y")
                logging.info("Market data fetched for %s", proper_symbol)

                # Updated query prompt including rationale requirement
                query = f"""Analyze {proper_symbol} with price ${current_price:.8f}. Also consider the following details:
Sentiment: {sentiment}
News Score: {news_score}
Volume: ${volume_24h:,.0f}, Market Cap: ${market_cap:,.0f}

Give:
1. 🚀 Clear recommendation (Buy/Hold/Sell) along with a detailed rationale explaining why.
2. 💡 Key factors (Include technical analysis, fundamental analysis, news sentiment, and social media hype)
3. 📅 Short-term outlook (1 week) with specific details
4. 📈 Price targets (Provide support and resistance levels)

Each field is mandatory – do not leave any section blank. Even if uncertain, provide at least a default analysis.
Keep analysis about 150 words. Be decisive, avoid neutral language."""
                # Run the agent query and obtain analysis
                response = agent.run(query)
                decoded_content = response.content
                recommendation, rationale, key_factors, short_term_outlook, price_targets = parse_agent_response(decoded_content)
                
                # Enforce non-empty values with fallback messages if necessary
                if recommendation in ["N/A", ""]:
                    recommendation = "No recommendation provided. Please review market data carefully."
                if rationale in ["", "No rationale provided."]:
                    rationale = "Rationale information is missing. Please consider market trends and data."
                if key_factors in ["No detailed factors available.", ""]:
                    key_factors = "Key factors information missing. Consider technical trends, fundamentals, sentiment, and hype."
                if short_term_outlook in ["No specific outlook available.", ""]:
                    short_term_outlook = "Short-term outlook is unavailable. Monitor market trends closely."
                if price_targets in ["No specific price targets available.", ""]:
                    price_targets = "Price targets are not specified. Identify possible support/resistance levels manually."

                st.markdown("### 📊 Quick Stats")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Symbol", proper_symbol)  # Display the validated coin symbol
                with col2:
                    # Format current price: 2 decimals if value >= 1, else 8 decimals for precision
                    formatted_price = f"${current_price:,.2f}" if current_price >= 1 else f"${current_price:,.8f}"
                    st.metric("Current Price", formatted_price)
                with col3:
                    st.metric("24h Volume", f"${volume_24h:,.0f}")
                with col4:
                    st.metric("Market Cap", f"${market_cap:,.0f}")

                st.markdown(f"**Last Updated (UTC+7):** {last_updated}")
                st.markdown("---")

                # Display the final recommendation returned by the AI agent
                st.markdown("### 🚨 Final Recommendation")
                st.markdown(f"#### 📌 Recommendation: **{recommendation}**")
                st.markdown(f"#### 📖 Rationale: {rationale}")

                # Parse the key factors for enhanced display formatting
                reasoning_lines = key_factors.split('*')
                reasoning_lines = [line.strip() for line in reasoning_lines if line.strip()]
                formatted_reasoning = []

                for line in reasoning_lines:
                    if ',' in line:
                        parts = line.split(',', 1)
                        title = parts[0].strip()
                        content = parts[1].strip()
                        formatted_reasoning.append(f"🔸 **{title}**: {content}")  # Use Markdown for proper emphasis

                for item in formatted_reasoning:
                    st.markdown(item)
            
                # Display the short-term outlook provided by the AI agent
                st.markdown("#### ⏳ 1-Week Outlook")
                if short_term_outlook == "No specific outlook available.":
                    st.markdown("🔸 The AI could not provide a specific short-term outlook. **Consider monitoring market trends.**")
                else:
                    st.markdown(f"🔸 {short_term_outlook.strip()}")

                # Display the price targets if they were specified in the analysis
                st.markdown("#### 🎯 Price Targets")
                if price_targets == "No specific price targets available.":
                    st.markdown("🔸 The AI could not determine specific price targets. **Look for support and resistance levels manually.**")
                else:
                    price_targets = price_targets.replace("**", "").replace("*", "")
                    price_targets_lines = price_targets.split("\n")
                    for line in price_targets_lines:
                        if line.strip():
                            st.markdown(f"🔸 {line.strip()}")

            except Exception as e:
                logging.error("Error processing crypto analysis: %s", e)
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
