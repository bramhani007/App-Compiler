import json
from openai import OpenAI
from dotenv import load_dotenv
from jsonschema import validate, ValidationError

load_dotenv()
client = OpenAI()

import os
schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "schemas", "architecture.json")
with open(schema_path) as f:
    ARCH_SCHEMA = json.load(f)

SYSTEM_PROMPT = f"""
You are a system architect. Given the structured intent, design a complete app architecture.
Output JSON exactly matching this schema:
{json.dumps(ARCH_SCHEMA["properties"], indent=2)}

The output must contain:
- pages: list of page names
- entities: objects with name and fields
- apis: list of API endpoints (path, method, description)
- roles: list of roles

Use the intent to infer the architecture. Do not add extra keys.
"""

def design_architecture(intent: dict) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(intent)}
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )
    arch = json.loads(response.choices[0].message.content)
    validate(instance=arch, schema=ARCH_SCHEMA)
    return arch