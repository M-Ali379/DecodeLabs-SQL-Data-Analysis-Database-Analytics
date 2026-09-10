import sqlite3

DB_PATH = "space_missions.db"

def execute_filtering_queries():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    queries = [
        {
            "technique": "1. Exact Matching",
            "condition": "WHERE destination = 'Mars'",
            "sql": """
SELECT mission_id, agency, launch_year, mission_duration_days, destination, mission_status
FROM space_missions
WHERE destination = 'Mars'
LIMIT 10;
            """
        },
        {
            "technique": "2. Numeric Range Filtering",
            "condition": "WHERE mission_duration_days >= 1000",
            "sql": """
SELECT mission_id, agency, launch_year, mission_duration_days, destination, mission_status
FROM space_missions
WHERE mission_duration_days >= 1000
LIMIT 10;
            """
        },
        {
            "technique": "3. Pattern Matching (LIKE)",
            "condition": "WHERE mission_id LIKE 'M01%'",
            "sql": """
SELECT mission_id, agency, launch_year, mission_duration_days, destination, mission_status
FROM space_missions
WHERE mission_id LIKE 'M01%';
            """
        }
    ]

    for q in queries:
        print("=" * 85)
        print(f"TECHNIQUE: {q['technique']}")
        print(f"CONDITION: {q['condition']}")
        print("-" * 85)
        print("SQL QUERY:")
        print(q['sql'].strip())
        print("-" * 85)
        
        cursor.execute(q['sql'])
        rows = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]
        
        # Display header
        header = " | ".join(f"{name:<20}" for name in col_names)
        print(header)
        print("-" * len(header))
        
        # Display rows
        for r in rows:
            row_str = " | ".join(f"{str(val if val is not None else 'NULL'):<20}" for val in r)
            print(row_str)
        print(f"\n[Total Rows Returned: {len(rows)}]\n")

    conn.close()

if __name__ == "__main__":
    execute_filtering_queries()
