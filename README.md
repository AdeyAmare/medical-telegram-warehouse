# Ethiopian Medical Telegram Data Warehouse

This repository contains a **full pipeline** for extracting, storing, transforming, and analyzing public Telegram messages from **Ethiopian medical and pharmaceutical channels**. It combines **Python scripts**, a **data lake**, **PostgreSQL**, **dbt models**, **FastAPI**, and **Dagster orchestration** for a complete analytics workflow.

---

## Table of Contents

* [Project Overview](#project-overview)
* [Key Components](#key-components)
* [Data Lake](#data-lake)
* [Scripts](#scripts)
* [YOLO Image Detection](#yolo-image-detection)
* [DBT Warehouse](#dbt-warehouse)
* [FastAPI Service](#fastapi-service)
* [Dagster Pipeline](#dagster-pipeline)
* [Project Workflow](#project-workflow)
* [Running the Pipeline](#running-the-pipeline)
* [Environment Variables](#environment-variables)
* [Notes](#notes)

---

## Project Overview

**Objectives:**

1. Scrape messages and images from public Telegram channels.
2. Persist raw messages and images in a structured **data lake**.
3. Load raw messages and image detections into PostgreSQL.
4. Transform raw data into **dimension and fact tables** using dbt.
5. Provide an **API** for querying insights.
6. Automate the full ETL and enrichment workflow using **Dagster**.

---

## Key Components

| Layer              | Description                                                                                                      |
| ------------------ | ---------------------------------------------------------------------------------------------------------------- |
| **Scripts**        | Scraper (`scraper.py`), raw loader (`load_raw_data.py`), YOLO loader (`load_yolo_postgres.py`)                   |
| **Data Lake**      | `src/datalake.py`: manages JSON messages, images, CSVs, and manifests                                            |
| **YOLO Detection** | `src/yolo_detect.py`: object detection and classification for images                                             |
| **Database**       | PostgreSQL schema `raw` with tables `telegram_messages` and `yolo_detections`                                    |
| **DBT Models**     | Staging: cleans and casts raw data<br>Marts: `dim_channels`, `dim_dates`, `fct_messages`, `fct_image_detections` |
| **API**            | FastAPI (`api/main.py` + `schemas.py`) for analytics and search endpoints                                        |
| **Dagster**        | Orchestration (`pipeline.py`), schedules daily execution of scraping, ingestion, YOLO enrichment, and dbt runs   |

---

## Data Lake (`src/datalake.py`)

* Organizes **raw messages** and images into **date-partitioned directories**.
* Maintains **manifests** for metadata and auditing.
* Utility functions:

```
data/
└── raw/
    ├── telegram_messages/YYYY-MM-DD/channel.json
    ├── images/{channel_name}/{message_id}.jpg
    └── csv/YYYY-MM-DD/telegram_data.csv
logs/
└── scrape_YYYY-MM-DD.log
```

---

## Scripts

### 1. `scraper.py`

* Scrapes channels asynchronously using **Telethon API**.
* Downloads messages, images, and CSV backups.
* Handles rate limits and logs progress.

```bash
python scripts/scraper.py --path data --limit 500
```

**Required `.env` variables:**

```
Tg_API_ID=your_api_id
Tg_API_HASH=your_api_hash
```

---

### 2. `load_raw_data.py`

* Loads JSON messages into PostgreSQL `raw.telegram_messages`.
* Creates schema/table if missing.
* Bulk inserts messages efficiently with `execute_values`.

```bash
python scripts/load_raw_data.py
```

**Required `.env` variables:**

```
DATABASE_NAME=your_db
DATABASE_USER=your_user
DATABASE_PASSWORD=your_password
DATABASE_HOST=your_host
DATABASE_PORT=your_port
```

---

### 3. `load_yolo_postgres.py`

* Loads YOLO detection CSV into PostgreSQL `raw.yolo_detections`.
* Cleans `message_id`, fills missing `confidence_score`, and replaces empty `detected_objects`.
* Creates schema/table if missing.

```bash
python scripts/load_yolo_postgres.py
```

---

## YOLO Image Detection (`src/yolo_detect.py`)

* Uses **YOLOv8 nano model** for local image inference.

* Detects objects (person, bottle, cup, wine glass, vase) in Telegram images.

* Categorizes images:

  * `promotional` → person + product
  * `product_display` → product only
  * `lifestyle` → person only
  * `other` → no relevant objects

* Saves results to `data/raw/yolo_detections.csv`.

```bash
python -m yolo_detect
```

---

## DBT Warehouse (`medical_warehouse/`)

### Sources

* PostgreSQL schema: `raw`
* Table: `telegram_messages`

### Staging Models

* `stg_telegram_messages` — cleans, standardizes, and casts raw messages.
* Adds `message_length`, `has_image`, and filters invalid rows.

### Marts Models

* `dim_channels` — metadata and categorization for channels.
* `dim_dates` — full date dimension for time-based analytics.
* `fct_messages` — fact table linking messages to channels/dates with engagement metrics.
* `fct_image_detections` — fact table for YOLO image detections (category, confidence, count).

### Tests

* Uniqueness & non-null primary keys (`channel_key`, `date_key`, `message_id`).
* Foreign keys linking fact/dimension tables.
* Custom SQL tests (no future messages, positive view counts).

**Run dbt commands:**

```bash
dbt run
dbt test
dbt compile
dbt debug
```

---

## FastAPI Service (`api/`)

* Provides REST endpoints for analytics and search:

| Endpoint                                | Description                                |
| --------------------------------------- | ------------------------------------------ |
| `/api/reports/top-products`             | Returns top mentioned products             |
| `/api/channels/{channel_name}/activity` | Returns daily message counts for a channel |
| `/api/search/messages`                  | Keyword search in messages                 |
| `/api/reports/visual-content`           | Returns YOLO image category stats          |

**Run locally:**

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Access interactive docs at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## Dagster Pipeline (`pipeline.py`)

* Orchestrates full ETL workflow:

1. Scrape Telegram messages/images.
2. Load raw messages into PostgreSQL.
3. Run YOLO detection & load into PostgreSQL.
4. Execute dbt transformations.

**Run locally with Dagster:**

```bash
dagster dev -f pipeline.py
```

* Scheduled to run daily at midnight via Cron.

---

## Project Workflow

1. **Scrape messages/images** → `scraper.py`
2. **Load raw messages** → `load_raw_data.py`
3. **Detect images with YOLO** → `yolo_detect.py`
4. **Load YOLO results** → `load_yolo_postgres.py`
5. **Transform raw data** → dbt staging & marts (`dim_*`, `fct_*`)
6. **Expose API** → FastAPI endpoints
7. **Orchestration & scheduling** → Dagster

---

## Running the Pipeline End-to-End

1. Ensure PostgreSQL is running and accessible.
2. Set environment variables in `.env`:

```
# Telegram API
Tg_API_ID=
Tg_API_HASH=

# PostgreSQL
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
DATABASE_PORT=
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run scripts, YOLO, and loaders:

```bash
python scripts/scraper.py --path data --limit 500
python scripts/load_raw_data.py
python -m yolo_detect
python scripts/load_yolo_postgres.py
```

5. Run dbt transformations and tests:

```bash
dbt run -m stg_*
dbt run -m marts
dbt test
dbt docs generate
dbt docs serve
```

6. Optionally, run Dagster for full orchestration:

```bash
dagster dev -f pipeline.py
```

7. Start FastAPI to expose endpoints:

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Notes

* Designed for **incremental updates**; new messages/images can be appended daily.
* Fully modular and **extensible** — new channels, DBT models, or API endpoints can be added.
* Provides **end-to-end analytics**: raw data → cleaned/structured warehouse → YOLO enrichment → API access.
* Supports **automation and scheduling** via Dagster.

## Diagram Representation

**Flow:**

```
Telegram Channels
      │
      ▼
┌──────────────────┐
│  scraper.py      │
│  - Fetch messages│
│  - Download images│
└──────────────────┘
      │
      ▼
┌──────────────────┐
│  Data Lake       │
│  - JSON messages │
│  - Images        │
│  - CSV backups   │
└──────────────────┘
      │
      ▼
┌──────────────────┐
│ load_raw_data.py │
│  - Insert raw    │
│    messages into │
│    PostgreSQL    │
└──────────────────┘
      │
      ▼
┌──────────────────┐
│ yolo_detect.py   │
│  - Detect objects│
│  - Classify images│
│  - Output CSV    │
└──────────────────┘
      │
      ▼
┌─────────────────────────┐
│ load_yolo_postgres.py   │
│  - Load CSV into        │
│    raw.yolo_detections  │
└─────────────────────────┘
      │
      ▼
┌──────────────────┐
│  DBT Warehouse   │
│  - Staging       │
│  - Marts         │
│    (dim_channels,│
│     dim_dates,   │
│     fct_messages,│
│     fct_image_detections) │
└──────────────────┘
      │
      ▼
┌──────────────────┐
│  PostgreSQL      │
│  Analytics-ready │
│  tables          │
└──────────────────┘
      │
      ▼
┌─────────────┐       ┌───────────────┐
│ FastAPI API │       │  Dagster Job │
│  - Query    │       │  - Schedule  │
│    endpoints│       │    scraping, │
│    (top-    │       │    ingestion,│
│     products│       │    YOLO,     │
│     channel │       │    dbt run)  │
│     activity│       └───────────────┘
└─────────────┘
```

---

✅ **Legend / Notes:**

* Each block is a **module/script/service**.
* Arrows show **data flow** from scraping → storage → enrichment → warehouse → API/Orchestration.
* Dagster orchestrates the entire workflow **automatically**.
