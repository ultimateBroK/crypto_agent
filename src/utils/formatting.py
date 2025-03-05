"""
Formatting utilities for the Crypto Analysis Pro Dashboard.
"""

def format_price(price: float) -> str:
    """Format price with appropriate decimal places based on magnitude."""
    if price >= 1000:
        return f"${price:,.2f}"
    elif price >= 1:
        return f"${price:.2f}"
    elif price >= 0.01:
        return f"${price:.4f}"
    elif price >= 0.0001:
        return f"${price:.6f}"
    else:
        return f"${price:.8f}"

def format_large_number(num: float, prefix: str = "") -> str:
    """Format large numbers with K, M, B, T suffixes."""
    if num is None:
        return "N/A"
    
    if num >= 1_000_000_000_000:
        return f"{prefix}{num / 1_000_000_000_000:.2f}T"
    elif num >= 1_000_000_000:
        return f"{prefix}{num / 1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"{prefix}{num / 1_000_000:.2f}M"
    elif num >= 1_000:
        return f"{prefix}{num / 1_000:.2f}K"
    else:
        return f"{prefix}{num:.2f}"

def format_percentage(pct: float) -> str:
    """Format percentage with appropriate sign and decimal places."""
    if pct > 0:
        return f"+{pct:.2f}%"
    else:
        return f"{pct:.2f}%"
