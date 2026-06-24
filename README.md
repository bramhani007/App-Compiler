# App Builder – Multi-Stage Compiler Pipeline

Converts natural language app descriptions into a validated, executable configuration (UI, API, DB, Auth, Business Logic).

## Setup
1. `pip install -r requirements.txt`
2. Create `.env` with `OPENAI_API_KEY=your-key`
3. Ensure JSON schema files are in `schemas/`

## Run Pipeline (CLI)
`python main.py "Build a CRM with login, contacts, dashboard, role-based access..."`

## Streamlit UI
`streamlit run ui/app.py`

## Runtime Simulation
After generating a config (saved as `final_config.json`):
`python runtime/server.py`
Open http://localhost:8000 to see the generated app skeleton.

## Evaluation
`python evaluation/evaluate.py`
Generates `evaluation_results.csv` with success rates and latency.

## Architecture
Multi-stage pipeline: Intent Extraction → System Design → Schema Generation (UI, API, DB, Auth, Biz Logic) → Refinement & Validation → Executable Output.