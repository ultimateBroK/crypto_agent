"""
Chart components for the Crypto Analysis Pro Dashboard.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, Any, List, Optional

from src.utils.constants import TIMEFRAMES

def create_candlestick_chart(historical_data: pd.DataFrame, price_data: pd.DataFrame, current_price: float, 
                            coin_symbol: str, timeframe: str) -> Optional[go.Figure]:
    """Create an interactive candlestick chart with technical indicators."""
    if historical_data.empty:
        return None
    
    # Create figure with secondary y-axis
    fig = make_subplots(
        rows=3, 
        cols=1, 
        shared_xaxes=True,
        vertical_spacing=0.02,
        row_heights=[0.6, 0.2, 0.2],
        subplot_titles=(
            f"{coin_symbol.upper()} Price ({TIMEFRAMES[timeframe]['label']})", 
            "Volume", 
            "RSI"
        )
    )
    
    # Add candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=historical_data.index,
            open=historical_data['open'],
            high=historical_data['high'],
            low=historical_data['low'],
            close=historical_data['close'],
            name="Price",
            increasing_line_color='#10B981',
            decreasing_line_color='#EF4444'
        ),
        row=1, col=1
    )
    
    # Add volume bar chart
    colors = ['#10B981' if row['close'] >= row['open'] else '#EF4444' for _, row in historical_data.iterrows()]
    
    fig.add_trace(
        go.Bar(
            x=historical_data.index,
            y=historical_data['volume'],
            name="Volume",
            marker_color=colors,
            opacity=0.8
        ),
        row=2, col=1
    )
    
    # Add RSI if available
    if 'rsi' in historical_data.columns:
        fig.add_trace(
            go.Scatter(
                x=historical_data.index,
                y=historical_data['rsi'],
                name="RSI",
                line=dict(color='#6366F1', width=1.5)
            ),
            row=3, col=1
        )
        
        # Add RSI reference lines
        fig.add_hline(y=70, line_width=1, line_dash="dash", line_color="#EF4444", row=3, col=1)
        fig.add_hline(y=30, line_width=1, line_dash="dash", line_color="#10B981", row=3, col=1)
    
    # Add EMA lines if available
    if 'ema12' in historical_data.columns:
        fig.add_trace(
            go.Scatter(
                x=historical_data.index,
                y=historical_data['ema12'],
                name="EMA 12",
                line=dict(color='#F59E0B', width=1.5)
            ),
            row=1, col=1
        )
    
    if 'ema26' in historical_data.columns:
        fig.add_trace(
            go.Scatter(
                x=historical_data.index,
                y=historical_data['ema26'],
                name="EMA 26",
                line=dict(color='#3B82F6', width=1.5)
            ),
            row=1, col=1
        )
    
    if 'ema50' in historical_data.columns:
        fig.add_trace(
            go.Scatter(
                x=historical_data.index,
                y=historical_data['ema50'],
                name="EMA 50",
                line=dict(color='#8B5CF6', width=1.5, dash='dot')
            ),
            row=1, col=1
        )
    
    if 'ema200' in historical_data.columns:
        fig.add_trace(
            go.Scatter(
                x=historical_data.index,
                y=historical_data['ema200'],
                name="EMA 200",
                line=dict(color='#EC4899', width=1.5, dash='dot')
            ),
            row=1, col=1
        )
    
    # Add Bollinger Bands if available
    if all(col in historical_data.columns for col in ['bollinger_upper', 'sma20', 'bollinger_lower']):
        fig.add_trace(
            go.Scatter(
                x=historical_data.index,
                y=historical_data['bollinger_upper'],
                name="Upper Bollinger Band",
                line=dict(color='rgba(99, 102, 241, 0.3)', width=1),
                showlegend=True
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=historical_data.index,
                y=historical_data['sma20'],
                name="SMA 20",
                line=dict(color='rgba(99, 102, 241, 0.8)', width=1),
                showlegend=True
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=historical_data.index,
                y=historical_data['bollinger_lower'],
                name="Lower Bollinger Band",
                line=dict(color='rgba(99, 102, 241, 0.3)', width=1),
                fill='tonexty',
                fillcolor='rgba(99, 102, 241, 0.05)',
                showlegend=True
            ),
            row=1, col=1
        )
    
    # Add MACD if available
    if all(col in historical_data.columns for col in ['macd', 'macd_signal']):
        # Add MACD line
        fig.add_trace(
            go.Scatter(
                x=historical_data.index,
                y=historical_data['macd'],
                name="MACD",
                line=dict(color='#3B82F6', width=1.5)
            ),
            row=3, col=1
        )
        
        # Add MACD signal line
        fig.add_trace(
            go.Scatter(
                x=historical_data.index,
                y=historical_data['macd_signal'],
                name="MACD Signal",
                line=dict(color='#F59E0B', width=1.5)
            ),
            row=3, col=1
        )
        
        # Add MACD histogram
        if 'macd_histogram' in historical_data.columns:
            colors = ['#10B981' if val >= 0 else '#EF4444' for val in historical_data['macd_histogram']]
            
            fig.add_trace(
                go.Bar(
                    x=historical_data.index,
                    y=historical_data['macd_histogram'],
                    name="MACD Histogram",
                    marker_color=colors,
                    opacity=0.8
                ),
                row=3, col=1
            )
    
    # Add current price line
    fig.add_hline(
        y=current_price,
        line_width=1,
        line_dash="dash",
        line_color="black",
        annotation_text=f"Current: ${current_price:.2f}",
        annotation_position="right",
        row=1, col=1
    )
    
    # Add support and resistance levels from price_data
    if not price_data.empty:
        for _, row in price_data.iterrows():
            if row['type'].lower() == 'support':
                fig.add_hline(
                    y=row['price'],
                    line_width=1,
                    line_dash="dot",
                    line_color="#10B981",
                    annotation_text=f"Support: ${row['price']:.2f} ({row['confidence']}%)",
                    annotation_position="left",
                    row=1, col=1
                )
            elif row['type'].lower() == 'resistance':
                fig.add_hline(
                    y=row['price'],
                    line_width=1,
                    line_dash="dot",
                    line_color="#EF4444",
                    annotation_text=f"Resistance: ${row['price']:.2f} ({row['confidence']}%)",
                    annotation_position="left",
                    row=1, col=1
                )
    
    # Update layout
    fig.update_layout(
        title=f"{coin_symbol.upper()} Technical Analysis",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        legend_title="Indicators",
        height=800,
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    # Update y-axis labels
    fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    fig.update_yaxes(title_text="RSI", row=3, col=1)
    
    # Update x-axis
    fig.update_xaxes(
        rangeslider_visible=False,
        rangebreaks=[
            dict(bounds=["sat", "mon"])  # hide weekends
        ]
    )
    
    # Add hover data
    fig.update_layout(hovermode="x unified")
    
    return fig

def display_volume_analysis(historical_data: pd.DataFrame, symbol: str):
    """Display volume analysis with trend detection and anomaly highlighting."""
    if historical_data.empty:
        st.warning("No historical data available for volume analysis.")
        return
    
    # Create a copy of the data for analysis
    volume_data = historical_data.copy()
    
    # Calculate volume metrics
    volume_data['volume_sma20'] = volume_data['volume'].rolling(window=20).mean()
    volume_data['volume_std20'] = volume_data['volume'].rolling(window=20).std()
    
    # Detect volume spikes (more than 2 standard deviations above the mean)
    volume_data['volume_spike'] = volume_data['volume'] > (volume_data['volume_sma20'] + 2 * volume_data['volume_std20'])
    
    # Calculate volume trend (ratio of current volume to 20-day SMA)
    volume_data['volume_trend'] = volume_data['volume'] / volume_data['volume_sma20']
    
    # Calculate daily volume change
    volume_data['volume_change'] = volume_data['volume'].pct_change() * 100
    
    # Create subplots
    fig = make_subplots(
        rows=2, 
        cols=1, 
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.7, 0.3],
        subplot_titles=(
            f"{symbol.upper()} Volume Analysis", 
            "Volume Change %"
        )
    )
    
    # Add volume bars
    colors = ['#10B981' if row['close'] >= row['open'] else '#EF4444' for _, row in volume_data.iterrows()]
    
    # Highlight volume spikes with different color
    for i, is_spike in enumerate(volume_data['volume_spike']):
        if is_spike:
            colors[i] = '#8B5CF6'  # Purple for spikes
    
    fig.add_trace(
        go.Bar(
            x=volume_data.index,
            y=volume_data['volume'],
            name="Volume",
            marker_color=colors,
            opacity=0.8
        ),
        row=1, col=1
    )
    
    # Add volume SMA
    fig.add_trace(
        go.Scatter(
            x=volume_data.index,
            y=volume_data['volume_sma20'],
            name="20-day SMA",
            line=dict(color='#3B82F6', width=2)
        ),
        row=1, col=1
    )
    
    # Add upper threshold for spike detection
    fig.add_trace(
        go.Scatter(
            x=volume_data.index,
            y=volume_data['volume_sma20'] + 2 * volume_data['volume_std20'],
            name="Spike Threshold",
            line=dict(color='#8B5CF6', width=1, dash='dot')
        ),
        row=1, col=1
    )
    
    # Add volume change percentage
    colors_change = ['#10B981' if val >= 0 else '#EF4444' for val in volume_data['volume_change']]
    
    fig.add_trace(
        go.Bar(
            x=volume_data.index,
            y=volume_data['volume_change'],
            name="Volume Change %",
            marker_color=colors_change,
            opacity=0.8
        ),
        row=2, col=1
    )
    
    # Add zero line for volume change
    fig.add_hline(
        y=0,
        line_width=1,
        line_dash="solid",
        line_color="black",
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        height=600,
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    # Update y-axis labels
    fig.update_yaxes(title_text="Volume", row=1, col=1)
    fig.update_yaxes(title_text="Change %", row=2, col=1)
    
    # Add hover data
    fig.update_layout(hovermode="x unified")
    
    # Show the figure
    import streamlit as st
    st.plotly_chart(fig, use_container_width=True)
    
    # Display volume statistics
    col1, col2, col3 = st.columns(3)
    
    # Calculate statistics
    avg_volume = volume_data['volume'].mean()
    max_volume = volume_data['volume'].max()
    max_volume_date = volume_data.loc[volume_data['volume'].idxmax()].name.strftime('%Y-%m-%d')
    spike_count = volume_data['volume_spike'].sum()
    
    # Recent volume trend
    recent_trend = volume_data['volume_trend'].iloc[-5:].mean()
    if recent_trend > 1.5:
        trend_text = "Strongly Increasing"
        trend_color = "#10B981"
    elif recent_trend > 1.1:
        trend_text = "Increasing"
        trend_color = "#10B981"
    elif recent_trend < 0.7:
        trend_text = "Strongly Decreasing"
        trend_color = "#EF4444"
    elif recent_trend < 0.9:
        trend_text = "Decreasing"
        trend_color = "#EF4444"
    else:
        trend_text = "Stable"
        trend_color = "#F59E0B"
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Average Daily Volume</div>
            <div class="metric-value">{avg_volume:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Volume Trend (5-day)</div>
            <div class="metric-value" style="color: {trend_color};">{trend_text}</div>
            <div class="metric-change-neutral">{recent_trend:.2f}x average</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Volume Spikes</div>
            <div class="metric-value">{spike_count}</div>
            <div class="metric-change-neutral">in the analyzed period</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display volume anomalies
    if spike_count > 0:
        st.markdown("### Volume Anomalies")
        
        # Get dates with volume spikes
        spike_dates = volume_data[volume_data['volume_spike']].index
        
        # Create a table with spike information
        spike_data = []
        for date in spike_dates:
            row = volume_data.loc[date]
            spike_data.append({
                "Date": date.strftime('%Y-%m-%d'),
                "Volume": f"{row['volume']:,.0f}",
                "vs Average": f"{row['volume'] / row['volume_sma20']:.2f}x",
                "Price Change": f"{(row['close'] - row['open']) / row['open'] * 100:.2f}%",
                "Close Price": f"${row['close']:.2f}"
            })
        
        # Convert to DataFrame for display
        spike_df = pd.DataFrame(spike_data)
        
        # Display as a styled table
        st.dataframe(
            spike_df,
            use_container_width=True,
            hide_index=True
        )
