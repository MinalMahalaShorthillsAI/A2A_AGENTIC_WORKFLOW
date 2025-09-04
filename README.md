# A2A Agentic Workflow - Distributed Multi-Agent System

A production-ready distributed multi-agent system demonstrating Agent-to-Agent (A2A) communication for IoT and Camera device failure prediction, diagnosis, and automated remediation across multiple machines.

## 🏗️ Architecture Overview

This system implements a **circular workflow** with three specialized agents running on separate machines:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MACHINE 1     │    │   MACHINE 2     │    │   MACHINE 3     │
│                 │    │                 │    │                 │
│  Log Analysis   │───▶│   Diagnosis     │───▶│  Remediation    │
│     Agent       │    │     Agent       │    │     Agent       │
│                 │◀───┼─────────────────┼────┘                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Agent Flow:
1. **Agent 1 (Log Analysis)**: Processes IoT/Camera data, classifies severity (LOW/MEDIUM/HIGH/CRITICAL)
2. **Agent 2 (Diagnosis)**: Receives MEDIUM+ severity issues, performs root cause analysis
3. **Agent 3 (Remediation)**: Executes automated fixes and sends results back to Agent 1

## 🔧 Technology Stack

- **Framework**: Google ADK (Agent Development Kit)
- **LLM**: Gemini-1.5-pro, Gemini-1.5-flash
- **Communication**: HTTP-based A2A protocol
- **Languages**: Python 3.x
- **Web Framework**: FastAPI with Uvicorn
- **Data Format**: CSV processing, JSON responses

## 📁 Project Structure

```
Real_3_agent_system/
├── machine1_log_analysis/          # Agent 1: Log Analysis
│   ├── agent_gemini.py            # Main agent implementation
│   ├── a2a_server.py              # HTTP server for A2A communication
│   ├── tools.py                   # Analysis tools
│   ├── logger_config.py           # Logging configuration
│   └── logs/
│       └── log_analysis_agent.log
├── machine2_diagnosis/             # Agent 2: Diagnosis
│   ├── agent_gemini.py            # Diagnosis agent
│   ├── a2a_server.py              # A2A communication server
│   ├── tools.py                   # Diagnostic tools
│   └── logs/
│       └── diagnosis_agent.log
├── machine3_remediation/           # Agent 3: Remediation
│   ├── agent_gemini.py            # Remediation agent
│   ├── a2a_server.py              # A2A communication server
│   ├── tools.py                   # Remediation tools
│   └── logs/
│       └── remediation_agent.log
├── test_files/                    # Testing and validation
│   └── test_workflow_simple.py    # Complete workflow test
├── datasets/                      # Sample data
│   ├── IoT_Failure_Prediction_Dataset.csv
│   └── camera_dataset.csv
├── config.py                      # Machine IP/port configuration
├── cost_tracker.py               # LLM cost monitoring
└── requirements.txt               # Dependencies
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed on all machines
2. **Google AI API Key** for Gemini access
3. **Network connectivity** between machines

### Installation

1. **Clone the repository on all machines:**
```bash
git clone <repository-url>
cd Real_3_agent_system
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
```bash
export GEMINI_API_KEY="your-gemini-api-key"
```

4. **Update machine configurations in `config.py`:**
```python
MACHINE1_IP = "192.168.1.100"  # Agent 1 IP
MACHINE1_PORT = "8001"
MACHINE2_IP = "192.168.1.101"  # Agent 2 IP  
MACHINE2_PORT = "8002"
MACHINE3_IP = "192.168.1.102"  # Agent 3 IP
MACHINE3_PORT = "8003"
```

### Starting the Agents

**On Machine 1 (Log Analysis):**
```bash
cd machine1_log_analysis
python a2a_server.py
```

**On Machine 2 (Diagnosis):**
```bash
cd machine2_diagnosis
python a2a_server.py
```

**On Machine 3 (Remediation):**
```bash
cd machine3_remediation
python a2a_server.py
```

### Running the Workflow Test

```bash
cd test_files
python test_workflow_simple.py
```

## 📊 Expected Output

```
================================================================================
DISTRIBUTED AGENT WORKFLOW EXECUTION
================================================================================
DEMO STATUS: Processing 6 records through 3-agent pipeline...
Agent 1: Analyzing data and making routing decisions
Agent 2: Diagnosing issues for medium/high severity items
Agent 3: Executing remediation actions
================================================================================

WORKFLOW EXECUTION RESULTS
================================================================================
WORKFLOW COMPLETED SUCCESSFULLY
Status: completed

SEVERITY ANALYSIS:
   LOW: 3 records (50.0%)
   MEDIUM: 2 records (33.3%)
   HIGH: 1 records (16.7%)
   CRITICAL: 0 records (0.0%)

PROCESSING SUMMARY:
   Total Records Processed: 6
   Records with MEDIUM/HIGH/CRITICAL severity: 3
   Records handled by Agent 1 only (LOW): 3
   Complete flows (Agent 1→2→3→1): 3

AGENT COMMUNICATION:
   Agent 1 → Agent 2 (Diagnosis): 3 requests forwarded.
   Agent 2 → Agent 3 (Remediation): 3 requests forwarded.
   Agent 3 → Agent 1 (Results): 3 remediation reports received

DETAILED REMEDIATION REPORTS
================================================================================
Found 3 detailed remediation reports:

REMEDIATION REPORT #1:
   Remediation Status: SUCCESS
   Device Type: IoT
   Actions Taken: [System Restart, Configuration Update]
   Results Summary: Device successfully remediated

WORKFLOW STATUS:
   ✅ OPTIMAL - All 3/3 expected flows completed
   Status: PASS - Perfect distributed workflow execution
```

## 🔧 Key Features

### ✅ **Multi-Agent Coordination**
- Distributed processing across 3 specialized agents
- Automatic A2A communication and routing
- Circular workflow with result confirmation

### ✅ **Intelligent Severity Classification**
- Automatic triage of IoT/Camera issues
- LOW severity handled by Agent 1 only
- MEDIUM/HIGH/CRITICAL escalated through full pipeline

### ✅ **Automated Remediation**
- System restarts and configuration updates
- Sensor calibration and threshold adjustments
- Comprehensive result reporting

### ✅ **Production Monitoring**
- Real-time logging on all agents
- HTTP request/response tracking
- Cost monitoring for LLM usage
- Comprehensive workflow validation

## 🛠️ Agent Capabilities

### Agent 1 (Log Analysis)
- **CSV data processing** for IoT and Camera datasets
- **Severity classification** using Gemini LLM
- **Routing decisions** based on severity levels
- **A2A communication** initiation to downstream agents

### Agent 2 (Diagnosis)
- **Root cause analysis** for device failures
- **Diagnostic recommendations** generation
- **Issue classification** and priority assessment
- **Automated forwarding** to remediation agent

### Agent 3 (Remediation)
- **System restart** automation
- **Configuration adjustments** (timeouts, thresholds)
- **Sensor calibration** for IoT devices
- **Result validation** and reporting

## 🔄 Workflow Logic

1. **Data Ingestion**: Agent 1 receives IoT/Camera CSV data
2. **Severity Analysis**: LLM classifies each record (LOW/MEDIUM/HIGH/CRITICAL)
3. **Routing Decision**: 
   - LOW severity: Handled locally by Agent 1
   - MEDIUM+ severity: Forwarded to Agent 2 via A2A
4. **Diagnosis**: Agent 2 analyzes issues and forwards to Agent 3
5. **Remediation**: Agent 3 executes fixes and reports back to Agent 1
6. **Confirmation**: Agent 1 receives and logs final results

## 📈 Performance Metrics

- **Throughput**: Processes 6 records in ~60 seconds
- **Success Rate**: 100% completion for valid data
- **Latency**: <20 seconds per A2A hop
- **Scalability**: Horizontal scaling via additional machine instances

## 🔒 Security & Configuration

- **API Key Management**: Secure Gemini API key handling
- **Network Security**: HTTP-based communication (HTTPS recommended for production)
- **Logging**: Comprehensive audit trails on all agents
- **Error Handling**: Graceful degradation and retry logic

## 🚨 Troubleshooting

### Common Issues:

1. **Agent Not Responding**
   - Verify agent is running: `curl http://MACHINE_IP:PORT/.well-known/agent-card.json`
   - Check firewall/network connectivity
   - Review agent logs for errors

2. **A2A Communication Failures**
   - Confirm IP addresses in `config.py`
   - Verify port availability
   - Check GEMINI_API_KEY configuration

3. **Incomplete Workflows**
   - Monitor agent terminals for real-time status
   - Check log files for timing issues
   - Verify all 3 agents are running

## 📝 Development Notes

- **Built with Google ADK**: Leverages official Agent Development Kit patterns
- **Production Ready**: Includes comprehensive logging, monitoring, and error handling
- **Extensible**: Easy to add new agents or modify workflow logic
- **Tested**: Includes validation scripts for end-to-end testing

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-capability`
3. Test across all three agents
4. Submit pull request with detailed description

## 📄 License

[Your License Here]

---

**For support or questions, please contact [Your Contact Information]**