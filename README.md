# Crypto Reimagined Dashboard

This Streamlit application provides AI-powered cryptocurrency analysis using real-time market data from Coinpaprika and Google's Gemini AI models. Get instant insights, technical signals, and investment recommendations in an intuitive interface.

## Features

- **Real-Time Market Data:** Access up-to-date cryptocurrency prices, volumes, market cap, and trends from Coinpaprika API
- **AI-Powered Analysis:** Leverage Google Gemini models to generate comprehensive investment recommendations
- **Technical Indicators:** View technical signals including RSI-based buy/sell/hold recommendations
- **Sentiment Analysis:** Track market mood (Bullish/Neutral/Bearish) and social buzz metrics
- **Detailed Insights:** Get rationale, key factors, short-term outlook, and price targets for each cryptocurrency
- **Visual Representations:** See price targets and support levels in easy-to-understand formats
- **Enhanced UI:** Intuitive interface with expandable sections, card-based layouts, and visual indicators

## Getting Started

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/crypto_agent.git
   cd crypto_agent
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the App:**
   ```bash
   streamlit run crypto_agent.py
   ```

4. **Required API Keys:**
   - Get a Google AI Studio API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - No API key is required for Coinpaprika's public endpoints

## Usage

1. Enter your Google API key in the sidebar
2. Input the cryptocurrency symbol or name you want to analyze (e.g., BTC, Ethereum)
3. View the comprehensive market summary with current data
4. Review the AI-generated analysis including:
   - Technical signal (buy/sell/hold)
   - Investment recommendation with rationale
   - Key market factors
   - 1-week market outlook
   - Price targets and support levels

## Notes

- Market data is cached for 5 minutes to minimize API calls
- The app supports the top 30 cryptocurrencies by market cap
- For cryptocurrencies without sufficient data, the app provides estimated indicators

---

Built with Streamlit, Coinpaprika API, and Google Gemini AI