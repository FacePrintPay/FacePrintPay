#!/data/data/com.termux/files/usr/bin/bash

echo "Starting FacePrintPay Gateway System..."

# Start Gateway
cd ~/FacePrintPay
node gateway.js > logs/gateway.log 2>&1 &
echo $! > logs/gateway.pid
echo "✓ Gateway started (PID: $(cat logs/gateway.pid))"

# Start Forensic API
cd ~/forensic_api
node server.js > logs/api.log 2>&1 &
echo $! > logs/api.pid
echo "✓ Forensic API started (PID: $(cat logs/api.pid))"

# Start Services
cd ~/FacePrintPay/services/dashboard
node dashboard.js > ../../logs/dashboard.log 2>&1 &
echo $! > ../../logs/dashboard.pid
echo "✓ Dashboard started (PID: $(cat ../../logs/dashboard.pid))"

cd ~/FacePrintPay/services/keys_api
node keys_api.js > ../../logs/keys_api.log 2>&1 &
echo $! > ../../logs/keys_api.pid
echo "✓ Keys API started (PID: $(cat ../../logs/keys_api.pid))"

cd ~/FacePrintPay/services/swarm_api
node swarm_api.js > ../../logs/swarm_api.log 2>&1 &
echo $! > ../../logs/swarm_api.pid
echo "✓ Swarm API started (PID: $(cat ../../logs/swarm_api.pid))"

echo ""
echo "All services started!"
echo ""
echo "Access points:"
echo "  Gateway:      http://localhost:8080"
echo "  Forensic API: http://localhost:3000"
echo "  Dashboard:    http://localhost:3001"
echo "  Keys API:     http://localhost:3002"
echo "  Swarm API:    http://localhost:3003"
