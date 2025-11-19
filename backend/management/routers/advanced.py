from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime, timedelta
import random
import json
import os
from ..schemas.heartbeat import NFHeartbeat, NFHeartbeatList, NFStatus
from ..schemas.logs import LogEntry, LogList
from ..schemas.timeline import PDUSessionTimeline, PDUSessionTimelineList
from ..schemas.alerts import Alert, AlertList, AlertType, AlertSeverity

router = APIRouter(prefix="/mgmt", tags=["advanced"])

# Mock data for NF Heartbeats
@router.get("/nfs/heartbeat", response_model=NFHeartbeatList)
async def get_nf_heartbeats():
    """Get heartbeat status of all network functions"""
    heartbeats = [
        NFHeartbeat(
            name="amf-01",
            type="AMF",
            status=NFStatus.UP,
            last_heartbeat=datetime.utcnow() - timedelta(seconds=random.randint(1, 30)),
            endpoint="127.0.0.1:8001"
        ),
        NFHeartbeat(
            name="smf-01",
            type="SMF",
            status=NFStatus.UP,
            last_heartbeat=datetime.utcnow() - timedelta(seconds=random.randint(1, 30)),
            endpoint="127.0.0.1:8005"
        ),
        NFHeartbeat(
            name="upf-01",
            type="UPF",
            status=NFStatus.UP,
            last_heartbeat=datetime.utcnow() - timedelta(seconds=random.randint(1, 30)),
            endpoint="127.0.0.1:8004"
        ),
        NFHeartbeat(
            name="ausf-01",
            type="AUSF",
            status=NFStatus.UP,
            last_heartbeat=datetime.utcnow() - timedelta(seconds=random.randint(1, 30)),
            endpoint="127.0.0.1:8010"
        ),
        NFHeartbeat(
            name="udm-01",
            type="UDM",
            status=NFStatus.UP,
            last_heartbeat=datetime.utcnow() - timedelta(seconds=random.randint(1, 30)),
            endpoint="127.0.0.1:8010"
        ),
        NFHeartbeat(
            name="nrf-01",
            type="NRF",
            status=NFStatus.UP,
            last_heartbeat=datetime.utcnow() - timedelta(seconds=random.randint(1, 30)),
            endpoint="127.0.0.1:8000"
        ),
        NFHeartbeat(
            name="nssf-01",
            type="NSSF",
            status=NFStatus.UNREACHABLE if random.random() > 0.8 else NFStatus.UP,
            last_heartbeat=datetime.utcnow() - timedelta(seconds=random.randint(60, 300)) if random.random() > 0.8 else datetime.utcnow() - timedelta(seconds=random.randint(1, 30)),
            endpoint="127.0.0.1:8002"
        )
    ]
    return NFHeartbeatList(heartbeats=heartbeats)

# Mock log data (in production, read from actual log files)
@router.get("/logs/amf", response_model=LogList)
async def get_amf_logs():
    """Get AMF logs"""
    logs = generate_mock_logs("AMF")
    return LogList(logs=logs)

@router.get("/logs/smf", response_model=LogList)
async def get_smf_logs():
    """Get SMF logs"""
    logs = generate_mock_logs("SMF")
    return LogList(logs=logs)

@router.get("/logs/upf", response_model=LogList)
async def get_upf_logs():
    """Get UPF logs"""
    logs = generate_mock_logs("UPF")
    return LogList(logs=logs)

def generate_mock_logs(source: str) -> List[LogEntry]:
    """Generate mock log entries for testing"""
    levels = ["INFO", "WARNING", "ERROR"]
    messages = {
        "AMF": [
            "UE registration successful",
            "Authentication request sent",
            "Security mode complete",
            "Initial context setup",
            "UE detach request"
        ],
        "SMF": [
            "PDU session establishment",
            "QoS flow established",
            "Session modification request",
            "Session release initiated",
            "N4 session established"
        ],
        "UPF": [
            "Packet forwarding active",
            "QoS enforcement applied",
            "Tunnel established",
            "Statistics report generated",
            "Flow rule updated"
        ]
    }
    
    logs = []
    for i in range(200):
        timestamp = datetime.utcnow() - timedelta(seconds=i*5)
        level = random.choice(levels)
        message = random.choice(messages.get(source, ["Generic log message"]))
        logs.append(LogEntry(
            timestamp=timestamp,
            level=level,
            message=message,
            source=source
        ))
    
    return logs

# PDU Session Timeline
@router.get("/sessions/timeline", response_model=PDUSessionTimelineList)
async def get_pdu_session_timeline():
    """Get PDU session timeline data"""
    sessions = []
    current_time = datetime.utcnow()
    
    # Generate mock session data
    for i in range(20):
        start_time = current_time - timedelta(minutes=random.randint(10, 120))
        end_time = None if random.random() > 0.3 else start_time + timedelta(minutes=random.randint(5, 60))
        
        sessions.append(PDUSessionTimeline(
            session_id=i + 1,
            ue_id=f"{i+1:04d}",
            slice=random.choice(["internet", "iot", "emergency", "mbb"]),
            start=start_time,
            end=end_time,
            qos=random.randint(1, 9),
            upf_node=f"upf-0{random.randint(1, 3)}"
        ))
    
    return PDUSessionTimelineList(sessions=sessions)

# Alerts Panel
@router.get("/alerts", response_model=AlertList)
async def get_alerts():
    """Get real-time alerts"""
    alerts = []
    current_time = datetime.utcnow()
    
    # Generate mock alerts
    alert_types = [
        (AlertType.UE_DETACHED, "UE 0001 detached from AMF", AlertSeverity.WARNING),
        (AlertType.UPF_FAILURE, "UPF unreachable for 3 seconds", AlertSeverity.CRITICAL),
        (AlertType.HIGH_LATENCY, "High latency detected on slice internet", AlertSeverity.WARNING),
        (AlertType.HIGH_BYTES_USAGE, "High bytes usage threshold exceeded", AlertSeverity.INFO),
        (AlertType.NF_UNREACHABLE, "NSSF node unreachable", AlertSeverity.CRITICAL)
    ]
    
    for i, (alert_type, message, severity) in enumerate(alert_types):
        alerts.append(Alert(
            type=alert_type,
            message=message,
            severity=severity,
            timestamp=current_time - timedelta(seconds=i*10)
        ))
    
    return AlertList(alerts=alerts)
