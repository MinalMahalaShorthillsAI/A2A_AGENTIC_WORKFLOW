# machine1_log_analysis/tools.py
from logger_config import logger

def analyze_device_metrics(device_id: str, cpu_usage: float, memory_usage: float) -> str:
    """
    Analyze basic device metrics for anomalies.
    
    Args:
        device_id: Device identifier
        cpu_usage: CPU usage percentage (0-100)
        memory_usage: Memory usage percentage (0-100)
    
    Returns:
        Analysis result as string
    """
    logger.info(f"TOOL: analyze_device_metrics() called for device {device_id}")
    
    issues = []
    
    if cpu_usage > 60:
        issues.append(f"HIGH CPU usage: {cpu_usage}%")
    if memory_usage > 60:
        issues.append(f"HIGH memory usage: {memory_usage}%")
    
    if issues:
        severity = "HIGH" if cpu_usage > 90 or memory_usage > 90 else "MEDIUM"
        result = f"Device {device_id}: {severity} severity. Issues: {', '.join(issues)}"
    else:
        severity = "LOW"
        result = f"Device {device_id}: {severity} severity. Metrics within normal range."
    
    logger.info(f"Analysis result: {severity} severity")
    return result


def check_device_health(device_id: str, temperature: float, battery_level: float) -> str:
    """
    Check overall device health status.
    
    Args:
        device_id: Device identifier  
        temperature: Device temperature in Celsius
        battery_level: Battery level percentage (0-100)
    
    Returns:
        Health status as string
    """
    logger.info(f"TOOL: check_device_health() called for device {device_id}")
    
    issues = []
    
    if temperature > 60:
        issues.append(f"HIGH temperature: {temperature}°C")
    if battery_level < 20:
        issues.append(f"LOW battery: {battery_level}%")
    
    if issues:
        severity = "CRITICAL" if temperature > 70 or battery_level < 10 else "MEDIUM"
        result = f"Device {device_id}: {severity} health issues. {', '.join(issues)}"
    else:
        result = f"Device {device_id}: GOOD health status."
    
    logger.info(f"Health status: {result}")
    return result


def analyze_network_performance(device_id: str, latency: float, packet_loss: float) -> str:
    """
    Analyze network performance metrics for connectivity issues.
    
    Args:
        device_id: Device identifier
        latency: Network latency in milliseconds
        packet_loss: Packet loss percentage (0-100)
    
    Returns:
        Network performance analysis as string
    """
    logger.info(f"TOOL: analyze_network_performance() called for device {device_id}")
    
    issues = []
    
    if latency > 300:
        issues.append(f"HIGH latency: {latency}ms")
    elif latency > 150:
        issues.append(f"ELEVATED latency: {latency}ms")
    
    if packet_loss > 3:
        issues.append(f"HIGH packet loss: {packet_loss}%")
    elif packet_loss > 1:
        issues.append(f"ELEVATED packet loss: {packet_loss}%")
    
    if issues:
        severity = "HIGH" if latency > 500 or packet_loss > 5 else "MEDIUM"
        result = f"Device {device_id}: {severity} network issues. {', '.join(issues)}"
    else:
        severity = "GOOD"
        result = f"Device {device_id}: {severity} network performance."
    
    logger.info(f"Network analysis: {severity}")
    return result


def analyze_operational_metrics(device_id: str, uptime_hrs: float, workload_intensity: int, error_count: int, failure_type: int) -> str:
    """
    Analyze operational metrics for device stability and reliability issues.
    
    Args:
        device_id: Device identifier
        uptime_hrs: Device uptime in hours
        workload_intensity: Processing workload level (numeric scale)
        error_count: Number of errors/failures detected
        failure_type: Type/category of failure (numeric code)
    
    Returns:
        Operational analysis as string
    """
    logger.info(f"TOOL: analyze_operational_metrics() called for device {device_id}")
    
    issues = []
    risk_factors = []
    
    # Analyze uptime patterns
    if uptime_hrs < 24:
        issues.append(f"SHORT uptime: {uptime_hrs:.1f} hours (recent restart)")
    elif uptime_hrs > 720:  # >30 days
        risk_factors.append(f"EXTENDED uptime: {uptime_hrs:.1f} hours (may need maintenance)")
    
    # Analyze workload intensity
    if workload_intensity >= 8:
        issues.append(f"EXTREME workload: intensity {workload_intensity}")
    elif workload_intensity >= 6:
        issues.append(f"HIGH workload: intensity {workload_intensity}")
    elif workload_intensity >= 4:
        risk_factors.append(f"MODERATE workload: intensity {workload_intensity}")
    
    # Analyze error patterns
    if error_count > 20:
        issues.append(f"CRITICAL error rate: {error_count} errors")
    elif error_count > 10:
        issues.append(f"HIGH error rate: {error_count} errors")
    elif error_count > 5:
        risk_factors.append(f"ELEVATED error rate: {error_count} errors")
    elif error_count > 0:
        risk_factors.append(f"Some errors detected: {error_count} errors")
    
    # Analyze failure type (higher numbers typically indicate more severe failure categories)
    if failure_type >= 8:
        issues.append(f"SEVERE failure type: {failure_type}")
    elif failure_type >= 5:
        issues.append(f"SIGNIFICANT failure type: {failure_type}")
    elif failure_type >= 3:
        risk_factors.append(f"Moderate failure type: {failure_type}")
    elif failure_type > 0:
        risk_factors.append(f"Minor failure type: {failure_type}")
    
    # Determine overall operational status
    if issues:
        severity = "CRITICAL" if (error_count > 20 or workload_intensity >= 8 or failure_type >= 8) else "HIGH"
        result = f"Device {device_id}: {severity} operational issues. {', '.join(issues)}"
        if risk_factors:
            result += f" Additional concerns: {', '.join(risk_factors)}"
    elif risk_factors:
        severity = "MEDIUM"
        result = f"Device {device_id}: {severity} operational concerns. {', '.join(risk_factors)}"
    else:
        severity = "GOOD"
        result = f"Device {device_id}: {severity} operational status."
    
    logger.info(f"Operational analysis: {severity}")
    return result



# Tool registry for Log Analysis Agent - ADK compliant simple tools only
log_analysis_tools = [
    analyze_device_metrics,
    check_device_health,
    analyze_network_performance,
    analyze_operational_metrics,
]


# --------------------
# Camera analysis tools
# --------------------

def analyze_camera_core_specs(model: str, max_resolution: float, effective_pixels: float, zoom_wide: float, zoom_tele: float) -> str:
    """
    Analyze core camera specifications for capability and potential issues.

    Args:
        model: Camera model name
        max_resolution: Maximum image resolution (e.g., 4000.0)
        effective_pixels: Effective megapixels (e.g., 12.0)
        zoom_wide: Wide-end focal length equivalent (mm)
        zoom_tele: Tele-end focal length equivalent (mm)

    Returns:
        Text summary of core spec assessment
    """
    logger.info(f"TOOL: analyze_camera_core_specs() called for model {model}")

    findings = []

    # Basic capability checks
    if effective_pixels < 2.0:
        findings.append(f"Very low effective pixels: {effective_pixels}MP")
    elif effective_pixels < 6.0:
        findings.append(f"Low effective pixels: {effective_pixels}MP")

    if max_resolution < 1600:
        findings.append(f"Low max resolution: {max_resolution}")

    # Zoom coverage
    if zoom_tele - zoom_wide >= 200:
        findings.append(f"Large zoom range: {zoom_wide}-{zoom_tele}mm")
    elif zoom_tele - zoom_wide <= 20 and zoom_tele > 0 and zoom_wide > 0:
        findings.append(f"Limited zoom range: {zoom_wide}-{zoom_tele}mm")

    if findings:
        result = f"Model {model}: SPEC considerations. {', '.join(findings)}"
    else:
        result = f"Model {model}: Specs look balanced for general use."

    logger.info("Camera core specs analysis completed")
    return result


def assess_camera_value(model: str, release_year: int, price: float, effective_pixels: float) -> str:
    """
    Assess camera value based on age, price, and effective pixels.

    Args:
        model: Camera model name
        release_year: Four digit year (e.g., 2007)
        price: Price in same units as dataset
        effective_pixels: Effective megapixels

    Returns:
        Text summary of value assessment
    """
    logger.info(f"TOOL: assess_camera_value() called for model {model}")

    concerns = []
    year = int(release_year)

    if year <= 2000 and price > 500:
        concerns.append("Very old generation with high price")
    elif year <= 2005 and price > 1000:
        concerns.append("Old generation likely overpriced")

    if effective_pixels < 3 and price > 300:
        concerns.append("Low megapixels for the price")

    if concerns:
        result = f"Model {model}: VALUE concerns. {', '.join(concerns)}"
    else:
        result = f"Model {model}: Value appears reasonable given year and specs."

    logger.info("Camera value assessment completed")
    return result


def evaluate_camera_portability(model: str, weight_g: float, dimensions: str = "") -> str:
    """
    Evaluate portability based on weight and optional dimensions string.

    Args:
        model: Camera model name
        weight_g: Weight including batteries (grams)
        dimensions: Optional dimensions string from dataset

    Returns:
        Text summary of portability assessment
    """
    logger.info(f"TOOL: evaluate_camera_portability() called for model {model}")

    notes = []

    if weight_g >= 800:
        notes.append(f"Heavy body: {weight_g}g")
    elif weight_g >= 500:
        notes.append(f"Moderate weight: {weight_g}g")
    elif weight_g > 0:
        notes.append(f"Lightweight: {weight_g}g")
    else:
        notes.append("Weight not specified")

    if dimensions:
        notes.append(f"Dimensions: {dimensions}")

    result = f"Model {model}: PORTABILITY assessment. {', '.join(notes)}"
    logger.info("Camera portability evaluation completed")
    return result


# Extend registry with camera tools so the LLM can select them when Camera schema is detected
log_analysis_tools.extend([
    analyze_camera_core_specs,
    assess_camera_value,
    evaluate_camera_portability,
])
