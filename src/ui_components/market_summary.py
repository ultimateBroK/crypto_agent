"""
Market summary UI components for the Crypto Analysis Pro Dashboard.
"""

import streamlit as st
from typing import Dict, Any

from src.utils.formatting import format_price, format_large_number

def display_market_summary(stats: Dict[str, Any], symbol: str, update_time: str):
    """Display market summary using native Streamlit components with improved UI."""
    # Market summary section with improved styling
    st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
        <h2 style="margin: 0; color: #E5E7EB;">Market Summary</h2>
        <div class="tooltip" style="margin-left: 0.5rem;">
            <span style="color: #60A5FA; cursor: help;">ℹ️</span>
            <span class="tooltip-text">Key market metrics for the selected cryptocurrency</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a card-like container with improved dark theme
    st.markdown("""
    <div style="
        background-color: rgba(30, 41, 59, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 0.75rem;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(148, 163, 184, 0.3);
        transition: all 0.2s ease;
    ">
    """, unsafe_allow_html=True)
    
    # Create columns for layout with improved spacing
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Price and change with improved styling and visual feedback
        price = stats.get('price', 0)
        price_change_pct = stats.get('price_change_pct', 0)
        
        # Determine color based on price change
        if price_change_pct > 0:
            price_color = "#10B981"  # Green
            price_icon = "↗"
            price_bg = "rgba(16, 185, 129, 0.2)"
        elif price_change_pct < 0:
            price_color = "#EF4444"  # Red
            price_icon = "↘"
            price_bg = "rgba(239, 68, 68, 0.2)"
        else:
            price_color = "#F59E0B"  # Amber for better visibility
            price_icon = "→"
            price_bg = "rgba(245, 158, 11, 0.2)"
        
        # Display price with improved dark theme styling
        st.markdown(f"""
        <div style="margin-bottom: 0.75rem;">
            <div class="tooltip">
                <span style="font-size: 1rem; color: #94A3B8; font-weight: 600;">Current Price</span>
                <span class="tooltip-text">Latest trading price with 24h change</span>
            </div>
        </div>
        <div style="display: flex; align-items: baseline; margin-bottom: 0.75rem;">
            <span style="font-size: 2.5rem; font-weight: 700; color: #F8FAFC; margin-right: 0.75rem;">
                {format_price(price)}
            </span>
            <span style="font-size: 1.25rem; font-weight: 600; color: {price_color}; background-color: {price_bg}; padding: 0.375rem 0.75rem; border-radius: 0.375rem; transition: all 0.2s ease;">
                {price_icon} {price_change_pct:.2f}%
            </span>
        </div>
        <div style="font-size: 0.875rem; color: #94A3B8; display: flex; align-items: center;">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 0.375rem;"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
            Last updated: {update_time}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Market data with improved styling and tooltips
        volume = stats.get('volume', 0)
        cap = stats.get('cap', 0)
        
        st.markdown(f"""
        <div style="margin-bottom: 1rem; background-color: rgba(37, 37, 37, 0.9); padding: 1rem; border-radius: 0.5rem; transition: all 0.2s ease; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <div style="font-size: 0.875rem; color: #94A3B8; margin-bottom: 0.375rem; display: flex; align-items: center;">
                <span>Trading Volume (24h)</span>
                <div class="tooltip" style="margin-left: 0.375rem;">
                    <span style="color: #60A5FA; cursor: help; font-size: 0.75rem;">ℹ️</span>
                    <span class="tooltip-text">Total trading volume over the past 24 hours</span>
                </div>
            </div>
            <div style="font-size: 1.375rem; font-weight: 600; color: #F8FAFC;">
                {format_large_number(volume, "$")}
            </div>
        </div>
        <div style="background-color: rgba(37, 37, 37, 0.9); padding: 1rem; border-radius: 0.5rem; transition: all 0.2s ease; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <div style="font-size: 0.875rem; color: #94A3B8; margin-bottom: 0.375rem; display: flex; align-items: center;">
                <span>Market Cap</span>
                <div class="tooltip" style="margin-left: 0.375rem;">
                    <span style="color: #60A5FA; cursor: help; font-size: 0.75rem;">ℹ️</span>
                    <span class="tooltip-text">Total market value of all coins in circulation</span>
                </div>
            </div>
            <div style="font-size: 1.375rem; font-weight: 600; color: #F8FAFC;">
                {format_large_number(cap, "$")}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Market sentiment with improved styling and tooltips
        mood = stats.get('mood', 'Neutral')
        buzz = stats.get('buzz', 'Moderate')
        
        # Determine mood color and icon
        if mood == "Bullish":
            mood_color = "#10B981"  # Green
            mood_icon = "📈"
            mood_bg = "rgba(16, 185, 129, 0.2)"
        elif mood == "Bearish":
            mood_color = "#EF4444"  # Red
            mood_icon = "📉"
            mood_bg = "rgba(239, 68, 68, 0.2)"
        else:
            mood_color = "#F59E0B"  # Amber
            mood_icon = "📊"
            mood_bg = "rgba(245, 158, 11, 0.2)"
        
        # Determine buzz color and icon
        if buzz == "High":
            buzz_color = "#10B981"  # Green
            buzz_icon = "🔥"
            buzz_bg = "rgba(16, 185, 129, 0.2)"
        elif buzz == "Low":
            buzz_color = "#EF4444"  # Red
            buzz_icon = "❄️"
            buzz_bg = "rgba(239, 68, 68, 0.2)"
        else:
            buzz_color = "#F59E0B"  # Amber
            buzz_icon = "⚡"
            buzz_bg = "rgba(245, 158, 11, 0.2)"
        
        st.markdown(f"""
        <div style="margin-bottom: 1rem; background-color: rgba(37, 37, 37, 0.9); padding: 1rem; border-radius: 0.5rem; transition: all 0.2s ease; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <div style="font-size: 0.875rem; color: #94A3B8; margin-bottom: 0.375rem; display: flex; align-items: center;">
                <span>Market Sentiment</span>
                <div class="tooltip" style="margin-left: 0.375rem;">
                    <span style="color: #60A5FA; cursor: help; font-size: 0.75rem;">ℹ️</span>
                    <span class="tooltip-text">Overall market mood based on technical and social indicators</span>
                </div>
            </div>
            <div style="font-size: 1.25rem; font-weight: 600; background-color: {mood_bg}; color: {mood_color}; padding: 0.375rem 0.75rem; border-radius: 0.375rem; display: inline-flex; align-items: center; gap: 0.5rem; transition: all 0.2s ease;">
                <span>{mood_icon}</span>
                <span>{mood}</span>
            </div>
        </div>
        <div style="background-color: rgba(37, 37, 37, 0.9); padding: 1rem; border-radius: 0.5rem; transition: all 0.2s ease; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <div style="font-size: 0.875rem; color: #94A3B8; margin-bottom: 0.375rem; display: flex; align-items: center;">
                <span>Trading Activity</span>
                <div class="tooltip" style="margin-left: 0.375rem;">
                    <span style="color: #60A5FA; cursor: help; font-size: 0.75rem;">ℹ️</span>
                    <span class="tooltip-text">Current trading volume relative to historical averages</span>
                </div>
            </div>
            <div style="font-size: 1.25rem; font-weight: 600; background-color: {buzz_bg}; color: {buzz_color}; padding: 0.375rem 0.75rem; border-radius: 0.375rem; display: inline-flex; align-items: center; gap: 0.5rem; transition: all 0.2s ease;">
                <span>{buzz_icon}</span>
                <span>{buzz}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Close the card container
    st.markdown("</div>", unsafe_allow_html=True)
