"""
A2A Server for Log Analysis Agent
Runs the A2A server (A2A setup handled in agent_gemini.py)
"""

import os
import sys
import uvicorn
import warnings

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import MACHINE1_IP, MACHINE1_PORT

# Suppress experimental ADK warnings to reduce noise
warnings.filterwarnings("ignore", category=UserWarning)

from agent_gemini import log_analysis_a2a_app
from logger_config import logger

def run_log_analysis_a2a_server():
    """Run the Log Analysis Agent A2A server"""
    # Bind to specific IP address from config
    host = MACHINE1_IP
    port = MACHINE1_PORT
    
    logger.info("Starting Log Analysis A2A Server...")
    logger.info(f"Host: {host}")
    logger.info(f"Port: {port}")
    logger.info(f"Agent Card URL: http://{host}:{port}/.well-known/agent-card.json")
    
    # Run the server with request logging enabled to see hits
    uvicorn.run(
        log_analysis_a2a_app, 
        host=host, 
        port=port,
        log_level="info",    # Show request logs
        access_log=True      # Enable access logging to see hits
    )

if __name__ == "__main__":
    run_log_analysis_a2a_server()
