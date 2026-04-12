#!/usr/bin/env python3
import json, os, sys, uuid, datetime
from rich.console import Console
from rich.table import Table

console = Console()

goal = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""

if not goal:
    console.print("[red]No goal provided[/red]")
    sys.exit(1)

plan_id = str(uuid.uuid4())[:8]
timestamp = datetime.datetime.now().isoformat()

steps = [
    {
        "step_id": 1,
        "title": "Market & Problem Validation",
        "objective": "Deep dive into target users, pain points, and TAM for this goal",
        "status": "pending"
    },
    {
        "step_id": 2,
        "title": "Offer & Product Architecture",
        "objective": "Define concrete offers, pricing tiers, and the core product experience",
        "status": "pending"
    },
    {
        "step_id": 3,
        "title": "Financial Model & Valuation",
        "objective": "Build a 3–5 year P&L, unit economics, and funding targets",
        "status": "pending"
    },
    {
        "step_id": 4,
        "title": "Competitive Moat",
        "objective": "Map competitors and carve out a defensible edge (sovereign + biometric + legal)",
        "status": "pending"
    },
    {
        "step_id": 5,
        "title": "Regulatory & Compliance",
        "objective": "Frame GDPR/AI Act/data sovereignty + risk narrative for investors and partners",
        "status": "pending"
    },
    {
        "step_id": 6,
        "title": "Go-to-Market & Traction",
        "objective": "Define ICPs, first 10–20 paying customers, channels, and timeline",
        "status": "pending"
    },
    {
        "step_id": 7,
        "title": "Team & Advisory Layer",
        "objective": "Design the minimum viable team + advisory roster that makes this credible",
        "status": "pending"
    },
    {
        "step_id": 8,
        "title": "Deck / Narrative System",
        "objective": "Outline the 10-slide \"Banani-ready\" deck tied to this plan",
        "status": "pending"
    },
    {
        "step_id": 9,
        "title": "Investor / Buyer Target List",
        "objective": "Generate a list of 30–50 funds, angels, or buyers aligned with this thesis",
        "status": "pending"
    },
    {
        "step_id": 10,
        "title": "Outreach & Follow-up Engine",
        "objective": "Design the outreach copy, follow-up cadences, and calendar booking flow",
        "status": "pending"
    },
]

plan = {
    "plan_id": plan_id,
    "goal": goal,
    "created_at": timestamp,
    "status": "planned",
    "steps": steps
}

plans_dir = os.path.expanduser("~/plans")
os.makedirs(plans_dir, exist_ok=True)
filename = f"plan_{plan_id}_{int(datetime.datetime.now().timestamp())}.json"
plan_path = os.path.join(plans_dir, filename)

with open(plan_path, "w") as f:
    json.dump(plan, f, indent=2)

console.print(f"[bold green]Plan created![/bold green] → {plan_path}")
console.print(f"[bold]Goal:[/bold] {goal}\n")

table = Table(title="Sovereign Architect Plan Steps", show_lines=True)
table.add_column("#", justify="right", style="cyan", no_wrap=True)
table.add_column("Title", style="magenta")
table.add_column("Objective", style="white")
table.add_column("Status", style="green")

for s in steps:
    table.add_row(
        str(s["step_id"]),
        s["title"],
        s["objective"],
        s["status"]
    )

console.print(table)
