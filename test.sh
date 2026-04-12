#!/data/data/com.termux/files/usr/bin/bash

echo "Testing FacePrintPay Gateway System..."
echo ""

echo "1. Gateway Health:"
curl -s http://localhost:8080/api/health | jq

echo ""
echo "2. Gateway Overview:"
curl -s http://localhost:8080/api/overview | jq

echo ""
echo "3. List Vaults:"
curl -s http://localhost:8080/api/vaults | jq

echo ""
echo "4. Service Status:"
curl -s http://localhost:8080/api/services | jq

echo ""
echo "5. Forensic API Health:"
curl -s http://localhost:3000/health | jq
