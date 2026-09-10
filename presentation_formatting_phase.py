import sqlite3

DB_PATH = "space_missions.db"

def execute_presentation_queries():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    queries = [
        {
            "title": "1. Executive Agency Summary (Aliases & Alias Sorting)",
            "description": "Column Aliases: Space Agency, Total Mission Volume, Average Duration (Days), Peak Duration (Days) | Sorting: ORDER BY 'Average Duration (Days)' DESC",
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
            "title": "2. Destination Flight Distribution Report",
            "description": "Column Aliases: Target Destination, Flight Count, Mean Orbital Days | Sorting: ORDER BY 'Flight Count' DESC, 'Target Destination' ASC",
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
            "title": "3. Result Set Validation & Data Audit",
            "description": "Validation: Auditing group result sets for missing calculation values or null anomalies",
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

    for q in queries:
        print("=" * 90)
        print(f"REPORT: {q['title']}")
        print(f"Details: {q['description']}")
        print("-" * 90)
        print("SQL STATEMENT:")
        print(q['sql'].strip())
        print("-" * 90)
        
        cursor.execute(q['sql'])
        rows = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]
        
        # Display header
        header = " | ".join(f"{name:<25}" for name in col_names)
        print(header)
        print("-" * len(header))
        
        # Display rows
        for r in rows:
            row_str = " | ".join(f"{str(val if val is not None else 'NULL'):<25}" for val in r)
            print(row_str)
        print(f"\n[Validated Row Count: {len(rows)}]\n")

    conn.close()

if __name__ == "__main__":
    execute_presentation_queries()
