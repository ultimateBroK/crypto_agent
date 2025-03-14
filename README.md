# 🚀 Crypto Analysis Pro Dashboard (COMPLETELY BUGGY, FIXING TIME)

<div align="center">
  
![Crypto Dashboard Banner](https://img.shields.io/badge/Crypto-Analysis-blueviolet?style=for-the-badge&logo=bitcoin)

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Powered%20by-Streamlit-FF4B4B.svg?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-4285F4?style=flat&logo=google&logoColor=white)](https://ai.google.dev)
[![Binance API](https://img.shields.io/badge/Data-Binance-F0B90B?style=flat&logo=binance&logoColor=black)](https://binance.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

An advanced cryptocurrency analysis platform combining real-time market data from Binance with Google's Gemini AI to deliver professional-grade investment insights, technical analysis, and strategic trading recommendations.


## ✨ Features Spotlight

<table>
  <tr>
    <td width="50%">
      <h3>🧠 AI-Powered Analysis</h3>
      <p>Harnesses Google Gemini models to generate sophisticated investment recommendations with detailed rationales</p>
    </td>
    <td width="50%">
      <h3>📊 Interactive Charts</h3>
      <p>Professional-grade candlestick charts with technical indicators and support/resistance visualization</p>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>📈 Advanced Technical Analysis</h3>
      <p>Real-time RSI, MACD, and EMA crossover indicators derived from actual Binance market data</p>
    </td>
    <td width="50%">
      <h3>⚖️ Trading Strategies</h3>
      <p>Actionable trading strategies with risk-reward ratios and confidence levels</p>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>🌡️ Market Sentiment</h3>
      <p>Dynamic assessment of market mood with visual indicators based on price movement and volume analysis</p>
    </td>
    <td width="50%">
      <h3>🕒 Multi-Timeframe Analysis</h3>
      <p>Analyze price action across different timeframes (1H, 4H, 1D, 1W, 1M)</p>
    </td>
  </tr>
</table>

**Additional Features:**
- 🎯 **Price Target Visualization:** Support and resistance levels displayed with confidence metrics
- 📱 **Responsive UI:** Modern card-based interface with color-coded signals and visual indicators
- ⚡ **Smart Data Handling:** Intelligent caching system minimizes API calls while keeping data fresh
- 🔍 **Advanced Search:** Find cryptocurrencies by partial name or symbol with smart matching
- 📈 **Volume Analysis:** Advanced volume trend analysis with spike detection and pattern recognition

## 🖼️ Screenshots

<div align="center">
  <p><i>📸 Screenshots coming soon! 📸</i></p>
</div>

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Google AI Studio API key
- Internet connection for Binance market data

### Quick Start Guide

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/ultimateBroK/crypto_agent.git
   cd crypto_agent
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Dashboard:**
   ```bash
   streamlit run app.py
   ```

5. **Access the Application:**
   Open your browser and navigate to http://localhost:8501

### 🔑 Setting Up API Keys

<details>
<summary>Click to expand instructions</summary>

#### Google Gemini API Key:
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create or use an existing Google Cloud project
3. Generate an API key
4. Enter the key in the dashboard sidebar when prompted

> **Note**: No API key is required for accessing Binance public API endpoints.
</details>

## 🧩 How It Works

<div align="center">
  <pre>
  ┌───────────────────┐     ┌─────────────────────┐     ┌────────────────────┐     ┌─────────────────┐
  │                   │     │                     │     │                    │     │                 │
  │   Binance API     │───▶│   Data Processing   │───▶│  Technical Analysis│───▶│   Google Gemini │
  │   Market Data     │     │   & Caching Layer   │     │  Engine            │     │   AI Model      │
  │                   │     │                     │     │                    │     │                 │
  └───────────────────┘     └─────────────────────┘     └────────────────────┘     └────────┬────────┘
                                                                                            │
                                                                                            │
                                                                                            ▼
  ┌───────────────────┐     ┌─────────────────────┐     ┌────────────────────┐     ┌─────────────────┐
  │                   │     │                     │     │                    │     │                 │
  │   User Interface  │◀───│ Trading Strategies  │◀───│ Price Targets &    │◀───│   Analysis      │
  │   Dashboard       │     │ & Recommendations   │     │ Support/Resistance │     │   Generator     │
  │                   │     │                     │     │                    │     │                 │
  └───────────────────┘     └─────────────────────┘     └────────────────────┘     └─────────────────┘
  </pre>
</div>

### Data Flow & Processing

1. **Market Data Acquisition**
   - Real-time cryptocurrency data is fetched from Binance API
   - Historical price data is retrieved for candlestick charts and technical analysis
   - Intelligent caching minimizes API calls while ensuring data freshness

2. **Technical Analysis Engine**
   - Multiple technical indicators calculated including RSI, MACD, and EMA crossovers
   - Signal strength determined through weighted combination of indicators
   - Market sentiment derived from price action and volume patterns

3. **AI Analysis Pipeline**
   - Technical data formatted into comprehensive prompts for Gemini AI
   - Analysis structured into recommendation, rationale, and price targets
   - AI responses enhanced for clarity and confidence metrics

4. **Advanced Visualization Layer**
   - Interactive candlestick charts with multiple timeframe options
   - Support/resistance levels plotted directly on charts
   - Trading strategies presented with clear risk-reward metrics

## 🔎 Supported Cryptocurrencies

The dashboard supports all major USDT trading pairs on Binance, including:

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="https://cryptologos.cc/logos/bitcoin-btc-logo.svg" width="20"/> Bitcoin (BTC)</td>
      <td align="center"><img src="https://cryptologos.cc/logos/ethereum-eth-logo.svg" width="20"/> Ethereum (ETH)</td>
      <td align="center"><img src="https://cryptologos.cc/logos/binance-coin-bnb-logo.svg" width="20"/> Binance Coin (BNB)</td>
    </tr>
    <tr>
      <td align="center"><img src="https://cryptologos.cc/logos/xrp-xrp-logo.svg" width="20"/> XRP</td>
      <td align="center"><img src="https://cryptologos.cc/logos/cardano-ada-logo.svg" width="20"/> Cardano (ADA)</td>
      <td align="center"><img src="https://cryptologos.cc/logos/solana-sol-logo.svg" width="20"/> Solana (SOL)</td>
    </tr>
    <tr>
      <td colspan="3" align="center">And many more...</td>
    </tr>
  </table>
</div>

## 🛠️ Advanced Features

- **Multi-Model Fallback:** Automatically tries multiple Gemini models if primary is unavailable
- **Bookmarkable Analysis:** URL parameters support direct linking to specific coins and timeframes
- **Trading Strategy Generation:** Custom strategies with entry/exit points based on market conditions
- **Technical Signal Aggregation:** Weighted technical signals from multiple indicators
- **Risk-Reward Analysis:** Calculated metrics for potential trades with confidence levels

## 📝 Technical Details

<details>
<summary>Click to expand technical specifications</summary>

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
</details>

## 🏗️ Project Structure

```
crypto_agent/
├── app.py                  # Main application entry point
├── requirements.txt        # Project dependencies
├── README.md              # Project documentation
├── CHANGELOG.md           # Version history and changes
├── project_status.txt     # Current project status
└── src/                   # Source code directory
    ├── analytics/         # Analysis modules
    │   ├── ai_analysis.py         # AI integration
    │   └── technical_indicators.py # Technical indicators
    ├── data_processing/   # Data retrieval and processing
    │   ├── binance_api.py         # Binance integration
    │   └── market_data.py         # Data handling
    ├── ui_components/     # UI components
    │   ├── analysis_display.py    # Analysis display
    │   ├── charts.py              # Chart visualization
    │   ├── market_summary.py      # Market summary
    │   ├── price_targets.py       # Price targets
    │   ├── sidebar.py             # Sidebar components
    │   ├── styles.py              # CSS styling
    │   └── trading_strategy.py    # Trading strategies
    └── utils/             # Utility functions
        ├── constants.py           # Constants
        ├── formatting.py          # Formatting utilities
        └── logger.py              # Logging configuration
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ⭐ Star History

<div align="center">

[![Star History Chart](https://api.star-history.com/svg?repos=ultimatebrok/crypto_agent&type=Date)](https://star-history.com/#ultimatebrok/crypto_agent&Date)

</div>

## ⚠️ Disclaimer

<div align="left">
    <tr>
      <td style="background-color: #fff3cd; align="center"; padding: 15px; border-radius: 8px; border-left: 5px solid #ffc107;">
        <h4>⚠️ Investment Risk Warning</h4>
        <ul>
          <li>This application provides analysis for informational purposes only and does not constitute financial advice.</li>
          <li>Cryptocurrency investments are highly volatile and speculative. You may lose your entire investment.</li>
          <li>Past performance is not indicative of future results.</li>
          <li>Technical indicators and AI predictions cannot guarantee profitable trades.</li>
          <li>Always conduct your own research and consider consulting with a licensed financial advisor before making investment decisions.</li>
          <li>The developers of this application are not responsible for any financial losses incurred.</li>
        </ul>
      </td>
    </tr>
</div>

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">Built with ❤️ using Streamlit, Binance API, and Google Gemini AI</p>
<p align="center">
  <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Made%20with-Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Made with Streamlit"></a>
  <a href="https://binance.com/"><img src="https://img.shields.io/badge/Data-Binance-F0B90B?style=flat-square&logo=binance&logoColor=black" alt="Data: Binance"></a>
  <a href="https://ai.google.dev/"><img src="https://img.shields.io/badge/AI-Google%20Gemini-blue?style=flat-square&logo=google&logoColor=white" alt="AI: Google Gemini"></a>
</p>

<div align="center">
  <a href="#"><img src="https://visitor-badge.laobi.icu/badge?page_id=crypto-analysis-pro-dashboard" alt="Visitors"></a>
  <a href="https://github.com/ultimatebrok/crypto_agent/stargazers"><img src="https://img.shields.io/github/stars/ultimatebrok/crypto_agent" alt="Stars"></a>
  <a href="https://github.com/ultimatebrok/crypto_agent/issues"><img src="https://img.shields.io/github/issues/ultimatebrok/crypto_agent" alt="Issues"></a>
</div>
