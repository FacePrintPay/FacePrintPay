#!/usr/bin/env python3
import json, sys
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: fanout_tasks_to_files.py TASK_BUNDLE_JSON")
    sys.exit(1)

bundle_path = Path(sys.argv[1]).expanduser()
if not bundle_path.exists():
    print(f"Bundle not found: {bundle_path}")
    sys.exit(1)

with bundle_path.open("r") as f:
    bundle = json.load(f)

plan_id = bundle.get("plan_id", "unknown")
tasks = bundle.get("tasks", [])

tasks_root = Path.home() / "tasks"
active_root = tasks_root / "active"
plan_dir = active_root / f"plan_{plan_id}"
plan_dir.mkdir(parents=True, exist_ok=True)

print(f"Plan ID: {plan_id}")
print(f"Total tasks in bundle: {len(tasks)}")
print(f"Writing to: {plan_dir}")

count = 0
for t in tasks:
    tid = t.get("task_id", f"{plan_id}-{count+1:04d}")
    filename = plan_dir / f"{tid}.json"
    with filename.open("w") as f:
        json.dump(t, f, indent=2)
    count += 1
    if count % 100 == 0:
        print(f"  → {count} tasks written...")

print(f"Done. Wrote {count} task files into {plan_dir}")
