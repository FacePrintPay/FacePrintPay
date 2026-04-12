#!/usr/bin/env python3
import sys, json, datetime

payload = {
    "status": "todo",
    "message": "Queue/worker system not implemented yet.",
    "args": sys.argv[1:],
    "timestamp": datetime.datetime.now().isoformat()
}

print(json.dumps(payload, indent=2))
