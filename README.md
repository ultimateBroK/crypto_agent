# 🚀 Crypto Reimagined Dashboard

![Crypto Dashboard Banner](https://img.shields.io/badge/Crypto-Reimagined-blueviolet?style=for-the-badge&logo=bitcoin)

An advanced cryptocurrency analysis platform combining real-time market data from Coinpaprika with Google's Gemini AI to deliver professional-grade investment insights and recommendations.

## ✨ Features Spotlight

- **🧠 AI-Powered Analysis:** Harnesses Google Gemini models to generate sophisticated investment recommendations with detailed rationales
- **📊 Visual Price Targets:** Interactive charting shows support levels and price targets based on AI analysis
- **📈 Technical Indicators:** Real-time technical signals including RSI-based insights derived from actual market movements
- **🌡️ Market Sentiment:** Dynamic assessment of market mood (Bullish/Neutral/Bearish) with visual indicators
- **📱 Responsive UI:** Beautiful card-based interface with color-coded signals and visual progress indicators
- **⚡ Smart Data Handling:** Intelligent caching system minimizes API calls while keeping data fresh
- **🔍 Advanced Search:** Find cryptocurrencies by partial name or symbol with smart matching algorithm

## 🖼️ Screenshots

![Dashboard Preview](https://via.placeholder.com/800x450?text=Crypto+Reimagined+Dashboard)

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Google AI Studio API key
- Internet connection for market data

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

Note: No API key is required for accessing Coinpaprika market data.

## 🧩 How It Works

1. **Market Data Acquisition:**
   - Real-time cryptocurrency data is fetched from Coinpaprika's free API
   - Price, volume, market cap, and change percentages are collected

2. **Technical Analysis:**
   - The app calculates custom technical indicators including a weighted RSI
   - Market sentiment is derived from volume/cap ratio and price momentum

3. **AI Analysis Pipeline:**
   - The collected data is formatted into a prompt for the Gemini AI model
   - Analysis is structured into recommendation, rationale, factors, outlook, and targets

4. **Visualization:**
   - Price targets are extracted and displayed in an interactive chart
   - Technical signals are color-coded based on buy/sell/hold recommendations

## 🔎 Supported Cryptocurrencies

The dashboard supports the top 30 cryptocurrencies by market cap, including:
- Bitcoin (BTC)
- Ethereum (ETH)
- XRP
- And many more!

## 🛠️ Advanced Features

- **Multi-Model Fallback:** Automatically tries multiple Gemini models if the primary one is unavailable
- **Smart Number Formatting:** Large numbers are displayed with appropriate K/M/B suffixes
- **Visual Progress Indicators:** Loading spinners and progress bars for long operations
- **Enhanced Searching:** Find cryptocurrencies using partial matches and smart ranking

## 📝 Notes

- Market data is cached for 5 minutes to optimize performance
- Technical signals are calculated using real market movements when available
- For cryptocurrencies with limited data, the app provides estimated indicators based on available information

---

<p align="center">Built with ❤️ using Streamlit, Coinpaprika API, and Google Gemini AI</p>
<p align="center">
  <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Made%20with-Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Made with Streamlit"></a>
  <a href="https://coinpaprika.com/"><img src="https://img.shields.io/badge/Data-Coinpaprika-gold?style=flat-square" alt="Data: Coinpaprika"></a>
  <a href="https://ai.google.dev/"><img src="https://img.shields.io/badge/AI-Google%20Gemini-blue?style=flat-square&logo=google&logoColor=white" alt="AI: Google Gemini"></a>
</p>