# `src/` Folder

This folder contains the core source code for the **Telegram Medical Data Warehouse** project.

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
