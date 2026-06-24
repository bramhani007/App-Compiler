import json
from openai import OpenAI
from jsonschema import validate

from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()

schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "schemas", "db.json")
with open(schema_path) as f:
    DB_SCHEMA = json.load(f)

SYSTEM_PROMPT = f"""
Generate a database schema (tables, columns, relations) from the architecture entities.
Follow this schema:
{json.dumps(DB_SCHEMA["properties"], indent=2)}
"""

def generate_db(architecture: dict) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(architecture)}
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )
    db = json.loads(response.choices[0].message.content)
    validate(instance=db, schema=DB_SCHEMA)
    return db