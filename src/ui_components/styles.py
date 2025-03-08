"""
UI styles and CSS for the Crypto Analysis Pro Dashboard.
"""

import streamlit as st

def setup_page_style():
    """Set up page style with enhanced CSS for better typography and modern UI components."""
    st.set_page_config(
        page_title="Crypto Analysis Pro Dashboard",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Set theme properties
    st.markdown('''
    <script>
        var elements = window.parent.document.querySelectorAll('.stApp')
        elements[0].style.fontFamily = "'Inter', 'Segoe UI', Roboto, sans serif";
    </script>
    ''', unsafe_allow_html=True)
    
    # Custom CSS for modern UI styling
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');
    
    /* Base styling */
    * {
        box-sizing: border-box;
        transition: all 0.2s ease;
    }
    
    /* Main container styling - improved spacing and readability */
    .main .block-container {
        padding: 1.5rem 2rem;
        max-width: 1400px;
        background: linear-gradient(135deg, rgba(17, 24, 39, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Super efficient dashboard grid system */
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 0.5rem;
        width: 100%;
        margin-bottom: 0.5rem;
    }
    
    /* Two-column layout - more compact */
    .two-column-grid {
        display: grid;
        grid-template-columns: 3fr 1fr;
        gap: 0.5rem;
        width: 100%;
    }
    
    /* Modern dark theme with improved contrast */
    .stApp {
        background: linear-gradient(135deg, #111827 0%, #1E293B 100%);
    }
    
    /* Make all text elements light with improved typography and contrast */
    .stMarkdown, .stText, p, span, label, div {
        color: #F8FAFC !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans serif;
    }
    
    /* Improved tooltip styling */
    .stTooltipIcon {
        color: #60A5FA !important;
        font-size: 1.2rem !important;
    }
    
    /* Add hover effect to interactive elements */
    [data-testid="stWidgetLabel"]:hover {
        color: #60A5FA !important;
        transition: color 0.2s ease;
    }
    
    /* Style sidebar with glass morphism effect - more compact */
    .css-1d391kg, .css-12oz5g7 {
        background-color: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(148, 163, 184, 0.1);
        padding: 1rem 0.75rem;
    }
    
    /* Style widgets with more compact look */
    .stSelectbox > div, .stTextInput > div, .stNumberInput > div {
        background-color: rgba(30, 41, 59, 0.8);
        border-radius: 6px;
        border: 1px solid rgba(148, 163, 184, 0.2);
        color: #F1F5F9;
        transition: all 0.3s ease;
        min-height: 36px;
    }
    
    .stSelectbox > div:hover, .stTextInput > div:hover, .stNumberInput > div:hover {
        border-color: rgba(56, 189, 248, 0.5);
        box-shadow: 0 0 0 1px rgba(56, 189, 248, 0.2);
    }
    
    /* Style dropdown options */
    .stSelectbox [data-baseweb=select] > div {
        background-color: rgba(30, 41, 59, 0.9);
        color: #F1F5F9;
        min-height: 36px;
    }
    
    /* Button styling - enhanced visibility and feedback */
    .stButton > button {
        background: linear-gradient(90deg, #3B82F6, #2563EB);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        min-width: 160px;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, rgba(255,255,255,0.1), rgba(255,255,255,0.2));
        transform: translateX(-100%);
        transition: transform 0.5s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #2563EB, #1D4ED8);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
        transform: translateY(-2px);
    }
    
    .stButton > button:hover::before {
        transform: translateX(100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    /* Button icons */
    .stButton > button[data-baseweb="button"]::after {
        font-family: "Material Icons";
        margin-left: 0.5rem;
    }
    
    .stButton > button[aria-label*="Technical"]::after {
        content: "📊";
    }
    
    .stButton > button[aria-label*="Analysis"]::after {
        content: "🔍";
    }
    
    .stButton > button[aria-label*="Strategy"]::after {
        content: "📈";
    }
    
    /* Typography improvements with modern font stack - ultra-compact */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', 'Segoe UI', Tahoma, Geneva, sans serif;
        font-weight: 600;
        letter-spacing: -0.025em;
        color: #F1F5F9;
        margin-bottom: 0.25rem;
        line-height: 1.1;
    }
    
    h1 {
        font-size: 1.5rem;
        background: linear-gradient(90deg, #38BDF8, #818CF8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    h2 {
        font-size: 1.25rem;
        color: #E0F2FE;
        padding-bottom: 0.25rem;
        position: relative;
        margin-top: 0.75rem;
        margin-bottom: 0.5rem;
    }
    
    h2::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 40px;
        height: 2px;
        background: linear-gradient(90deg, #38BDF8, #818CF8);
        border-radius: 2px;
    }
    
    h3 {
        font-size: 1rem;
        color: #BAE6FD;
        margin-bottom: 0.375rem;
    }
    
    p, li, div {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans serif;
        font-size: 0.9rem;
        line-height: 1.5;
        color: #F1F5F9;
    }
    
    /* Improved card styling with better contrast and visibility */
    .card {
        background: rgba(30, 41, 59, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        padding: 1rem;
        margin-bottom: 0.75rem;
        border: 1px solid rgba(148, 163, 184, 0.3);
        transition: all 0.2s ease;
        max-width: 100%;
        overflow: hidden;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        border-color: rgba(56, 189, 248, 0.5);
    }
    
    /* Add visual indicator for interactive cards */
    .card.interactive {
        cursor: pointer;
        position: relative;
    }
    
    .card.interactive::after {
        content: '⟩';
        position: absolute;
        right: 1rem;
        top: 50%;
        transform: translateY(-50%);
        color: #60A5FA;
        font-size: 1.2rem;
        opacity: 0.7;
        transition: all 0.2s ease;
    }
    
    .card.interactive:hover::after {
        right: 0.8rem;
        opacity: 1;
    }
    
    /* Ultra-efficient card grid layout */
    .card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 0.375rem;
        width: 100%;
        margin-bottom: 0.375rem;
    }
    
    .card-compact {
        padding: 0.375rem;
        margin-bottom: 0.375rem;
    }
    
    /* Flexible layouts - more compact */
    .flex-row {
        display: flex;
        flex-direction: row;
        gap: 0.375rem;
        flex-wrap: wrap;
        align-items: center;
    }
    
    .flex-col {
        display: flex;
        flex-direction: column;
        gap: 0.375rem;
    }
    
    /* Optimized signal styling with consistent color scheme */
    .signal {
        font-weight: 600;
        padding: 0.25rem 0.4rem;
        border-radius: 4px;
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
        text-transform: uppercase;
        font-size: 0.7rem;
        letter-spacing: 0.025em;
        white-space: nowrap;
    }
    
    /* Enhanced color scheme for signals */
    .signal-buy {
        color: white !important;
        background: #10B981;  /* Green */
        border: none;
    }
    
    .signal-sell {
        color: white !important;
        background: #EF4444;  /* Red */
        border: none;
    }
    
    .signal-hold {
        color: #0F172A !important;
        background: #FBBF24;  /* Yellow */
        border: none;
    }
    
    /* Enhanced metrics styling with improved readability */
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9));
        backdrop-filter: blur(10px);
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        border: 1px solid rgba(148, 163, 184, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        border-color: rgba(56, 189, 248, 0.5);
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.95));
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 3px;
        height: 100%;
        background: linear-gradient(180deg, #3B82F6, #60A5FA);
        opacity: 0.7;
    }
    
    .metric-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #BAE6FD;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .metric-title::after {
        content: "ℹ️";
        font-size: 0.9rem;
        opacity: 0.7;
        cursor: help;
    }
    
    .metric-value {
        font-size: 1.25rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.25rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Technical indicator tooltips */
    [data-tooltip] {
        position: relative;
        cursor: help;
    }

    [data-tooltip]::before {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        padding: 0.75rem;
        background: rgba(15, 23, 42, 0.95);
        color: #F8FAFC;
        border-radius: 6px;
        font-size: 0.85rem;
        white-space: normal;
        width: max-content;
        max-width: 300px;
        visibility: hidden;
        opacity: 0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(148, 163, 184, 0.3);
        z-index: 1000;
    }

    [data-tooltip]:hover::before {
        visibility: visible;
        opacity: 1;
        bottom: calc(100% + 10px);
    }
    
    .metric-change {
        display: inline-flex;
        align-items: center;
        padding: 0.2rem 0.5rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    .metric-change-positive {
        color: #10B981;  /* Green */
        background-color: rgba(16, 185, 129, 0.1);
    }
    
    .metric-change-negative {
        color: #EF4444;  /* Red */
        background-color: rgba(239, 68, 68, 0.1);
    }
    
    .metric-change-neutral {
        color: #94A3B8;
        background-color: rgba(148, 163, 184, 0.1);
    }
    
    /* Mood indicators with consistent color scheme */
    .mood {
        display: inline-flex;
        align-items: center;
        gap: 0.375rem;
        padding: 0.25rem 0.5rem;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    
    .mood-bullish {
        color: #10B981;  /* Green */
        background-color: rgba(16, 185, 129, 0.1);
    }
    
    .mood-bearish {
        color: #EF4444;  /* Red */
        background-color: rgba(239, 68, 68, 0.1);
    }
    
    .mood-neutral {
        color: #FBBF24;  /* Yellow */
        background-color: rgba(251, 191, 36, 0.1);
    }
    
    /* Table styling with more compact design */
    .styled-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin: 1rem 0;
        font-size: 0.85rem;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
    }
    
    .styled-table thead tr {
        background: linear-gradient(90deg, #3B82F6, #2563EB);
        color: white;
        text-align: left;
    }
    
    .styled-table th,
    .styled-table td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid rgba(148, 163, 184, 0.2);
    }
    
    .styled-table tbody tr {
        transition: all 0.3s ease;
    }
    
    .styled-table tbody tr:nth-of-type(even) {
        background-color: rgba(30, 41, 59, 0.4);
    }
    
    .styled-table tbody tr:last-of-type {
        border-bottom: none;
    }
    
    .styled-table tbody tr:hover {
        background-color: rgba(56, 189, 248, 0.1);
        transform: translateY(-1px);
    }
    
    /* Enhanced timeframe buttons with better visibility and feedback */
    .timeframe-buttons {
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
        margin: 1.5rem 0;
        padding: 1rem;
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.8));
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid rgba(148, 163, 184, 0.2);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .timeframe-button {
        background: rgba(30, 41, 59, 0.8);
        border: 2px solid rgba(148, 163, 184, 0.3);
        color: #E2E8F0;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-size: 0.95rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
        min-width: 100px;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .timeframe-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, rgba(59, 130, 246, 0.1), rgba(37, 99, 235, 0.1));
        transform: translateX(-100%);
        transition: transform 0.5s ease;
    }
    
    .timeframe-button:hover {
        background: rgba(56, 189, 248, 0.15);
        border-color: rgba(56, 189, 248, 0.5);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        color: #F8FAFC;
    }
    
    .timeframe-button:hover::before {
        transform: translateX(100%);
    }
    
    .timeframe-button.active {
        background: linear-gradient(90deg, #3B82F6, #2563EB);
        border-color: #60A5FA;
        color: white;
        box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
        transform: translateY(-1px);
    }
    
    .timeframe-button.active::after {
        content: '✓';
        margin-left: 0.5rem;
        font-size: 1rem;
    }

    /* Add tooltips to timeframe buttons */
    .timeframe-button[data-tooltip] {
        position: relative;
    }

    .timeframe-button[data-tooltip]::before {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        padding: 0.5rem 0.75rem;
        background: rgba(15, 23, 42, 0.95);
        color: #F8FAFC;
        border-radius: 6px;
        font-size: 0.8rem;
        white-space: nowrap;
        visibility: hidden;
        opacity: 0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(148, 163, 184, 0.3);
        z-index: 1000;
    }

    .timeframe-button[data-tooltip]:hover::before {
        visibility: visible;
        opacity: 1;
        bottom: calc(100% + 10px);
    }
    
    /* Strategy section with more compact styling */
    .strategy-container {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 8px;
        padding: 1.25rem;
        margin-top: 1.5rem;
        border: 1px solid rgba(148, 163, 184, 0.2);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .strategy-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #8B5CF6, #6366F1);
        border-radius: 4px 0 0 4px;
    }
    
    .strategy-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
        border-color: rgba(139, 92, 246, 0.3);
    }
    
    .strategy-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #F1F5F9;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(148, 163, 184, 0.2);
        background: linear-gradient(90deg, #8B5CF6, #6366F1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .strategy-section {
        margin-bottom: 1rem;
        padding: 0.75rem;
        background: rgba(15, 23, 42, 0.3);
        border-radius: 6px;
        border: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    .strategy-section-title {
        font-size: 1rem;
        font-weight: 600;
        color: #E0F2FE;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.375rem;
    }
    
    .strategy-section-title::before {
        content: '';
        display: inline-block;
        width: 10px;
        height: 10px;
        background: linear-gradient(90deg, #8B5CF6, #6366F1);
        border-radius: 50%;
    }
    
    .strategy-point {
        display: flex;
        align-items: flex-start;
        margin-bottom: 0.5rem;
        padding: 0.375rem 0.5rem;
        background: rgba(30, 41, 59, 0.4);
        border-radius: 4px;
        transition: all 0.2s ease;
    }
    
    .strategy-point:hover {
        background: rgba(30, 41, 59, 0.6);
        transform: translateX(2px);
    }
    
    .strategy-point-icon {
        color: #A78BFA;
        margin-right: 0.5rem;
        font-weight: bold;
    }
    
    .strategy-point-text {
        color: #CBD5E1;
        line-height: 1.4;
        font-size: 0.85rem;
    }
    
    /* Risk-reward indicator with more compact styling */
    .risk-reward-container {
        background: rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(8px);
        border-radius: 6px;
        padding: 0.75rem;
        margin-top: 1rem;
        border: 1px solid rgba(148, 163, 184, 0.2);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .risk-reward-container:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-color: rgba(56, 189, 248, 0.3);
    }
    
    .risk-reward-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #E0F2FE;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.375rem;
    }
    
    .risk-reward-title::before {
        content: '';
        display: inline-block;
        width: 8px;
        height: 8px;
        background: linear-gradient(90deg, #10B981, #3B82F6);
        border-radius: 50%;
    }
    
    .risk-reward-bar {
        height: 0.5rem;
        background-color: rgba(30, 41, 59, 0.6);
        border-radius: 9999px;
        overflow: hidden;
        margin-bottom: 0.5rem;
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    .risk-reward-fill {
        height: 100%;
        border-radius: 9999px;
        background: linear-gradient(90deg, #10B981, #3B82F6);
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    .risk-reward-labels {
        display: flex;
        justify-content: space-between;
        font-size: 0.75rem;
        font-weight: 500;
        color: #94A3B8;
        padding: 0 0.25rem;
    }
    
    /* Volume analysis with consistent color scheme */
    .volume-indicator {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-weight: 600;
        gap: 0.375rem;
        font-size: 0.8rem;
    }
    
    .volume-spike {
        color: #EF4444;  /* Red */
        background-color: rgba(239, 68, 68, 0.1);
        border-left: 3px solid #EF4444;
    }
    
    .volume-trend-up {
        color: #10B981;  /* Green */
        background-color: rgba(16, 185, 129, 0.1);
        border-left: 3px solid #10B981;
    }
    
    .volume-trend-down {
        color: #EF4444;  /* Red */
        background-color: rgba(239, 68, 68, 0.1);
        border-left: 3px solid #EF4444;
    }
    
    /* Tabs styling with more compact look */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.375rem;
        background: rgba(15, 23, 42, 0.3);
        padding: 0.375rem;
        border-radius: 8px;
        border: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: auto;
        padding: 0.5rem 0.75rem;
        white-space: pre-wrap;
        background-color: rgba(30, 41, 59, 0.6);
        border-radius: 6px;
        border: 1px solid rgba(148, 163, 184, 0.2);
        color: #CBD5E1;
        font-weight: 500;
        transition: all 0.2s ease;
        font-size: 0.85rem;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(56, 189, 248, 0.1);
        border-color: rgba(56, 189, 248, 0.3);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #3B82F6, #2563EB);
        border-color: #2563EB;
        color: white;
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
    }
    
    /* Expander styling with more compact look */
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 6px;
        border: 1px solid rgba(148, 163, 184, 0.2);
        padding: 0.5rem 0.75rem;
        font-weight: 600;
        color: #E0F2FE;
        transition: all 0.2s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(30, 41, 59, 0.8);
        border-color: rgba(56, 189, 248, 0.3);
    }
    
    /* Status styling with more compact design */
    .stStatus {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 6px;
        border: 1px solid rgba(148, 163, 184, 0.2);
        padding: 0.75rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Bullet list with more compact styling */
    .bullet-list {
        list-style-type: none;
        padding-left: 1.25rem;
        margin-bottom: 0.75rem;
    }
    
    .bullet-list li {
        position: relative;
        margin-bottom: 0.5rem;
        padding-left: 0.5rem;
        color: #E0F2FE;
        transition: all 0.2s ease;
        font-size: 0.85rem;
    }
    
    .bullet-list li:hover {
        transform: translateX(2px);
    }
    
    .bullet-list li:before {
        content: "";
        position: absolute;
        left: -0.75rem;
        top: 0.4rem;
        width: 6px;
        height: 6px;
        background: linear-gradient(90deg, #3B82F6, #60A5FA);
        border-radius: 50%;
    }
    
    /* These styles ensure consistent color scheme across all components */
    .buy, .bullish, .positive, .up {
        color: #10B981 !important;  /* Green */
    }
    
    .sell, .bearish, .negative, .down {
        color: #EF4444 !important;  /* Red */
    }
    
    .hold, .neutral, .stable {
        color: #FBBF24 !important;  /* Yellow */
    }
    
    /* Remove unnecessary padding in containers */
    .stDataFrame, .stSelectbox, .stMultiselect {
        padding: 0 !important;
    }
    
    /* Make streamlit containers more compact */
    div[data-testid="stVerticalBlock"] {
        gap: 0.5rem !important;
    }
    
    /* Reduce spacing between elements */
    .element-container {
        margin-bottom: 0.5rem !important;
    }

    /* Improve container spacing */
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        padding: 1rem;
    }
    
    /* Fix sidebar width */
    .css-1d391kg {
        width: 320px !important;
        max-width: 320px !important;
    }
    
    /* Improve card layouts */
    .card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Enhanced metrics cards */
    .metric-card {
        background: rgba(30, 41, 59, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 0.75rem;
        border: 1px solid rgba(148, 163, 184, 0.2);
        padding: 1rem;
        height: 100%;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
    }
    
    /* Improve text contrast */
    .text-label {
        color: #94A3B8 !important;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .text-value {
        color: #E5E7EB !important;
        font-size: 1.25rem;
        font-weight: 600;
    }
    
    /* Better tooltips */
    .tooltip .tooltip-text {
        min-width: 200px;
        max-width: 300px;
        line-height: 1.4;
    }

    /* Cải thiện layout chính */
    .main .block-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
        display: grid;
        gap: 1.5rem;
        grid-template-columns: minmax(0, 1fr) 320px;
    }

    /* Fix cột bên phải */
    .technical-metrics {
        position: sticky;
        top: 1rem;
        height: fit-content;
        width: 320px;
    }

    /* Cải thiện card layout */
    .card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1rem;
        align-items: start;
    }

    /* Thêm padding và margin hợp lý */
    .section {
        margin-bottom: 1.5rem;
        padding: 1rem;
        background: rgba(30, 41, 59, 0.85);
        border-radius: 0.75rem;
        border: 1px solid rgba(148, 163, 184, 0.2);
    }

    /* Căn chỉnh các elements */
    .flex-container {
        display: flex;
        gap: 1rem;
        align-items: flex-start;
    }

    .flex-column {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    /* Tối ưu khoảng cách */
    .stMarkdown {
        margin-bottom: 0.75rem !important;
    }

    /* Giảm padding của container */
    .element-container {
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Fix sidebar width */
    .css-1d391kg {
        width: 320px !important;
        padding: 1rem !important;
    }

    /* Cải thiện responsive */
    @media screen and (max-width: 768px) {
        .main .block-container {
            grid-template-columns: 1fr;
        }
        
        .technical-metrics {
            position: static;
            width: 100%;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def apply_card_style():
    """Apply improved card style with better contrast and visual cues."""
    return """
    <style>
    .card {
        background: rgba(30, 41, 59, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        padding: 1rem;
        margin-bottom: 0.75rem;
        border: 1px solid rgba(148, 163, 184, 0.3);
        transition: all 0.2s ease;
        max-width: 100%;
        overflow: hidden;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        border-color: rgba(56, 189, 248, 0.5);
    }
    
    .card.interactive {
        cursor: pointer;
        position: relative;
    }
    
    .card.interactive::after {
        content: '⟩';
        position: absolute;
        right: 1rem;
        top: 50%;
        transform: translateY(-50%);
        color: #60A5FA;
        font-size: 1.2rem;
        opacity: 0.7;
        transition: all 0.2s ease;
    }
    
    .card.interactive:hover::after {
        right: 0.8rem;
        opacity: 1;
    }
    
    .card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 0.75rem;
        width: 100%;
    }
    
    .card-compact {
        padding: 0.75rem;
        margin-bottom: 0.75rem;
    }
    
    /* Add tooltips for better user guidance */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    .tooltip .tooltip-text {
        visibility: hidden;
        width: 200px;
        background-color: rgba(15, 23, 42, 0.95);
        color: #F8FAFC;
        text-align: center;
        border-radius: 6px;
        padding: 0.5rem;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 0.8rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(148, 163, 184, 0.3);
    }
    
    .tooltip:hover .tooltip-text {
        visibility: visible;
        opacity: 1;
    }
    </style>
    """


def get_signal_class(signal):
    """Get the CSS class for a signal with optimized color scheme."""
    signal = signal.lower() if isinstance(signal, str) else ""
    base_class = "signal "
    if "buy" in signal or "strong buy" in signal:
        return base_class + "signal-buy"
    elif "sell" in signal or "strong sell" in signal:
        return base_class + "signal-sell"
    else:
        return base_class + "signal-hold"


def get_signal_icon(signal):
    """Get an appropriate icon for a trading signal."""
    signal = signal.lower() if isinstance(signal, str) else ""
    
    if "buy" in signal or "strong buy" in signal:
        return "↗️"
    elif "sell" in signal or "strong sell" in signal:
        return "↘️"
    else:
        return "↔️"


def get_mood_class(mood):
    """Get the CSS class for a market mood with consistent color scheme."""
    mood = mood.lower()
    base_class = "mood "
    if "bullish" in mood:
        return base_class + "mood-bullish"
    elif "bearish" in mood:
        return base_class + "mood-bearish"
    else:
        return base_class + "mood-neutral"


def get_confidence_class(confidence):
    """Get the CSS class for a confidence level with consistent colors."""
    confidence = confidence.lower()
    base_class = "confidence "
    if "high" in confidence:
        return base_class + "confidence-high"
    elif "medium" in confidence or "moderate" in confidence:
        return base_class + "confidence-medium"
    else:
        return base_class + "confidence-low"


def get_price_level_class(level_type):
    """Get the CSS class for a price level (support/resistance) with consistent colors."""
    level_type = level_type.lower()
    base_class = "price-level "
    if "support" in level_type:
        return base_class + "support"
    else:
        return base_class + "resistance"


def get_volume_class(volume_type):
    """Get the CSS class for volume indicators with consistent colors."""
    volume_type = volume_type.lower()
    base_class = "volume-indicator "
    if "spike" in volume_type:
        return base_class + "volume-spike"
    elif "up" in volume_type or "increase" in volume_type:
        return base_class + "volume-trend-up"
    else:
        return base_class + "volume-trend-down"
