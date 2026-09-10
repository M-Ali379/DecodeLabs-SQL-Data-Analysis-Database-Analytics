import sys
import os

def run_all():
    print("#" * 90)
    print("      COMPLETE END-TO-END SQL DATA ANALYSIS PIPELINE EXECUTION")
    print("      Project: Space Missions Dataset Analytics")
    print("#" * 90)
    print("\n")

    steps = [
        ("STEP 1: Database Setup & Data Ingestion", "setup_database.py"),
        ("STEP 2: Declarative Query Structuring", "structured_queries.py"),
        ("STEP 3: Row-Level Filtering (WHERE)", "filtering_phase.py"),
        ("STEP 4: Aggregation & Grouping (GROUP BY & HAVING)", "aggregation_phase.py"),
        ("STEP 5: Presentation & Report Formatting (SELECT & ORDER BY)", "presentation_formatting_phase.py"),
        ("STEP 6: Query Engine Optimization & Debugging", "optimization_debugging_phase.py"),
        ("STEP 7: Executive CSV Reports Export", "export_portfolio_reports.py")
    ]

    for title, script in steps:
        print("#" * 90)
        print(f" >>> RUNNING {title} ({script})")
        print("#" * 90)
        print("\n")
        
        # Execute script
        ret = os.system(f"{sys.executable} {script}")
        if ret != 0:
            print(f"[ERROR] Script {script} failed with exit code {ret}")
            sys.exit(ret)
        print("\n" + "." * 90 + "\n")

    print("#" * 90)
    print(" SUCCESS: ALL 7 STEPS EXECUTED SUCCESSFULLY!")
    print("#" * 90)

if __name__ == "__main__":
    run_all()
