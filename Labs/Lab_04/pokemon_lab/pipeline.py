#!/usr/bin/env python3
# ...existing code...
import sys
import update_portfolio
import generate_summary

def run_production_pipeline():
    print("Starting production pipeline...", file=sys.stderr)
    print("Running ETL (update_portfolio)...", file=sys.stderr)
    update_portfolio.main()
    print("Running reporting (generate_summary)...", file=sys.stderr)
    generate_summary.main()
    print("Production pipeline complete.", file=sys.stderr)

if __name__ == "__main__":
    run_production_pipeline()
# ...existing code...