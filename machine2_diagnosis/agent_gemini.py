import os
import google.generativeai as genai
from google.adk.agents.llm_agent import LlmAgent  # Use LlmAgent for full ADK features
from google.adk.models import Gemini
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent 
from pydantic import BaseModel, Field  # For input/output schemas
from typing import Optional, Literal, List
from tools import diagnosis_tools, get_tool_call_counter, reset_tool_call_counter
from logger_config import logger
from cost_tracker import get_cost_tracker, estimate_tokens
from starlette.responses import JSONResponse
from starlette.routing import Route
import sys
sys.path.append('..')
from config import MACHINE3_IP, MACHINE3_PORT, MACHINE2_IP, MACHINE2_PORT

def setup_gemini_client():
    """Setup Gemini API client"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    
    genai.configure(api_key=api_key)
    logger.info("Gemini API client configured successfully")
    return api_key

def create_diagnosis_agent():
    """Create and configure the Diagnosis Agent following ADK LlmAgent patterns"""
    try:
   
        
        model = Gemini(
            model_name="gemini-1.5-pro",
            generation_config={
                "temperature": 0.0,  # Zero temperature for deterministic tool calling
                "max_output_tokens": 8192,
                "candidate_count": 1  # Most deterministic setting
            }
        )
        # Define input schema using Pydantic BaseModel
        class DiagnosisInput(BaseModel):
            """Input schema for multi-schema diagnostic analysis (IoT + Camera)"""
            anomaly_details: str = Field(description="Comprehensive analysis report from Log Analysis Agent containing device metrics or equipment specs")
            device_id: Optional[str] = Field(description="Device ID or Equipment Model identifier")
            schema_type: Optional[Literal["IoT", "Camera", "Unknown"]] = Field(
                description="Detected schema type from the analysis report"
            )
            initial_severity: Optional[Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]] = Field(
                description="Initial severity assessment from Log Analysis Agent"
            )
            source_context: Optional[str] = Field(description="Additional context about data source and processing")
        
        # INDEPENDENT TOOL EXECUTION INSTRUCTIONS
        enhanced_instruction = """
        You receive diagnostic reports from Machine 1 (log analysis agent).
        
        PROCESS:
        1. Identify device type (IoT or Camera) from the report
        2. Call ALL tools independently with the SAME original report:
           - For IoT: diagnose_iot_device(report)
           - analyze_root_cause(report)
           - assess_severity_level(report)
           - generate_remediation_plan(report)

           - For Camera: diagnose_camera_equipment(report)  
           - analyze_root_cause(report)
           - assess_severity_level(report)
           - generate_remediation_plan(report)

        3. Create comprehensive diagnosis combining all tool results
        4. Forward all the requests to remediation_agent sub-agent (A2A call)
        5. Create a report based upon the all the tools results and forward to remediation_agent sub-agent (A2A call)
        
        CRITICAL: All tools work independently - pass the SAME original report to each tool.
        
        AVAILABLE TOOLS: diagnose_iot_device, diagnose_camera_equipment, analyze_root_cause, assess_severity_level, generate_remediation_plan
        AVAILABLE SUB-AGENTS: remediation_agent (for A2A forwarding)
        """

        remediation_remote_agent = RemoteA2aAgent(
            name="remediation_agent",
            agent_card=f"http://{MACHINE3_IP}:{MACHINE3_PORT}/.well-known/agent-card.json"
        )
        logger.info(f"RemoteA2aAgent configured for remediation_agent at {MACHINE3_IP}:{MACHINE3_PORT}")
        
        # Initialize cost tracker for this agent
        global cost_tracker
        cost_tracker = get_cost_tracker("diagnosis_agent", logger)
        logger.info("Cost tracker initialized for diagnosis_agent")
        
        # Create LlmAgent with enhanced data-driven capabilities
        agent = LlmAgent(
            name="diagnosis_agent",
            description="Expert intelligent diagnosis agent with built-in orchestration and data-driven analysis. Intelligently selects and executes appropriate diagnostic tools based on report content analysis. Performs threshold-based IoT device diagnostics and Camera equipment analysis with metric extraction from LOG REFERENCE DATA sections.",
            model=model,
            instruction=enhanced_instruction,
            tools=diagnosis_tools,
            input_schema=DiagnosisInput,
            sub_agents=[remediation_remote_agent]
        )
        
        # Function call logging is built into each tool function
        
        logger.info("Enhanced Multi-Schema Diagnosis LlmAgent created following ADK patterns")
        logger.info(f"Model: gemini-1.5-pro")
        logger.info(f"Tools available: {len(diagnosis_tools)} (IoT + Camera diagnostics)")
        logger.info(f"Tool names: {[tool.__name__ for tool in diagnosis_tools]}")
        logger.info(f"A2A Sub-agents: 1 (remediation_agent) - ADK managed")
        logger.info(f"Input schema: defined for multi-schema diagnosis requests")
        logger.info(f"Description: Expert multi-schema diagnosis with intelligent tool selection...")
        
        return agent
        
    except Exception as e:
        logger.error(f"Failed to create Diagnosis Agent: {str(e)}")
        raise

async def get_corrected_diagnosis_agent_card(request):
    """Serve corrected agent card with enhanced data-driven diagnostic capabilities"""
    agent_card = {
        "capabilities": {},
        "defaultInputModes": ["text/plain"],
        "defaultOutputModes": ["text/plain"],
        "description": "Expert intelligent diagnosis agent with built-in orchestration for IoT devices and Camera equipment",
        "name": "diagnosis_agent",
        "preferredTransport": "JSONRPC",
        "protocolVersion": "0.3.0",
        "skills": [
            {
                "description": "Intelligent LLM diagnosis agent with built-in orchestration and metric-based analysis",
                "id": "diagnosis_agent",
                "name": "model",
                "tags": ["llm", "data-driven", "metrics", "thresholds"]
            },
            {
                "description": "Enhanced IoT device diagnostics - extracts and analyzes numerical metrics (CPU%, Memory%, Latency ms, Error counts)",
                "id": "diagnosis_agent-diagnose_iot_device",
                "name": "diagnose_iot_device",
                "tags": ["llm", "tools", "iot", "metrics", "thresholds"]
            },
            {
                "description": "Enhanced camera equipment analysis - evaluates specs with numerical precision (Resolution, Weight, Price)",
                "id": "diagnosis_agent-diagnose_camera_equipment", 
                "name": "diagnose_camera_equipment",
                "tags": ["llm", "tools", "camera", "specs", "analysis"]
            },
            {
                "description": "Metric-based root cause analysis - identifies specific causes using actual threshold values",
                "id": "diagnosis_agent-analyze_root_cause",
                "name": "analyze_root_cause", 
                "tags": ["llm", "tools", "root-cause", "metrics"]
            },
            {
                "description": "Data-driven remediation planning - provides actionable steps based on specific metric thresholds",
                "id": "diagnosis_agent-generate_remediation_plan",
                "name": "generate_remediation_plan",
                "tags": ["llm", "tools", "remediation", "actionable", "thresholds"]
            },
            {
                "description": "Enhanced severity assessment - uses actual metric values for precise priority evaluation",
                "id": "diagnosis_agent-assess_severity_level",
                "name": "assess_severity_level",
                "tags": ["llm", "tools", "severity", "metrics", "precision"]
            }
        ],
        "supportsAuthenticatedExtendedCard": False,
        "url": f"http://{MACHINE2_IP}:{MACHINE2_PORT}",  
        "version": "2.1.0"
    }
    
    return JSONResponse(content=agent_card)

def create_diagnosis_a2a_app():
    """Create A2A app using to_a2a() function"""
    
    # Create A2A app from agent using to_a2a
    app = to_a2a(diagnosis_agent)
    
    # Add corrected agent card route to override the default localhost URL
    corrected_route = Route("/.well-known/agent-card.json", get_corrected_diagnosis_agent_card, methods=["GET"])
    
    # Add the route to the app's router (this overrides the existing route)
    app.router.routes.insert(0, corrected_route)  # Insert at beginning for priority
    
    # Request logging middleware with cost tracking and data loss detection
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
                    
                    request._body = body
            except Exception as e:
                logger.warning(f"Could not read request body for cost tracking: {e}")
        
        # Process request
        response = await call_next(request)
        
        # Check tool execution and data flow
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
                model_name="gemini-1.5-pro",  # Default model for Machine 2
                input_tokens=estimated_input_tokens,
                output_tokens=estimated_output_tokens,
                request_type="a2a_diagnosis",
                additional_context={
                    "tool_calls": tool_count,
                    "request_path": str(request.url.path),
                    "response_size": response_size
                }
            )
        except Exception as e:
            logger.warning(f"Cost tracking error: {e}")
        
        # Tool execution summary (only for POST requests)
        if request.method == "POST":
            if tool_count >= 4:
                logger.info(f"All diagnostic tools called: {tool_count}")
                logger.info(f"REMEDIATION REPORT: Should be forwarded to Machine 3")
                logger.info(f"DATA FLOW CHECK: Review logs above for any data loss warnings")
            elif tool_count >= 3:
                logger.warning(f"Partial execution: {tool_count} tools called - missing remediation_agent call")
            elif tool_count > 0:
                logger.warning(f"Partial execution: Only {tool_count} tools called - check LLM instructions")
            # Only log error for POST requests with 0 tools (GET requests are expected to have 0 tools)
        
        return response
    
    logger.info(f"Diagnosis Agent ready on {MACHINE2_IP}:{MACHINE2_PORT}")
    
    return app

# Create the agent instance
diagnosis_agent = create_diagnosis_agent()

# Create the A2A app instance  
diagnosis_a2a_app = create_diagnosis_a2a_app()
