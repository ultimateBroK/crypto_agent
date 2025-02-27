# 🚀 Crypto Analysis Pro Dashboard

![Crypto Dashboard Banner](https://img.shields.io/badge/Crypto-Analysis-blueviolet?style=for-the-badge&logo=bitcoin)

An advanced cryptocurrency analysis platform combining real-time market data from Binance with Google's Gemini AI to deliver professional-grade investment insights, technical analysis, and strategic trading recommendations.

## ✨ Features Spotlight

- **🧠 AI-Powered Analysis:** Harnesses Google Gemini models to generate sophisticated investment recommendations with detailed rationales
- **📊 Interactive Charts:** Professional-grade candlestick charts with technical indicators and support/resistance visualization
- **📈 Advanced Technical Analysis:** Real-time RSI, MACD, and EMA crossover indicators derived from actual Binance market data
- **⚖️ Trading Strategies:** Actionable trading strategies with risk-reward ratios and confidence levels
- **🌡️ Market Sentiment:** Dynamic assessment of market mood with visual indicators based on price movement and volume analysis
- **🕒 Multi-Timeframe Analysis:** Analyze price action across different timeframes (1H, 4H, 1D, 1W, 1M)
- **🎯 Price Target Visualization:** Support and resistance levels displayed on interactive charts with confidence metrics
- **📱 Responsive UI:** Modern card-based interface with color-coded signals and visual progress indicators
- **⚡ Smart Data Handling:** Intelligent caching system minimizes API calls while keeping data fresh
- **🔍 Advanced Search:** Find cryptocurrencies by partial name or symbol with smart matching algorithm

## 🖼️ Screenshots

![Dashboard Preview](https://via.placeholder.com/800x450?text=Crypto+Analysis+Pro+Dashboard)

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Google AI Studio API key
- Internet connection for Binance market data

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/crypto_agent.git
   cd crypto_agent
   ```

2. **Create a Virtual Environment (Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the App:**
   ```bash
   streamlit run crypto_agent.py
   ```

5. **Access the Dashboard:**
   Open your browser and go to http://localhost:8501

## 🔑 API Keys

This application requires a Google API key to access Gemini AI models:

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create or use an existing Google Cloud project
3. Generate an API key
4. Enter the key in the dashboard sidebar when prompted

No API key is required for accessing Binance public API endpoints.

## 🧩 How It Works

1. **Market Data Acquisition:**
   - Real-time cryptocurrency data is fetched from Binance API
   - Historical price data is retrieved for candlestick charts and technical analysis
   - Price, volume, market cap, and change percentages are collected

2. **Technical Analysis:**
   - Multiple technical indicators calculated including RSI, MACD, and EMA crossovers
   - Signal strength is determined through a weighted combination of indicators
   - Market sentiment is derived from price action and volume patterns

3. **AI Analysis Pipeline:**
   - Technical data is formatted into a comprehensive prompt for the Gemini AI model
   - Analysis is structured into recommendation, rationale, factors, outlook, and price targets
   - AI responses are enhanced for clarity and confidence

4. **Advanced Visualization:**
   - Interactive candlestick charts with multiple timeframe options
   - Support and resistance levels plotted directly on charts
   - Technical indicators displayed as separate panels for detailed analysis
   - Trading strategies presented with clear risk-reward metrics

## 🔎 Supported Cryptocurrencies

The dashboard supports the top USDT trading pairs on Binance, including:
- Bitcoin (BTC)
- Ethereum (ETH)
- XRP
- And many more!

## 🛠️ Advanced Features

- **Multi-Model Fallback:** Automatically tries multiple Gemini models if the primary one is unavailable
- **Bookmarkable Analysis:** URL parameters support direct linking to specific coins and timeframes
- **Trading Strategy Generation:** Custom strategies based on current market conditions with entry/exit points
- **Technical Signal Aggregation:** Weighted technical signals from multiple indicators for higher accuracy
- **Risk-Reward Analysis:** Calculated metrics for potential trades with confidence levels
- **Smart Number Formatting:** Large numbers are displayed with appropriate K/M/B suffixes

## 📝 Technical Details

- **Data Source:** Binance API for real-time and historical market data
- **AI Model:** Google Gemini 2.0 Pro with fallbacks to other versions
- **Technical Indicators:**
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - EMA (Exponential Moving Averages) - 12, 26, 50, and 200 periods
  - Volume analysis and price momentum
- **Visualization:** Interactive Plotly charts with custom styling
- **Market data caching:** 5-minute cache to optimize performance
- **Programming:** Built with Python, Streamlit, Pandas, NumPy, and Plotly

## ⚠️ Disclaimer

The analysis and recommendations provided by this application are for informational purposes only and should not be considered financial advice. Always conduct your own research before making investment decisions.

---

<p align="center">Built with ❤️ using Streamlit, Binance API, and Google Gemini AI</p>
<p align="center">
  <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Made%20with-Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Made with Streamlit"></a>
  <a href="https://binance.com/"><img src="https://img.shields.io/badge/Data-Binance-F0B90B?style=flat-square&logo=binance&logoColor=black" alt="Data: Binance"></a>
  <a href="https://ai.google.dev/"><img src="https://img.shields.io/badge/AI-Google%20Gemini-blue?style=flat-square&logo=google&logoColor=white" alt="AI: Google Gemini"></a>
</p>