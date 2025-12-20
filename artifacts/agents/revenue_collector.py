#!/usr/bin/env python3
"""
Revenue Collector - Connects completed tasks to actual payment
Monitors done tasks and generates invoices/payment requests
"""
import json
import os
from pathlib import Path
from datetime import datetime

# Your Cash App
CASHAPP_TAG = "$ThaCyg"

# Service pricing (what you charge per task type)
TASK_PRICING = {
    "Funnel": 50,      # $50 per funnel task
    "Avatar": 75,      # $75 per avatar task  
    "Ops": 100,        # $100 per ops task
    "default": 25      # $25 for any other task
}

def scan_completed_tasks():
    """Find all completed tasks that haven't been invoiced"""
    done_dir = Path("~/tasks/done").expanduser()
    invoices_dir = Path("~/sovereign-architect/storage/invoices").expanduser()
    invoices_dir.mkdir(parents=True, exist_ok=True)
    
    completed = []
    for plan_dir in done_dir.glob("plan_*"):
        for task_file in plan_dir.glob("*.json"):
            # Check if already invoiced
            invoice_marker = invoices_dir / f"{task_file.stem}_invoiced.json"
            if not invoice_marker.exists():
                with open(task_file) as f:
                    task = json.load(f)
                completed.append((task, task_file, invoice_marker))
    
    return completed

def calculate_revenue(task):
    """Calculate what to charge for this task"""
    task_type = task.get("tags", ["default"])[0] if task.get("tags") else "default"
    price = TASK_PRICING.get(task_type, TASK_PRICING["default"])
    return price

def generate_invoice(task, amount):
    """Generate invoice for completed work"""
    invoice = {
        "invoice_id": f"INV-{datetime.now().strftime('%Y%m%d')}-{task['task_id']}",
        "task_id": task["task_id"],
        "task_title": task["title"],
        "amount": amount,
        "payment_method": CASHAPP_TAG,
        "status": "pending",
        "generated_at": datetime.now().isoformat(),
        "payment_url": f"https://cash.app/{CASHAPP_TAG}/{amount}"
    }
    return invoice

def main():
    print("🔍 Scanning completed tasks...")
    completed = scan_completed_tasks()
    
    if not completed:
        print("✓ No new completed tasks to invoice")
        return
    
    invoices_dir = Path("~/sovereign-architect/storage/invoices").expanduser()
    total_revenue = 0
    
    for task, task_file, invoice_marker in completed:
        amount = calculate_revenue(task)
        invoice = generate_invoice(task, amount)
        
        # Save invoice
        invoice_file = invoices_dir / f"{invoice['invoice_id']}.json"
        with open(invoice_file, 'w') as f:
            json.dump(invoice, f, indent=2)
        
        # Mark as invoiced
        with open(invoice_marker, 'w') as f:
            json.dump({"invoiced_at": datetime.now().isoformat()}, f)
        
        total_revenue += amount
        print(f"💰 ${amount:>6} - {task['title'][:60]}")
    
    print(f"\n{'='*70}")
    print(f"Total Revenue Generated: ${total_revenue}")
    print(f"Payment Method: {CASHAPP_TAG}")
    print(f"Invoices: ~/sovereign-architect/storage/invoices/")
    print(f"{'='*70}\n")
    
    # Generate payment collection email
    collection_file = invoices_dir / f"collection_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(collection_file, 'w') as f:
        f.write(f"INVOICE SUMMARY - {datetime.now().strftime('%Y-%m-%d')}\n")
        f.write(f"{'='*70}\n\n")
        f.write(f"Total Due: ${total_revenue}\n")
        f.write(f"Payment: {CASHAPP_TAG}\n")
        f.write(f"Tasks Completed: {len(completed)}\n\n")
        f.write("PAYMENT LINK:\n")
        f.write(f"https://cash.app/{CASHAPP_TAG}/{total_revenue}\n\n")
        f.write("Individual Tasks:\n")
        for task, _, _ in completed:
            amount = calculate_revenue(task)
            f.write(f"  • ${amount:>6} - {task['title']}\n")
    
    print(f"📧 Collection email saved: {collection_file}")
    print(f"\n🚀 NEXT STEP: Send invoices to customers")
    print(f"   OR: Post services on Fiverr/Upwork and link these outputs\n")

if __name__ == "__main__":
    main()
