# Escape the Matrix Agent: Crypto Analysis & AI Investment

This Streamlit app leverages an AI-powered agent based on the Google Gemini model to analyze cryptocurrencies. Receive clear recommendations and insights using real-time market data from CoinGecko and advanced analysis techniques.

## Features
- **AI-Powered Analysis:** Utilize the Google Gemini model for decisive buy/hold/sell recommendations.
- **Real-Time Market Data:** Fetch current prices, 24h volume, market cap, and last updated timestamps from the CoinGecko API.
- **Detailed Insights:** Get technical analysis, fundamental factors, short-term outlook (1-week) and support/resistance levels.
- **Streamlit Interface:** Interactive UI for easy input of your Google API key and crypto symbol/name.

## How to Get Started

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/Crypto_agent.git
   cd Crypto_agent
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the App:**
   ```bash
   streamlit run crypto_agent.py
   ```

4. **Usage:**
   - Enter your Google API key.
   - Input the cryptocurrency name or symbol (e.g., Bitcoin or BTC).
   - View real-time market stats and a concise AI-generated recommendation.

## Notes
- Ensure you have a valid Google API key to initialize the AI agent.
- The coin data is cached for one hour to minimize API calls.

---

Happy investing and enjoy exploring the market trends with the Escape the Matrix Agent!