import sqlite3

DB_PATH = "space_missions.db"

def execute_structured_queries():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    queries = [
        {
            "title": "Requirement 1: Agency Performance & Average Mission Duration",
            "description": "Columns: agency, total_missions, avg_duration_days | Filter: Non-empty agency | Group: agency | Having: >= 2 missions | Order: avg_duration_days DESC",
            "sql": """
SELECT 
    agency, 
    COUNT(*) AS total_missions, 
    ROUND(AVG(mission_duration_days), 2) AS avg_duration_days
FROM space_missions
WHERE agency IS NOT NULL AND agency != ''
GROUP BY agency
HAVING COUNT(*) >= 2
ORDER BY avg_duration_days DESC;
            """
        },
        {
            "title": "Requirement 2: Mission Outcomes by Destination",
            "description": "Columns: destination, mission_status, mission_count | Filter: Non-empty destination | Group: destination, mission_status | Order: destination ASC, mission_count DESC",
            "sql": """
SELECT 
    destination, 
    mission_status, 
    COUNT(*) AS mission_count
FROM space_missions
WHERE destination IS NOT NULL AND destination != ''
GROUP BY destination, mission_status
ORDER BY destination ASC, mission_count DESC;
            """
        },
        {
            "title": "Requirement 3: Yearly Launch Trends & High-Activity Years",
            "description": "Columns: launch_year, annual_launches, min_duration, max_duration | Filter: Non-empty launch_year | Group: launch_year | Having: >= 3 launches | Order: launch_year ASC",
            "sql": """
SELECT 
    launch_year, 
    COUNT(*) AS annual_launches,
    MIN(mission_duration_days) AS min_duration,
    MAX(mission_duration_days) AS max_duration
FROM space_missions
WHERE launch_year IS NOT NULL
GROUP BY launch_year
HAVING COUNT(*) >= 3
ORDER BY launch_year ASC;
            """
        }
    ]

    for q in queries:
        print("=" * 80)
        print(f"QUERY: {q['title']}")
        print(f"Details: {q['description']}")
        print("-" * 80)
        print("SQL STATEMENT:")
        print(q['sql'].strip())
        print("-" * 80)
        
        cursor.execute(q['sql'])
        rows = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]
        
        # Display header
        header = " | ".join(f"{name:<22}" for name in col_names)
        print(header)
        print("-" * len(header))
        
        # Display rows
        for r in rows:
            row_str = " | ".join(f"{str(val if val is not None else 'NULL'):<22}" for val in r)
            print(row_str)
        print("\n")

    conn.close()

if __name__ == "__main__":
    execute_structured_queries()
