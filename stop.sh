#!/data/data/com.termux/files/usr/bin/bash

echo "Stopping FacePrintPay Gateway System..."

for service in gateway api dashboard keys_api swarm_api; do
    if [ -f logs/${service}.pid ]; then
        PID=$(cat logs/${service}.pid)
        kill $PID 2>/dev/null && echo "✓ Stopped $service (PID: $PID)"
        rm logs/${service}.pid
    fi
done

# Additional cleanup for forensic API
if [ -f ~/forensic_api/logs/api.pid ]; then
    PID=$(cat ~/forensic_api/logs/api.pid)
    kill $PID 2>/dev/null && echo "✓ Stopped Forensic API (PID: $PID)"
    rm ~/forensic_api/logs/api.pid
fi

echo "All services stopped."
