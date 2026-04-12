#!/usr/bin/env python3
import json, sys, os, pathlib, datetime
from rich.console import Console

console = Console()

if len(sys.argv) < 2:
    console.print("[red]Usage: simple_plan_executor.py PLAN_PATH[/red]")
    sys.exit(1)

plan_path = pathlib.Path(sys.argv[1]).expanduser()
if not plan_path.exists():
    console.print(f"[red]Plan not found:[/red] {plan_path}")
    sys.exit(1)

with open(plan_path, "r") as f:
    plan = json.load(f)

plan_id = plan.get("plan_id", "unknown")
goal = plan.get("goal", "(no goal)")
steps = plan.get("steps", [])

root = pathlib.Path(os.path.expanduser("~/sovereign-architect"))
outputs_root = root / "storage" / "outputs"
outputs_root.mkdir(parents=True, exist_ok=True)

plan_dir = outputs_root / f"plan_{plan_id}"
plan_dir.mkdir(parents=True, exist_ok=True)

console.print(f"[bold green]Executing plan {plan_id}[/bold green]")
console.print(f"[bold]Goal:[/bold] {goal}")
console.print(f"[bold]Steps:[/bold] {len(steps)}")
console.print(f"[bold]Output dir:[/bold] {plan_dir}")

for step in steps:
    sid = step.get("step_id")
    title = step.get("title", "")
    obj = step.get("objective", "")
    status = step.get("status", "pending")

    filename = plan_dir / f"step_{sid:02d}.md"
    with open(filename, "w") as f:
        f.write(f"# Step {sid}: {title}\n\n")
        f.write(f"**Objective:** {obj}\n\n")
        f.write(f"**Status:** {status}\n\n")
        f.write(f"_Generated at {datetime.datetime.now().isoformat()}_\n")

    console.print(f"  → Wrote [cyan]{filename}[/cyan]")

console.print("[bold green]Plan materialization complete.[/bold green]")
