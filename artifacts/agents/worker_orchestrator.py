#!/usr/bin/env python3
"""
Worker Orchestrator - Executes plan steps using Claude API
"""
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from anthropic import Anthropic
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

# Initialize Anthropic client
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def load_plan(plan_id):
    """Load a plan by ID"""
    plan_file = Path(f"~/sovereign-architect/plans/plan_{plan_id}.json").expanduser()
    if not plan_file.exists():
        # Try without timestamp suffix
        plans = list(Path("~/sovereign-architect/plans").expanduser().glob(f"plan_{plan_id}*.json"))
        if plans:
            plan_file = plans[0]
        else:
            return None
    
    with open(plan_file) as f:
        return json.load(f)

def save_plan(plan):
    """Save updated plan"""
    plan_file = Path(f"~/sovereign-architect/plans/plan_{plan['plan_id']}.json").expanduser()
    # Find the actual file with timestamp
    plans = list(Path("~/sovereign-architect/plans").expanduser().glob(f"plan_{plan['plan_id']}*.json"))
    if plans:
        plan_file = plans[0]
    
    with open(plan_file, 'w') as f:
        json.dump(plan, f, indent=2)

def execute_step(step, plan_context):
    """Execute a single plan step using Claude"""
    console.print(f"\n[bold cyan]Executing Step {step['step_id']}: {step['title']}[/bold cyan]")
    console.print(f"[dim]Objective: {step['objective']}[/dim]")
    
    # Build context-aware prompt
    prompt = f"""You are a world-class strategic advisor working on a Series A fundraising deck.

OVERALL GOAL: {plan_context['goal']}

CURRENT STEP: {step['title']}
OBJECTIVE: {step['objective']}

Your task is to produce a comprehensive, investor-ready section that addresses this objective with extreme depth and clarity.

Requirements:
- Be specific, data-driven, and compelling
- Use real market data where possible (you can search the web)
- Format as markdown with clear sections
- Include concrete numbers, timelines, and metrics
- Write at the level of a top-tier VC pitch deck

Produce the complete section now:"""

    try:
        # Call Claude API
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        output = response.content[0].text
        
        # Save output to storage
        output_dir = Path("~/sovereign-architect/storage/outputs").expanduser()
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"step_{step['step_id']}_{step['title'].lower().replace(' ', '_')}.md"
        with open(output_file, 'w') as f:
            f.write(f"# {step['title']}\n\n")
            f.write(f"**Objective:** {step['objective']}\n\n")
            f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")
            f.write("---\n\n")
            f.write(output)
        
        console.print(f"[green]✓ Completed[/green] → {output_file}")
        
        return {
            "success": True,
            "output_file": str(output_file),
            "summary": output[:200] + "..."
        }
        
    except Exception as e:
        console.print(f"[red]✗ Failed: {str(e)}[/red]")
        return {
            "success": False,
            "error": str(e)
        }

def execute_plan(plan_id):
    """Execute all steps in a plan"""
    console.print(f"\n[bold]Loading plan: {plan_id}[/bold]\n")
    
    plan = load_plan(plan_id)
    if not plan:
        console.print(f"[red]Plan {plan_id} not found[/red]")
        return
    
    console.print(f"[cyan]Goal:[/cyan] {plan['goal']}")
    console.print(f"[cyan]Steps:[/cyan] {len(plan['steps'])}\n")
    
    # Update status
    plan['status'] = 'executing'
    save_plan(plan)
    
    # Execute each step
    completed = 0
    for step in plan['steps']:
        if step['status'] == 'completed':
            console.print(f"[dim]Step {step['step_id']} already completed, skipping[/dim]")
            completed += 1
            continue
        
        # Update step status
        step['status'] = 'executing'
        save_plan(plan)
        
        # Execute
        result = execute_step(step, {
            'goal': plan['goal'],
            'completed_steps': completed
        })
        
        # Update with result
        if result['success']:
            step['status'] = 'completed'
            step['output_file'] = result['output_file']
            step['completed_at'] = datetime.now().isoformat()
            completed += 1
        else:
            step['status'] = 'failed'
            step['error'] = result.get('error')
        
        save_plan(plan)
    
    # Final status
    if completed == len(plan['steps']):
        plan['status'] = 'completed'
        console.print(f"\n[bold green]🎉 Plan completed! All {completed} steps executed.[/bold green]")
    else:
        plan['status'] = 'partial'
        console.print(f"\n[yellow]⚠ Plan partially completed: {completed}/{len(plan['steps'])} steps[/yellow]")
    
    plan['completed_at'] = datetime.now().isoformat()
    save_plan(plan)
    
    # Show outputs
    console.print(f"\n[bold]📁 Outputs saved to:[/bold]")
    output_dir = Path("~/sovereign-architect/storage/outputs").expanduser()
    for f in sorted(output_dir.glob("step_*.md")):
        console.print(f"  • {f.name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[red]Usage: worker_orchestrator.py <plan_id>[/red]")
        console.print("\nAvailable plans:")
        plans_dir = Path("~/sovereign-architect/plans").expanduser()
        for p in sorted(plans_dir.glob("plan_*.json")):
            with open(p) as f:
                plan = json.load(f)
            status_color = "green" if plan.get('status') == 'completed' else "yellow"
            console.print(f"  [{status_color}]{plan['plan_id']}[/{status_color}]: {plan['goal'][:60]}...")
        sys.exit(1)
    
    plan_id = sys.argv[1]
    execute_plan(plan_id)
