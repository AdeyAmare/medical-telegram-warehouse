import json
from pathlib import Path
from src.datalake import (
    write_channel_messages_json,
    write_manifest,
    telegram_messages_partition_dir,
)


def test_write_channel_messages_json(tmp_path):
    """
    Basic test:
    - writes channel messages JSON
    - file exists
    - content matches input
    """
    base_path = tmp_path
    date_str = "2026-01-18"
    channel_name = "testchannel"

    messages = [
        {
            "message_id": 1,
            "channel_name": channel_name,
            "message_text": "Hello world",
            "views": 10,
        }
    ]

    out_path = write_channel_messages_json(
        base_path=str(base_path),
        date_str=date_str,
        channel_name=channel_name,
        messages=messages,
    )

    # File exists
    assert Path(out_path).exists()

    # Content is correct
    with open(out_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data == messages


def test_write_manifest(tmp_path):
    """
    Basic test:
    - writes manifest JSON
    - totals are correct
    """
    base_path = tmp_path
    date_str = "2026-01-18"

    channel_counts = {
        "cheMed123": 10,
        "tikvahpharma": 5,
    }

    out_path = write_manifest(
        base_path=str(base_path),
        date_str=date_str,
        channel_message_counts=channel_counts,
    )

    assert Path(out_path).exists()

    with open(out_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    assert manifest["date"] == date_str
    assert manifest["channels"] == channel_counts
    assert manifest["total_messages"] == 15


def test_partition_directory_created(tmp_path):
    """
    Ensures partition directory is created correctly
    """
    date_str = "2026-01-18"

    partition_dir = telegram_messages_partition_dir(
        base_path=str(tmp_path),
        date_str=date_str,
    )

    assert partition_dir.endswith(date_str)
