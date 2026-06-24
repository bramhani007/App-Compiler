import json
import time
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from main import run_pipeline
from test_prompts import prompts
import pandas as pd

results = []
for idx, prompt in enumerate(prompts):
    start = time.time()
    try:
        config = run_pipeline(prompt)
        if "error" in config:
            success = False
            failure_type = "clarification" if config.get("error")=="clarification_needed" else "other"
        else:
            issues = config.get("_remaining_issues", [])
            success = len(issues) == 0
            failure_type = "inconsistencies" if not success else "none"
        latency = time.time() - start
        results.append({
            "prompt": prompt[:100],
            "success": success,
            "failure_type": failure_type,
            "latency": latency,
            "retries": 0  # simplified, we don't track retries in this quick version
        })
    except Exception as e:
        results.append({
            "prompt": prompt[:100],
            "success": False,
            "failure_type": str(e)[:50],
            "latency": time.time() - start,
            "retries": 0
        })

df = pd.DataFrame(results)
print(df)
print("\nSuccess rate:", df["success"].mean())
print("Average latency:", df["latency"].mean())
df.to_csv("evaluation_results.csv", index=False)