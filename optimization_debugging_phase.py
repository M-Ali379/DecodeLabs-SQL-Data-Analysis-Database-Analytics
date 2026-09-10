import sqlite3

DB_PATH = "space_missions.db"

def execute_optimization_and_debugging():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("=" * 90)
    print("STEP 6: QUERY ENGINE OPTIMIZATION & DEBUGGING DEMONSTRATION")
    print("Logical Order: FROM/JOIN (1) -> WHERE (2) -> GROUP BY (3) -> HAVING (4) -> SELECT (5) -> ORDER BY (6)")
    print("=" * 90)
    print("\n")

    # -------------------------------------------------------------------------
    # DEMO 1: THE ALIAS TRAP (Error Prevention & Fix)
    # -------------------------------------------------------------------------
    print("-" * 90)
    print("DEMO 1: AVOIDING THE ALIAS TRAP")
    print("Description: Demonstrates why WHERE (Step 2) fails when accessing SELECT aliases (Step 5), and provides corrected syntax.")
    print("-" * 90)
    
    broken_sql = """
SELECT agency AS clean_agency, COUNT(*) AS cnt
FROM space_missions
WHERE clean_agency = 'NASA'
GROUP BY clean_agency;
    """
    print("Attempting Broken SQL (Accessing SELECT alias 'clean_agency' in WHERE clause):")
    print(broken_sql.strip())
    
    try:
        cursor.execute(broken_sql)
    except sqlite3.OperationalError as e:
        print(f"\n[EXPECTED RUNTIME ERROR]: {e}")
        print("EXPLANATION: WHERE (Step 2) evaluates BEFORE SELECT (Step 5). The alias 'clean_agency' does not exist yet when WHERE executes!\n")

    fixed_sql = """
SELECT agency AS clean_agency, COUNT(*) AS cnt
FROM space_missions
WHERE agency = 'NASA' OR agency = 'nasa'
GROUP BY agency
ORDER BY cnt DESC;
    """
    print("Executing Corrected SQL (Filtering using underlying column in WHERE clause):")
    print(fixed_sql.strip())
    print("-" * 90)
    cursor.execute(fixed_sql)
    rows = cursor.fetchall()
    for r in rows:
        print(f"clean_agency: {r[0]:<15} | cnt: {r[1]}")
    print("\n")

    # -------------------------------------------------------------------------
    # DEMO 2: EARLY ROW FILTERING (WHERE vs HAVING Performance Optimization)
    # -------------------------------------------------------------------------
    print("-" * 90)
    print("DEMO 2: EARLY ROW FILTERING (WHERE vs HAVING OPTIMIZATION)")
    print("Description: Compares filtering early in WHERE (Step 2) vs filtering late in HAVING (Step 4).")
    print("-" * 90)

    late_filter_sql = """
SELECT agency, COUNT(*) AS total_missions
FROM space_missions
GROUP BY agency
HAVING agency = 'ESA';
    """
    print("Unoptimized (Late Filter in HAVING - aggregates all rows first):")
    print(late_filter_sql.strip())

    early_filter_sql = """
SELECT agency, COUNT(*) AS total_missions
FROM space_missions
WHERE agency = 'ESA'
GROUP BY agency;
    """
    print("\nOptimized (Early Filter in WHERE - prunes rows prior to GROUP BY):")
    print(early_filter_sql.strip())
    print("-" * 90)
    cursor.execute(early_filter_sql)
    print("Result Set (Optimized):", cursor.fetchall())
    print("\n")

    # -------------------------------------------------------------------------
    # DEMO 3: EXPLAIN QUERY PLAN (Query Engine Inspection)
    # -------------------------------------------------------------------------
    print("-" * 90)
    print("DEMO 3: EXPLAIN QUERY PLAN (Engine Inspection)")
    print("Description: Inspecting internal engine execution plan to verify table scans and optimization steps.")
    print("-" * 90)

    explain_sql = """
EXPLAIN QUERY PLAN
SELECT 
    agency AS "Space Agency", 
    COUNT(*) AS "Total Missions", 
    ROUND(AVG(mission_duration_days), 2) AS "Avg Duration"
FROM space_missions
WHERE agency IS NOT NULL AND agency != ''
GROUP BY agency
HAVING COUNT(*) >= 2
ORDER BY "Avg Duration" DESC;
    """
    print("Executing EXPLAIN QUERY PLAN:")
    print(explain_sql.strip())
    print("-" * 90)
    cursor.execute(explain_sql)
    plan_rows = cursor.fetchall()
    print(f"{'id':<5} | {'parent':<8} | {'notused':<8} | {'detail':<50}")
    print("-" * 75)
    for row in plan_rows:
        print(f"{row[0]:<5} | {row[1]:<8} | {row[2]:<8} | {row[3]:<50}")
    print("\n")

    conn.close()

if __name__ == "__main__":
    execute_optimization_and_debugging()
