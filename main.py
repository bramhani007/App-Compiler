import json
from pipeline.intent import extract_intent
from pipeline.design import design_architecture
from pipeline.generators.ui import generate_ui
from pipeline.generators.api import generate_api
from pipeline.generators.db import generate_db
from pipeline.generators.auth import generate_auth
from pipeline.generators.business_logic import generate_business_logic
from pipeline.refinement import refine_and_repair
from pipeline.validation import cross_validate

def run_pipeline(user_prompt: str) -> dict:
    print("Stage 1: Intent extraction...")
    intent = extract_intent(user_prompt)
    if intent.get("clarification_needed"):
        return {"error": "clarification_needed", "question": intent.get("clarification_question", "Please clarify your request.")}
    
    print("Stage 2: System design...")
    architecture = design_architecture(intent)
    
    # Generate Intermediate Representation (IR)
    import datetime
    import os
    ir = {
        "app_type": intent.get("app_type", ""),
        "features": intent.get("features", []),
        "roles": intent.get("roles", []),
        "entities": architecture.get("entities", []),
        "assumptions": intent.get("assumptions", []),
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    # Save to ir.json
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ir_path = os.path.join(current_dir, "ir.json")
        with open(ir_path, "w") as f:
            json.dump(ir, f, indent=2)
        print("Saved Intermediate Representation to ir.json")
    except Exception as e:
        print(f"Warning: Failed to save ir.json: {e}")
    
    print("Stage 3: Generating schemas...")
    ui_config = generate_ui(architecture)
    api_config = generate_api(architecture)
    db_config = generate_db(architecture)
    auth_config = generate_auth(architecture)
    biz_config = generate_business_logic(architecture, intent)
    
    config = {
        "ui": ui_config,
        "api": api_config,
        "db": db_config,
        "auth": auth_config,
        "business_logic": biz_config
    }
    
    print("Stage 4: Cross-validation and repair...")
    final_config = refine_and_repair(config, architecture, intent)
    
    # Final validation
    issues = cross_validate(final_config)
    if issues:
        print(f"Warning: Remaining inconsistencies: {issues}")
        final_config["_remaining_issues"] = issues
    
    # Add metadata
    final_config["assumptions"] = intent.get("assumptions", [])
    return final_config

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = "Build a CRM with login, contacts, dashboard, role-based access, and premium plan with payments. Admins can see analytics."
    result = run_pipeline(prompt)
    print(json.dumps(result, indent=2))