# `medical_warehouse/` — DBT Project for Telegram Medical Data Warehouse

This folder contains the **dbt project** responsible for transforming raw Telegram channel data into structured, analytics-ready tables for Ethiopian medical and pharmaceutical channels.

---

## Project Overview

**Purpose:**

* Transform raw Telegram messages stored in PostgreSQL (`raw.telegram_messages`) into **dimension and fact tables**.
* Enable reporting and analytics on channels, messages, engagement, and time-based trends.
* Ensure data quality through dbt tests.

**Data Sources:**

* PostgreSQL schema: `raw`
* Table: `telegram_messages`
* Contains raw messages scraped from public Telegram channels, including metadata, views, forwards, and media.

---

## Folder Structure

```
medical_warehouse/
├── models/
│   ├── staging/
│   │   ├── sources.yml         # Defines source table(s) for raw data
│   │   └── stg_telegram_messages.sql
│   └── marts/
│       ├── dim_channels.sql
│       ├── dim_dates.sql
│       ├── fct_messages.sql
│       └── schema.yml          # Metadata & tests for marts
├── tests/
│   ├── assert_no_future_messages.sql
│   └── assert_positive_views.sql
└── dbt_project.yml
```

---

## Models

### Staging Layer (`staging/`)

* **`stg_telegram_messages.sql`**

  * Cleans and standardizes raw Telegram messages.
  * Converts column names to **snake_case** and casts data types.
  * Filters out invalid messages (e.g., missing `message_id` or `message_text`).
  * Adds calculated fields like `message_length` and `has_image`.

### Marts Layer (`marts/`)

* **`dim_channels.sql`** — Dimension table for Telegram channels.

  * Computes a `channel_key` (MD5 hash) and classifies channels by type.
  * Includes total posts, first/last post dates, and average views.

* **`dim_dates.sql`** — Date dimension for time-based analysis.

  * Generates a complete date series between min and max message dates.
  * Includes attributes like day of week, month, quarter, and weekend flag.

* **`fct_messages.sql`** — Fact table for Telegram messages.

  * Links each message to `dim_channels` and `dim_dates`.
  * Stores engagement metrics (`view_count`, `forward_count`) and media flags.

---

## Tests

* **Source & Marts Tests (`schema.yml`)**

  * Ensures primary keys (`channel_key`, `date_key`, `message_id`) are unique and not null.
  * Validates foreign key relationships between fact and dimension tables.

* **Custom SQL Tests (`tests/`)**

  * `assert_no_future_messages.sql` — Checks no messages have dates in the future.
  * `assert_positive_views.sql` — Ensures `view_count` values are positive.

---

## dbt Commands

Run dbt models:

```bash
dbt run
```

Run dbt tests:

```bash
dbt test
```

Compile and check DAG:

```bash
dbt compile
dbt debug
```

---

## Running dbt End-to-End

1. Ensure PostgreSQL is running and accessible.
2. Copy `profiles.yml` to `~/.dbt/profiles.yml` and set environment variables:
   - DB_HOST
   - DB_USER
   - DB_PASSWORD
   - DB_NAME
   - DB_SCHEMA (optional)
3. Activate your Python environment with dbt installed.
4. Run dbt commands:

# Install dependencies (if any)
dbt deps

# Run staging models
dbt run -m stg_*

# Run marts (fact and dimension tables)
dbt run -m marts

# Test all models
dbt test

# Generate documentation
dbt docs generate
dbt docs serve


## Notes

* The project is **incremental-friendly**; new Telegram messages can be added daily.
* All transformations follow **cleaning, casting, and enrichment best practices**.
* Dimensions (`dim_channels`, `dim_dates`) are reusable for multiple facts or analytics queries.

