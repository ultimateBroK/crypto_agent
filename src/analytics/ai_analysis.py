"""
AI analysis functions for cryptocurrency data.
"""

import pandas as pd
import numpy as np
import re
import os
from typing import Dict, Any, List, Tuple, Optional
from dotenv import load_dotenv

def analyze_with_ai(
    symbol: str, 
    current_price: float,
    indicators: Dict[str, float], 
    tech_signal: str,
    timeframe: str
) -> Tuple[str, str, str, str, str]:
    """
    Generate AI analysis based on technical indicators and market data.
    This is a mock implementation - in a real app, this would call a large language model API.
    
    Returns:
    - recommendation (str): Buy, Sell, or Hold recommendation
    - rationale (str): Explanation for the recommendation
    - factors (str): Key market and technical factors
    - outlook (str): Market outlook
    - targets (str): Price targets
    """
    # For sample data, return different analysis based on symbol
    recommendation = get_sample_recommendation(symbol, tech_signal)
    
    # Generate detailed analysis based on the recommendation and indicators
    rationale = generate_rationale(symbol, recommendation, indicators, current_price, timeframe)
    factors = generate_factors(symbol, indicators)
    outlook = generate_outlook(symbol, recommendation, indicators)
    
    # Generate price targets based on current price
    targets = generate_price_targets(symbol, current_price, recommendation, indicators)
    
    return recommendation, rationale, factors, outlook, targets

def get_sample_recommendation(symbol: str, tech_signal: str) -> str:
    """Generate a sample recommendation based on symbol."""
    # Map to ensure consistent signals for certain coins
    symbol_recommendations = {
        "BTC": "Strong Buy" if tech_signal == "Strong Buy" else "Buy",
        "ETH": "Hold",
        "SOL": "Buy",
        "ADA": "Sell",
        "BNB": "Buy"
    }
    
    # Use the technical signal to influence the recommendation
    if tech_signal in ["Strong Buy", "Buy"]:
        bias = 0.7  # 70% chance to agree with technical signal
    elif tech_signal in ["Strong Sell", "Sell"]:
        bias = 0.7  # 70% chance to agree with technical signal
    else:
        bias = 0.5  # 50/50 chance
    
    # Use the mapped recommendation or randomly select one
    if symbol in symbol_recommendations:
        return symbol_recommendations[symbol]
    
    # For other symbols, randomly pick based on technical signal bias
    if np.random.rand() < bias:
        if tech_signal in ["Strong Buy", "Buy"]:
            return np.random.choice(["Strong Buy", "Buy"])
        elif tech_signal in ["Strong Sell", "Sell"]:
            return np.random.choice(["Strong Sell", "Sell"])
        else:
            return "Hold"
    else:
        # Contrarian view
        if tech_signal in ["Strong Buy", "Buy"]:
            return np.random.choice(["Sell", "Hold"])
        elif tech_signal in ["Strong Sell", "Sell"]:
            return np.random.choice(["Buy", "Hold"])
        else:
            return np.random.choice(["Buy", "Sell"])

def generate_rationale(symbol: str, recommendation: str, indicators: Dict[str, float], 
                     current_price: float, timeframe: str) -> str:
    """Generate trading rationale based on the recommendation."""
    rsi = indicators.get('rsi', 50)
    macd = indicators.get('macd', 0)
    macd_signal = indicators.get('macd_signal', 0)
    ema50 = indicators.get('ema50', current_price * 0.95)
    ema200 = indicators.get('ema200', current_price * 0.9)
    
    if "buy" in recommendation.lower():
        rationale = f"""
        The AI analysis for {symbol} indicates a buying opportunity based on multiple factors:
        
        • The price is showing bullish momentum with key technical indicators aligned for upward movement.
        • RSI at {rsi:.1f} {' is in oversold territory and' if rsi < 30 else ' shows positive momentum and'} suggests potential for continued uptrend.
        • MACD {' is above signal line' if macd > macd_signal else ''}, indicating strength in the current trend.
        • Price is trading {'above' if current_price > ema50 else 'near'} the EMA50, signaling medium-term bullish sentiment.
        • {'Golden cross pattern detected with EMA50 crossing above EMA200, a strong bullish indicator.' if ema50 > ema200 else ''}
        • The coin shows resilience at current levels with solid support.
        • Volume analysis shows {'increasing buying interest' if np.random.rand() > 0.5 else 'accumulation patterns'}.
        """
    elif "sell" in recommendation.lower():
        rationale = f"""
        The AI analysis for {symbol} indicates a selling opportunity based on the following factors:
        
        • The price is showing bearish momentum with key technical indicators aligned for downward movement.
        • RSI at {rsi:.1f} {' is in overbought territory and' if rsi > 70 else ' shows negative momentum and'} suggests potential for continued downtrend.
        • MACD {' is below signal line' if macd < macd_signal else ''}, indicating weakness in the current trend.
        • Price is trading {'below' if current_price < ema50 else 'at risk of falling below'} the EMA50, signaling medium-term bearish sentiment.
        • {'Death cross pattern detected with EMA50 crossing below EMA200, a strong bearish indicator.' if ema50 < ema200 else ''}
        • The coin shows weakness at current levels with resistance overhead.
        • Volume analysis shows {'increasing selling pressure' if np.random.rand() > 0.5 else 'distribution patterns'}.
        """
    else:  # Hold
        rationale = f"""
        The AI analysis for {symbol} indicates a neutral position is appropriate based on these factors:
        
        • The price is showing mixed signals with technical indicators not clearly aligned in either direction.
        • RSI at {rsi:.1f} is in neutral territory, suggesting a balanced market.
        • MACD lacks clear directional momentum, with minimal divergence from the signal line.
        • Price is consolidating {'above' if current_price > ema50 else 'below'} the EMA50, without strong directional bias.
        • The coin is currently in a ranging pattern, with no clear breakout imminent.
        • Volume analysis shows average trading activity without significant accumulation or distribution.
        • Wait for stronger signals before entering new positions.
        """
    
    # Add timeframe context
    timeframe_text = ""
    if timeframe == "1d":
        timeframe_text = "This is a short-term trading recommendation focused on intraday price action."
    elif timeframe == "1w":
        timeframe_text = "This is a swing trading recommendation appropriate for a 1-7 day timeframe."
    elif timeframe == "1m":
        timeframe_text = "This is a medium-term trading recommendation with a 2-4 week outlook."
    elif timeframe in ["3m", "6m", "1y"]:
        timeframe_text = "This is a longer-term position recommendation with a multi-month outlook."
    
    rationale += f"\n\n{timeframe_text}"
    
    return rationale

def generate_factors(symbol: str, indicators: Dict[str, float]) -> str:
    """Generate key market and technical factors impacting the price."""
    rsi = indicators.get('rsi', 50)
    price = indicators.get('price', 100)
    bb_width = indicators.get('bb_width', 0.1)
    momentum_1d = indicators.get('momentum_1d', 0)
    momentum_1w = indicators.get('momentum_1w', 0)
    
    # Create a list of market factors
    market_factors = [
        f"Market sentiment for {symbol} is {'positive' if np.random.rand() > 0.5 else 'cautiously optimistic'}.",
        f"Trading volume is {np.random.choice(['above average', 'increasing', 'steady', 'below average'])}.",
        f"Institutional interest {'appears to be growing' if np.random.rand() > 0.5 else 'remains stable'}.",
        f"Overall crypto market correlation is {np.random.choice(['high', 'moderate', 'low'])}, affecting {symbol}'s price action.",
        f"Recent {'regulatory developments' if np.random.rand() > 0.7 else 'network upgrades'} may impact price in the {'short-term' if np.random.rand() > 0.5 else 'long-term'}."
    ]
    
    # Create a list of technical factors
    technical_factors = [
        f"RSI at {rsi:.1f} is {'oversold' if rsi < 30 else 'overbought' if rsi > 70 else 'neutral'}.",
        f"Price volatility is {np.random.choice(['high', 'moderate', 'low'])}, with a BB width of {bb_width:.4f}.",
        f"Daily momentum is {momentum_1d:.2f}%, indicating {'strong' if abs(momentum_1d) > 5 else 'moderate' if abs(momentum_1d) > 2 else 'weak'} {'upward' if momentum_1d > 0 else 'downward'} pressure.",
        f"Weekly momentum is {momentum_1w:.2f}%, showing a {'bullish' if momentum_1w > 0 else 'bearish'} trend.",
        f"Key {'support' if np.random.rand() > 0.5 else 'resistance'} levels are being tested."
    ]
    
    # Combine and shuffle factors
    all_factors = market_factors + technical_factors
    np.random.shuffle(all_factors)
    
    return "\n".join(all_factors)

def generate_outlook(symbol: str, recommendation: str, indicators: Dict[str, float]) -> str:
    """Generate market outlook based on the recommendation."""
    price = indicators.get('price', 100)
    
    if "buy" in recommendation.lower():
        outlook = f"""
        The short-term outlook for {symbol} appears positive:
        
        • Price action suggests potential for upward momentum in the coming sessions.
        • Key resistance levels may be tested and possibly broken if buying pressure continues.
        • The coin is likely to outperform the broader market if current conditions persist.
        • Watch for increased volume to confirm the bullish momentum.
        • A shift in overall crypto market sentiment could accelerate this positive trend.
        """
    elif "sell" in recommendation.lower():
        outlook = f"""
        The short-term outlook for {symbol} appears negative:
        
        • Price action suggests potential for downward momentum in the coming sessions.
        • Key support levels may be tested and possibly broken if selling pressure continues.
        • The coin may underperform the broader market under current conditions.
        • Watch for increased volume to confirm the bearish momentum.
        • A broader crypto market downturn could accelerate this negative trend.
        """
    else:  # Hold
        outlook = f"""
        The short-term outlook for {symbol} is neutral:
        
        • Price action suggests a period of consolidation or ranging behavior.
        • The coin is likely to move in line with broader market trends in the near term.
        • Watch for a breakout above resistance or below support for new directional cues.
        • Volume patterns suggest neither strong accumulation nor distribution at current levels.
        • Monitor overall market sentiment for potential shifts that could impact direction.
        """
    
    return outlook

def generate_price_targets(symbol: str, current_price: float, recommendation: str, indicators: Dict[str, float]) -> str:
    """Generate price targets based on current price and recommendation."""
    # Calculate support and resistance levels
    supports = []
    resistances = []
    
    # Calculate based on technical levels
    if indicators:
        # Use Fibonacci retracement/extension levels
        daily_range = indicators.get('high', current_price * 1.05) - indicators.get('low', current_price * 0.95)
        
        # Support levels
        supports.extend([
            {
                "price": round(current_price * 0.95, 4),
                "confidence": 80,
                "description": "Short-term support level"
            },
            {
                "price": round(current_price * 0.90, 4),
                "confidence": 60,
                "description": "Medium-term support level"
            },
            {
                "price": round(current_price * 0.85, 4),
                "confidence": 40,
                "description": "Longer-term support level"
            }
        ])
        
        # Resistance levels
        resistances.extend([
            {
                "price": round(current_price * 1.05, 4),
                "confidence": 75,
                "description": "Short-term resistance level"
            },
            {
                "price": round(current_price * 1.10, 4),
                "confidence": 55,
                "description": "Medium-term resistance level"
            },
            {
                "price": round(current_price * 1.15, 4),
                "confidence": 35,
                "description": "Longer-term resistance level"
            }
        ])
        
        # Add EMA-based levels if available
        if 'ema50' in indicators:
            ema50 = indicators['ema50']
            if ema50 < current_price:
                supports.append({
                    "price": round(ema50, 4),
                    "confidence": 65,
                    "description": "EMA50 support level"
                })
            else:
                resistances.append({
                    "price": round(ema50, 4),
                    "confidence": 70,
                    "description": "EMA50 resistance level"
                })
        
        if 'ema200' in indicators:
            ema200 = indicators['ema200']
            if ema200 < current_price:
                supports.append({
                    "price": round(ema200, 4),
                    "confidence": 75,
                    "description": "EMA200 support level (major)"
                })
            else:
                resistances.append({
                    "price": round(ema200, 4),
                    "confidence": 85,
                    "description": "EMA200 resistance level (major)"
                })
        
        # Add Bollinger Bands if available
        if 'bollinger_upper' in indicators and 'bollinger_lower' in indicators:
            upper = indicators['bollinger_upper']
            lower = indicators['bollinger_lower']
            
            if upper > current_price:
                resistances.append({
                    "price": round(upper, 4),
                    "confidence": 60,
                    "description": "Bollinger upper band resistance"
                })
            
            if lower < current_price:
                supports.append({
                    "price": round(lower, 4),
                    "confidence": 60,
                    "description": "Bollinger lower band support"
                })
    
    # Format the price targets string
    if "buy" in recommendation.lower():
        targets_text = f"""
        **Price Targets for {symbol}**
        
        • **Support Levels:**
          - Strong support at ${supports[0]['price']} (confidence: {supports[0]['confidence']}%)
          - Additional support at ${supports[1]['price']} (confidence: {supports[1]['confidence']}%)
          - Major support zone: ${supports[2]['price']} (confidence: {supports[2]['confidence']}%)
        
        • **Resistance Levels:**
          - Initial resistance at ${resistances[0]['price']} (confidence: {resistances[0]['confidence']}%)
          - Key resistance level at ${resistances[1]['price']} (confidence: {resistances[1]['confidence']}%)
          - Long-term target at ${resistances[2]['price']} (confidence: {resistances[2]['confidence']}%)
        
        • **Entry Strategy:**
          - Consider buying at current levels with stops below ${supports[0]['price']}
          - Alternative entry on pullbacks to ${supports[0]['price']} or ${supports[1]['price']}
        
        • **Exit Strategy:**
          - Take partial profits at ${resistances[0]['price']} and ${resistances[1]['price']}
          - Consider trailing stops as price advances
        """
    elif "sell" in recommendation.lower():
        targets_text = f"""
        **Price Targets for {symbol}**
        
        • **Resistance Levels:**
          - Immediate resistance at ${resistances[0]['price']} (confidence: {resistances[0]['confidence']}%)
          - Strong resistance at ${resistances[1]['price']} (confidence: {resistances[1]['confidence']}%)
          - Major resistance zone: ${resistances[2]['price']} (confidence: {resistances[2]['confidence']}%)
        
        • **Support Levels:**
          - Initial support at ${supports[0]['price']} (confidence: {supports[0]['confidence']}%)
          - Key support level at ${supports[1]['price']} (confidence: {supports[1]['confidence']}%)
          - Critical support at ${supports[2]['price']} (confidence: {supports[2]['confidence']}%)
        
        • **Entry Strategy:**
          - Consider selling at current levels with stops above ${resistances[0]['price']}
          - Alternative entry on rallies to ${resistances[0]['price']} or ${resistances[1]['price']}
        
        • **Exit Strategy:**
          - Take partial profits at ${supports[0]['price']} and ${supports[1]['price']}
          - Consider closing positions if price breaks above ${resistances[1]['price']}
        """
    else:  # Hold
        targets_text = f"""
        **Price Targets for {symbol}**
        
        • **Range Boundaries:**
          - Upper range bound: ${resistances[0]['price']} to ${resistances[1]['price']}
          - Lower range bound: ${supports[0]['price']} to ${supports[1]['price']}
        
        • **Breakout Levels:**
          - Bullish breakout above ${resistances[1]['price']} (confidence: {resistances[1]['confidence']}%)
          - Bearish breakdown below ${supports[1]['price']} (confidence: {supports[1]['confidence']}%)
        
        • **Trading Strategy:**
          - Consider range-trading between support and resistance levels
          - Avoid new positions until a clear breakout/breakdown occurs
        """
    
    return targets_text

def extract_signal(recommendation: str) -> str:
    """Extract the core signal (buy/sell/hold) from a recommendation."""
    if not recommendation:
        return "hold"
        
    recommendation = recommendation.lower()
    
    if "buy" in recommendation or "bullish" in recommendation:
        return "buy"
    elif "sell" in recommendation or "bearish" in recommendation:
        return "sell"
    else:
        return "hold"

def enhance_ai_analysis(rec: str, rationale: str, factors: str, outlook: str, targets: str) -> Tuple[str, str, str, str, str]:
    """Enhance AI analysis results for more polished presentation."""
    # Clean up any empty fields or None values
    if rec is None or not rec or rec.strip() == "":
        rec = "Hold"
    
    if rationale is None or not rationale or rationale.strip() == "":
        rationale = "Analysis not available."
    
    if factors is None or not factors or factors.strip() == "":
        factors = "No factor data available."
    
    if outlook is None or not outlook or outlook.strip() == "":
        outlook = "Outlook data not available."
    
    if targets is None or not targets or targets.strip() == "":
        targets = "No price targets available."
    
    # Ensure consistent formatting
    rec = str(rec).strip()
    rationale = str(rationale).strip()
    factors = str(factors).strip()
    outlook = str(outlook).strip()
    targets = str(targets).strip()
    
    return rec, rationale, factors, outlook, targets

def setup_ai_agent(api_key=None):
    """
    Initialize and configure the AI agent for cryptocurrency analysis.
    
    Args:
        api_key: API key for the AI service (optional)
        
    Returns:
        Agent or dict: Configuration for the AI agent
    """
    # Load environment variables for API keys if needed
    load_dotenv()
    
    # If no API key is provided, try to get it from environment variables
    if not api_key:
        api_key = os.getenv('OPENAI_API_KEY', None)
    
    # Create a configuration dictionary for the AI agent
    # This is a mock implementation - in a real app, this would initialize an actual AI agent
    ai_config = {
        'model_type': 'local',  # Could be 'openai', 'local', etc.
        'temperature': 0.7,
        'max_tokens': 1000,
        'api_key': api_key
    }
    
    return ai_config

def generate_analysis_prompt(
    symbol: str,
    stats: Dict[str, Any],
    indicators: Dict[str, float],
    historical_data: pd.DataFrame
) -> str:
    """
    Generate a prompt for the AI model to analyze cryptocurrency data.
    
    Args:
        symbol: Cryptocurrency symbol
        timeframe: Analysis timeframe (e.g., '1d', '1w', '1m')
        current_price: Current price of the cryptocurrency
        indicators: Dictionary of technical indicators
        historical_data: DataFrame containing historical price data
        
    Returns:
        str: Formatted prompt for AI analysis
    """
    # Extract current price and other stats
    current_price = stats.get('price', 0.0)
    market_cap = stats.get('market_cap', 0.0)
    volume_24h = stats.get('volume_24h', 0.0)
    
    # Create a basic prompt template
    prompt = f"""
    Analyze the cryptocurrency {symbol} with the following data:
    
    Current Price: ${current_price:.2f}
    Market Cap: ${market_cap:.2f}
    24h Volume: ${volume_24h:.2f}
    
    Technical Indicators:
    """
    
    # Add technical indicators to the prompt
    for indicator, value in indicators.items():
        if isinstance(value, float):
            prompt += f"- {indicator}: {value:.4f}\n"
        else:
            prompt += f"- {indicator}: {value}\n"
    
    # Add recent price action summary
    if not historical_data.empty:
        recent_change = ((current_price - historical_data['close'].iloc[0]) / 
                         historical_data['close'].iloc[0] * 100)
        
        prompt += f"\nRecent Performance:\n"
        prompt += f"- Price change over period: {recent_change:.2f}%\n"
        prompt += f"- Highest price: ${historical_data['high'].max():.2f}\n"
        prompt += f"- Lowest price: ${historical_data['low'].min():.2f}\n"
    
    # Add analysis request
    prompt += """
    Based on this information, provide:
    1. A trading recommendation (Buy, Sell, or Hold)
    2. Rationale for the recommendation
    3. Key market and technical factors
    4. Market outlook
    5. Price targets (support and resistance levels)
    """
    
    return prompt

def run_ai_analysis(
    agent: Any,
    prompt: str,
    symbol: str = "BTC",
    current_price: float = 0.0,
    indicators: Dict[str, float] = None,
    tech_signal: str = "HOLD",
    timeframe: str = "1d"
) -> Tuple[str, str, str, str, str]:
    """
    Run AI analysis on cryptocurrency data.
    
    This function either calls an external AI API if configured,
    or falls back to the local mock implementation.
    
    Args:
        symbol: Cryptocurrency symbol
        current_price: Current price
        indicators: Technical indicators
        tech_signal: Technical signal (Buy, Sell, Hold)
        timeframe: Analysis timeframe
        historical_data: Optional historical price data
        ai_config: Optional AI configuration
        
    Returns:
        Tuple containing:
        - recommendation (str): Buy, Sell, or Hold recommendation
        - rationale (str): Explanation for the recommendation
        - factors (str): Key market and technical factors
        - outlook (str): Market outlook
        - targets (str): Price targets
    """
    # Default values for indicators if not provided
    if indicators is None:
        indicators = {}
    
    # If we have a valid AI agent and it has an API key, we could call an external AI API
    if agent and isinstance(agent, dict) and agent.get('api_key'):
        # This would be where you'd implement the call to an external AI API
        # For now, we'll just use our mock implementation
        pass
    
    # Extract current price from the prompt if not provided directly
    if current_price <= 0 and "Current Price: $" in prompt:
        try:
            price_line = [line for line in prompt.split('\n') if "Current Price: $" in line][0]
            current_price = float(price_line.split('$')[1].strip())
        except (IndexError, ValueError):
            current_price = 1000.0  # Default fallback for BTC
    
    # Fall back to the local mock implementation
    recommendation, rationale, factors, outlook, targets = analyze_with_ai(
        symbol, current_price, indicators, tech_signal, timeframe
    )
    
    # Enhance the analysis results for better presentation
    recommendation, rationale, factors, outlook, targets = enhance_ai_analysis(
        recommendation, rationale, factors, outlook, targets
    )
    
    return recommendation, rationale, factors, outlook, targets

def extract_price_targets(targets_text: str, current_price: float) -> pd.DataFrame:
    """Extract price targets from text into structured DataFrame."""
    try:
        if not targets_text or targets_text is None or "no data" in str(targets_text).lower():
            return pd.DataFrame()
        
        # Initialize lists for data
        data = []
        
        # Regular expressions to find price patterns
        price_pattern = r'\$([0-9,.]+)'
        confidence_pattern = r'confidence: (\d+)%'
        
        # Find all prices in the text
        prices = re.findall(price_pattern, str(targets_text))
        if not prices:
            # If no prices found, return empty DataFrame
            return pd.DataFrame()
            
        # Convert prices to float, handling potential format issues
        cleaned_prices = []
        for price in prices:
            try:
                cleaned_prices.append(float(price.replace(',', '')))
            except (ValueError, AttributeError):
                continue
        
        prices = cleaned_prices
        if not prices:
            # If no valid prices, return empty DataFrame
            return pd.DataFrame()
        
        # Find all confidence levels
        confidences = re.findall(confidence_pattern, str(targets_text))
        cleaned_confidences = []
        for conf in confidences:
            try:
                cleaned_confidences.append(int(conf))
            except (ValueError, AttributeError):
                continue
        
        confidences = cleaned_confidences
        
        # If we don't have enough confidence values, fill with defaults
        while len(confidences) < len(prices):
            confidences.append(70)  # Default confidence
        
        # Determine if each price is support or resistance
        for i, price in enumerate(prices):
            confidence = confidences[i] if i < len(confidences) else 70
            
            try:
                if price < current_price:
                    price_type = "Support"
                    # Generate description based on distance from current price
                    difference = abs(current_price - price) / current_price * 100
                    if difference < 3:
                        description = "Near-term support"
                    elif difference < 7:
                        description = "Medium-term support"
                    else:
                        description = "Long-term support"
                else:
                    price_type = "Resistance"
                    # Generate description based on distance from current price
                    difference = abs(price - current_price) / current_price * 100
                    if difference < 3:
                        description = "Near-term resistance"
                    elif difference < 7:
                        description = "Medium-term resistance"
                    else:
                        description = "Long-term target"
                
                data.append({
                    "price": price,
                    "confidence": confidence,
                    "type": price_type,
                    "description": description
                })
            except Exception as e:
                import logging
                logging.error(f"Error processing price target: {e}")
                continue
        
        # If we couldn't extract any valid data, return empty DataFrame
        if not data:
            return pd.DataFrame()
            
        # Convert to DataFrame and sort by price
        df = pd.DataFrame(data)
        df = df.sort_values("price", ascending=False)
        
        return df
    except Exception as e:
        import logging
        logging.error(f"Error extracting price targets: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error
