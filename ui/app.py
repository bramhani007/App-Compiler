import streamlit as st
import sys
sys.path.append("..")
from main import run_pipeline
import json

st.set_page_config(page_title="App Builder Pipeline", layout="wide")
st.title("🧠 App Builder – Multi‑Stage Compiler")

user_input = st.text_area("Describe your application:", "Build a CRM with login, contacts, dashboard, role-based access, and premium plan with payments. Admins can see analytics.")

if st.button("Generate Configuration", type="primary"):
    with st.spinner("Running pipeline..."):
        try:
            result = run_pipeline(user_input)
            if "error" in result and result["error"] == "clarification_needed":
                st.warning(f"Need clarification: {result['question']}")
            else:
                st.success("Configuration generated!")
                st.json(result)
                # Save for runtime
                import os
                root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                config_path = os.path.join(root_dir, "final_config.json")
                with open(config_path, "w") as f:
                    json.dump(result, f, indent=2)
                st.info("Saved to final_config.json in project root. You can now run the runtime server.")
        except Exception as e:
            st.error(f"Pipeline failed: {str(e)}")