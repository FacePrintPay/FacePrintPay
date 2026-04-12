#!/bin/bash
# Execute a plan by ID

if [ -z "$1" ]; then
    echo "Usage: execute_plan.sh <plan_id>"
    echo ""
    echo "Available plans:"
    ls -1 ~/sovereign-architect/plans/plan_*.json | while read f; do
        plan_id=$(basename "$f" | sed 's/plan_//' | sed 's/_.*//')
        goal=$(jq -r '.goal' "$f" | cut -c1-60)
        echo "  • $plan_id: $goal..."
    done
    exit 1
fi

cd ~/sovereign-architect
python3 agents/worker_orchestrator.py "$1"
