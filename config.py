"""
Centralized Configuration for BARCO Agent-to-Agent System
All IP addresses and ports managed through environment variables
"""

import os

# Machine 1 (Log Analysis Agent) Configuration
MACHINE1_IP = os.getenv("MACHINE1_IP", "127.0.0.1")             # Machine 1 IP >
MACHINE1_PORT = int(os.getenv("MACHINE1_PORT", "8000"))             # Use 8000 to >

# Machine 2 (Diagnosis Agent) Configuration  
MACHINE2_IP = os.getenv("MACHINE2_IP", "127.0.0.1")               # Machine 2>
MACHINE2_PORT = int(os.getenv("MACHINE2_PORT", "8001"))

# Machine 3 (Remediation Agent) Configuration
MACHINE3_IP = os.getenv("MACHINE3_IP", "127.0.0.1")
MACHINE3_PORT = int(os.getenv("MACHINE3_PORT", "8003"))

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Utility functions removed - not used in current implementation
