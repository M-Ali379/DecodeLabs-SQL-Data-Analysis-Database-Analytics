import sqlite3

DB_PATH = "space_missions.db"

def execute_aggregation_queries():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    queries = [
        {
            "title": "1. Agency Executive Metrics (SUM, AVG, COUNT, HAVING)",
            "description": "Categorical Bucketing: agency | HAVING: SUM(duration) > 10000 | Aggregates: COUNT(*), SUM(), AVG()",
            "sql": """
SELECT 
    agency, 
    COUNT(*) AS total_missions, 
    SUM(mission_duration_days) AS total_space_days, 
    ROUND(AVG(mission_duration_days), 2) AS avg_space_days
FROM space_missions
WHERE agency IS NOT NULL AND agency != ''
GROUP BY agency
HAVING SUM(mission_duration_days) > 10000
ORDER BY total_space_days DESC;
            """
        },
        {
            "title": "2. Destination Volume & Orbit Metrics",
            "description": "Categorical Bucketing: destination | HAVING: COUNT(*) >= 10 | Aggregates: COUNT(*), SUM(), AVG()",
            "sql": """
SELECT 
    destination, 
    COUNT(*) AS mission_volume, 
    SUM(mission_duration_days) AS total_days_in_orbit, 
    ROUND(AVG(mission_duration_days), 1) AS avg_days_in_orbit
FROM space_missions
WHERE destination IS NOT NULL AND destination != ''
GROUP BY destination
HAVING COUNT(*) >= 10
ORDER BY total_days_in_orbit DESC;
            """
        },
        {
            "title": "3. Multi-Level Grouping (Agency & Status)",
            "description": "Categorical Bucketing: agency, mission_status | HAVING: AVG(duration) >= 800",
            "sql": """
SELECT 
    agency, 
    mission_status, 
    COUNT(*) AS volume, 
    SUM(mission_duration_days) AS cumulative_duration, 
    ROUND(AVG(mission_duration_days), 2) AS mean_duration
FROM space_missions
WHERE agency IS NOT NULL AND agency != ''
GROUP BY agency, mission_status
HAVING AVG(mission_duration_days) >= 800
ORDER BY agency ASC, mean_duration DESC;
            """
        }
    ]

    for q in queries:
        print("=" * 85)
        print(f"QUERY: {q['title']}")
        print(f"Details: {q['description']}")
        print("-" * 85)
        print("SQL STATEMENT:")
        print(q['sql'].strip())
        print("-" * 85)
        
        cursor.execute(q['sql'])
        rows = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]
        
        # Display header
        header = " | ".join(f"{name:<23}" for name in col_names)
        print(header)
        print("-" * len(header))
        
        # Display rows
        for r in rows:
            row_str = " | ".join(f"{str(val if val is not None else 'NULL'):<23}" for val in r)
            print(row_str)
        print(f"\n[Total Metric Groups Returned: {len(rows)}]\n")

    conn.close()

if __name__ == "__main__":
    execute_aggregation_queries()
