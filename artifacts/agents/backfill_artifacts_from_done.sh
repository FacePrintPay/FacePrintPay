#!/bin/bash
# Backfill artifacts for already completed tasks in tasks/done/

set -euo pipefail

PLAN_ID="${1:-52f7b763}"

DONE_DIR="$HOME/tasks/done/plan_${PLAN_ID}"
ARTIFACT_ROOT="$HOME/sovereign-architect/storage/artifacts/plan_${PLAN_ID}"

mkdir -p "$ARTIFACT_ROOT"

if [ ! -d "$DONE_DIR" ]; then
  echo "No done directory at $DONE_DIR"
  exit 0
fi

count=0

for TASK_FILE in "$DONE_DIR"/*.json; do
  [ -f "$TASK_FILE" ] || continue

  BASENAME="$(basename "$TASK_FILE")"
  TASK_ID="$(jq -r '.task_id // empty' "$TASK_FILE")"
  [ -z "$TASK_ID" ] && TASK_ID="${BASENAME%.json}"

  TITLE="$(jq -r '.title // "(no title)"' "$TASK_FILE")"
  DESC="$(jq -r '.description // "(no description)"' "$TASK_FILE")"
  STEP_ID="$(jq -r '.step_id // 0' "$TASK_FILE")"
  STEP_TITLE="$(jq -r '.step_title // "(no step title)"' "$TASK_FILE")"
  PRIORITY="$(jq -r '.priority // "unassigned"' "$TASK_FILE")"

  TASK_ART_DIR="$ARTIFACT_ROOT/$TASK_ID"
  mkdir -p "$TASK_ART_DIR"

  cp "$TASK_FILE" "$TASK_ART_DIR/${TASK_ID}.task.json"

  cat > "$TASK_ART_DIR/${TASK_ID}.md" << MD
# Task: $TITLE

**Task ID:** \`$TASK_ID\`  
**Plan ID:** \`$PLAN_ID\`  
**Step:** $STEP_ID – $STEP_TITLE  
**Priority:** $PRIORITY  

---

## Task Description

$DESC

---

## Work Notes

(Backfilled artifact for a previously completed task.)

MD

  count=$((count + 1))
done

echo "Backfilled artifacts for $count tasks into:"
echo "  $ARTIFACT_ROOT"
