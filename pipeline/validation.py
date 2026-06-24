import json
from typing import Dict, List, Tuple

def cross_validate(config: dict) -> List[str]:
    """
    Check cross-layer consistency:
    - API fields match DB columns
    - UI dataBindings reference existing APIs
    - Auth roles mapped to API rolesAllowed
    Returns a list of inconsistencies found.
    """
    issues = []
    
    # Extract pieces safely
    api_endpoints = config.get("api", {}).get("endpoints", []) or []
    db_tables = config.get("db", {}).get("tables", []) or []
    ui_pages = config.get("ui", {}).get("pages", []) or []
    auth_roles = config.get("auth", {}).get("roles", []) or []
    
    # Build API path registry (case-insensitive)
    api_registry = {f"{ep.get('method')} {ep.get('path')}".lower() for ep in api_endpoints if ep.get("method") and ep.get("path")}
    
    # Check UI dataBindings
    for page in ui_pages:
        for comp in page.get("components", []):
            binding = comp.get("dataBinding")
            if binding and binding.lower() not in api_registry:
                issues.append(f"UI component '{comp['type']}' on page '{page['name']}' references unknown API: {binding}")
    
    # Check API <-> DB field consistency
    for ep in api_endpoints:
        path = ep.get("path", "")
        # Skip system, auth, and analytics/stats endpoints
        skip_keywords = ["login", "logout", "auth", "analytics", "stats", "session"]
        if any(kw in path.lower() for kw in skip_keywords):
            continue
            
        resp = ep.get("response", {})
        if not resp:
            continue
            
        # Support both nested schema properties and flat dict key formats
        if "properties" in resp:
            resp_fields = list(resp.get("properties", {}).keys())
        else:
            resp_fields = [k for k in resp.keys() if k != "type"]
            
        # Ignore common non-DB fields in response
        ignored_fields = {"token", "success", "error", "message", "status", "count", "page", "limit"}
        resp_fields = [f for f in resp_fields if f not in ignored_fields]
        
        if not resp_fields:
            continue
            
        # Heuristic: find tables whose names overlap with the API path words
        path_words = [w.strip("/").lower() for w in path.split("/") if w]
        
        found = False
        for table in db_tables:
            table_name_lower = table.get("name", "").lower()
            is_related_table = any(w in table_name_lower or table_name_lower in w for w in path_words)
            if is_related_table:
                table_fields = [col.get("name", "").lower() for col in table.get("columns", [])]
                if all(f.lower() in table_fields for f in resp_fields):
                    found = True
                    break
        
        # Fallback: check across all tables if no related table matches
        if not found:
            for table in db_tables:
                table_fields = [col.get("name", "").lower() for col in table.get("columns", [])]
                if all(f.lower() in table_fields for f in resp_fields):
                    found = True
                    break
                    
        if not found:
            issues.append(f"API {ep.get('method')} {ep.get('path')} response fields {resp_fields} not found in any matching DB table columns")
    
    # Check auth roles vs api rolesAllowed
    role_names = [r.get("name") for r in auth_roles if r.get("name")]
    for ep in api_endpoints:
        if ep.get("authRequired"):
            allowed = ep.get("rolesAllowed") or []
            for r in allowed:
                if r not in role_names:
                    issues.append(f"API {ep.get('method')} {ep.get('path')} references unknown role '{r}'")
    
    return issues