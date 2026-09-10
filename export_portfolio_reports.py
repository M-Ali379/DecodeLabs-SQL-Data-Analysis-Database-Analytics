import sqlite3
import csv
import os

DB_PATH = "space_missions.db"
EXPORTS_DIR = "exports"

def export_portfolio_reports():
    os.makedirs(EXPORTS_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    reports = [
        {
            "filename": "executive_agency_performance.csv",
            "title": "Executive Agency Performance Report",
            "sql": """
SELECT 
    agency AS "Space Agency", 
    COUNT(*) AS "Total Mission Volume", 
    ROUND(AVG(mission_duration_days), 2) AS "Average Duration (Days)",
    MAX(mission_duration_days) AS "Peak Duration (Days)"
FROM space_missions
WHERE agency IS NOT NULL AND agency != ''
GROUP BY agency
ORDER BY "Average Duration (Days)" DESC;
            """
        },
        {
            "filename": "destination_orbit_report.csv",
            "title": "Destination Orbit Distribution Report",
            "sql": """
SELECT 
    destination AS "Target Destination", 
    COUNT(*) AS "Flight Count", 
    ROUND(AVG(mission_duration_days), 1) AS "Mean Orbital Days"
FROM space_missions
WHERE destination IS NOT NULL AND destination != ''
GROUP BY destination
ORDER BY "Flight Count" DESC, "Target Destination" ASC;
            """
        },
        {
            "filename": "annual_launch_trends.csv",
            "title": "Annual Launch Activity Trends",
            "sql": """
SELECT 
    launch_year AS "Launch Year", 
    COUNT(*) AS "Annual Launch Count",
    MIN(mission_duration_days) AS "Min Duration (Days)",
    MAX(mission_duration_days) AS "Max Duration (Days)"
FROM space_missions
WHERE launch_year IS NOT NULL
GROUP BY launch_year
HAVING COUNT(*) >= 3
ORDER BY "Launch Year" ASC;
            """
        },
        {
            "filename": "data_audit_validation.csv",
            "title": "Data Audit & Integrity Validation Report",
            "sql": """
SELECT 
    agency AS "Space Agency",
    mission_status AS "Mission Status",
    COUNT(*) AS "Record Count",
    SUM(CASE WHEN mission_duration_days IS NULL THEN 1 ELSE 0 END) AS "Missing Duration Count"
FROM space_missions
WHERE agency IS NOT NULL AND agency != ''
GROUP BY agency, mission_status
ORDER BY "Space Agency" ASC, "Mission Status" ASC;
            """
        }
    ]

    print("=" * 80)
    print("STARTING EXECUTIVE CSV REPORT EXPORT")
    print("=" * 80)

    for r in reports:
        filepath = os.path.join(EXPORTS_DIR, r["filename"])
        cursor.execute(r["sql"])
        rows = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(col_names)
            writer.writerows(rows)

        print(f"[EXPORT SUCCESS] Saved '{r['title']}' ({len(rows)} rows) -> {filepath}")

    conn.close()
    print("=" * 80)
    print("ALL PORTFOLIO REPORT EXPORTS COMPLETED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    export_portfolio_reports()
