# `tests/` Folder

This folder contains **unit tests** for the `src.datalake` module of the Telegram data pipeline.

## Tests Included

1. **`test_write_channel_messages_json`**

   * Verifies that `write_channel_messages_json()` correctly writes messages to a JSON file.
   * Checks that the file exists and the contents match the input messages.

2. **`test_write_manifest`**

   * Verifies that `write_manifest()` correctly writes a manifest JSON file.
   * Checks that totals are computed correctly and the file exists.

3. **`test_partition_directory_created`**

   * Ensures that `telegram_messages_partition_dir()` correctly returns the expected directory path.

## Running the Tests

From the project root, run:

```bash
pytest -v tests/
```

* `-v` shows detailed output.
* All tests are **self-contained** and use `tmp_path` to avoid writing to real data directories.

## Notes

* These are **unit tests** only; they do **not** connect to the database or scrape Telegram channels.
* They focus on **file creation, JSON output, and directory paths**.
