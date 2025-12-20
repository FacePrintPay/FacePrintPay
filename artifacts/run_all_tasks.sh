#!/bin/bash
# Drain all tasks for a given PLAN_ID using yesquid_task_worker

set -euo pipefail

PLAN_ID="${1:-52f7b763}"

while true; do
  ./agents/yesquid_task_worker.sh "$PLAN_ID" || break
done

echo "✅ Finished run_all_tasks for plan ${PLAN_ID}"
