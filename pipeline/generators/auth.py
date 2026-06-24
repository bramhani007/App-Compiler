import json
from openai import OpenAI
from jsonschema import validate

from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()

schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "schemas", "auth.json")
with open(schema_path) as f:
    AUTH_SCHEMA = json.load(f)

SYSTEM_PROMPT = f"""
Generate an authentication/authorization schema.
Roles and permissions should align with the architecture's roles and APIs.
Follow this schema:
{json.dumps(AUTH_SCHEMA["properties"], indent=2)}
"""

def generate_auth(architecture: dict) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(architecture)}
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )
    auth = json.loads(response.choices[0].message.content)
    validate(instance=auth, schema=AUTH_SCHEMA)
    return auth