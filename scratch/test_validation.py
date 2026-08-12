import sys
import os
import json

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from ashen_vector.api.services.validation_runner import run_validation_job

def run():
    print("Starting validation test...")
    try:
        res = run_validation_job(
            symbol="AAPL",
            model_name="LightGBM Classification",
            horizon=21,
            n_splits=3
        )
        print("Success! Keys:")
        print(res.keys())
        print("\nPredictive Performance:")
        print(json.dumps(res["predictive_performance"], indent=2))
        print("\nTrading Performance:")
        print(json.dumps(res["trading_performance"], indent=2))
        print("\nVerdict:")
        print(res["verdict"])
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    run()
