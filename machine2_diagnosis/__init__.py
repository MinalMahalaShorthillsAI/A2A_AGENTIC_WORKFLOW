"""
Diagnosis Agent Package  
Contains ADK LlmAgent for system diagnosis, root cause analysis, and A2A communication.
"""

__version__ = "1.0.0"
__author__ = "BARCO Agent System"

# Main exports for package users
from .agent_gemini import diagnosis_agent, diagnosis_a2a_app
from .a2a_client import DiagnosisAgentClient

__all__ = [
    "diagnosis_agent",
    "diagnosis_a2a_app", 
    "DiagnosisAgentClient"
]
