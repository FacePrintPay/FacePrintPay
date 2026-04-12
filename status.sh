#!/data/data/com.termux/files/usr/bin/bash

echo "FacePrintPay Gateway System Status"
echo "═══════════════════════════════════════════════════════════"

check_service() {
    local name=$1
    local pid_file=$2
    local port=$3
    
    if [ -f "$pid_file" ]; then
        PID=$(cat "$pid_file")
        if ps -p $PID > /dev/null; then
            echo "✓ $name is running (PID: $PID, Port: $port)"
            curl -s "http://localhost:$port/health" | jq -r '.status' 2>/dev/null | \
                xargs -I {} echo "  Health: {}"
        else
            echo "✗ $name not running (stale PID)"
            rm "$pid_file"
        fi
    else
        echo "✗ $name not running"
    fi
}

check_service "Gateway      " "logs/gateway.pid" "8080"
check_service "Forensic API " "~/forensic_api/logs/api.pid" "3000"
check_service "Dashboard    " "logs/dashboard.pid" "3001"
check_service "Keys API     " "logs/keys_api.pid" "3002"
check_service "Swarm API    " "logs/swarm_api.pid" "3003"

echo "═══════════════════════════════════════════════════════════"
