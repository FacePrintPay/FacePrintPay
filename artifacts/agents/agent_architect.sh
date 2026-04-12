#!/bin/bash
# Thin wrapper to call the Python planner

GOAL="$*"

if [[ -z "$GOAL" ]]; then
  echo "Usage: agent_architect.sh \"your goal here\""
  exit 1
fi

python "$HOME/sovereign-architect/agents/architect_planner.py" "$GOAL"
