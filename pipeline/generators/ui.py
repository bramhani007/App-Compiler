import json
from openai import OpenAI
from jsonschema import validate

from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()

schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "schemas", "ui.json")
with open(schema_path) as f:
    UI_SCHEMA = json.load(f)

SYSTEM_PROMPT = f"""
You are a UI schema generator. Based on the architecture (pages, entities, APIs),
generate a UI configuration that matches this schema:
{json.dumps(UI_SCHEMA["properties"], indent=2)}

Each page must have a layout and components. Components should reference APIs in dataBinding when applicable (e.g. "GET /contacts").
Use common UI components like Table, Form, Button, etc.
Output ONLY valid JSON.
"""

def generate_ui(architecture: dict) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(architecture)}
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )
    ui = json.loads(response.choices[0].message.content)
    validate(instance=ui, schema=UI_SCHEMA)
    return ui