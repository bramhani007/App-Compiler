import json
from openai import OpenAI
from jsonschema import validate

from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()

schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "schemas", "api.json")
with open(schema_path) as f:
    API_SCHEMA = json.load(f)

SYSTEM_PROMPT = f"""
You generate an API schema from an architecture.
Include full request/response bodies consistent with the entities.
Schema to follow:
{json.dumps(API_SCHEMA["properties"], indent=2)}
"""

def generate_api(architecture: dict) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(architecture)}
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )
    api = json.loads(response.choices[0].message.content)
    validate(instance=api, schema=API_SCHEMA)
    return api