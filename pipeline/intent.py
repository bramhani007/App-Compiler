import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load the intent JSON schema for reference in prompt
import os
schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "schemas", "intent.json")
with open(schema_path) as f:
    INTENT_SCHEMA = json.load(f)

SYSTEM_PROMPT = f"""
You are an intent extraction system. Analyze the user's app description.
Output a strict JSON object following this schema (with exactly these fields):
{json.dumps(INTENT_SCHEMA["properties"], indent=2)}

Rules:
- If the user is vague, set "clarification_needed": true and provide a question.
- Make reasonable assumptions for missing details and list them in "assumptions".
- Never add extra keys. Only the fields in the schema.
- Output ONLY valid JSON, nothing else.
"""

def extract_intent(user_prompt: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )
    raw = response.choices[0].message.content
    intent = json.loads(raw)
    # Validate against schema
    from jsonschema import validate, ValidationError
    try:
        validate(instance=intent, schema=INTENT_SCHEMA)
    except ValidationError as e:
        # In production you'd trigger repair here; for now raise
        raise ValueError(f"Intent validation failed: {e.message}")
    return intent