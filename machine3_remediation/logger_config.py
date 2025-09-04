"""
Logger configuration for Remediation Agent
"""
from loguru import logger
import sys
import os

# Configure logger for remediation agent
logger.remove()  # Remove default handler

# Console handler with custom format
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>remediation_agent</cyan> | <level>{message}</level>", # Changed agent name
    level="INFO"
)

# File handler for persistent logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logger.add(
    f"{log_dir}/remediation_agent.log", # Changed log file name
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | remediation_agent | {message}", # Changed agent name
    level="DEBUG",
    rotation="10 MB",
    retention="7 days"
)

logger.info("Remediation Agent logger configured") # Changed log message
