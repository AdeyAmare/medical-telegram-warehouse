# `src/` Folder

This folder contains the core source code for the **Telegram Medical Data Warehouse** project.

---

## Module: `datalake.py`

`datalake.py` provides utility functions for **storing raw Telegram channel data** and maintaining a simple **data lake structure**.

### Key Functions

1. **`ensure_dir(path: str)`**

   * Creates a directory if it does not already exist.

2. **`telegram_messages_partition_dir(base_path, date_str)`**

   * Returns the path for storing Telegram messages for a given date partition.

3. **`telegram_images_dir(base_path)`**

   * Returns the base path for storing downloaded images.

4. **`channel_messages_json_path(base_path, date_str, channel_name)`**

   * Returns the full path for a channel’s messages JSON file and ensures the directory exists.

5. **`write_channel_messages_json(...)`**

   * Writes a list of messages to a JSON file for a given channel and date.
   * Returns the path to the created file.

6. **`manifest_path(base_path, date_str)`**

   * Returns the path for the manifest JSON file for a given date.

7. **`write_manifest(...)`**

   * Writes a metadata manifest for the day’s scrape, including channel message counts and total messages.
   * Optionally includes extra metadata.

### Usage

These functions are used by the Telegram scraper to:

* Persist raw messages in a structured, date-partitioned format.
* Maintain metadata about each day’s scraping run.
* Organize images and JSON files consistently in the data lake.

---

## Module: `yolo_detect.py`

`yolo_detect.py` provides a pipeline for **AI-based image detection and classification** using the YOLOv8 model.

### Key Functions

1. **YOLO Model Initialization**

   * Loads the `yolov8n.pt` model for efficient object detection on local machines.

2. **`classify_image(detected_objects)`**

   * Categorizes images based on the objects detected:

     * `promotional` — person and product present.
     * `product_display` — only product detected.
     * `lifestyle` — only person detected.
     * `other` — no relevant objects detected.

3. **`run_yolo_pipeline()`**

   * Scans all images in the data lake (`data/raw/images/`) across channel subfolders.
   * Performs YOLO inference for each image.
   * Extracts detected objects, maximum confidence, and assigns an image category.
   * Captures channel name and message ID from folder/file structure.
   * Saves results to a CSV (`yolo_detections.csv`) in the raw data directory.

### Usage

* This module is used after images are downloaded by the scraper to:

  * Detect objects in Telegram images (products, people, etc.).
  * Classify images into categories for enrichment (`fct_image_detections` in dbt).
  * Generate a CSV of all detections, which can be loaded into PostgreSQL for analytics.

### Run the Pipeline

From the `src/` folder (or project root), run:

```bash
python -m yolo_detect
```

This will:

* Process all images in `data/raw/images/`.
* Perform object detection using YOLOv8.
* Save the results to `data/raw/yolo_detections.csv`.

---
