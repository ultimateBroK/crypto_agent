"""
Crypto Analysis Pro Dashboard - Main Application

A modular, maintainable Streamlit application for cryptocurrency analysis
with AI-powered insights and technical indicators.
"""

import streamlit as st
import pandas as pd
import logging
import os
from datetime import datetime
from dotenv import load_dotenv
from agno.agent import Agent

# Import modules
from src.utils.logger import setup_logger
from src.utils.constants import DEFAULT_COIN, TIMEFRAMES, DEFAULT_TIMEFRAME, GEMINI_API_KEY
from src.utils.formatting import format_price, format_large_number

from src.data_processing.binance_api import get_coin_list, get_ticker_price, get_historical_klines
from src.data_processing.market_data import get_market_data, update_market_data_cache

from src.analytics.technical_indicators import calculate_binance_technical_indicators
from src.analytics.ai_analysis import setup_ai_agent, generate_analysis_prompt, run_ai_analysis

from src.ui_components.styles import setup_page_style
from src.ui_components.sidebar import setup_sidebar, display_coin_metrics
from src.ui_components.market_summary import display_market_summary
from src.ui_components.analysis_display import display_analysis
from src.ui_components.charts import display_volume_analysis

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logger()

def main():
    """Main application function."""
    # Set up page configuration and styles
    setup_page_style()
    
    # Initialize session state
    if 'market_data_cache' not in st.session_state:
        st.session_state.market_data_cache = {}
    
    if 'last_update_time' not in st.session_state:
        st.session_state.last_update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Get coin list
    try:
        coins_list = get_coin_list()
    except Exception as e:
        logger.error(f"Error fetching coin list: {str(e)}")
        st.error("Error fetching cryptocurrency list. Please try again later.")
        coins_list = []
    
    # Setup sidebar and get user inputs
    coin_query, timeframe = setup_sidebar(coins_list)
    
    # Process user query
    if not coin_query:
        coin_query = DEFAULT_COIN
    
    # Standardize coin symbol format
    coin_symbol = coin_query.upper().replace("USDT", "")
    full_symbol = f"{coin_symbol}USDT"  # Keep the original case for display, API will handle formatting
    
    # Display header
    st.markdown(f"# {coin_symbol} Analysis Dashboard")
    st.markdown(f"<p style='color: #6B7280;'>Comprehensive analysis and AI-powered insights for {coin_symbol}.</p>", unsafe_allow_html=True)
    
    # Main content
    try:
        # Get market data
        coin_info = next((coin for coin in coins_list if coin["binance_symbol"].lower() == full_symbol), None)
        
        if not coin_info:
            # Try with just the symbol as fallback
            coin_info = next((coin for coin in coins_list if coin["symbol"].lower() == coin_symbol.lower()), None)
            
            if not coin_info:
                st.warning(f"Cryptocurrency {coin_symbol} not found. Please try another symbol.")
                return
        
        # Get market data with caching
        stats = get_market_data(coin_symbol, coin_info)
        
        # Display market summary
        display_market_summary(stats, coin_symbol, st.session_state.last_update_time)
        
        # Calculate technical indicators
        tech_indicators = calculate_binance_technical_indicators(full_symbol, TIMEFRAMES[timeframe]["interval"])
        
        # Display coin metrics in sidebar
        display_coin_metrics(stats, tech_indicators)
        
        # Get historical data for charts
        historical_data = get_historical_klines(
            full_symbol, 
            TIMEFRAMES[timeframe]["interval"], 
            TIMEFRAMES[timeframe]["limit"]
        )
        
        # Determine technical signal
        tech_signal = "HOLD"  # Default
        
        # Simple logic based on RSI and MACD
        rsi = tech_indicators.get('rsi', 50)
        macd = tech_indicators.get('macd', 0)
        macd_signal = tech_indicators.get('macd_signal', 0)
        
        if rsi < 30 and macd > macd_signal:
            tech_signal = "BUY"
        elif rsi > 70 and macd < macd_signal:
            tech_signal = "SELL"
        
        # Setup AI agent
        try:
            agent = setup_ai_agent(GEMINI_API_KEY)
            
            # Generate analysis prompt
            prompt = generate_analysis_prompt(
                coin_symbol, 
                stats, 
                tech_indicators, 
                historical_data
            )
            
            # Run AI analysis
            with st.spinner("Generating AI analysis..."):
                rec, rationale, factors, outlook, targets = run_ai_analysis(agent, prompt)
                
                # Display analysis
                display_analysis(
                    rec, 
                    rationale, 
                    factors, 
                    outlook, 
                    targets, 
                    tech_signal, 
                    stats, 
                    historical_data, 
                    coin_symbol, 
                    timeframe
                )
        
        except Exception as e:
            logger.error(f"Error in AI analysis: {str(e)}")
            st.error(f"Error generating AI analysis: {str(e)}")
            
            # Display a simplified analysis without AI
            st.markdown("### Technical Analysis")
            st.markdown(f"**Signal:** {tech_signal}")
            
            # Display basic chart
            if not historical_data.empty:
                st.line_chart(historical_data['close'])
        
        # Volume Analysis Section
        st.markdown("## Volume Analysis")
        if not historical_data.empty:
            display_volume_analysis(historical_data, coin_symbol)
        else:
            st.warning("No historical data available for volume analysis.")
    
    except Exception as e:
        logger.error(f"Error in main application: {str(e)}")
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
