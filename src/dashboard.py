"""
Main dashboard application for the Crypto Analysis Pro dashboard.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List, Tuple
import time
import traceback

from src.data.coin_data import get_coin_data, get_historical_data
from src.analytics.technical_analysis import perform_technical_analysis, get_technical_signal
from src.analytics.ai_analysis import analyze_with_ai
from src.ui_components.styles import setup_page_style
from src.ui_components.sidebar import setup_sidebar, display_coin_metrics
from src.ui_components.market_summary import display_market_summary
from src.ui_components.analysis_display import display_analysis
from src.ui_components.charts import create_candlestick_chart, display_volume_analysis
from src.utils.constants import TIMEFRAMES

def main():
    """Main function to run the Crypto Analysis Pro dashboard."""
    # Set up page style with modern UI
    setup_page_style()
    
    # App title
    st.title("Crypto Analysis Pro Dashboard")
    
    # Setup sidebar with search
    coin_query, timeframe = setup_sidebar(get_coin_list())
    
    # Check if we have a coin query
    if not coin_query:
        display_welcome_screen()
        return

    # Fetch and display data for the selected coin
    try:
        with st.spinner(f"Analyzing {coin_query.upper()}..."):
            display_coin_analysis(coin_query.upper(), timeframe)
    except Exception as e:
        st.error(f"Error analyzing {coin_query.upper()}: {str(e)}")
        st.exception(e)

def get_coin_list() -> List[Dict[str, str]]:
    """Get list of available coins."""
    # This would normally fetch from API or database
    # For demo purposes, return a sample list
    return [
        {"symbol": "BTC", "name": "Bitcoin"},
        {"symbol": "ETH", "name": "Ethereum"},
        {"symbol": "SOL", "name": "Solana"},
        {"symbol": "ADA", "name": "Cardano"},
        {"symbol": "BNB", "name": "Binance Coin"}
    ]

def display_welcome_screen():
    """Display welcome screen with instructions."""
    st.markdown("""
    <div style="background-color: #1E1E1E; border-radius: 0.75rem; padding: 1.5rem; margin: 2rem 0; border: 1px solid #333; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);">
        <h2 style="margin-bottom: 1rem; color: #60A5FA;">Welcome to Crypto Analysis Pro 👋</h2>
        <p style="color: #E5E7EB; margin-bottom: 1rem;">Get comprehensive AI-powered analysis of cryptocurrency markets with advanced technical indicators and price targets.</p>
        
        <h3 style="color: #BAE6FD; margin: 1.5rem 0 0.5rem 0;">How to use</h3>
        <ol style="color: #E5E7EB; padding-left: 1.5rem; margin-bottom: 1.5rem;">
            <li style="margin-bottom: 0.5rem;">Use the search box in the sidebar to enter a cryptocurrency symbol (e.g., BTC, ETH, SOL)</li>
            <li style="margin-bottom: 0.5rem;">Select your preferred timeframe for analysis</li>
            <li style="margin-bottom: 0.5rem;">Explore comprehensive market analysis, technical indicators, and AI-generated trading strategies</li>
        </ol>
        
        <h3 style="color: #BAE6FD; margin: 1.5rem 0 0.5rem 0;">Key Features</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-bottom: 1rem;">
            <div style="background-color: rgba(30, 41, 59, 0.7); padding: 1rem; border-radius: 0.5rem; border: 1px solid rgba(148, 163, 184, 0.2);">
                <h4 style="color: #60A5FA; margin-bottom: 0.5rem;">Technical Analysis</h4>
                <p style="color: #CBD5E1; font-size: 0.9rem;">Advanced indicators including RSI, MACD, Bollinger Bands, and moving averages with visual charts</p>
            </div>
            
            <div style="background-color: rgba(30, 41, 59, 0.7); padding: 1rem; border-radius: 0.5rem; border: 1px solid rgba(148, 163, 184, 0.2);">
                <h4 style="color: #60A5FA; margin-bottom: 0.5rem;">AI Analysis</h4>
                <p style="color: #CBD5E1; font-size: 0.9rem;">Machine learning-powered market insights, sentiment analysis, and trading recommendations</p>
            </div>
            
            <div style="background-color: rgba(30, 41, 59, 0.7); padding: 1rem; border-radius: 0.5rem; border: 1px solid rgba(148, 163, 184, 0.2);">
                <h4 style="color: #60A5FA; margin-bottom: 0.5rem;">Trading Strategies</h4>
                <p style="color: #CBD5E1; font-size: 0.9rem;">Custom trading strategies with entry/exit points, risk management, and position sizing guidance</p>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <p style="color: #94A3B8; font-size: 0.875rem;">Start by searching for a cryptocurrency in the sidebar.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sample coins for quick selection
    st.markdown("<h3 style='color: #BAE6FD; margin: 1rem 0;'>Popular Cryptocurrencies</h3>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("Bitcoin (BTC)", use_container_width=True):
            st.switch_page("dashboard.py?coin_query=BTC")
    with col2:
        if st.button("Ethereum (ETH)", use_container_width=True):
            st.switch_page("dashboard.py?coin_query=ETH")
    with col3:
        if st.button("Solana (SOL)", use_container_width=True):
            st.switch_page("dashboard.py?coin_query=SOL")
    with col4:
        if st.button("Cardano (ADA)", use_container_width=True):
            st.switch_page("dashboard.py?coin_query=ADA")
    with col5:
        if st.button("Binance Coin (BNB)", use_container_width=True):
            st.switch_page("dashboard.py?coin_query=BNB")

def display_coin_analysis(symbol: str, timeframe: str):
    """Display comprehensive analysis for the selected coin."""
    # Fetch coin data - in a real app, this would be an API call
    coin_data = get_coin_data(symbol)
    
    # Check if we have data
    if not coin_data:
        st.error(f"No data found for {symbol}. Please try another cryptocurrency.")
        return
    
    # Display market summary
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    display_market_summary(coin_data, symbol, update_time)
    
    # Fetch historical data
    historical_data = get_historical_data(symbol, timeframe)
    
    # Perform technical analysis
    tech_indicators = perform_technical_analysis(historical_data)
    tech_signal = get_technical_signal(tech_indicators)
    
    # Display technical metrics to the right of the market summary
    display_coin_metrics(coin_data, tech_indicators)
    
    # Create tabs for different analysis sections
    tab1, tab2, tab3 = st.tabs(["AI Analysis", "Technical Charts", "Volume Analysis"])
    
    with tab1:
        # Generate AI analysis
        rec, rationale, factors, outlook, targets = analyze_with_ai(
            symbol, 
            coin_data.get('price', 0), 
            tech_indicators, 
            tech_signal,
            timeframe
        )
        
        # Display analysis with visualizations
        display_analysis(
            rec, 
            rationale, 
            factors, 
            outlook, 
            targets, 
            tech_signal, 
            coin_data, 
            historical_data, 
            symbol, 
            timeframe
        )
    
    with tab2:
        st.markdown("""
        <div style="background-color: #1E1E1E; border-radius: 0.75rem; padding: 1.5rem; margin-bottom: 1.5rem; border: 1px solid #333; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);">
            <h3 style="margin-bottom: 1rem; color: #60A5FA;">Technical Price Charts</h3>
        """, unsafe_allow_html=True)
        
        # Display timeframe selection
        timeframe_options = list(TIMEFRAMES.keys())
        
        # Build the HTML string for timeframe buttons
        buttons_html = []
        for tf in timeframe_options:
            active_class = "active" if tf == timeframe else ""
            active_style = "background-color: #3B82F6; color: white;" if tf == timeframe else "background-color: #374151; color: #E5E7EB;"
            button_html = f'<button style="{active_style} margin-right: 0.5rem; padding: 0.5rem 1rem; border: none; border-radius: 0.25rem; cursor: pointer; font-weight: 500; transition: all 0.2s ease;" onclick="window.location.href=\'?coin_query={symbol}&timeframe={tf}\'">{TIMEFRAMES[tf]["label"]}</button>'
            buttons_html.append(button_html)
        
        st.markdown(
            f"""
            <div style="display: flex; flex-wrap: wrap; margin-bottom: 1rem;">
                {"".join(buttons_html)}
            </div>
            """,
            unsafe_allow_html=True
        )
        
        with st.spinner("Generating technical charts..."):
            if not historical_data.empty:
                fig = create_candlestick_chart(
                    historical_data, 
                    pd.DataFrame(),  # Empty DataFrame since we don't have price targets here
                    coin_data.get('price', 0), 
                    symbol, 
                    timeframe
                )
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Unable to generate technical chart due to insufficient data.")
            else:
                st.warning("No historical data available for the selected timeframe.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown("""
        <div style="background-color: #1E1E1E; border-radius: 0.75rem; padding: 1.5rem; margin-bottom: 1.5rem; border: 1px solid #333; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);">
            <h3 style="margin-bottom: 1rem; color: #60A5FA;">Volume Analysis</h3>
        """, unsafe_allow_html=True)
        
        with st.spinner("Analyzing trading volume patterns..."):
            display_volume_analysis(historical_data, symbol)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
