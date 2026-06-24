import json
from openai import OpenAI
from jsonschema import validate

from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()

schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "schemas", "business_logic.json")
with open(schema_path) as f:
    BL_SCHEMA = json.load(f)

SYSTEM_PROMPT = f"""
Generate business logic configuration (premium features, role gating)
based on the intent and architecture.
Schema:
{json.dumps(BL_SCHEMA["properties"], indent=2)}
"""

def generate_business_logic(architecture: dict, intent: dict) -> dict:
    user_msg = {"architecture": architecture, "intent": intent}
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(user_msg)}
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )
    bl = json.loads(response.choices[0].message.content)
    validate(instance=bl, schema=BL_SCHEMA)
    return bl