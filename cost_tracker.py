# Cost Tracking Utility for Gemini Model Usage
# Tracks token usage and calculates costs per request/transaction

import time
import uuid
from datetime import datetime
from typing import Dict, Optional, Any
import json
import logging

# Gemini Pricing (as of 2024) - Update these rates as needed
GEMINI_PRICING = {
    "gemini-1.5-flash": {
        "input_tokens_per_1k": 0.000075,   # $0.075 per 1K input tokens
        "output_tokens_per_1k": 0.0003,    # $0.30 per 1K output tokens
    },
    "gemini-1.5-pro": {
        "input_tokens_per_1k": 0.00125,    # $1.25 per 1K input tokens  
        "output_tokens_per_1k": 0.005,     # $5.00 per 1K output tokens
    }
}

class CostTracker:
    def __init__(self, agent_name: str, logger: logging.Logger):
        self.agent_name = agent_name
        self.logger = logger
        self.session_costs = []
        self.total_session_cost = 0.0
        
    def generate_transaction_id(self) -> str:
        """Generate unique transaction ID for each request"""
        return f"{self.agent_name}_{int(time.time())}_{str(uuid.uuid4())[:8]}"
    
    def calculate_cost(self, model_name: str, input_tokens: int, output_tokens: int) -> Dict[str, Any]:
        """Calculate cost based on token usage and model pricing"""
        
        # Default to flash if model not found
        pricing_key = "gemini-1.5-flash"
        if "pro" in model_name.lower():
            pricing_key = "gemini-1.5-pro"
        elif "flash" in model_name.lower():
            pricing_key = "gemini-1.5-flash"
            
        pricing = GEMINI_PRICING.get(pricing_key, GEMINI_PRICING["gemini-1.5-flash"])
        
        # Calculate costs
        input_cost = (input_tokens / 1000) * pricing["input_tokens_per_1k"]
        output_cost = (output_tokens / 1000) * pricing["output_tokens_per_1k"]
        total_cost = input_cost + output_cost
        
        return {
            "model_used": pricing_key,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "input_cost_usd": round(input_cost, 6),
            "output_cost_usd": round(output_cost, 6),
            "total_cost_usd": round(total_cost, 6),
            "pricing_rate": pricing
        }
    
    def log_request_cost(self, transaction_id: str, model_name: str, 
                        input_tokens: int, output_tokens: int, 
                        request_type: str = "standard", 
                        additional_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Log cost for a single request/transaction"""
        
        timestamp = datetime.now().isoformat()
        cost_info = self.calculate_cost(model_name, input_tokens, output_tokens)
        
        # Build comprehensive cost log entry
        cost_entry = {
            "timestamp": timestamp,
            "transaction_id": transaction_id,
            "agent_name": self.agent_name,
            "request_type": request_type,
            **cost_info
        }
        
        if additional_context:
            cost_entry["context"] = additional_context
            
        # Add to session tracking
        self.session_costs.append(cost_entry)
        self.total_session_cost += cost_info["total_cost_usd"]
        
        # Log the cost information
        self.logger.info(
            f"COST_TRACKING | {self.agent_name} | "
            f"TXN: {transaction_id} | "
            f"MODEL: {cost_info['model_used']} | "
            f"TOKENS: {cost_info['input_tokens']}→{cost_info['output_tokens']} | "
            f"COST: ${cost_info['total_cost_usd']:.6f} | "
            f"SESSION_TOTAL: ${self.total_session_cost:.6f}"
        )
        
        # Detailed cost breakdown log
        self.logger.info(
            f"COST_BREAKDOWN | {transaction_id} | "
            f"Input: {cost_info['input_tokens']} tokens (${cost_info['input_cost_usd']:.6f}) | "
            f"Output: {cost_info['output_tokens']} tokens (${cost_info['output_cost_usd']:.6f}) | "
            f"Rate: ${cost_info['pricing_rate']['input_tokens_per_1k']:.6f}/1K in, "
            f"${cost_info['pricing_rate']['output_tokens_per_1k']:.6f}/1K out"
        )
        
        return cost_entry
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get summary of costs for current session"""
        if not self.session_costs:
            return {"total_requests": 0, "total_cost_usd": 0.0, "average_cost_per_request": 0.0}
            
        total_input_tokens = sum(entry["input_tokens"] for entry in self.session_costs)
        total_output_tokens = sum(entry["output_tokens"] for entry in self.session_costs)
        
        return {
            "agent_name": self.agent_name,
            "total_requests": len(self.session_costs),
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "total_tokens": total_input_tokens + total_output_tokens,
            "total_cost_usd": round(self.total_session_cost, 6),
            "average_cost_per_request": round(self.total_session_cost / len(self.session_costs), 6),
            "session_start": self.session_costs[0]["timestamp"] if self.session_costs else None,
            "session_end": self.session_costs[-1]["timestamp"] if self.session_costs else None
        }
    
    def log_session_summary(self):
        """Log session cost summary"""
        summary = self.get_session_summary()
        
        self.logger.info(
            f"📈 SESSION_SUMMARY | {self.agent_name} | "
            f"REQUESTS: {summary['total_requests']} | "
            f"TOTAL_COST: ${summary['total_cost_usd']:.6f} | "
            f"AVG_PER_REQUEST: ${summary['average_cost_per_request']:.6f} | "
            f"TOTAL_TOKENS: {summary['total_tokens']}"
        )

# Global cost trackers for each agent
_cost_trackers: Dict[str, CostTracker] = {}

def get_cost_tracker(agent_name: str, logger: logging.Logger) -> CostTracker:
    """Get or create cost tracker for an agent"""
    if agent_name not in _cost_trackers:
        _cost_trackers[agent_name] = CostTracker(agent_name, logger)
    return _cost_trackers[agent_name]

def estimate_tokens(text: str) -> int:
    """Rough estimation of tokens from text (approximate)"""
    # Rough approximation: ~4 characters per token for English text
    return max(1, len(text) // 4)

def log_all_session_summaries():
    """Log session summaries for all active cost trackers"""
    for tracker in _cost_trackers.values():
        tracker.log_session_summary()
