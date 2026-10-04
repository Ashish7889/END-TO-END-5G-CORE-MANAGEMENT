#!/bin/bash

# 5G Core Management - Startup Script
# This script starts all required services for the 5G Core Management prototype

echo "Starting 5G Core Management Services..."

# Set project root
PROJECT_ROOT="/home/ashish/CascadeProjects/5g-core-mgmt"
cd "$PROJECT_ROOT"

# Activate virtual environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "Virtual environment activated"
else
    echo "Warning: Virtual environment not found. Creating one..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r backend/requirements.txt
fi

# Create data directory if it doesn't exist
mkdir -p data

# Function to start a service in background
start_service() {
    local service_name=$1
    local port=$2
    local module_path=$3
    
    echo "Starting $service_name on port $port..."
    cd "$PROJECT_ROOT"
    python3 -m uvicorn "$module_path:app" --host 0.0.0.0 --port $port --reload > "logs/${service_name}.log" 2>&1 &
    echo $! > "logs/${service_name}.pid"
    echo "$service_name started with PID $(cat "logs/${service_name}.pid")"
}

# Create logs directory
mkdir -p logs

# Kill any existing processes
echo "Cleaning up existing processes..."
for service in nrf amf smf upf pcf nssf udm_ausf management; do
    if [ -f "logs/${service}.pid" ]; then
        pid=$(cat "logs/${service}.pid")
        if kill -0 $pid 2>/dev/null; then
            echo "Stopping existing $service (PID: $pid)"
            kill $pid
        fi
        rm -f "logs/${service}.pid"
    fi
done

# Start core network functions
start_service "nrf" 8000 "backend.nrf.main"
start_service "amf" 8001 "backend.amf.main"
start_service "smf" 8005 "backend.smf.main"
start_service "upf" 8004 "backend.upf.main"
start_service "pcf" 8003 "backend.pcf.main"
start_service "nssf" 8002 "backend.nssf.main"
start_service "udm_ausf" 8010 "backend.udm_ausf.main"

# Start management service (last)
start_service "management" 8009 "backend.management.main"

# Start frontend static server
echo "Starting frontend on port 8080..."
cd "$PROJECT_ROOT/frontend/static"
source "$PROJECT_ROOT/.venv/bin/activate"
python3 -m http.server 8080 > "$PROJECT_ROOT/logs/frontend.log" 2>&1 &
echo $! > "$PROJECT_ROOT/logs/frontend.pid"
echo "Frontend started with PID $(cat "$PROJECT_ROOT/logs/frontend.pid")"

echo ""
echo "=================================="
echo "5G Core Management Services Started!"
echo "=================================="
echo ""
echo "Services:"
echo "  NRF:        http://localhost:8000"
echo "  AMF:        http://localhost:8001"
echo "  NSSF:       http://localhost:8002"
echo "  UPF:        http://localhost:8004"
echo "  PCF:        http://localhost:8003"
echo "  SMF:        http://localhost:8005"
echo "  UDM/AUSF:   http://localhost:8010"
echo "  Management: http://localhost:8009"
echo "  Frontend:   http://localhost:8080"
echo ""
echo "API Key: configured through ADMIN_API_KEY environment variable"
echo ""
echo "Dashboard URL: http://localhost:8080"
echo ""
echo "Logs are available in the 'logs/' directory"
echo "To stop all services, run: ./stop_services.sh"
