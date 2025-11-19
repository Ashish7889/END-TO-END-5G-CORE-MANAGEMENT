#!/bin/bash

# 5G Core Management - Stop Script
# This script stops all running services

echo "Stopping 5G Core Management Services..."

PROJECT_ROOT="/home/ashish/CascadeProjects/5g-core-mgmt"
cd "$PROJECT_ROOT"

# Stop all services
for service in nrf amf smf upf pcf nssf udm_ausf management frontend; do
    if [ -f "logs/${service}.pid" ]; then
        pid=$(cat "logs/${service}.pid")
        if kill -0 $pid 2>/dev/null; then
            echo "Stopping $service (PID: $pid)"
            kill $pid
            # Wait a moment for graceful shutdown
            sleep 1
            # Force kill if still running
            if kill -0 $pid 2>/dev/null; then
                echo "Force killing $service"
                kill -9 $pid
            fi
        else
            echo "$service not running"
        fi
        rm -f "logs/${service}.pid"
    else
        echo "$service PID file not found"
    fi
done

echo ""
echo "All services stopped."
