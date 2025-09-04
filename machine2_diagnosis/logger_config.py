"""
Logger configuration for Diagnosis Agent
"""
from loguru import logger
import sys
import os

# Configure logger for diagnosis agent
logger.remove()  # Remove default handler

# Console handler with custom format
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>DIAGNOSIS_AGENT</cyan> | <level>{message}</level>",
    level="INFO"
)

# File handler for persistent logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logger.add(
    f"{log_dir}/diagnosis_agent.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | DIAGNOSIS_AGENT | {message}",
    level="DEBUG",
    rotation="10 MB",
    retention="7 days"
)

logger.info("Diagnosis Agent logger initialized")
