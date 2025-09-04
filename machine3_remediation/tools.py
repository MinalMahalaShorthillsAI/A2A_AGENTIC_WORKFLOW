# Device-Specific Remediation Tools for IoT and Camera Systems

import os
import json
import asyncio
from datetime import datetime
import random

# try:
#     from .logger_config import logger
# except ImportError:
#     from logger_config import logger
from logger_config import logger
import sys
sys.path.append('..')
from config import MACHINE1_IP, MACHINE1_PORT, MACHINE2_IP, MACHINE2_PORT, MACHINE3_IP, MACHINE3_PORT

# Global counter for tracking tool calls in this session
_tool_call_counter = 0

def get_tool_call_counter():
    """Get current tool call count"""
    return _tool_call_counter

def reset_tool_call_counter():
    """Reset tool call counter for new request"""
    global _tool_call_counter
    _tool_call_counter = 0

def _increment_tool_counter():
    """Increment tool call counter"""
    global _tool_call_counter
    _tool_call_counter += 1
    logger.info(f"TOOL_CALL_COUNT: {_tool_call_counter}")

# ============== IoT DEVICE REMEDIATION FUNCTIONS ==============

def restart_iot_system(device_id: str, device_type: str):
    """
    Restarts an IoT device system to resolve performance and connectivity issues.
    """
    _increment_tool_counter()
    logger.info(f"MOCK: Restarting IoT system for device {device_id}")
    
    # Simulate restart success/failure
    success = random.choice([True, True, True, False])  # 75% success rate
    
    if success:
        return {
            "status": "iot_system_restarted",
            "device_id": device_id,
            "device_type": device_type,
            "timestamp": datetime.now().isoformat(),
            "action": "System Restart",
            "message": f"IoT device {device_id} system restarted successfully. CPU and memory cleared, network reconnected.",
            "result": "SUCCESS",
            "estimated_downtime": "30 seconds"
        }
    else:
        return {
            "status": "iot_restart_failed",
            "device_id": device_id,
            "device_type": device_type,
            "timestamp": datetime.now().isoformat(),
            "action": "System Restart",
            "message": f"IoT device {device_id} restart failed. Hardware intervention may be required.",
            "result": "FAILURE",
            "error_code": "SYS_RESTART_TIMEOUT"
        }

def adjust_iot_settings(device_id: str, setting_type: str, new_value: str):
    """
    Adjusts configuration settings on IoT devices (sampling rate, thresholds, etc.).
    """
    _increment_tool_counter()
    logger.info(f"MOCK: Adjusting IoT setting {setting_type} to {new_value} for device {device_id}")
    
    # Common IoT settings adjustments
    setting_configs = {
        "sampling_rate": {"unit": "Hz", "typical_range": "1-100"},
        "cpu_threshold": {"unit": "%", "typical_range": "70-95"},
        "memory_threshold": {"unit": "%", "typical_range": "80-95"},
        "network_timeout": {"unit": "ms", "typical_range": "1000-10000"},
        "sensor_calibration": {"unit": "offset", "typical_range": "-10 to +10"}
    }
    
    config = setting_configs.get(setting_type, {"unit": "value", "typical_range": "varies"})
    
    return {
        "status": "iot_setting_adjusted",
        "device_id": device_id,
        "setting_type": setting_type,
        "new_value": new_value,
        "unit": config["unit"],
        "timestamp": datetime.now().isoformat(),
        "action": "Configuration Update",
        "message": f"IoT device {device_id} {setting_type} adjusted to {new_value} {config['unit']}",
        "result": "SUCCESS",
        "previous_value": "auto-detected"
    }

def calibrate_iot_sensors(device_id: str, sensor_types: str):
    """
    Calibrates IoT device sensors to improve data accuracy.
    """
    _increment_tool_counter()
    logger.info(f"MOCK: Calibrating IoT sensors {sensor_types} for device {device_id}")
    
    sensors = sensor_types.split(",")
    calibration_results = []
    
    for sensor in sensors:
        sensor = sensor.strip()
        # Simulate calibration offset
        offset = round(random.uniform(-2.5, 2.5), 2)
        accuracy_improvement = round(random.uniform(5, 15), 1)
        
        calibration_results.append({
            "sensor_type": sensor,
            "calibration_offset": offset,
            "accuracy_improvement": f"{accuracy_improvement}%",
            "status": "calibrated"
        })
    
    return {
        "status": "iot_sensors_calibrated",
        "device_id": device_id,
        "sensors_calibrated": calibration_results,
        "timestamp": datetime.now().isoformat(),
        "action": "Sensor Calibration",
        "message": f"IoT device {device_id} sensors calibrated: {len(sensors)} sensors optimized",
        "result": "SUCCESS",
        "total_sensors": len(sensors)
    }

# ============== CAMERA SYSTEM REMEDIATION FUNCTIONS ==============

def restart_camera_system(camera_id: str, camera_model: str = "Camera"):
    """
    Restarts camera system to resolve imaging and performance issues.
    """
    _increment_tool_counter()
    logger.info(f"MOCK: Restarting camera system for {camera_id}")
    
    # Simulate restart with different outcomes
    success = random.choice([True, True, True, False])  # 75% success rate
    
    if success:
        return {
            "status": "camera_system_restarted",
            "camera_id": camera_id,
            "camera_model": camera_model,
            "timestamp": datetime.now().isoformat(),
            "action": "Camera System Restart",
            "message": f"Camera {camera_id} system restarted successfully. Image processor cleared, autofocus reset.",
            "result": "SUCCESS",
            "estimated_downtime": "45 seconds",
            "systems_reset": ["image_processor", "autofocus", "exposure_control"]
        }
    else:
        return {
            "status": "camera_restart_failed",
            "camera_id": camera_id,
            "camera_model": camera_model,
            "timestamp": datetime.now().isoformat(),
            "action": "Camera System Restart",
            "message": f"Camera {camera_id} restart failed. Lens mechanism may be stuck.",
            "result": "FAILURE",
            "error_code": "CAM_RESTART_BLOCKED"
        }

def adjust_camera_brightness(camera_id: str, brightness_level: str, auto_adjust: bool = True):
    """
    Adjusts camera brightness and exposure settings for optimal imaging.
    """
    _increment_tool_counter()
    logger.info(f"MOCK: Adjusting camera brightness to {brightness_level} for {camera_id}")
    
    # Convert brightness level to technical values
    brightness_mapping = {
        "low": {"iso": 100, "exposure": "1/60", "aperture": "f/8"},
        "medium": {"iso": 400, "exposure": "1/30", "aperture": "f/5.6"},
        "high": {"iso": 800, "exposure": "1/15", "aperture": "f/4"},
        "auto": {"iso": "auto", "exposure": "auto", "aperture": "auto"}
    }
    
    settings = brightness_mapping.get(brightness_level.lower(), brightness_mapping["medium"])
    
    return {
        "status": "camera_brightness_adjusted",
        "camera_id": camera_id,
        "brightness_level": brightness_level,
        "iso_setting": settings["iso"],
        "exposure_time": settings["exposure"],
        "aperture": settings["aperture"],
        "auto_adjust_enabled": auto_adjust,
        "timestamp": datetime.now().isoformat(),
        "action": "Brightness Adjustment",
        "message": f"Camera {camera_id} brightness adjusted to {brightness_level} level with optimized exposure settings",
        "result": "SUCCESS"
    }

def adjust_camera_focus(camera_id: str, focus_mode: str = "auto", focus_distance: str = "infinity"):
    """
    Adjusts camera focus settings to improve image sharpness.
    """
    _increment_tool_counter()
    logger.info(f"MOCK: Adjusting camera focus to {focus_mode} mode for {camera_id}")
    
    # Focus adjustment simulation
    focus_results = {
        "auto": {"method": "continuous_af", "accuracy": "95%", "speed": "fast"},
        "manual": {"method": "manual_ring", "accuracy": "99%", "speed": "manual"},
        "macro": {"method": "close_focus", "accuracy": "98%", "speed": "slow"},
        "sport": {"method": "predictive_af", "accuracy": "92%", "speed": "very_fast"}
    }
    
    result = focus_results.get(focus_mode.lower(), focus_results["auto"])
    
    return {
        "status": "camera_focus_adjusted", 
        "camera_id": camera_id,
        "focus_mode": focus_mode,
        "focus_distance": focus_distance,
        "focus_method": result["method"],
        "focus_accuracy": result["accuracy"],
        "focus_speed": result["speed"],
        "timestamp": datetime.now().isoformat(),
        "action": "Focus Adjustment",
        "message": f"Camera {camera_id} focus adjusted to {focus_mode} mode with {result['accuracy']} accuracy",
        "result": "SUCCESS"
    }

# ============== TOOLS LIST ==============

remediation_tools = [
    restart_iot_system,
    adjust_iot_settings,
    calibrate_iot_sensors,
    restart_camera_system,
    adjust_camera_brightness,
    adjust_camera_focus
]
