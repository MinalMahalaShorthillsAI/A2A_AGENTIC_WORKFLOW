import os
import google.generativeai as genai
from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.models import Gemini
from pydantic import BaseModel, Field
from typing import Optional, Literal
from tools import remediation_tools, get_tool_call_counter, reset_tool_call_counter
from logger_config import logger
from starlette.responses import JSONResponse
from starlette.routing import Route
import sys
sys.path.append('..')
from config import MACHINE1_IP, MACHINE1_PORT, MACHINE3_IP, MACHINE3_PORT
from cost_tracker import get_cost_tracker, estimate_tokens

def setup_gemini_client():
    """Setup Gemini API client"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    
    genai.configure(api_key=api_key)
    logger.info("Gemini API client configured successfully")
    return api_key

def create_remediation_agent(): # Renamed function
    """Create and configure the Remediation Agent following ADK LlmAgent patterns"""
    try:
        api_key = setup_gemini_client()
        
        model = Gemini(model_name="gemini-1.5-pro")
        logger.info("Gemini model created: gemini-1.5-pro")
        
        class RemediationInput(BaseModel): # Renamed class
            """Input schema for device-specific remediation requests"""
            diagnosis_report: str = Field(description="Complete diagnosis report from Agent2 containing device analysis and recommendations")
            device_type: Optional[Literal["IoT", "Camera", "Unknown"]] = Field(
                description="Type of device requiring remediation (IoT or Camera)"
            )
            device_id: Optional[str] = Field(description="Device ID or equipment identifier")
            severity: Optional[Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]] = Field(
                description="Severity level from diagnosis report"
            )
            recommended_actions: Optional[str] = Field(description="Specific remediation actions recommended by Agent2")
        
        enhanced_instruction = """# Device-Specific Remediation Agent - ADK A2A Infrastructure Pattern

            You are a specialized Remediation Agent that performs device-specific remediation actions for IoT devices and Camera systems.

            ## YOUR PRIMARY ROLE:
            Execute device-specific remediation actions based on diagnosis reports from Agent2 and provide clear confirmation back to Agent1 through A2A Call.

            ## DEVICE-SPECIFIC REMEDIATION WORKFLOW:
            1. **Analyze Diagnosis Report**: Identify the device type (IoT or Camera) and specific issues from Agent2's diagnosis.
            2. **Select Appropriate Tools**: Choose the correct remediation tools based on device type and issues:

            **For IoT Devices:**
            - `restart_iot_system(device_id, device_type)` → Restart IoT device to clear memory/CPU issues
            - `adjust_iot_settings(device_id, setting_type, new_value)` → Adjust CPU thresholds, memory limits, network timeouts
            - `calibrate_iot_sensors(device_id, sensor_types)` → Calibrate sensors for accuracy improvements

            **For Camera Systems:**
            - `restart_camera_system(camera_id, camera_model)` → Restart camera to resolve imaging issues
            - `adjust_camera_brightness(camera_id, brightness_level, auto_adjust)` → Optimize exposure and brightness
            - `adjust_camera_focus(camera_id, focus_mode, focus_distance)` → Fix focus and sharpness issues

            3. **Execute Remediation**: Apply 1-3 appropriate remediation actions based on the diagnosis severity and issues identified.
            4. **Consolidate Results**: Combine all remediation results into a clear status summary.
            5. **Send Confirmation**: Forward the remediation confirmation to Agent1 via A2A communication.

            ## IMPORTANT OUTPUT FORMAT:
            Your final confirmation MUST include:
            - "Remediation Status: [SUCCESS/PARTIAL/FAILURE]"
            - "Device Type: [IoT/Camera]"
            - "Actions Taken: [list of specific actions performed]"
            - "Results Summary: [brief outcome description]"

            Keep responses concise and focused on remediation outcomes for Agent1."""
        
        log_analysis_agent = RemoteA2aAgent(
            name="log_analysis_agent",
            agent_card=f"http://{MACHINE1_IP}:{MACHINE1_PORT}/.well-known/agent-card.json"
        )
        logger.info(f"RemoteA2aAgent configured for log_analysis_agent at {MACHINE1_IP}:{MACHINE1_PORT}")
        
        # Initialize cost tracker for this agent
        global cost_tracker
        cost_tracker = get_cost_tracker("remediation_agent", logger)
        logger.info("Cost tracker initialized for remediation_agent")
        
        agent = LlmAgent(
            name="remediation_agent", # Renamed agent
            description="Device-specific remediation agent for IoT devices and Camera systems with cost tracking and comprehensive logging", # Updated description
            model=model,
            instruction=enhanced_instruction,
            tools=remediation_tools, # Changed from log_analysis_tools
            input_schema=RemediationInput, # Changed from LogAnalysisInput
            sub_agents=[log_analysis_agent]
        )
        
        logger.info("Remediation LlmAgent created following ADK A2A infrastructure patterns")
        logger.info(f"Model: gemini-1.5-pro")
        logger.info(f"Tools available: {len(remediation_tools)}")
        logger.info(f"A2A Sub-agents: 1 (diagnosis_agent) - ADK managed")
        logger.info(f"Input schema: defined for structured requests")
        logger.info(f"Description: {agent.description[:100]}...")
        
        return agent
        
    except Exception as e:
        logger.error(f"Failed to create Remediation Agent: {str(e)}") # Updated log message
        raise

async def get_corrected_remediation_agent_card(request):
    """Serve corrected agent card with proper IP instead of localhost"""
    agent_card = {
        "capabilities": {},
        "defaultInputModes": ["text/plain"],
        "defaultOutputModes": ["text/plain"],
        "description": "Device-specific remediation agent for IoT devices and Camera systems with specialized repair functions",
        "name": "remediation_agent", # Renamed agent
        "preferredTransport": "JSONRPC",
        "protocolVersion": "0.3.0",
        "skills": [
            {
                "description": "Device-specific LLM remediation agent for IoT devices and Camera systems",
                "id": "remediation_agent",
                "name": "model",
                "tags": ["llm", "a2a", "device-specific", "iot", "camera"]
            },
            {
                "description": "Restarts IoT device systems to resolve performance and connectivity issues",
                "id": "remediation_agent-restart_iot_system",
                "name": "restart_iot_system",
                "tags": ["llm", "tools", "iot", "restart", "performance"]
            },
            {
                "description": "Adjusts IoT device settings like thresholds, sampling rates, and network timeouts",
                "id": "remediation_agent-adjust_iot_settings",
                "name": "adjust_iot_settings",
                "tags": ["llm", "tools", "iot", "configuration", "settings"]
            },
            {
                "description": "Calibrates IoT sensors to improve data accuracy and measurement precision",
                "id": "remediation_agent-calibrate_iot_sensors",
                "name": "calibrate_iot_sensors",
                "tags": ["llm", "tools", "iot", "sensors", "calibration"]
            },
            {
                "description": "Restarts camera systems to resolve imaging and performance issues",
                "id": "remediation_agent-restart_camera_system",
                "name": "restart_camera_system",
                "tags": ["llm", "tools", "camera", "restart", "imaging"]
            },
            {
                "description": "Adjusts camera brightness and exposure settings for optimal image quality",
                "id": "remediation_agent-adjust_camera_brightness",
                "name": "adjust_camera_brightness",
                "tags": ["llm", "tools", "camera", "brightness", "exposure"]
            },
            {
                "description": "Adjusts camera focus settings to improve image sharpness and clarity",
                "id": "remediation_agent-adjust_camera_focus",
                "name": "adjust_camera_focus",
                "tags": ["llm", "tools", "camera", "focus", "sharpness"]
            }
        ],
        "supportsAuthenticatedExtendedCard": False,
        "url": f"http://{MACHINE3_IP}:{MACHINE3_PORT}", # Changed from MACHINE1_IP/PORT
        "version": "0.0.1"
    }
    
    return JSONResponse(content=agent_card)

def create_remediation_a2a_app(): # Renamed function
    """Create A2A app using to_a2a() function with comprehensive cost tracking"""
    
    app = to_a2a(remediation_agent) # Changed from log_analysis_agent
    
    corrected_route = Route("/.well-known/agent-card.json", get_corrected_remediation_agent_card, methods=["GET"])
    
    app.router.routes.insert(0, corrected_route)
    
    # Request logging middleware with cost tracking and remediation flow monitoring
    @app.middleware("http")
    async def log_requests(request, call_next):
        # Basic logging
        logger.info(f"HTTP {request.method} {request.url.path}")
        
        # Reset counter before request
        reset_tool_call_counter()
        
        # Cost tracking - capture request data
        transaction_id = cost_tracker.generate_transaction_id()
        request_body = None
        estimated_input_tokens = 0
        tool_count = 0  # Initialize for cost tracking
        
        if request.method == "POST":
            try:
                # Read request body for cost estimation
                body = await request.body()
                if body:
                    request_body = body.decode('utf-8')
                    estimated_input_tokens = estimate_tokens(request_body)
                    logger.info(f"COST_START | Transaction: {transaction_id} | Input tokens (estimated): {estimated_input_tokens}")
                    
                    # Recreate request with body for downstream processing
                    from starlette.requests import Request as StarletteRequest
                    import io
                    request._body = body
            except Exception as e:
                logger.warning(f"Could not read request body for cost tracking: {e}")
        
        # Process request
        response = await call_next(request)
        
        # Check tool execution and remediation flow
        tool_count = get_tool_call_counter()
        
        # Cost tracking - estimate output tokens and log cost
        try:
            # Estimate output tokens from response (rough approximation)
            response_size = 0
            if hasattr(response, 'body'):
                response_size = len(response.body) if response.body else 0
            elif hasattr(response, 'content'):
                response_size = len(str(response.content))
            
            estimated_output_tokens = max(1, response_size // 4)  # Rough token estimation
            
            # Log the cost for this transaction
            cost_entry = cost_tracker.log_request_cost(
                transaction_id=transaction_id,
                model_name="gemini-1.5-pro",  # Default model for Machine 3
                input_tokens=estimated_input_tokens,
                output_tokens=estimated_output_tokens,
                request_type="a2a_remediation",
                additional_context={
                    "tool_calls": tool_count,
                    "request_path": str(request.url.path),
                    "response_size": response_size,
                    "remediation_functions_called": tool_count
                }
            )
        except Exception as e:
            logger.warning(f"Cost tracking error: {e}")
        
        # Remediation execution flow monitoring (only for POST requests)
        if request.method == "POST":
            if tool_count >= 1:
                logger.info(f"Remediation tools executed: {tool_count}")
                logger.info(f"REMEDIATION CONFIRMATION: Should be sent back to Machine 1")
                logger.info(f"DEVICE_SPECIFIC_FLOW: Review logs above for IoT/Camera specific actions")
                logger.info(f"A2A_FLOW_STATUS: Remediation -> Agent 1 (completing circular flow)")
            elif tool_count == 0:
                logger.warning(f"No remediation tools called - check LLM instructions and diagnosis input")
        
        return response
    
    logger.info("A2A App created for Remediation Agent using to_a2a()") # Updated log message
    logger.info(f"Agent: {remediation_agent.name}") # Changed from log_analysis_agent
    logger.info(f"Port: {MACHINE3_PORT}") # Changed from MACHINE1_PORT
    logger.info(f"Agent card URL fixed to: http://{MACHINE3_IP}:{MACHINE3_PORT}")
    logger.info(f"Cost tracking middleware enabled for all requests")
    logger.info(f"Tool call monitoring enabled for remediation flow tracking")
    
    return app

remediation_agent = create_remediation_agent() # Renamed agent instance

remediation_a2a_app = create_remediation_a2a_app() # Renamed app instance
