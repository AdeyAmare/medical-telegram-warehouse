# `scripts/` Folder

This folder contains **Python scripts** for scraping Telegram channels and loading raw data into the PostgreSQL database.

## Scripts

### 1. `scraper.py`

**Purpose:**
Scrapes public Telegram channels related to Ethiopian medical and pharmaceutical businesses.

**Key Features:**

* Downloads messages and images from multiple channels.
* Stores messages as JSON files, images in a structured directory, and CSV backups.
* Logs the scraping process with timestamps and errors.
* Handles Telegram rate limits (`FloodWaitError`) and supports message/channel delays.

**Output Structure:**

```
data/
└── raw/
    ├── telegram_messages/YYYY-MM-DD/channel.json
    ├── images/{channel_name}/{message_id}.jpg
    └── csv/YYYY-MM-DD/telegram_data.csv
logs/
└── scrape_YYYY-MM-DD.log
```

**Usage:**

```bash
python scripts/scraper.py --path data --limit 500
```

**Required Environment Variables (.env):**

```text
Tg_API_ID=your_api_id
Tg_API_HASH=your_api_hash
```

---

### 2. `load_raw_data.py`

**Purpose:**
Loads the JSON messages produced by the scraper into a PostgreSQL database.

**Key Features:**

* Connects to a PostgreSQL database using credentials from `.env`.
* Creates the schema and table if they don’t exist.
* Reads JSON messages from `data/raw/telegram_messages/YYYY-MM-DD/`.
* Handles missing/invalid messages gracefully.
* Inserts messages into `raw.telegram_messages` table, avoiding duplicates.

**Required Environment Variables (.env):**

```text
DATABASE_NAME=your_db
DATABASE_USER=your_user
DATABASE_PASSWORD=your_password
DATABASE_HOST=your_host
DATABASE_PORT=your_port
```

**Usage:**

```bash
python scripts/load_raw_data.py
```

**Notes:**

* This script assumes the JSON files exist in the directory structure created by `scraper.py`.
* Uses `execute_values` for bulk insertion for better performance.

---

**Summary:**

* `scraper.py` → Collects Telegram messages and saves them in the raw data lake.
* `load_raw_data.py` → Loads raw messages into PostgreSQL for further processing or analysis.
