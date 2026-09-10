import sqlite3
import csv
import os

DB_PATH = "space_missions.db"
CSV_PATH = "kdd_space_messy_dataset.csv"

def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Drop existing table if re-running
    cursor.execute("DROP TABLE IF EXISTS space_missions;")

    # Create target table schema
    cursor.execute("""
    CREATE TABLE space_missions (
        mission_id VARCHAR(10),
        agency VARCHAR(50),
        launch_year INT,
        mission_duration_days INT,
        destination VARCHAR(50),
        mission_status VARCHAR(50)
    );
    """)

    # Read and bulk insert CSV data
    inserted_count = 0
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mission_id = row['mission_id'].strip() if row['mission_id'] else None
            agency = row['agency'].strip() if row['agency'] else None
            
            launch_year_raw = row['launch_year'].strip()
            launch_year = int(launch_year_raw) if launch_year_raw.isdigit() else None
            
            duration_raw = row['mission_duration_days'].strip()
            mission_duration_days = int(duration_raw) if duration_raw.isdigit() else None
            
            destination = row['destination'].strip() if row['destination'] else None
            mission_status = row['mission_status'].strip() if row['mission_status'] else None

            cursor.execute("""
                INSERT INTO space_missions (
                    mission_id, agency, launch_year, mission_duration_days, destination, mission_status
                ) VALUES (?, ?, ?, ?, ?, ?);
            """, (mission_id, agency, launch_year, mission_duration_days, destination, mission_status))
            inserted_count += 1

    conn.commit()
    print(f"[SUCCESS] Database created and {inserted_count} records inserted successfully into 'space_missions' table.\n")

    # Verify Data Ingestion (SELECT * FROM table_name LIMIT 10;)
    print("--- SQL QUERY VERIFICATION ---")
    print("Executing: SELECT * FROM space_missions LIMIT 10;\n")
    
    cursor.execute("SELECT * FROM space_missions LIMIT 10;")
    rows = cursor.fetchall()
    
    # Get column names
    col_names = [description[0] for description in cursor.description]
    
    # Format table output
    header_str = " | ".join(f"{name:<21}" for name in col_names)
    print(header_str)
    print("-" * len(header_str))
    
    for row in rows:
        row_str = " | ".join(f"{str(val if val is not None else 'NULL'):<21}" for val in row)
        print(row_str)

    conn.close()

if __name__ == "__main__":
    setup_database()
