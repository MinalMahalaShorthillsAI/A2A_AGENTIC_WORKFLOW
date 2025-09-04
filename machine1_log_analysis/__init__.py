"""
Log Analysis Agent Package
Contains ADK LlmAgent for log analysis, anomaly detection, and A2A communication.
"""

__version__ = "1.0.0"
__author__ = "BARCO Agent System"

# Main exports for package users
from .agent_gemini import log_analysis_agent, log_analysis_a2a_app

__all__ = [
    "log_analysis_agent", 
    "log_analysis_a2a_app"
]
