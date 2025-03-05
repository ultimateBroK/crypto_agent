"""
Trading strategy UI components for the Crypto Analysis Pro Dashboard.
"""

import pandas as pd
from typing import Dict, Any, List

def generate_trading_strategy(tech_signal: str, ai_signal: str, current_price: float, 
                             price_data: pd.DataFrame, stats: Dict[str, Any]) -> str:
    """Generate a trading strategy based on signals and price targets."""
    
    # Normalize signals
    tech_signal = tech_signal.lower()
    ai_signal = ai_signal.lower()
    
    # Determine overall signal (weighted combination)
    if tech_signal == ai_signal:
        overall_signal = tech_signal
        confidence = "high"
    elif tech_signal in ["buy", "strong buy"] and ai_signal in ["hold", "neutral"]:
        overall_signal = "cautious buy"
        confidence = "moderate"
    elif tech_signal in ["sell", "strong sell"] and ai_signal in ["hold", "neutral"]:
        overall_signal = "cautious sell"
        confidence = "moderate"
    elif ai_signal in ["buy", "strong buy"] and tech_signal in ["hold", "neutral"]:
        overall_signal = "cautious buy"
        confidence = "moderate"
    elif ai_signal in ["sell", "strong sell"] and tech_signal in ["hold", "neutral"]:
        overall_signal = "cautious sell"
        confidence = "moderate"
    elif (tech_signal in ["buy", "strong buy"] and ai_signal in ["sell", "strong sell"]) or \
         (ai_signal in ["buy", "strong buy"] and tech_signal in ["sell", "strong sell"]):
        overall_signal = "conflicting signals"
        confidence = "low"
    else:
        overall_signal = "hold"
        confidence = "moderate"
    
    # Extract support and resistance levels
    support_levels = price_data[price_data['type'].str.lower() == 'support'].sort_values('price', ascending=False)
    resistance_levels = price_data[price_data['type'].str.lower() == 'resistance'].sort_values('price')
    
    # Find closest support and resistance
    closest_support = None
    closest_resistance = None
    
    if not support_levels.empty:
        # Get supports below current price
        supports_below = support_levels[support_levels['price'] < current_price]
        if not supports_below.empty:
            closest_support = supports_below.iloc[0]
    
    if not resistance_levels.empty:
        # Get resistances above current price
        resistances_above = resistance_levels[resistance_levels['price'] > current_price]
        if not resistances_above.empty:
            closest_resistance = resistances_above.iloc[0]
    
    # Calculate risk-reward ratio if both support and resistance are available
    risk_reward_ratio = None
    if closest_support is not None and closest_resistance is not None:
        potential_gain = closest_resistance['price'] - current_price
        potential_loss = current_price - closest_support['price']
        
        if potential_loss > 0:  # Avoid division by zero
            risk_reward_ratio = potential_gain / potential_loss
    
    # Generate strategy HTML
    strategy_html = """
    <div class="strategy-container">
        <div class="strategy-title">Trading Strategy Recommendation</div>
    """
    
    # Signal section
    signal_color = "#F59E0B"  # Default amber
    if overall_signal in ["buy", "strong buy", "cautious buy"]:
        signal_color = "#10B981"  # Green
    elif overall_signal in ["sell", "strong sell", "cautious sell"]:
        signal_color = "#EF4444"  # Red
    
    strategy_html += f"""
        <div class="strategy-section">
            <div class="strategy-section-title">Signal Summary</div>
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <div style="
                    color: white;
                    background-color: {signal_color};
                    padding: 0.5rem 1rem;
                    border-radius: 0.25rem;
                    font-weight: 600;
                    text-transform: uppercase;
                    margin-right: 1rem;
                ">
                    {overall_signal}
                </div>
                <div style="color: #6B7280; font-size: 0.875rem;">
                    Confidence: <span style="font-weight: 600;">{confidence.title()}</span>
                </div>
            </div>
    """
    
    # Add signal explanation
    strategy_html += """
            <div class="strategy-point">
                <div class="strategy-point-icon">•</div>
                <div class="strategy-point-text">
    """
    
    if overall_signal in ["buy", "strong buy"]:
        strategy_html += "Technical indicators and AI analysis both suggest a <strong>buying opportunity</strong>. Consider entering a position with proper risk management."
    elif overall_signal == "cautious buy":
        strategy_html += "Mixed signals with a <strong>bullish bias</strong>. Consider a smaller position size or wait for additional confirmation."
    elif overall_signal in ["sell", "strong sell"]:
        strategy_html += "Technical indicators and AI analysis both suggest a <strong>selling opportunity</strong>. Consider exiting positions or opening short positions with proper risk management."
    elif overall_signal == "cautious sell":
        strategy_html += "Mixed signals with a <strong>bearish bias</strong>. Consider reducing position size or wait for additional confirmation before selling."
    elif overall_signal == "hold":
        strategy_html += "Current signals suggest <strong>holding existing positions</strong>. Not an ideal time to enter or exit positions."
    elif overall_signal == "conflicting signals":
        strategy_html += "<strong>Conflicting signals</strong> between technical indicators and AI analysis. Consider waiting for clearer signals before taking action."
    
    strategy_html += """
                </div>
            </div>
        </div>
    """
    
    # Entry/Exit strategy section
    strategy_html += """
        <div class="strategy-section">
            <div class="strategy-section-title">Entry/Exit Strategy</div>
    """
    
    # Entry points
    if overall_signal in ["buy", "strong buy", "cautious buy"]:
        strategy_html += """
            <div class="strategy-point">
                <div class="strategy-point-icon">•</div>
                <div class="strategy-point-text">
                    <strong>Entry Points:</strong>
        """
        
        if closest_support is not None:
            strategy_html += f" Consider buying at current price (${current_price:.4f}) or on pullbacks to support at ${closest_support['price']:.4f}."
        else:
            strategy_html += f" Consider buying at current price (${current_price:.4f}) with appropriate stop loss."
        
        strategy_html += """
                </div>
            </div>
        """
    
    # Exit points
    if overall_signal in ["sell", "strong sell", "cautious sell"]:
        strategy_html += """
            <div class="strategy-point">
                <div class="strategy-point-icon">•</div>
                <div class="strategy-point-text">
                    <strong>Exit Points:</strong>
        """
        
        if closest_support is not None:
            strategy_html += f" Consider selling at current price (${current_price:.4f}). If holding, set stop loss below ${closest_support['price']:.4f}."
        else:
            strategy_html += f" Consider selling at current price (${current_price:.4f}) to protect capital."
        
        strategy_html += """
                </div>
            </div>
        """
    
    # Take profit levels
    if overall_signal in ["buy", "strong buy", "cautious buy", "hold"]:
        strategy_html += """
            <div class="strategy-point">
                <div class="strategy-point-icon">•</div>
                <div class="strategy-point-text">
                    <strong>Take Profit Levels:</strong>
        """
        
        if not resistance_levels.empty:
            # Get top 2 resistance levels
            top_resistances = resistance_levels.head(min(2, len(resistance_levels)))
            resistance_texts = []
            
            for _, res in top_resistances.iterrows():
                pct_gain = (res['price'] - current_price) / current_price * 100
                resistance_texts.append(f"${res['price']:.4f} ({pct_gain:.1f}%)")
            
            strategy_html += " " + " and ".join(resistance_texts)
        else:
            # Default take profit suggestion
            strategy_html += f" Consider taking profits at 5-10% above entry price."
        
        strategy_html += """
                </div>
            </div>
        """
    
    # Stop loss levels
    if overall_signal in ["buy", "strong buy", "cautious buy", "hold"]:
        strategy_html += """
            <div class="strategy-point">
                <div class="strategy-point-icon">•</div>
                <div class="strategy-point-text">
                    <strong>Stop Loss Levels:</strong>
        """
        
        if closest_support is not None:
            pct_loss = (current_price - closest_support['price']) / current_price * 100
            strategy_html += f" Set stop loss slightly below ${closest_support['price']:.4f} ({pct_loss:.1f}% from current price)."
        else:
            # Default stop loss suggestion
            strategy_html += f" Consider setting stop loss at 5-8% below entry price."
        
        strategy_html += """
                </div>
            </div>
        """
    
    strategy_html += """
        </div>
    """
    
    # Risk management section
    strategy_html += """
        <div class="strategy-section">
            <div class="strategy-section-title">Risk Management</div>
    """
    
    # Position sizing
    strategy_html += """
            <div class="strategy-point">
                <div class="strategy-point-icon">•</div>
                <div class="strategy-point-text">
                    <strong>Position Sizing:</strong>
    """
    
    if confidence == "high":
        strategy_html += " Consider standard position size (1-2% of portfolio)."
    elif confidence == "moderate":
        strategy_html += " Consider reduced position size (0.5-1% of portfolio)."
    else:  # low confidence
        strategy_html += " Consider minimal position size (0.25-0.5% of portfolio) or wait for clearer signals."
    
    strategy_html += """
                </div>
            </div>
    """
    
    # Risk-reward
    strategy_html += """
            <div class="strategy-point">
                <div class="strategy-point-icon">•</div>
                <div class="strategy-point-text">
                    <strong>Risk-Reward Ratio:</strong>
    """
    
    if risk_reward_ratio is not None:
        if risk_reward_ratio >= 3:
            strategy_html += f" Excellent risk-reward ratio of {risk_reward_ratio:.1f}:1."
        elif risk_reward_ratio >= 2:
            strategy_html += f" Good risk-reward ratio of {risk_reward_ratio:.1f}:1."
        elif risk_reward_ratio >= 1:
            strategy_html += f" Acceptable risk-reward ratio of {risk_reward_ratio:.1f}:1."
        else:
            strategy_html += f" Poor risk-reward ratio of {risk_reward_ratio:.1f}:1. Consider waiting for better setup."
    else:
        strategy_html += " Aim for a minimum risk-reward ratio of 2:1 for any trade."
    
    strategy_html += """
                </div>
            </div>
    """
    
    # Risk-reward visualization
    if risk_reward_ratio is not None:
        # Calculate fill percentage (capped at 100%)
        fill_percentage = min(risk_reward_ratio / 3 * 100, 100)
        
        # Determine color based on ratio
        if risk_reward_ratio >= 3:
            fill_color = "#10B981"  # Green
        elif risk_reward_ratio >= 2:
            fill_color = "#F59E0B"  # Amber
        elif risk_reward_ratio >= 1:
            fill_color = "#F59E0B"  # Amber
        else:
            fill_color = "#EF4444"  # Red
        
        strategy_html += f"""
            <div class="risk-reward-container">
                <div class="risk-reward-title">Risk-Reward Visualization</div>
                <div class="risk-reward-bar">
                    <div class="risk-reward-fill" style="width: {fill_percentage}%; background-color: {fill_color};"></div>
                </div>
                <div class="risk-reward-labels">
                    <div>1:1</div>
                    <div>2:1</div>
                    <div>3:1</div>
                </div>
            </div>
        """
    
    # Market conditions
    strategy_html += """
            <div class="strategy-point">
                <div class="strategy-point-icon">•</div>
                <div class="strategy-point-text">
                    <strong>Market Conditions:</strong>
    """
    
    # Get market mood
    mood = stats.get('mood', 'Neutral')
    
    if mood == "Bullish":
        strategy_html += " Overall market sentiment is <span class='mood-bullish'>Bullish</span>, favorable for long positions."
    elif mood == "Bearish":
        strategy_html += " Overall market sentiment is <span class='mood-bearish'>Bearish</span>, exercise caution with long positions."
    else:
        strategy_html += " Overall market sentiment is <span class='mood-neutral'>Neutral</span>, monitor for directional bias."
    
    strategy_html += """
                </div>
            </div>
        </div>
    """
    
    # Timeframe considerations
    strategy_html += """
        <div class="strategy-section">
            <div class="strategy-section-title">Timeframe Considerations</div>
            <div class="strategy-point">
                <div class="strategy-point-icon">•</div>
                <div class="strategy-point-text">
                    <strong>Short-term:</strong> This analysis is primarily focused on short to medium-term trading opportunities (days to weeks).
                </div>
            </div>
            <div class="strategy-point">
                <div class="strategy-point-icon">•</div>
                <div class="strategy-point-text">
                    <strong>Long-term:</strong> For long-term investing, consider fundamental factors beyond this technical analysis.
                </div>
            </div>
        </div>
    """
    
    # Disclaimer
    strategy_html += """
        <div style="font-size: 0.75rem; color: #6B7280; margin-top: 1rem; font-style: italic;">
            Disclaimer: This trading strategy is generated based on technical analysis and AI insights. 
            It should not be considered as financial advice. Always conduct your own research and consider 
            your risk tolerance before making investment decisions.
        </div>
    </div>
    """
    
    return strategy_html
