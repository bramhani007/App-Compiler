import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import os

app = FastAPI()
current_dir = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))

# In a real scenario, the config would be loaded from a file or passed
config_file = os.path.join(current_dir, "..", "final_config.json")
if os.path.exists(config_file):
    with open(config_file) as f:
        config = json.load(f)
else:
    # Use a sample hardcoded config for testing
    config = {
        "api": {
            "endpoints": [
                {"path": "/login", "method": "POST", "response": {"token": "string"}, "authRequired": False},
                {"path": "/contacts", "method": "GET", "response": {"contacts": "array"}, "authRequired": True, "rolesAllowed": ["user", "admin"]},
                {"path": "/analytics", "method": "GET", "response": {"stats": "object"}, "authRequired": True, "rolesAllowed": ["admin"]}
            ]
        },
        "auth": {
            "roles": [{"name": "user", "permissions": ["read_contacts"]}, {"name": "admin", "permissions": ["read_contacts", "read_analytics"]}]
        }
    }

# Load Intermediate Representation (IR)
ir_file = os.path.join(current_dir, "..", "ir.json")
if os.path.exists(ir_file):
    with open(ir_file) as f:
        ir_data = json.load(f)
else:
    # Use a sample hardcoded IR for testing
    ir_data = {
        "app_type": "CRM (Customer Relationship Management)",
        "features": ["User login", "Contact management", "Dashboard analytics", "Role-based access", "Payments integration"],
        "roles": ["user", "admin"],
        "entities": [
            {"name": "contacts", "fields": ["id", "name", "email", "phone", "company"]},
            {"name": "payments", "fields": ["id", "amount", "status", "payment_date"]}
        ],
        "assumptions": [
            "Assume CRM will handle lead tracking, customer contact details, and basic sub-based payment status.",
            "Assume Stripe or similar third-party gateway for credit card details.",
            "Admins have all permissions of users plus custom sales reports access."
        ],
        "timestamp": "2026-06-24T17:00:00.000000"
    }

# Simple mock auth
def check_auth(request: Request, roles_allowed):
    # In a real app, you'd check JWT. Here we just allow all for demo.
    return True

# Dynamically create endpoints with correct path parameter signatures
import re

def create_endpoint_handler(path: str, response_data: dict):
    params = re.findall(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", path)
    param_str = ", ".join(f"{p}: str = None" for p in params)
    local_vars = {}
    func_code = f"async def handler({param_str}):\n    return response_data"
    exec(func_code, {"response_data": response_data}, local_vars)
    return local_vars["handler"]

for ep in config.get("api", {}).get("endpoints", []):
    path = ep["path"]
    method = ep["method"].lower()
    resp = ep.get("response")
    if isinstance(resp, dict):
        response_data = {"mock": True, **resp}
    else:
        response_data = {"mock": True, "data": resp}
    handler_func = create_endpoint_handler(path, response_data)
    # Register route
    app.add_api_route(path, handler_func, methods=[method])

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Render the UI from the config (simplified)
    ui_config = config.get("ui") or {"pages": []}
    return templates.TemplateResponse(
        request=request,
        name="app.html",
        context={"pages": ui_config.get("pages", []), "json_dumps": json.dumps, "ir": ir_data}
    )

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)