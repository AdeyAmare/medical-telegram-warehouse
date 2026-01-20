# Dagster Pipeline

This folder contains the **Dagster pipeline definition** for orchestrating the Medical Telegram Warehouse ETL workflow. It defines the steps to **scrape Telegram data, load it into PostgreSQL, enrich images with YOLOv8, and run dbt transformations**.

---

## Pipeline Overview

The pipeline consists of the following sequential steps:

1. **Scrape Telegram Data**

   * Fetches messages and images from configured public Telegram channels.
   * Uses `scripts/scraper.py`.

2. **Load Raw Data to PostgreSQL**

   * Ingests the scraped JSON/CSV data into the `raw` schema of the PostgreSQL database.
   * Uses `scripts/load_raw_data.py`.

3. **YOLO Image Enrichment**

   * Runs YOLOv8 object detection on downloaded images.
   * Loads detected objects into PostgreSQL.
   * Uses `src/yolo_detect.py` and `scripts/load_yolo_postgres.py`.

4. **DBT Transformations**

   * Executes dbt models to clean and transform raw data into analytics-ready tables/marts.
   * Uses the dbt project in `medical_warehouse/`.

**Dependencies:** Each step waits for its prerequisite to finish (e.g., ingestion waits for scraping).

---

## Files

* `pipeline.py` – Main Dagster job and operations definitions.
* `scripts/` – Contains supporting scripts for scraping, loading, and YOLO enrichment.
* `src/` – Contains YOLO detection scripts and other internal modules.

---

## Usage

1. **Start the Dagster UI locally:**

```bash
dagster dev -f pipeline.py
```

2. **Access the Dagster UI:**

   * Open your browser at [http://localhost:3000](http://localhost:3000)
   * You can run the pipeline manually or schedule it from the UI.

---

## Scheduling

* The pipeline includes a **daily schedule** (midnight) defined in the Dagster job.
* Use the UI or Dagster CLI to enable/disable schedules.

---

## Notes

* Ensure all dependencies (Python packages, dbt, PostgreSQL access, YOLO models) are installed and configured before execution.
* Scripts assume execution from the **project root** so that relative paths resolve correctly.
