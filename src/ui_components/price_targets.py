"""
Price targets UI components for the Crypto Analysis Pro Dashboard.
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, Any, List

def display_price_targets_table(price_data: pd.DataFrame):
    """Display price targets in a formatted table."""
    if price_data.empty:
        st.warning("No price targets available.")
        return
    
    # Create columns for layout
    col1, col2 = st.columns([1, 1])
    
    # Filter data by type
    support_data = price_data[price_data['type'].str.lower() == 'support']
    resistance_data = price_data[price_data['type'].str.lower() == 'resistance']
    
    # Support levels
    with col1:
        st.markdown("""
        <div style="
            background-color: rgba(16, 185, 129, 0.1);
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
        ">
            <h4 style="color: #10B981; margin-top: 0;">Support Levels</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not support_data.empty:
            # Create HTML table for support levels
            table_html = """
            <table class="styled-table">
                <thead>
                    <tr>
                        <th>Price ($)</th>
                        <th>Confidence</th>
                        <th>Description</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            # Add rows
            for _, row in support_data.iterrows():
                table_html += f"""
                <tr>
                    <td style="font-weight: 600;">${row['price']:.4f}</td>
                    <td>
                        <div style="
                            width: 100%;
                            background-color: #E5E7EB;
                            border-radius: 0.25rem;
                            height: 0.5rem;
                        ">
                            <div style="
                                width: {row['confidence']}%;
                                background-color: #10B981;
                                border-radius: 0.25rem;
                                height: 0.5rem;
                            "></div>
                        </div>
                        <div style="font-size: 0.75rem; text-align: right;">{row['confidence']}%</div>
                    </td>
                    <td>{row['description']}</td>
                </tr>
                """
            
            table_html += """
                </tbody>
            </table>
            """
            
            st.markdown(table_html, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="
                background-color: #F3F4F6;
                border-radius: 0.25rem;
                padding: 1rem;
                text-align: center;
                color: #6B7280;
            ">
                No support levels identified
            </div>
            """, unsafe_allow_html=True)
    
    # Resistance levels
    with col2:
        st.markdown("""
        <div style="
            background-color: rgba(239, 68, 68, 0.1);
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
        ">
            <h4 style="color: #EF4444; margin-top: 0;">Resistance Levels</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not resistance_data.empty:
            # Create HTML table for resistance levels
            table_html = """
            <table class="styled-table">
                <thead>
                    <tr>
                        <th>Price ($)</th>
                        <th>Confidence</th>
                        <th>Description</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            # Add rows
            for _, row in resistance_data.iterrows():
                table_html += f"""
                <tr>
                    <td style="font-weight: 600;">${row['price']:.4f}</td>
                    <td>
                        <div style="
                            width: 100%;
                            background-color: #E5E7EB;
                            border-radius: 0.25rem;
                            height: 0.5rem;
                        ">
                            <div style="
                                width: {row['confidence']}%;
                                background-color: #EF4444;
                                border-radius: 0.25rem;
                                height: 0.5rem;
                            "></div>
                        </div>
                        <div style="font-size: 0.75rem; text-align: right;">{row['confidence']}%</div>
                    </td>
                    <td>{row['description']}</td>
                </tr>
                """
            
            table_html += """
                </tbody>
            </table>
            """
            
            st.markdown(table_html, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="
                background-color: #F3F4F6;
                border-radius: 0.25rem;
                padding: 1rem;
                text-align: center;
                color: #6B7280;
            ">
                No resistance levels identified
            </div>
            """, unsafe_allow_html=True)
