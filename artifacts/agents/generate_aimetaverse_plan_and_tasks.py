#!/usr/bin/env python3
import json
import datetime
from pathlib import Path

# ----------------------------
# Config
# ----------------------------
PLAN_ID = "aimeta001"
GOAL = (
    "Make all Ai Metaverse navigation items, hubs, and experiences actually work "
    "end-to-end with user-visible outputs and monetizable flows."
)

NOW = datetime.datetime.now()
NOW_ISO = NOW.isoformat()

HOME = Path.home()
PLANS_DIR = HOME / "plans"
TASKS_INCOMING_DIR = HOME / "tasks" / "incoming"

PLANS_DIR.mkdir(parents=True, exist_ok=True)
TASKS_INCOMING_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------
# Step / Pillar definitions
# 10 steps × 10 features × 10 actions = 1000 tasks
# ----------------------------
STEPS = [
    {
        "step_id": 1,
        "title": "Funnel & Navigation",
        "objective": "Make all top-level Ai Metaverse navigation links work as real pages with consistent layout, copy, analytics, and CTAs.",
        "assigned_agent": "agent_funnel",
        "features": [
            "Home hero + free trial CTA",
            "Why AI explainer page",
            "Ai for Enterprise landing",
            "Free AI Tools nav link",
            "Meta-Port hub",
            "Planet.AI TV page",
            "Watch Ai_LIVE stream hub",
            "Ai Metaverse News & Blog",
            "Conversations with Bard archive",
            "Sign up / Auth + footer nav (Privacy, Terms, Cookies)"
        ],
    },
    {
        "step_id": 2,
        "title": "Identity & Avatar Clone",
        "objective": "Let users 'clone themselves' with selfie, voice snippet, and horoscope-style traits, wired to avatars and profiles.",
        "assigned_agent": "agent_identity",
        "features": [
            "Selfie capture onboarding",
            "Voice snippet upload",
            "Birthdate + horoscope traits capture",
            "Avatar generator integration",
            "Avatar-to-voice binding",
            "VerseDNA profile page",
            "Avatar gallery / switcher",
            "Privacy & consent for biometric data",
            "Avatar preview inside Meta-Port",
            "Account settings for identity & avatars"
        ],
    },
    {
        "step_id": 3,
        "title": "AI Tools & Hubs",
        "objective": "Wire all external AI hubs into a coherent app-hub experience with working links, SSO where possible, and tracking.",
        "assigned_agent": "agent_hubs",
        "features": [
            "Free AI Tools Directory integration",
            "Access Ai-Labs hub",
            "Ai_Education / Eduverse integration",
            "Virtual Shopping Cre8tor (PlanetAI Store) entry",
            "Build With BoTAblity funnel",
            "AI programming & certification hub",
            "AI developer & coding repo overview",
            "AI tools tagging & search",
            "Single sign-on across hubs (where supported)",
            "Usage metering & limits for tools"
        ],
    },
    {
        "step_id": 4,
        "title": "Creation Tools (Text / Image / Video / Object)",
        "objective": "Make text, image, video, and object generation flows actually usable from the Ai Metaverse front-door.",
        "assigned_agent": "agent_creation",
        "features": [
            "Text generation workspace",
            "Image generation via Craiyon",
            "Video generation via InVideo",
            "Face swaps via Reface",
            "Song lyrics generator (Ai.Records)",
            "Prompt library & templates",
            "Object / 3D asset generation handoff",
            "Export & share to social media",
            "User galleries & creation history",
            "Safety & content filters for generations"
        ],
    },
    {
        "step_id": 5,
        "title": "Metaverse & VR / 3D Environments",
        "objective": "Connect users into 3D / VR / metaverse environments with clear entry points and working deep links.",
        "assigned_agent": "agent_metaverse",
        "features": [
            "Ai_Metaverse dev zone (AIDevZone) entry",
            "Metaverse environments directory",
            "ReadyPlayerMe avatar pipeline",
            "Google Cardboard VR quickstart",
            "VR platform integrations list",
            "Explore Mars virtual tour",
            "Virtual real-estate search with AI",
            "XR / 3D environment launcher",
            "Session bookmarking & deep links",
            "Device compatibility & checks"
        ],
    },
    {
        "step_id": 6,
        "title": "Commerce & Payments (MyBuy'o, Bitbucks, Stores)",
        "objective": "Turn Ai Metaverse into a real revenue engine with working biometric payments, rewards, and storefronts.",
        "assigned_agent": "agent_commerce",
        "features": [
            "MyBuy'o biometric verification flow",
            "MyBuy'o payment checkout experience",
            "Bitbucks rewards earn & redeem",
            "Virtual retail store template",
            "In-store virtual shopping UX",
            "AI gadgets & accessories catalog",
            "Cart & order management",
            "Receipts & transaction history",
            "Subscription pricing & plans",
            "3rd-party payment gateways integration"
        ],
    },
    {
        "step_id": 7,
        "title": "Community, Social & Events",
        "objective": "Make the community layer real: friends, concerts, social rooms, and communication tools wired to Ai Metaverse.",
        "assigned_agent": "agent_social",
        "features": [
            "Ai.Records community & music hub",
            "Find friends in metaverse communities",
            "Virtual concerts & events directory",
            "Social VR rooms & venues list",
            "Anonymous / high-privacy chat hubs (safely mediated)",
            "Zoom AI Companion / Zoom Workplace hub",
            "Ai_Social sponsored tools strip",
            "User profiles & following system",
            "Notifications & email digests",
            "Moderation & abuse reporting tools"
        ],
    },
    {
        "step_id": 8,
        "title": "Developer & Integrations Hub",
        "objective": "Expose Ai Metaverse as a platform: APIs, SDKs, docs, and builder flows.",
        "assigned_agent": "agent_devhub",
        "features": [
            "Ai developer repo index",
            "Public API documentation",
            "Webhooks & event callbacks",
            "API keys & credentials management",
            "OAuth / identity for developers",
            "Sample apps & templates gallery",
            "Metaverse builder learning path",
            "App-builder hubs (Thunkable, Unbounce, etc.)",
            "SDK downloads & code snippets",
            "Changelog & release notes page"
        ],
    },
    {
        "step_id": 9,
        "title": "Data, Analytics & Personalization",
        "objective": "Wire tracking, analytics, personalization, and reporting across the whole Ai Metaverse stack.",
        "assigned_agent": "agent_data",
        "features": [
            "Site analytics instrumentation",
            "Product recommendation engine",
            "Personalized content rules",
            "Data visualization dashboard",
            "Wordtune-style writing assist hooks",
            "Brandwatch / social listening hooks",
            "A/B testing framework for funnels",
            "Data retention & deletion policies",
            "Exports to CSV / BI tools",
            "Platform health & metrics dashboard"
        ],
    },
    {
        "step_id": 10,
        "title": "Operations, Legal & Support",
        "objective": "Make Ai Metaverse compliant and support-ready, with real contact, uptime, and policy surfaces.",
        "assigned_agent": "agent_ops",
        "features": [
            "Contact form & map (1007 Yanceyville, etc.)",
            "Business hours display",
            "Support ticket intake flow",
            "Status / uptime page",
            "Error logging & alerting",
            "Privacy policy page",
            "Terms & conditions page",
            "Cookie banner & preferences center",
            "Legal/compliance documentation pack",
            "Admin console for operations team"
        ],
    },
]

# 10 generic actions applied to every feature
ACTIONS = [
    "Draft functional spec for {feature}",
    "Design UX flow and wireframes for {feature}",
    "Define data model and storage schema for {feature}",
    "Implement backend API endpoints for {feature}",
    "Implement frontend UI components for {feature}",
    "Hook up required 3rd-party integrations for {feature}",
    "Add analytics and logging events for {feature}",
    "Write user-facing copy and help text for {feature}",
    "Create automated tests and validation for {feature}",
    "Prepare launch checklist and operational runbook for {feature}",
]

TOTAL_EXPECTED_TASKS = 10 * 10 * 10  # 1000


def build_plan_dict():
    return {
        "plan_id": PLAN_ID,
        "goal": GOAL,
        "created_at": NOW_ISO,
        "status": "planned",
        "steps": [
            {
                "step_id": s["step_id"],
                "title": s["title"],
                "objective": s["objective"],
                "status": "pending",
                "assigned_agent": s["assigned_agent"],
            }
            for s in STEPS
        ],
    }


def generate_tasks(plan_path: Path):
    tasks = []
    global_index = 0

    for step in STEPS:
        step_id = step["step_id"]
        step_title = step["title"]
        step_agent = step["assigned_agent"]
        features = step["features"]

        local_idx = 0
        for feature in features:
            for action_tpl in ACTIONS:
                local_idx += 1
                global_index += 1

                # Priority heuristic: 1–100 high, 101–400 medium, rest low
                if global_index <= 100:
                    priority = "high"
                elif global_index <= 400:
                    priority = "medium"
                else:
                    priority = "low"

                action_text = action_tpl.format(feature=feature)
                short_action = action_text.split(" for ")[0]

                task_id = f"{PLAN_ID}-{step_id:02d}-{local_idx:03d}"

                expected_output = (
                    f"Concrete artifact for '{feature}' under '{step_title}' that reflects: {action_text}. "
                    f"For example: committed code, config, or content in sovereign-architect/storage/artifacts/plan_{PLAN_ID}/{task_id}/."
                )

                task = {
                    "task_id": task_id,
                    "plan_id": PLAN_ID,
                    "step_id": step_id,
                    "step_title": step_title,
                    "goal": GOAL,
                    "title": f"S{step_id:02d}.{local_idx:03d} - {feature} - {short_action}",
                    "description": action_text,
                    "status": "pending",
                    "priority": priority,
                    "assigned_agent": step_agent,
                    "tags": [
                        "aimetaverse",
                        "sovereign-architect",
                        f"step-{step_id}",
                        step_agent,
                    ],
                    "created_at": NOW_ISO,
                    "est_minutes": 30,
                    "expected_output": expected_output,
                    "context": {
                        "feature": feature,
                        "action": action_text,
                        "sequence_index": global_index,
                        "local_step_index": local_idx,
                        "plan_path": str(plan_path),
                    },
                }
                tasks.append(task)

    if len(tasks) != TOTAL_EXPECTED_TASKS:
        print(f"WARNING: generated {len(tasks)} tasks, expected {TOTAL_EXPECTED_TASKS}")

    bundle = {
        "plan_id": PLAN_ID,
        "goal": GOAL,
        "total_tasks": len(tasks),
        "generated_at": NOW_ISO,
        "source_plan_path": str(plan_path),
        "tasks": tasks,
    }
    return bundle


def main():
    # 1) Write plan JSON
    ts = int(NOW.timestamp())
    plan_path = PLANS_DIR / f"plan_{PLAN_ID}_{ts}.json"
    plan_dict = build_plan_dict()

    with plan_path.open("w") as f:
        json.dump(plan_dict, f, indent=2)

    # 2) Generate 1000 tasks based on that plan
    bundle = generate_tasks(plan_path)
    tasks_out = TASKS_INCOMING_DIR / f"plan_{PLAN_ID}_tasks_1000.json"
    with tasks_out.open("w") as f:
        json.dump(bundle, f, indent=2)

    # 3) Console summary
    print("===================================================")
    print(" Ai Metaverse – PLAN + 1000 TASKS GENERATED")
    print("---------------------------------------------------")
    print(f" Plan ID:           {PLAN_ID}")
    print(f" Goal:              {GOAL}")
    print(f" Plan JSON:         {plan_path}")
    print(f" Task bundle path:  {tasks_out}")
    print(f" Total tasks:       {bundle['total_tasks']}")
    print("---------------------------------------------------")
    print(" Next:")
    print("  1) Fan-out tasks to files:")
    print(f"       python3 agents/fanout_tasks_to_files.py {tasks_out}")
    print("  2) Run your strict worker loop on PLAN_ID=aimeta001")
    print("  3) Verify artifacts in:")
    print(f"       ~/sovereign-architect/storage/artifacts/plan_{PLAN_ID}/")
    print("===================================================")


if __name__ == '__main__':
    main()
