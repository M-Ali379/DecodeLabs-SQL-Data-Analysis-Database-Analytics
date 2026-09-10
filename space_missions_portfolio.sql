-- ============================================================================
-- SQL DATA ANALYSIS PORTFOLIO: SPACE MISSIONS DATASET
-- Database Engine: SQLite / PostgreSQL / MySQL Compatible ANSI SQL
-- Description: End-to-end data setup, row filtering, aggregation metrics,
--              presentation formatting, and query optimization pipeline.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- STEP 1: ENVIRONMENT & DATABASE SETUP
-- Business Logic: Create target schema to ingest raw space missions data.
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS space_missions;

CREATE TABLE space_missions (
    mission_id VARCHAR(10),
    agency VARCHAR(50),
    launch_year INT,
    mission_duration_days INT,
    destination VARCHAR(50),
    mission_status VARCHAR(50)
);

-- Data Verification: Inspect initial 10 records after CSV ingestion
SELECT * FROM space_missions LIMIT 10;


-- ----------------------------------------------------------------------------
-- STEP 2: INPUT PHASE - STRUCTURING RAW QUERIES
-- Business Logic: Construct declarative queries adhering to logical syntax order:
-- SELECT -> FROM -> WHERE -> GROUP BY -> HAVING -> ORDER BY
-- ----------------------------------------------------------------------------

-- Requirement 1: Agency performance & average mission duration
-- Logic: Group by agency, calculate total volume and average duration for agencies with >= 2 missions.
SELECT 
    agency, 
    COUNT(*) AS total_missions, 
    ROUND(AVG(mission_duration_days), 2) AS avg_duration_days
FROM space_missions
WHERE agency IS NOT NULL AND agency != ''
GROUP BY agency
HAVING COUNT(*) >= 2
ORDER BY avg_duration_days DESC;

-- Requirement 2: Mission outcomes distribution across destinations
-- Logic: Breakdown status counts per target destination.
SELECT 
    destination, 
    mission_status, 
    COUNT(*) AS mission_count
FROM space_missions
WHERE destination IS NOT NULL AND destination != ''
GROUP BY destination, mission_status
ORDER BY destination ASC, mission_count DESC;

-- Requirement 3: Annual launch trends & duration bounds
-- Logic: Aggregate launches per year for active years with >= 3 launches.
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


-- ----------------------------------------------------------------------------
-- STEP 3: FILTERING PHASE - ROW-LEVEL ISOLATION (WHERE)
-- Business Logic: Apply WHERE clauses prior to group aggregation to isolate candidate rows.
-- ----------------------------------------------------------------------------

-- 1. Exact Matching: Isolate missions targeted to Mars
SELECT mission_id, agency, launch_year, mission_duration_days, destination, mission_status
FROM space_missions
WHERE destination = 'Mars';

-- 2. Numeric Range Filtering: Isolate long-duration missions (>= 1,000 days)
SELECT mission_id, agency, launch_year, mission_duration_days, destination, mission_status
FROM space_missions
WHERE mission_duration_days >= 1000;

-- 3. Pattern Matching (LIKE): Match mission IDs starting with 'M01'
SELECT mission_id, agency, launch_year, mission_duration_days, destination, mission_status
FROM space_missions
WHERE mission_id LIKE 'M01%';


-- ----------------------------------------------------------------------------
-- STEP 4: AGGREGATION & GROUPING PHASE (GROUP BY & AGGREGATES)
-- Business Logic: Transform raw records into executive metrics (COUNT, SUM, AVG) with HAVING filters.
-- ----------------------------------------------------------------------------

-- Agency Executive Summary: Cumulative & average space duration
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

-- Destination Volume & Orbit Cumulative Time
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


-- ----------------------------------------------------------------------------
-- STEP 5: PRESENTATION & FORMATTING PHASE (SELECT & ORDER BY)
-- Business Logic: Assign clean business aliases and order results on projected aliases.
-- ----------------------------------------------------------------------------

-- Executive Agency Performance Report
SELECT 
    agency AS "Space Agency", 
    COUNT(*) AS "Total Mission Volume", 
    ROUND(AVG(mission_duration_days), 2) AS "Average Duration (Days)",
    MAX(mission_duration_days) AS "Peak Duration (Days)"
FROM space_missions
WHERE agency IS NOT NULL AND agency != ''
GROUP BY agency
ORDER BY "Average Duration (Days)" DESC;

-- Destination Flight Distribution Report
SELECT 
    destination AS "Target Destination", 
    COUNT(*) AS "Flight Count", 
    ROUND(AVG(mission_duration_days), 1) AS "Mean Orbital Days"
FROM space_missions
WHERE destination IS NOT NULL AND destination != ''
GROUP BY destination
ORDER BY "Flight Count" DESC, "Target Destination" ASC;

-- Data Audit & Validation Query (Checking for missing duration calculations)
SELECT 
    agency AS "Space Agency",
    mission_status AS "Mission Status",
    COUNT(*) AS "Record Count",
    SUM(CASE WHEN mission_duration_days IS NULL THEN 1 ELSE 0 END) AS "Missing Duration Count"
FROM space_missions
WHERE agency IS NOT NULL AND agency != ''
GROUP BY agency, mission_status
ORDER BY "Space Agency" ASC, "Mission Status" ASC;


-- ----------------------------------------------------------------------------
-- STEP 6: QUERY ENGINE OPTIMIZATION & DEBUGGING
-- Engine Execution Order: FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY
-- Note: Avoid alias traps (using SELECT aliases in WHERE). Filter early in WHERE!
-- ----------------------------------------------------------------------------

-- Optimized Query (Early Row Filtering in WHERE prior to GROUP BY)
SELECT agency AS clean_agency, COUNT(*) AS cnt
FROM space_missions
WHERE agency = 'NASA' OR agency = 'nasa'
GROUP BY agency
ORDER BY cnt DESC;

-- Query Engine Plan Inspection
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
