# Ethiopian Medical Telegram Data Warehouse

This project extracts, stores, and transforms public Telegram messages from Ethiopian medical and pharmaceutical channels into an **analytics-ready data warehouse**.

It combines **Python scripts** for scraping and loading data, a **data lake structure**, and **dbt models** for transformation and analytics.

---

## Project Overview

**Objectives:**

1. Scrape messages from public Telegram channels (including images).
2. Persist raw messages and images in a structured **data lake**.
3. Load raw messages into a PostgreSQL database.
4. Transform raw data into **dimension and fact tables** for reporting.
5. Ensure **data quality** with dbt tests.

**Key Components:**

| Layer          | Description                                                                                                     |
| -------------- | --------------------------------------------------------------------------------------------------------------- |
| **Scripts**    | Scraper (`scraper.py`) and loader (`load_raw_data.py`)                                                          |
| **Data Lake**  | `src/datalake.py`: organizes raw JSON, images, and manifests                                                    |
| **Database**   | PostgreSQL schema `raw` with table `telegram_messages`                                                          |
| **DBT Models** | Staging: cleans and casts raw data<br>Marts: dimensions (`dim_channels`, `dim_dates`) and fact (`fct_messages`) |
| **Tests**      | DBT schema tests (uniqueness, relationships), custom SQL tests (e.g., no future messages, positive views)       |

---

## Scripts

### `scraper.py`

* Scrapes channels asynchronously using the **Telethon API**.
* Saves messages as JSON, images in `data/raw/images/`, and CSV backups.
* Logs scraping progress and handles rate limits.
* Required environment variables in `.env`:

```text
Tg_API_ID=your_api_id
Tg_API_HASH=your_api_hash
```

Usage:

```bash
python scripts/scraper.py --path data --limit 500
```

---

### `load_raw_data.py`

* Loads JSON messages into PostgreSQL.
* Creates schema/table if missing.
* Inserts messages with `execute_values` for efficient bulk insertion.
* Required environment variables in `.env`:

```text
DATABASE_NAME=your_db
DATABASE_USER=your_user
DATABASE_PASSWORD=your_password
DATABASE_HOST=your_host
DATABASE_PORT=your_port
```

Usage:

```bash
python scripts/load_raw_data.py
```

---

## Data Lake (`src/datalake.py`)

* Organizes **raw messages** into date-partitioned directories.
* Maintains **manifests** for auditing and metadata.
* Provides utility functions for directory creation and JSON writing.

**Example structure:**

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

## DBT Warehouse (`medical_warehouse/`)

### Sources

* PostgreSQL schema: `raw`
* Table: `telegram_messages`

### Staging Models

* **`stg_telegram_messages`**: cleans, standardizes, and casts raw messages.
* Adds calculated fields (`message_length`, `has_image`) and filters invalid rows.

### Marts Models

* **`dim_channels`**: stores metadata and categorization for each channel.
* **`dim_dates`**: generates a complete date dimension.
* **`fct_messages`**: fact table linking messages to channels and dates, with engagement metrics.

### Tests

* Primary keys: uniqueness and non-null (`channel_key`, `date_key`, `message_id`)
* Foreign keys: relationships between fact and dimension tables
* Custom tests: no future messages, positive view counts

**Run dbt commands:**

```bash
dbt run
dbt test
dbt compile
dbt debug
```

---

## Project Workflow

1. **Scrape channels** → `scraper.py` → raw JSON/images/CSV
2. **Load raw data** → `load_raw_data.py` → PostgreSQL table `raw.telegram_messages`
3. **Transform & enrich** → dbt staging and marts → analytics-ready tables (`dim_*` and `fct_*`)
4. **Validate data** → dbt tests and custom SQL tests

---

## Notes

* Designed for **incremental updates**; new messages can be appended daily.
* Structured to support **analytics and reporting** across channels, messages, and time.
* Modular architecture allows easy addition of new channels or DBT models.

