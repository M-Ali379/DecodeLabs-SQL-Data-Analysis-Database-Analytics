# Space Missions SQL Data Analysis & Portfolio Pipeline

An end-to-end relational database analysis pipeline built with ANSI SQL / SQLite, demonstrating data ingestion, row-level filtering, aggregate metrics, executive report formatting, query engine optimization, and automated CSV export reporting.

---

## 📌 Project Overview

This repository contains the complete analytical workflow for processing raw space mission dataset (`75 records`) into structured business intelligence reports.

### Key Capabilities Demonstrated:
- **Database Engine Setup**: SQLite table schema creation with ANSI SQL data types (`VARCHAR`, `INT`).
- **Declarative Query Structuring**: SQL logical execution ordering ($\text{SELECT} \rightarrow \text{FROM} \rightarrow \text{WHERE} \rightarrow \text{GROUP BY} \rightarrow \text{HAVING} \rightarrow \text{ORDER BY}$).
- **Row-Level Isolation (`WHERE`)**: Exact string matching, numerical range filtering, and pattern matching (`LIKE`).
- **Executive Aggregations**: Volume counts (`COUNT(*)`), total space days (`SUM()`), mean duration (`AVG()`), and group filtering (`HAVING`).
- **Report Formatting (`SELECT` & `ORDER BY`)**: Descriptive column aliasing (`AS`) and sorting by projected aliases.
- **Engine Optimization & Debugging**: Alias trap avoidance, early row-level filtering, and execution plan inspection (`EXPLAIN QUERY PLAN`).
- **Automated Reporting**: Python-automated CSV export generation.

---

## 🗄️ Database Schema (`space_missions`)

```sql
CREATE TABLE space_missions (
    mission_id VARCHAR(10),
    agency VARCHAR(50),
    launch_year INT,
    mission_duration_days INT,
    destination VARCHAR(50),
    mission_status VARCHAR(50)
);
```

---

## 📁 Repository Structure

```text
├── space_missions_portfolio.sql     # Master SQL portfolio script with inline comments
├── setup_database.py                # Database initialization and raw CSV ingestion script
├── structured_queries.py            # Basic query structure demonstrations (Step 2)
├── filtering_phase.py               # Row-level isolation queries (Step 3)
├── aggregation_phase.py             # Aggregate metrics & HAVING filter queries (Step 4)
├── presentation_formatting_phase.py # Executive report formatting & aliases (Step 5)
├── optimization_debugging_phase.py # Query optimization & execution plan analysis (Step 6)
├── export_portfolio_reports.py     # Automated CSV report generation script (Step 7)
├── kdd_space_messy_dataset.csv      # Raw space missions dataset
├── space_missions.db                # SQLite database file
└── exports/                         # Executive CSV report outputs
    ├── executive_agency_performance.csv
    ├── destination_orbit_report.csv
    ├── annual_launch_trends.csv
    └── data_audit_validation.csv
```

---

## 📊 Key Executive Findings

### 1. Space Agency Performance Summary
| Space Agency | Total Missions | Avg Duration (Days) | Peak Duration (Days) |
| :--- | :--- | :--- | :--- |
| **ISRO** | 13 | 1,169.31 days | 1,917 days |
| **ESA** | 17 | 1,016.35 days | 1,758 days |
| **NASA** | 15 | 884.13 days | 1,688 days |

### 2. Destination Orbital Distribution
| Target Destination | Flight Volume | Mean Orbital Days |
| :--- | :--- | :--- |
| **Moon** | 19 | 1,280.2 days |
| **ISS** | 14 | 973.7 days |
| **Mars** | 14 | 873.4 days |

---

## 🚀 How to Run locally

### Prerequisites
- Python 3.x (with standard `sqlite3` and `csv` modules)

### Execution Steps
1. **Initialize Database & Ingest Data**:
   ```bash
   python setup_database.py
   ```
2. **Execute Full SQL Portfolio Script**:
   ```bash
   sqlite3 space_missions.db < space_missions_portfolio.sql
   ```
3. **Generate Executive CSV Reports**:
   ```bash
   python export_portfolio_reports.py
   ```

---

## ⚡ Query Engine Optimization Highlights

### Logical Execution Order
$$\text{1. FROM / JOIN} \longrightarrow \text{2. WHERE} \longrightarrow \text{3. GROUP BY} \longrightarrow \text{4. HAVING} \longrightarrow \text{5. SELECT} \longrightarrow \text{6. ORDER BY}$$

- **Alias Trap Prevention**: Column aliases defined in `SELECT` (Step 5) cannot be referenced in `WHERE` (Step 2).
- **Early Row Filtering**: Filtering rows in `WHERE` (Step 2) reduces scan size prior to memory-intensive `GROUP BY` operations.
