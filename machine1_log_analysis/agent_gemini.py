import os
import csv
import json
import google.generativeai as genai
from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.models import Gemini
from google.adk.runners import InMemoryRunner
from google.genai import types
from pydantic import BaseModel, Field
from tools import log_analysis_tools
from logger_config import logger
from cost_tracker import get_cost_tracker, estimate_tokens
from starlette.responses import JSONResponse
from starlette.routing import Route
from fastapi import Request
from fastapi.responses import StreamingResponse
import asyncio
import sys
sys.path.append('..')
from config import MACHINE1_IP, MACHINE1_PORT, MACHINE2_IP, MACHINE2_PORT, MACHINE3_IP, MACHINE3_PORT

# Global variables
agent_runner = None

def setup_gemini_client():
    """Setup Gemini API client"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    
    genai.configure(api_key=api_key)
    logger.info("Gemini API client configured successfully")
    return api_key

def create_log_analysis_agent():
    """Create and configure the Log Analysis Agent following ADK LlmAgent patterns"""
    try:
        # Setup Gemini client
        api_key = setup_gemini_client()
        
        # Use working Flash model (cameras work perfectly with it)
        model = Gemini(
            generation_config={
                "temperature": 0.1,
                "max_output_tokens": 8192,
                "candidate_count": 1
            }
        )
        logger.info("Gemini model configured with working Flash model (cameras work perfectly)")
        
        # Define input schema: single record analysis
        class RecordAnalysisInput(BaseModel):
            """Input schema: a single CSV record to analyze for anomalies."""
            record: dict = Field(description="A single CSV record as a dictionary")
        
        # Store the agent runner globally
        global agent_runner

        enhanced_instruction = """Analyze device records and write reports.
        You will get a single record at a time, you have to identify if the record is an IoT device or a camera log.
        For identification you will get the Device_ID,CPU_Usage (%),Memory_Usage (%),Battery_Level (%) etc for the iot device.
        For camera you will get the Model,Max resolution,Effective pixels,Zoom wide,Price etc.
        Now you have to call the appropriate tools for the device type.
        After calling the tools you have to write a report based upon the tools results.
        For IoT: "COMPREHENSIVE IoT DIAGNOSTIC REPORT - Device [id]"
        For Cameras: "CAMERA SPEC ANALYSIS - Model [name]"
        The report should contain all the keys and values of the record under LOG REFERENCE DATA: section. The report needs to be in a structured format with all the details and tools results.


        If the severity is MEDIUM/HIGH/CRITICAL you have to forward the report by A2A call to the diagnosis_agent sub-agent for further analysis and remediation recommendations.
        """
        # Create RemoteA2aAgent for diagnosis_agent via ADK A2A infrastructure
        diagnosis_remote_agent = RemoteA2aAgent(
            name="diagnosis_agent",
            agent_card=f"http://{MACHINE2_IP}:{MACHINE2_PORT}/.well-known/agent-card.json"
        )
        logger.info(f"RemoteA2aAgent configured for diagnosis_agent at {MACHINE2_IP}:{MACHINE2_PORT}")
        
        # Create LlmAgent with ADK A2A infrastructure pattern
        # Note: Using sub_agents for ADK-managed A2A communication via prompt triggers
        agent = LlmAgent(
            name="log_analysis_agent",
            description="Expert IoT analysis agent: performs comprehensive device analysis using multiple tools to generate detailed analytical reports. For MEDIUM/HIGH/CRITICAL cases, automatically consults diagnosis_agent sub-agent for specialized expertise and remediation recommendations.",
            model=model,
            instruction=enhanced_instruction,
            tools=log_analysis_tools,
            input_schema=RecordAnalysisInput,
            sub_agents=[diagnosis_remote_agent]
        )
        
        logger.info("Log Analysis LlmAgent created following ADK A2A infrastructure patterns")
        logger.info(f"Model: gemini-1.5-pro")
        logger.info(f"Tools available: {len(log_analysis_tools)}")
        logger.info(f"A2A Sub-agents: 1 (diagnosis_agent) - ADK managed")
        logger.info(f"Input schema: defined for structured requests")
        logger.info(f"Description: {agent.description[:100]}...")
        
        # Create in-memory runner for agent invocation
        runner = InMemoryRunner(
            agent=agent,
            app_name="log_analysis_agent"
        )
        agent_runner = runner
        logger.info("InMemoryRunner created for agent invocation")
        
        # Initialize cost tracker for this agent
        global cost_tracker
        cost_tracker = get_cost_tracker("log_analysis_agent", logger)
        logger.info("Cost tracker initialized for log_analysis_agent")
        
        return agent
        
    except Exception as e:
        logger.error(f"Failed to create Log Analysis Agent: {str(e)}")
        raise

async def get_corrected_log_agent_card(request):
    """Serve corrected agent card with proper IP and all available tools"""
    agent_card = {
        "capabilities": {},
        "defaultInputModes": ["text/plain"],
        "defaultOutputModes": ["text/plain"],
        "description": "Expert multi-schema analysis agent that generates comprehensive diagnostic reports with LOG REFERENCE DATA for IoT devices and Camera equipment using intelligent tool selection and A2A forwarding",
        "name": "log_analysis_agent",
        "preferredTransport": "JSONRPC",
        "protocolVersion": "0.3.0",
        "skills": [
            {
                "description": "Expert LLM agent that performs comprehensive multi-schema analysis (IoT + Camera) and generates structured diagnostic reports with detailed metric extraction",
                "id": "log_analysis_agent",
                "name": "model",
                "tags": ["llm", "expert", "multi-schema", "diagnostic", "iot", "camera", "a2a"]
            },
            {
                "description": "Analyze device CPU and memory performance metrics",
                "id": "log_analysis_agent-analyze_device_metrics",
                "name": "analyze_device_metrics",
                "tags": ["cpu", "memory", "performance", "iot"]
            },
            {
                "description": "Check device health status (temperature, battery levels)",
                "id": "log_analysis_agent-check_device_health",
                "name": "check_device_health",
                "tags": ["health", "temperature", "battery", "iot"]
            },
            {
                "description": "Analyze network performance (latency, packet loss)",
                "id": "log_analysis_agent-analyze_network_performance",
                "name": "analyze_network_performance",
                "tags": ["network", "latency", "packet-loss", "iot"]
            },
            {
                "description": "Analyze operational metrics (uptime, workload, errors, failures)",
                "id": "log_analysis_agent-analyze_operational_metrics",
                "name": "analyze_operational_metrics",
                "tags": ["operational", "uptime", "workload", "errors", "iot"]
            },
            {
                "description": "Analyze camera core specifications (resolution, pixels, zoom)",
                "id": "log_analysis_agent-analyze_camera_core_specs",
                "name": "analyze_camera_core_specs",
                "tags": ["camera", "resolution", "specs", "zoom"]
            },
            {
                "description": "Assess camera value based on age, price, and capabilities",
                "id": "log_analysis_agent-assess_camera_value",
                "name": "assess_camera_value",
                "tags": ["camera", "value", "price", "assessment"]
            },
            {
                "description": "Evaluate camera portability (weight, dimensions)",
                "id": "log_analysis_agent-evaluate_camera_portability",
                "name": "evaluate_camera_portability",
                "tags": ["camera", "portability", "weight", "dimensions"]
            }
        ],
        "supportsAuthenticatedExtendedCard": False,
        "url": f"http://{MACHINE1_IP}:{MACHINE1_PORT}",
        "version": "2.0.0"
    }
    
    return JSONResponse(content=agent_card)

async def stream_csv_endpoint(request: Request):
    """Stream CSV rows to the agent in real-time and yield results back to client"""
    try:
        data = await request.json()
        csv_paths = data.get("csv_paths")
        csv_path = data.get("csv_path")

        # Normalize sources list
        sources = []
        if isinstance(csv_paths, list) and csv_paths:
            sources = [str(p) for p in csv_paths]
        elif isinstance(csv_path, str) and csv_path:
            sources = [csv_path]
        else:
            return JSONResponse({"error": "csv_path or csv_paths is required"}, status_code=400)

        logger.info(f"Starting real-time analysis of {sources}")

        severity_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}

        async def row_generator():
            row_count = 0
            yield '{"status": "streaming", "results": ['  # JSON array start
            first = True

            # Open all files and create readers
            file_handles = []
            readers = []
            for source_path in sources:
                f = open(source_path, newline='')
                reader = csv.DictReader(f)
                file_handles.append(f)
                readers.append((reader, source_path))
            
            try:
                # Interleave processing: 1 record from each file in round-robin
                while readers:
                    # Process one record from each remaining file
                    readers_to_remove = []
                    
                    for i, (reader, source_path) in enumerate(readers):
                        try:
                            row = next(reader)
                            row_count += 1
                            device_id = row.get('Device_ID', row.get('Model', 'unknown'))
                            logger.info(f"Processing record {row_count}: {device_id} from {source_path}")
                            
                            # LOG DETAILED INPUT DATA
                            logger.info(f"Streaming input data for device {device_id}")
                            logger.info(f"Source file: {source_path}")
                            logger.info(f"Record number: {row_count}")
                            logger.info(f"Raw CSV data ({len(row)} fields)")
                            for key, value in row.items():
                                logger.info(f"   {key}: {value}")
                            logger.info(f"End of input data for device {device_id}")
                            logger.info(f"{'='*60}")

                        except StopIteration:
                            # This file is exhausted, mark for removal
                            readers_to_remove.append(i)
                            continue

                        try:
                            # Create session for each row
                            session = await agent_runner.session_service.create_session(
                                app_name="log_analysis_agent", user_id="stream_user"
                            )

                            # Prepare LLM input
                            llm_input = json.dumps({"record": row})
                            content = types.Content(
                                parts=[types.Part.from_text(text=llm_input)],
                                role="user"
                            )
                            
                            # COST TRACKING - Start transaction
                            transaction_id = cost_tracker.generate_transaction_id()
                            estimated_input_tokens = estimate_tokens(llm_input)
                            
                            # LOG LLM INPUT
                            logger.info(f"LLM input for device {device_id}")
                            logger.info(f"Structured input: {llm_input}")
                            logger.info(f"COST_START | Transaction: {transaction_id} | Input tokens (estimated): {estimated_input_tokens}")
                            logger.info(f"Sending to LLM Agent")
                            logger.info(f"{'─'*60}")

                            # Collect streamed agent response
                            response_text = ""
                            non_text_parts_count = 0
                            function_calls_completed = 0
                            
                            async for event in agent_runner.run_async(
                                user_id=session.user_id, session_id=session.id, new_message=content
                            ):
                                if hasattr(event, 'content') and event.content and hasattr(event.content, 'parts'):
                                    for part in event.content.parts:
                                        if hasattr(part, 'text') and part.text:
                                            response_text += part.text
                                        elif hasattr(part, 'function_call'):
                                            function_calls_completed += 1
                                            non_text_parts_count += 1
                                        else:
                                            non_text_parts_count += 1
                            
                            # Log if no text was generated (but don't try follow-up - it causes hangs)
                            if not response_text.strip() and function_calls_completed > 0:
                                logger.error(f"IoT generation failure: {function_calls_completed} tools called but no text generated for device {device_id}")
                                logger.error(f"This indicates LLM instruction compliance issue - function calls work but text generation fails")

                            # Log the complete response for analysis
                            device_id = row.get("Device_ID", row.get("Model", "unknown"))
                            logger.info(f"Complete report for device {device_id}")
                            logger.info(f"{'='*60}")
                            if response_text and response_text.strip():
                                logger.info(f"{response_text}")
                            else:
                                logger.error(f"Empty response for device {device_id}! This indicates LLM generation failure.")
                                logger.error(f"Row data: {json.dumps(row, indent=2)}")
                            logger.info(f"{'='*60}")
                            
                            # COST TRACKING - Calculate and log cost
                            estimated_output_tokens = estimate_tokens(response_text or "")
                            cost_entry = cost_tracker.log_request_cost(
                                transaction_id=transaction_id,
                                model_name="gemini-1.5-flash",  # Default model for Machine 1
                                input_tokens=estimated_input_tokens,
                                output_tokens=estimated_output_tokens,
                                request_type="csv_streaming",
                                additional_context={
                                    "device_id": device_id,
                                    "function_calls": function_calls_completed,
                                    "response_length": len(response_text or ""),
                                    "source_file": source_path
                                }
                            )
                            
                            # LOG COMPLETE LLM RESPONSE ANALYSIS
                            logger.info(f"LLM RESPONSE ANALYSIS FOR {device_id}:")
                            logger.info(f"Response length: {len(response_text)} characters")
                            if non_text_parts_count > 0:
                                logger.info(f"Non-text parts (function calls/tool calls) present: {non_text_parts_count}")
                            if response_text:
                                logger.info(f"Response Preview: {response_text[:200]}...")
                            logger.info(f"{'─'*60}")

                            # Determine severity with enhanced parsing
                            severity = None
                            if response_text and response_text.strip():
                                text_upper = response_text.upper()
                                # Look for RISK ASSESSMENT pattern first (most specific)
                                if 'RISK ASSESSMENT:' in text_upper:
                                    if 'RISK ASSESSMENT: CRITICAL' in text_upper:
                                        severity = 'CRITICAL'
                                    elif 'RISK ASSESSMENT: HIGH' in text_upper:
                                        severity = 'HIGH'
                                    elif 'RISK ASSESSMENT: MEDIUM' in text_upper:
                                        severity = 'MEDIUM'
                                    elif 'RISK ASSESSMENT: LOW' in text_upper:
                                        severity = 'LOW'
                                # Fallback to general keyword search
                                elif 'CRITICAL' in text_upper:
                                    severity = 'CRITICAL'
                                elif 'HIGH' in text_upper:
                                    severity = 'HIGH'
                                elif 'MEDIUM' in text_upper:
                                    severity = 'MEDIUM'
                                elif 'LOW' in text_upper:
                                    severity = 'LOW'
                            
                            # If no severity found and response exists, log for debugging
                            if not severity and response_text and response_text.strip():
                                logger.warning(f"SEVERITY PARSING FAILED for {device_id}. Response length: {len(response_text)}")
                                logger.debug(f"Response preview: {response_text[:200]}...")

                            # Log severity decision
                            logger.info(f"Severity assessment: {device_id} -> {severity}")

                            # Check for A2A sub-agent invocation requirement
                            if severity in ['MEDIUM', 'HIGH', 'CRITICAL']:
                                logger.info(f"A2A sub-agent consultation required: {device_id} ({severity} severity, schema-independent)")
                                logger.info(f"A2A FORWARDING (Agent 1): Instructing LLM to consult diagnosis_agent for {device_id}")

                                # Post-response detection: did we get a diagnosis_agent-style report back?
                                a2a_indicators = [
                                    "diagnosis_agent:",  # Actual diagnosis agent response indicator
                                    "Remediation Status:",  # Remediation confirmation from Agent 3
                                    "Device Type:",  # Agent 3 response structure
                                    "Actions Taken:",  # Remediation actions from Agent 3
                                    "Results Summary:",  # Final results from Agent 3
                                ]
                                # Debug: Check each indicator individually
                                logger.debug(f"A2A Detection Debug for {device_id}:")
                                logger.debug(f"Response text length: {len(response_text or '')}")
                                logger.debug(f"Response contains 'diagnosis_agent:': {'diagnosis_agent:' in (response_text or '')}")
                                for i, indicator in enumerate(a2a_indicators):
                                    found = indicator in (response_text or "")
                                    logger.debug(f"Indicator {i+1}: '{indicator}' -> {found}")
                                
                                a2a_detected = any(indicator in (response_text or "") for indicator in a2a_indicators)
                                if a2a_detected:
                                    logger.info(f"A2A sub-agent consultation detected: diagnosis_agent response embedded for device {device_id}")
                                else:
                                    logger.warning(f"A2A sub-agent consultation not detected in final response for device {device_id}. Check agent prompts and sub-agent availability.")
                                    logger.warning(f"Response preview for debugging: {(response_text or '')[:300]}...")
                            if severity in severity_counts:
                                severity_counts[severity] += 1

                            # Yield row result immediately
                            if not first:
                                yield ","
                            first = False
                            yield json.dumps({
                                "row": row_count,
                                "source": source_path,
                                "device_id": row.get("Device_ID", row.get("Model", "unknown")),
                                "response": response_text,
                                "severity": severity
                            })

                            await asyncio.sleep(0)  # allow other tasks to run

                        except Exception as e:
                            logger.error(f"Error processing row {row_count}: {str(e)}")
                            if not first:
                                yield ","
                            first = False
                            yield json.dumps({
                                "row": row_count,
                                "source": source_path,
                                "device_id": row.get("Device_ID", row.get("Model", "unknown")),
                                "error": str(e)
                            })
                    
                    # Remove exhausted readers
                    for i in reversed(readers_to_remove):
                        readers.pop(i)
                
            finally:
                # Close all file handles
                for f in file_handles:
                    f.close()
            
            # Log session cost summary
            cost_tracker.log_session_summary()
            session_summary = cost_tracker.get_session_summary()
            
            # Send summary at the end
            yield f'], "severity_counts": {json.dumps(severity_counts)}, "cost_summary": {json.dumps(session_summary)}, "status": "completed"}}'

        return StreamingResponse(row_generator(), media_type="application/json")

    except Exception as e:
        logger.error(f"Error in streaming endpoint: {str(e)}")
        return JSONResponse({"error": str(e)}, status_code=500)

def create_log_analysis_a2a_app():
    """Create A2A app using to_a2a() function"""
    
    # Create A2A app from agent using to_a2a
    app = to_a2a(log_analysis_agent)
    
    # Add corrected agent card route to override the default localhost URL
    corrected_route = Route("/.well-known/agent-card.json", get_corrected_log_agent_card, methods=["GET"])
    
    # Add streaming CSV endpoint
    streaming_route = Route("/stream_csv", stream_csv_endpoint, methods=["POST"])
    
    # Add the routes to the app's router
    app.router.routes.insert(0, corrected_route)  # Insert at beginning for priority
    app.router.routes.append(streaming_route)     # Add streaming endpoint
    
    logger.info("A2A App created for Log Analysis Agent using to_a2a()")
    logger.info(f"Agent: {log_analysis_agent.name}")
    logger.info(f"Port: {MACHINE1_PORT}")
    logger.info(f"Agent card URL fixed to: http://{MACHINE1_IP}:{MACHINE1_PORT}")
    logger.info(f"Streaming endpoint available at: http://{MACHINE1_IP}:{MACHINE1_PORT}/stream_csv")
    
    return app

# Create the agent instance
log_analysis_agent = create_log_analysis_agent()

# Create the A2A app instance  
log_analysis_a2a_app = create_log_analysis_a2a_app()
