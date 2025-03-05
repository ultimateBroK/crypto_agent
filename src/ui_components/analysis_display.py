"""
Analysis display UI components for the Crypto Analysis Pro Dashboard.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, List, Tuple

from src.utils.constants import TIMEFRAMES
from src.analytics.ai_analysis import extract_signal, enhance_ai_analysis, extract_price_targets
from src.ui_components.charts import create_candlestick_chart
from src.ui_components.price_targets import display_price_targets_table
from src.ui_components.trading_strategy import generate_trading_strategy

def format_section_with_bullets(text: str) -> str:
    """Format text as bullet points for better readability."""
    if not text or "no data" in text.lower():
        return text
    
    # Split by newlines and filter out empty lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Check if already has bullet points
    has_bullets = any(line.startswith('•') or line.startswith('-') or line.startswith('*') for line in lines)
    
    if has_bullets:
        # Already has bullet points, just ensure proper HTML
        formatted_lines = []
        for line in lines:
            # Remove existing bullet if present and add our own
            if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                clean_line = line[1:].strip()
                formatted_lines.append(f"<li>{clean_line}</li>")
            else:
                formatted_lines.append(f"<li>{line}</li>")
        
        return f"<ul class='bullet-list'>{''.join(formatted_lines)}</ul>"
    else:
        # No bullet points, add them
        formatted_lines = [f"<li>{line}</li>" for line in lines]
        return f"<ul class='bullet-list'>{''.join(formatted_lines)}</ul>"

def display_analysis(rec: str, rationale: str, factors: str, outlook: str, targets: str, 
                    tech_signal: str, stats: Dict[str, Any], hist_data: pd.DataFrame, 
                    coin_symbol: str, timeframe: str):
    """Display analysis using native Streamlit components with candlestick chart."""

    # Enhance the AI analysis for more confidence
    rec, rationale, factors, outlook, targets = enhance_ai_analysis(rec, rationale, factors, outlook, targets)

    # Format text sections with bullet points
    formatted_rationale = format_section_with_bullets(rationale)
    formatted_factors = format_section_with_bullets(factors)
    formatted_outlook = format_section_with_bullets(outlook)

    # Keep targets in original format for price extraction
    formatted_targets = format_section_with_bullets(targets) if targets != "No data" else targets

    # Create a stylish container for the analysis
    st.markdown("""
    <div style="background-color: #1E1E1E; border-radius: 0.75rem; padding: 1.5rem; margin: 1rem 0; border: 1px solid #333; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);">
        <h2 style="margin-bottom: 1.5rem; color: #60A5FA;">AI Analysis Report 🤖</h2>
    """, unsafe_allow_html=True)
    
    # Signal and recommendation section
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div style="background-color: #252525; padding: 1rem; border-radius: 0.5rem; height: 100%;"><h3 style="color: #E5E7EB; margin-bottom: 1rem;">Technical Signal</h3>', unsafe_allow_html=True)
        if tech_signal.lower() == "buy":
            st.markdown(f"<div style='background-color: rgba(16, 185, 129, 0.2); padding: 0.75rem; border-radius: 0.5rem; text-align: center;'><h3 style='color: #10B981; margin: 0;'>{tech_signal.upper()}</h3></div>", unsafe_allow_html=True)
        elif tech_signal.lower() == "sell":
            st.markdown(f"<div style='background-color: rgba(239, 68, 68, 0.2); padding: 0.75rem; border-radius: 0.5rem; text-align: center;'><h3 style='color: #EF4444; margin: 0;'>{tech_signal.upper()}</h3></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background-color: rgba(245, 158, 11, 0.2); padding: 0.75rem; border-radius: 0.5rem; text-align: center;'><h3 style='color: #F59E0B; margin: 0;'>{tech_signal.upper()}</h3></div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div style="background-color: #252525; padding: 1rem; border-radius: 0.5rem; height: 100%;"><h3 style="color: #E5E7EB; margin-bottom: 1rem;">AI Recommendation</h3>', unsafe_allow_html=True)
        rec_signal = extract_signal(rec)
        if rec_signal == "buy":
            st.markdown(f"<div style='background-color: rgba(16, 185, 129, 0.2); padding: 0.75rem; border-radius: 0.5rem; text-align: center;'><h3 style='color: #10B981; margin: 0;'>{rec}</h3></div>", unsafe_allow_html=True)
        elif rec_signal == "sell":
            st.markdown(f"<div style='background-color: rgba(239, 68, 68, 0.2); padding: 0.75rem; border-radius: 0.5rem; text-align: center;'><h3 style='color: #EF4444; margin: 0;'>{rec}</h3></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background-color: rgba(245, 158, 11, 0.2); padding: 0.75rem; border-radius: 0.5rem; text-align: center;'><h3 style='color: #F59E0B; margin: 0;'>{rec}</h3></div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="margin: 1.5rem 0;"></div>', unsafe_allow_html=True)
    
    # Organize content in tabs for better navigation
    analysis_tab, factors_tab, outlook_tab, targets_tab = st.tabs(["Analysis", "Key Factors", "Outlook", "Price Targets"])

    with analysis_tab:
        st.markdown('<div style="background-color: #252525; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem;">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #60A5FA; margin-bottom: 1rem;">Trading Rationale</h4>', unsafe_allow_html=True)
        st.markdown(formatted_rationale, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with factors_tab:
        st.markdown('<div style="background-color: #252525; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem;">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #60A5FA; margin-bottom: 1rem;">Key Market & Technical Factors</h4>', unsafe_allow_html=True)
        st.markdown(formatted_factors, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with outlook_tab:
        st.markdown('<div style="background-color: #252525; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem;">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #60A5FA; margin-bottom: 1rem;">Market Outlook</h4>', unsafe_allow_html=True)
        st.markdown(formatted_outlook, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with targets_tab:
        st.markdown('<div style="background-color: #252525; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem;">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #60A5FA; margin-bottom: 1rem;">Price Targets & Support Levels</h4>', unsafe_allow_html=True)
        st.markdown(formatted_targets, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
            
    # Close the main analysis container div
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Parse and visualize price targets
    try:
        if targets != "No data" and targets is not None:
            # Extract price targets into DataFrame
            current_price = stats.get('price', 0.0)
            price_data = extract_price_targets(targets, current_price)
            
            if not price_data.empty:
                # Display as table first with improved styling
                st.markdown('<div style="background-color: #1E1E1E; border-radius: 0.75rem; padding: 1.5rem; margin: 1.5rem 0; border: 1px solid #333; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);">', unsafe_allow_html=True)
                st.markdown('<h3 style="margin-bottom: 1rem; color: #60A5FA;">Target Levels</h3>', unsafe_allow_html=True)
                display_price_targets_table(price_data)
                st.markdown('</div>', unsafe_allow_html=True)

                # Display professional candlestick chart with improved styling
                st.markdown('<div style="background-color: #1E1E1E; border-radius: 0.75rem; padding: 1.5rem; margin: 1.5rem 0; border: 1px solid #333; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);">', unsafe_allow_html=True)
                st.markdown('<h3 style="margin-bottom: 1rem; color: #60A5FA;">Technical Analysis Chart</h3>', unsafe_allow_html=True)

                # Timeframe selection
                timeframe_options = list(TIMEFRAMES.keys())

                # Build the HTML string for timeframe buttons with improved styling
                buttons_html = []
                for tf in timeframe_options:
                    active_class = "active" if tf == timeframe else ""
                    active_style = "background-color: #3B82F6; color: white;" if tf == timeframe else "background-color: #374151; color: #E5E7EB;"
                    # Fix URL parameter handling
                    button_html = f'<a href="?coin_query={coin_symbol.upper()}&timeframe={tf}" style="{active_style} margin-right: 0.5rem; padding: 0.5rem 1rem; border: none; border-radius: 0.25rem; cursor: pointer; font-weight: 500; transition: all 0.2s ease; text-decoration: none; display: inline-block;">{TIMEFRAMES[tf]["label"]}</a>'
                    buttons_html.append(button_html)

                st.markdown(
                    f"""
                    <div style="display: flex; flex-wrap: wrap; margin-bottom: 1rem;">
                        {"".join(buttons_html)}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if not hist_data.empty:
                    with st.spinner("Generating candlestick chart..."):
                        candlestick_fig = create_candlestick_chart(hist_data, price_data, current_price, coin_symbol, timeframe)
                        if candlestick_fig:
                            st.plotly_chart(candlestick_fig, use_container_width=True)
                        else:
                            st.warning("Unable to create candlestick chart due to insufficient data.")
                else:
                    st.warning("Historical price data is not available for this cryptocurrency.")
                
                # Close the chart container div
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Generate and display trading strategy
                try:
                    strategy_html = generate_trading_strategy(tech_signal, rec, current_price, price_data, stats)
                    st.markdown(strategy_html, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error generating trading strategy: {str(e)}")
            else:
                st.info("No specific price targets could be extracted from the analysis.")
        else:
            st.info("No price targets available for this cryptocurrency.")
    except Exception as e:
        st.error(f"Error processing price targets: {str(e)}")
