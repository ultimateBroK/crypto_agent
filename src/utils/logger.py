"""
Logging configuration for the Crypto Analysis Pro Dashboard.
"""

import logging

# --- Setup logging ---
def setup_logger():
    """Configure and return a logger instance."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger("crypto_agent")

# Create a global logger instance
logger = setup_logger()
