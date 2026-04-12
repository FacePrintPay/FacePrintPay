#!/usr/bin/env python3
"""
Compile all completed steps into a final Series A deck
"""
import json
from pathlib import Path
from datetime import datetime
from rich.console import Console

console = Console()

def compile_deck(plan_id):
    """Compile all step outputs into a final deck"""
    console.print(f"\n[bold]Compiling deck for plan: {plan_id}[/bold]\n")
    
    # Load plan
    plans = list(Path("~/sovereign-architect/plans").expanduser().glob(f"plan_{plan_id}*.json"))
    if not plans:
        console.print("[red]Plan not found[/red]")
        return
    
    with open(plans[0]) as f:
        plan = json.load(f)
    
    # Create final deck
    deck_content = f"""# SovereignGTP Series A Deck

**Generated:** {datetime.now().strftime("%B %d, %Y")}

**Goal:** {plan['goal']}

---

"""
    
    # Add each completed step
    for step in plan['steps']:
        if step['status'] == 'completed' and 'output_file' in step:
            output_file = Path(step['output_file'])
            if output_file.exists():
                console.print(f"[green]✓[/green] Adding: {step['title']}")
                with open(output_file) as f:
                    content = f.read()
                    # Skip the metadata header
                    content = content.split('---', 2)[-1] if '---' in content else content
                    deck_content += f"\n\n## Slide {step['step_id']}: {step['title']}\n\n"
                    deck_content += content.strip()
                    deck_content += "\n\n---\n"
            else:
                console.print(f"[yellow]⚠[/yellow] Missing: {step['title']}")
    
    # Save final deck
    artifacts_dir = Path("~/sovereign-architect/storage/artifacts").expanduser()
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    
    deck_file = artifacts_dir / f"series_a_deck_{plan_id}_{datetime.now().strftime('%Y%m%d')}.md"
    with open(deck_file, 'w') as f:
        f.write(deck_content)
    
    console.print(f"\n[bold green]✓ Deck compiled![/bold green]")
    console.print(f"[cyan]📄 {deck_file}[/cyan]")
    console.print(f"\n[dim]You can now export this to Notion, Pitch, or Google Slides[/dim]")
    
    return deck_file

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        console.print("[red]Usage: compile_deck.py <plan_id>[/red]")
        sys.exit(1)
    
    compile_deck(sys.argv[1])
