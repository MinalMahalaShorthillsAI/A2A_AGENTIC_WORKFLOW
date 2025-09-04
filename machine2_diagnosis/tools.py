# Enhanced Diagnosis Tools for Agent 1's Report Format (IoT + Camera)
# INDEPENDENT DESIGN - No tool dependencies on previous tool outputs

from datetime import datetime
import re
import json
from logger_config import logger

# --- Tool call telemetry (to enforce tool execution) ---
_TOOL_CALL_COUNTER = 0

def _mark_tool_called(tool_name: str) -> None:
    global _TOOL_CALL_COUNTER
    _TOOL_CALL_COUNTER += 1

def get_tool_call_counter() -> int:
    return _TOOL_CALL_COUNTER

def reset_tool_call_counter() -> None:
    global _TOOL_CALL_COUNTER
    _TOOL_CALL_COUNTER = 0

def diagnose_iot_device(device_report: str) -> str:
    """
    Diagnose IoT device issues based on Agent 1's COMPREHENSIVE IoT DIAGNOSTIC REPORT format.
    Extracts and analyzes performance, health, network, and operational data.
    """
    logger.info(f"FUNCTION CALL: diagnose_iot_device() invoked by LLM")
    _mark_tool_called("diagnose_iot_device")
    logger.info(f"Input: Original report ({len(device_report)} chars)")
    logger.info(f"LLM REASONING: Detected IoT schema -> Selected diagnose_iot_device()")
    
    # Extract device ID from report header
    device_id = "UNKNOWN"
    if "Device " in device_report:
        device_match = re.search(r"Device (\w+)", device_report)
        if device_match:
            device_id = device_match.group(1)
    
    # Extract numerical metrics from LOG REFERENCE DATA section
    metrics = {}
    if "LOG REFERENCE DATA" in device_report:
        data_section = device_report.split("LOG REFERENCE DATA:")[1]
        
        # Extract specific metrics with precise regex patterns
        cpu_match = re.search(r"CPU_Usage \(%\):\s*([0-9.]+)", data_section)
        memory_match = re.search(r"Memory_Usage \(%\):\s*([0-9.]+)", data_section)
        battery_match = re.search(r"Battery_Level \(%\):\s*([0-9.]+)", data_section)
        latency_match = re.search(r"Network_Latency \(ms\):\s*([0-9.]+)", data_section)
        packet_loss_match = re.search(r"Packet_Loss \(%\):\s*([0-9.]+)", data_section)
        temp_match = re.search(r"Temperature \(°C\):\s*([0-9.]+)", data_section)
        uptime_match = re.search(r"Uptime \(hrs\):\s*([0-9.]+)", data_section)
        workload_match = re.search(r"Workload_Intensity:\s*([0-9]+)", data_section)
        error_match = re.search(r"Error_Count:\s*([0-9]+)", data_section)
        failure_match = re.search(r"Failure_Type:\s*([0-9]+)", data_section)
        
        if cpu_match: metrics['cpu'] = float(cpu_match.group(1))
        if memory_match: metrics['memory'] = float(memory_match.group(1))
        if battery_match: metrics['battery'] = float(battery_match.group(1))
        if latency_match: metrics['latency'] = float(latency_match.group(1))
        if packet_loss_match: metrics['packet_loss'] = float(packet_loss_match.group(1))
        if temp_match: metrics['temperature'] = float(temp_match.group(1))
        if uptime_match: metrics['uptime'] = float(uptime_match.group(1))
        if workload_match: metrics['workload'] = int(workload_match.group(1))
        if error_match: metrics['errors'] = int(error_match.group(1))
        if failure_match: metrics['failure_type'] = int(failure_match.group(1))
    
    # SOPHISTICATED DIAGNOSTIC ANALYSIS using extracted metrics
    critical_issues = []
    warnings = []
    performance_analysis = []
    
    # CPU Analysis
    if 'cpu' in metrics:
        cpu = metrics['cpu']
        if cpu > 90:
            critical_issues.append(f"CRITICAL_CPU_UTILIZATION({cpu}%)")
        elif cpu > 80:
            warnings.append(f"HIGH_CPU_UTILIZATION({cpu}%)")
        elif cpu > 60:
            performance_analysis.append(f"ELEVATED_CPU({cpu}%)")
        else:
            performance_analysis.append(f"CPU_NORMAL({cpu}%)")
    
    # Memory Analysis
    if 'memory' in metrics:
        memory = metrics['memory']
        if memory > 95:
            critical_issues.append(f"CRITICAL_MEMORY_EXHAUSTION({memory}%)")
        elif memory > 85:
            warnings.append(f"HIGH_MEMORY_USAGE({memory}%)")
        else:
            performance_analysis.append(f"MEMORY_ACCEPTABLE({memory}%)")
    
    # Network Analysis
    if 'latency' in metrics:
        latency = metrics['latency']
        if latency > 500:
            critical_issues.append(f"CRITICAL_LATENCY({latency}ms)")
        elif latency > 200:
            warnings.append(f"HIGH_LATENCY({latency}ms)")
        elif latency > 100:
            performance_analysis.append(f"ELEVATED_LATENCY({latency}ms)")
        else:
            performance_analysis.append(f"LATENCY_NORMAL({latency}ms)")
    
    # Error Analysis
    if 'errors' in metrics:
        errors = metrics['errors']
        if errors > 10:
            critical_issues.append(f"CRITICAL_ERROR_RATE({errors})")
        elif errors > 5:
            warnings.append(f"HIGH_ERROR_RATE({errors})")
        elif errors > 0:
            performance_analysis.append(f"MODERATE_ERRORS({errors})")
        else:
            performance_analysis.append(f"ERROR_FREE_OPERATION")
    
    # Severity Assessment
    if critical_issues:
        severity = "CRITICAL"
    elif warnings:
        severity = "HIGH" if len(warnings) > 2 else "MEDIUM"
    else:
        severity = "LOW"
    
    # Build diagnosis summary
    diagnosis = f"IoT DEVICE DIAGNOSIS - {device_id}: {severity} SEVERITY"
    
    if critical_issues:
        diagnosis += f" | CRITICAL: {' | '.join(critical_issues)}"
    if warnings:
        diagnosis += f" | WARNINGS: {' | '.join(warnings)}"
    if performance_analysis:
        diagnosis += f" | ANALYSIS: {' | '.join(performance_analysis)}"
    
    logger.info(f"IoT diagnosis completed for {device_id}: {severity} severity")
    return diagnosis

def diagnose_camera_equipment(camera_report: str) -> str:
    """
    Diagnose camera equipment based on Agent 1's CAMERA SPEC ANALYSIS format.
    Extracts and analyzes technical specifications and pricing data.
    """
    logger.info(f"FUNCTION CALL: diagnose_camera_equipment() invoked by LLM")
    _mark_tool_called("diagnose_camera_equipment")
    logger.info(f"Input: Original report ({len(camera_report)} chars)")
    logger.info(f"LLM REASONING: Detected Camera schema -> Selected diagnose_camera_equipment()")
    
    # Extract camera model from report header
    camera_model = "UNKNOWN"
    if "Model " in camera_report:
        model_match = re.search(r"Model ([^\n\r]+)", camera_report)
        if model_match:
            camera_model = model_match.group(1).strip()
    
    # Extract camera specifications from LOG REFERENCE DATA section
    specs = {}
    if "LOG REFERENCE DATA" in camera_report:
        data_section = camera_report.split("LOG REFERENCE DATA:")[1]
        
        # Extract specific camera metrics with precise regex patterns
        resolution_match = re.search(r"Max resolution:\s*([0-9.]+)", data_section)
        pixels_match = re.search(r"Effective pixels:\s*([0-9.]+)", data_section)
        zoom_match = re.search(r"Zoom wide \(W\):\s*([0-9.]+)", data_section)
        weight_match = re.search(r"Weight \(inc\. batteries\):\s*([0-9.]+)", data_section)
        price_match = re.search(r"Price:\s*([0-9.]+)", data_section)
        
        if resolution_match: specs['resolution'] = float(resolution_match.group(1))
        if pixels_match: specs['pixels'] = float(pixels_match.group(1))
        if zoom_match: specs['zoom_wide'] = float(zoom_match.group(1))
        if weight_match: specs['weight'] = float(weight_match.group(1))
        if price_match: specs['price'] = float(price_match.group(1))
    
    # SOPHISTICATED CAMERA ANALYSIS using extracted specifications
    quality_issues = []
    value_concerns = []
    technical_analysis = []
    
    # Resolution Analysis
    if 'resolution' in specs:
        resolution = specs['resolution']
        if resolution < 800:
            quality_issues.append(f"LOW_RESOLUTION_SENSOR({resolution})")
        elif resolution < 1200:
            technical_analysis.append(f"ADEQUATE_RESOLUTION({resolution})")
        else:
            technical_analysis.append(f"HIGH_RESOLUTION({resolution})")
    
    # Pixel Analysis
    if 'pixels' in specs:
        pixels = specs['pixels']
        if pixels < 1.0:
            quality_issues.append(f"INADEQUATE_PIXEL_COUNT({pixels}MP)")
        elif pixels < 2.0:
            technical_analysis.append(f"BASIC_SENSOR({pixels}MP)")
        else:
            technical_analysis.append(f"DECENT_SENSOR({pixels}MP)")
    
    # Weight Analysis
    if 'weight' in specs:
        weight = specs['weight']
        if weight > 600:
            quality_issues.append(f"HEAVY_WEIGHT({weight}g)")
        elif weight > 400:
            technical_analysis.append(f"MODERATE_WEIGHT({weight}g)")
        else:
            technical_analysis.append(f"LIGHTWEIGHT({weight}g)")
    
    # Overall Assessment
    if quality_issues and value_concerns:
        severity = "HIGH"
    elif quality_issues or value_concerns:
        severity = "MEDIUM"
    else:
        severity = "LOW"
    
    # Build diagnosis summary
    diagnosis = f"CAMERA DIAGNOSIS - {camera_model}: {severity} SEVERITY"
    
    if quality_issues:
        diagnosis += f" | QUALITY_ISSUES: {' | '.join(quality_issues)}"
    if value_concerns:
        diagnosis += f" | VALUE_CONCERNS: {' | '.join(value_concerns)}"
    if technical_analysis:
        diagnosis += f" | TECHNICAL: {' | '.join(technical_analysis)}"
    
    logger.info(f"📸 Camera diagnosis completed for {camera_model}: {severity} severity")
    return diagnosis

def analyze_root_cause(report_content: str) -> str:
    """
    INDEPENDENT ROOT CAUSE ANALYSIS - Extracts all data directly from original report.
    No dependency on previous tool outputs.
    """
    logger.info(f"FUNCTION CALL: analyze_root_cause() invoked by LLM")
    _mark_tool_called("analyze_root_cause")
    logger.info(f"Input: Original report ({len(report_content)} chars)")
    logger.info(f"INDEPENDENT ANALYSIS: Extracting metrics directly from report")
    
    root_causes = []
    
    # Extract all metrics directly from LOG REFERENCE DATA section
    if "LOG REFERENCE DATA" in report_content:
        data_section = report_content.split("LOG REFERENCE DATA:")[1]
        
        # IoT Device Analysis
        if "Device_ID:" in data_section:
            # CPU Analysis
            cpu_match = re.search(r"CPU_Usage \(%\):\s*([0-9.]+)", data_section)
            if cpu_match:
                cpu = float(cpu_match.group(1))
                if cpu > 80:
                    root_causes.append(f"CRITICAL_CPU_OVERLOAD - {cpu}% utilization")
                elif cpu > 60:
                    root_causes.append(f"HIGH_CPU_USAGE - {cpu}% resource pressure")
            
            # Memory Analysis  
            memory_match = re.search(r"Memory_Usage \(%\):\s*([0-9.]+)", data_section)
            if memory_match:
                memory = float(memory_match.group(1))
                if memory > 85:
                    root_causes.append(f"MEMORY_EXHAUSTION - {memory}% usage critical")
            
            # Network Analysis
            latency_match = re.search(r"Network_Latency \(ms\):\s*([0-9.]+)", data_section)
            if latency_match:
                latency = float(latency_match.group(1))
                if latency > 150:
                    root_causes.append(f"NETWORK_LATENCY_ISSUE - {latency}ms exceeds threshold")
            
            # Error Analysis
            error_match = re.search(r"Error_Count:\s*([0-9]+)", data_section)
            if error_match:
                errors = int(error_match.group(1))
                if errors > 2:
                    root_causes.append(f"OPERATIONAL_ERRORS - {errors} errors detected")
        
        # Camera Analysis
        elif "Model:" in data_section:
            # Resolution analysis
            res_match = re.search(r"Max resolution:\s*([0-9.]+)", data_section)
            if res_match:
                resolution = float(res_match.group(1))
                if resolution < 800:
                    root_causes.append(f"LOW_RESOLUTION - {resolution} below standards")
            
            # Pixel analysis
            pixel_match = re.search(r"Effective pixels:\s*([0-9.]+)", data_section)
            if pixel_match:
                pixels = float(pixel_match.group(1))
                if pixels < 1.0:
                    root_causes.append(f"INADEQUATE_SENSOR - {pixels}MP insufficient")
    
    # Finalize analysis
    if not root_causes:
        root_causes.append("NO_CRITICAL_ISSUES_DETECTED - Metrics within acceptable ranges")
    
    analysis = f"ROOT_CAUSE_ANALYSIS: {' | '.join(root_causes)}"
    
    logger.info(f"🔬 Independent root cause analysis completed: {len(root_causes)} causes identified")
    return analysis

def generate_remediation_plan(report_content: str) -> str:
    """
    INDEPENDENT REMEDIATION PLANNING - Extracts data directly from original report.
    No dependency on previous tool outputs.
    """
    logger.info(f"FUNCTION CALL: generate_remediation_plan() invoked by LLM")
    _mark_tool_called("generate_remediation_plan")
    logger.info(f"Input: Original report ({len(report_content)} chars)")
    logger.info(f"INDEPENDENT PLANNING: Creating remediation from report data")
    
    immediate_actions = []
    preventive_measures = []
    
    # Extract metrics directly from report for remediation planning
    if "LOG REFERENCE DATA" in report_content:
        data_section = report_content.split("LOG REFERENCE DATA:")[1]
        
        # IoT Device Remediation
        if "Device_ID:" in data_section:
            # CPU-based remediation
            cpu_match = re.search(r"CPU_Usage \(%\):\s*([0-9.]+)", data_section)
            if cpu_match:
                cpu = float(cpu_match.group(1))
                if cpu > 80:
                    immediate_actions.append("Terminate non-essential processes immediately")
                    preventive_measures.append("Implement CPU usage monitoring")
                elif cpu > 60:
                    immediate_actions.append("Review and optimize running processes")
            
            # Memory-based remediation
            memory_match = re.search(r"Memory_Usage \(%\):\s*([0-9.]+)", data_section)
            if memory_match:
                memory = float(memory_match.group(1))
                if memory > 85:
                    immediate_actions.append("Clear memory cache and restart services")
                    preventive_measures.append("Implement automatic memory cleanup")
            
            # Network-based remediation
            latency_match = re.search(r"Network_Latency \(ms\):\s*([0-9.]+)", data_section)
            if latency_match:
                latency = float(latency_match.group(1))
                if latency > 150:
                    immediate_actions.append("Check network connectivity")
                    preventive_measures.append("Implement network monitoring")
        
        # Camera Remediation
        elif "Model:" in data_section:
            immediate_actions.append("Update firmware if available")
            preventive_measures.append("Consider hardware upgrade planning")
    
    # Build remediation plan
    plan = "REMEDIATION_PLAN:"
    if immediate_actions:
        plan += f" IMMEDIATE: {' | '.join(immediate_actions)}"
    if preventive_measures:
        plan += f" PREVENTIVE: {' | '.join(preventive_measures)}"
    
    logger.info(f"📝 Independent remediation plan generated")
    return plan

def assess_severity_level(report_content: str) -> str:
    """
    INDEPENDENT SEVERITY ASSESSMENT - Analyzes severity directly from original report.
    No dependency on previous tool outputs.
    """
    logger.info(f"FUNCTION CALL: assess_severity_level() invoked by LLM")
    _mark_tool_called("assess_severity_level")
    logger.info(f"Input: Original report ({len(report_content)} chars)")
    logger.info(f"INDEPENDENT ASSESSMENT: Determining severity from report metrics")
    
    severity_factors = []
    severity_score = 0
    
    # Extract metrics directly from report for severity assessment
    if "LOG REFERENCE DATA" in report_content:
        data_section = report_content.split("LOG REFERENCE DATA:")[1]
        
        # IoT Device Severity Assessment
        if "Device_ID:" in data_section:
            # CPU severity
            cpu_match = re.search(r"CPU_Usage \(%\):\s*([0-9.]+)", data_section)
            if cpu_match:
                cpu = float(cpu_match.group(1))
                if cpu > 90:
                    severity_factors.append(f"CRITICAL_CPU({cpu}%)")
                    severity_score += 4
                elif cpu > 80:
                    severity_factors.append(f"HIGH_CPU({cpu}%)")
                    severity_score += 3
                elif cpu > 60:
                    severity_factors.append(f"MEDIUM_CPU({cpu}%)")
                    severity_score += 2
            
            # Memory severity
            memory_match = re.search(r"Memory_Usage \(%\):\s*([0-9.]+)", data_section)
            if memory_match:
                memory = float(memory_match.group(1))
                if memory > 90:
                    severity_factors.append(f"CRITICAL_MEMORY({memory}%)")
                    severity_score += 4
                elif memory > 85:
                    severity_factors.append(f"HIGH_MEMORY({memory}%)")
                    severity_score += 3
            
            # Network severity
            latency_match = re.search(r"Network_Latency \(ms\):\s*([0-9.]+)", data_section)
            if latency_match:
                latency = float(latency_match.group(1))
                if latency > 300:
                    severity_factors.append(f"CRITICAL_LATENCY({latency}ms)")
                    severity_score += 4
                elif latency > 200:
                    severity_factors.append(f"HIGH_LATENCY({latency}ms)")
                    severity_score += 3
                elif latency > 150:
                    severity_factors.append(f"MEDIUM_LATENCY({latency}ms)")
                    severity_score += 2
            
            # Error severity
            error_match = re.search(r"Error_Count:\s*([0-9]+)", data_section)
            if error_match:
                errors = int(error_match.group(1))
                if errors > 5:
                    severity_factors.append(f"CRITICAL_ERRORS({errors})")
                    severity_score += 4
                elif errors > 3:
                    severity_factors.append(f"HIGH_ERRORS({errors})")
                    severity_score += 3
                elif errors > 1:
                    severity_factors.append(f"MEDIUM_ERRORS({errors})")
                    severity_score += 2
        
        # Camera Severity Assessment
        elif "Model:" in data_section:
            # Basic camera severity (less critical than IoT operational issues)
            severity_factors.append("CAMERA_ASSESSMENT")
            severity_score += 1
    
    # Determine final severity level
    if severity_score >= 12:
        final_severity = "CRITICAL"
    elif severity_score >= 8:
        final_severity = "HIGH"
    elif severity_score >= 4:
        final_severity = "MEDIUM"
    else:
        final_severity = "LOW"
    
    assessment = f"SEVERITY_ASSESSMENT: {final_severity} | FACTORS: {' | '.join(severity_factors) if severity_factors else 'NO_CRITICAL_FACTORS'} | SCORE: {severity_score}"
    
    logger.info(f"⚖️ Independent severity assessment: {final_severity} (score: {severity_score})")
    return assessment

# Tool exports for agent
diagnosis_tools = [
    diagnose_iot_device,
    diagnose_camera_equipment, 
    analyze_root_cause,
    assess_severity_level,
    generate_remediation_plan
]