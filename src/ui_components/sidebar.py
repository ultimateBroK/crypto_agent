"""
Sidebar UI components for the Crypto Analysis Pro Dashboard.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, List, Tuple

from src.utils.constants import TIMEFRAMES

def setup_sidebar(coins_list: List[Dict[str, str]]) -> Tuple[str, str]:
    """Set up sidebar with search functionality and timeframe selection."""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1.5rem; padding: 1rem; background: linear-gradient(135deg, #1E293B, #0F172A); border-radius: 0.5rem;">
            <h2 style="margin-bottom: 0.5rem; color: #60A5FA;">Crypto Analysis Pro</h2>
            <p style="color: #94A3B8; font-size: 0.875rem;">Powered by AI & Technical Analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Search box with better styling
        st.markdown('<div style="margin-bottom: 1rem;"><strong>Search Cryptocurrency</strong></div>', unsafe_allow_html=True)
        coin_query = st.text_input(
            "Search Cryptocurrency",  # Adding a proper label to fix the warning
            placeholder="e.g. BTC, ETH, SOL...",
            help="Enter a cryptocurrency symbol to analyze",
            label_visibility="collapsed"  # Hide the label visually but keep it for accessibility
        )
        
        # Timeframe selection
        st.markdown("### Timeframe")
        
        timeframe_options = list(TIMEFRAMES.keys())
        timeframe_labels = [TIMEFRAMES[tf]["label"] for tf in timeframe_options]
        
        timeframe_index = 0  # Default to first option
        timeframe = st.radio(
            "Select analysis timeframe",
            options=timeframe_options,
            format_func=lambda x: TIMEFRAMES[x]["label"],
            index=timeframe_index,
            label_visibility="collapsed"
        )
        
        # Removed Top Cryptocurrencies section as requested
        
        # Additional information
        st.markdown("---")
        st.markdown("""
        <div style="font-size: 0.875rem; color: #6B7280;">
            <p><strong>About:</strong> This dashboard provides AI-powered analysis of cryptocurrency markets, combining technical indicators with advanced pattern recognition.</p>
            <p style="font-size: 0.75rem; margin-top: 1rem;">© 2025 Crypto Analysis Pro</p>
        </div>
        """, unsafe_allow_html=True)
    
    return coin_query, timeframe

def display_coin_metrics(stats: Dict[str, Any], tech_indicators: Dict[str, float]):
    """Display coin metrics in a dedicated container in the main area instead of sidebar."""
    # Create a stylish container for technical metrics
    st.markdown("""
    <div style="position: relative; float: right; width: 350px; background: linear-gradient(135deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.95));
         border-radius: 0.75rem; padding: 1.5rem; margin: 0 0 1.5rem 1.5rem;
         border: 1px solid rgba(148, 163, 184, 0.3); box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);">
        <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
            <h3 style="margin: 0; color: #60A5FA; font-size: 1.25rem;">Technical Metrics</h3>
            <div class="tooltip" style="margin-left: 0.5rem;">
                <span style="color: #60A5FA; cursor: help;">ℹ️</span>
                <span class="tooltip-text">Key technical indicators for market analysis</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # RSI with improved styling
    rsi = tech_indicators.get('rsi', 0)
    rsi_color = "#F59E0B"  # Default amber
    rsi_text = "Neutral"
    
    if rsi >= 70:
        rsi_color = "#EF4444"  # Red
        rsi_text = "Overbought"
    elif rsi <= 30:
        rsi_color = "#10B981"  # Green
        rsi_text = "Oversold"
    
    st.markdown(f"""
    <div style="background-color: #252525; padding: 0.75rem; border-radius: 0.5rem; margin-bottom: 0.75rem;">
        <div style="font-size: 0.875rem; color: #94A3B8; margin-bottom: 0.25rem;">RSI (14)</div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 1.25rem; font-weight: 600; color: #E5E7EB;">{rsi:.1f}</span>
            <span style="font-size: 0.75rem; background-color: rgba({','.join(['245, 158, 11' if rsi_color == '#F59E0B' else '239, 68, 68' if rsi_color == '#EF4444' else '16, 185, 129'])}, 0.2); 
                  color: {rsi_color}; padding: 0.25rem 0.5rem; border-radius: 0.25rem;">{rsi_text}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # MACD with improved styling
    macd = tech_indicators.get('macd', 0)
    macd_signal = tech_indicators.get('macd_signal', 0)
    macd_hist = macd - macd_signal
    
    macd_color = "#10B981" if macd_hist > 0 else "#EF4444"
    macd_text = "Bullish" if macd_hist > 0 else "Bearish"
    
    st.markdown(f"""
    <div style="background-color: #252525; padding: 0.75rem; border-radius: 0.5rem; margin-bottom: 0.75rem;">
        <div style="font-size: 0.875rem; color: #94A3B8; margin-bottom: 0.25rem;">MACD</div>
        <div style="font-size: 1.25rem; font-weight: 600; color: #E5E7EB; margin-bottom: 0.25rem;">{macd:.4f}</div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 0.75rem; color: #94A3B8;">Signal: {macd_signal:.4f}</span>
            <span style="font-size: 0.75rem; background-color: rgba({','.join(['16, 185, 129' if macd_color == '#10B981' else '239, 68, 68'])}, 0.2); 
                  color: {macd_color}; padding: 0.25rem 0.5rem; border-radius: 0.25rem;">{macd_text}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Bollinger Bands with improved styling
    bb_width = tech_indicators.get('bb_width', 0)
    price = stats.get('price', 0)
    bb_upper = tech_indicators.get('bb_upper', price * 1.05)
    bb_lower = tech_indicators.get('bb_lower', price * 0.95)
    
    # Calculate position within bands (0-100%)
    if bb_upper > bb_lower:  # Avoid division by zero
        band_position = (price - bb_lower) / (bb_upper - bb_lower) * 100
        band_position = max(0, min(100, band_position))  # Clamp to 0-100%
    else:
        band_position = 50
    
    # Determine color and text based on position
    if band_position > 80:
        bb_color = "#EF4444"  # Red
        bb_text = "Near Upper Band"
    elif band_position < 20:
        bb_color = "#10B981"  # Green
        bb_text = "Near Lower Band"
    else:
        bb_color = "#F59E0B"  # Amber
        bb_text = "Middle of Bands"
    
    st.markdown(f"""
    <div style="background-color: #252525; padding: 0.75rem; border-radius: 0.5rem; margin-bottom: 0.75rem;">
        <div style="font-size: 0.875rem; color: #94A3B8; margin-bottom: 0.5rem;">Bollinger Bands</div>
        <div style="height: 0.5rem; background-color: #333; border-radius: 0.25rem; margin-bottom: 0.5rem;">
            <div style="width: {band_position}%; height: 100%; background-color: {bb_color}; border-radius: 0.25rem;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.75rem;">
            <span style="color: #94A3B8;">Width: {bb_width:.2f}</span>
            <span style="background-color: rgba({','.join(['239, 68, 68' if bb_color == '#EF4444' else '16, 185, 129' if bb_color == '#10B981' else '245, 158, 11'])}, 0.2); 
                  color: {bb_color}; padding: 0.25rem 0.5rem; border-radius: 0.25rem;">{bb_text}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Moving Averages with improved styling
    ema50 = tech_indicators.get('ema50', 0)
    ema200 = tech_indicators.get('ema200', 0)
    
    if ema50 > ema200:
        ma_color = "#10B981"  # Green
        ma_text = "Bullish Trend"
    else:
        ma_color = "#EF4444"  # Red
        ma_text = "Bearish Trend"
    
    price_vs_ema50 = (price / ema50 - 1) * 100 if ema50 > 0 else 0
    price_vs_ema200 = (price / ema200 - 1) * 100 if ema200 > 0 else 0
    
    st.markdown(f"""
    <div style="background-color: #252525; padding: 0.75rem; border-radius: 0.5rem; margin-bottom: 0.75rem;">
        <div style="font-size: 0.875rem; color: #94A3B8; margin-bottom: 0.5rem;">Moving Averages</div>
        <div style="font-size: 0.875rem; margin-bottom: 0.5rem; background-color: rgba({','.join(['16, 185, 129' if ma_color == '#10B981' else '239, 68, 68'])}, 0.2); 
              color: {ma_color}; padding: 0.25rem 0.5rem; border-radius: 0.25rem; display: inline-block;">{ma_text}</div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
            <span style="font-size: 0.75rem; color: #94A3B8;">Price vs EMA50:</span>
            <span style="font-size: 0.75rem; color: {'#10B981' if price_vs_ema50 > 0 else '#EF4444'};">{price_vs_ema50:+.2f}%</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 0.75rem; color: #94A3B8;">Price vs EMA200:</span>
            <span style="font-size: 0.75rem; color: {'#10B981' if price_vs_ema200 > 0 else '#EF4444'};">{price_vs_ema200:+.2f}%</span>
        </div>
    </div>
    
    <!-- Close the technical metrics container -->
    </div>
    """, unsafe_allow_html=True)
