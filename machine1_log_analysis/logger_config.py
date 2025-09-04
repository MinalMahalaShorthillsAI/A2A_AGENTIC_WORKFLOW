"""
Logger configuration for Log Analysis Agent
"""
from loguru import logger
import sys
import os

# Configure logger for log analysis agent
logger.remove()  # Remove default handler

# Console handler with custom format
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>log_agent</cyan> | <level>{message}</level>",
    level="INFO"
)

# File handler for persistent logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logger.add(
    f"{log_dir}/log_analysis_agent.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | log_agent | {message}",
    level="DEBUG",
    rotation="10 MB",
    retention="7 days"
)

logger.info("Log Analysis Agent logger configured")
