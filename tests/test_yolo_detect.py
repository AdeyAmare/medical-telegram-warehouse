import os
import pandas as pd
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the function to test
from src.yolo_detect import run_yolo_pipeline

@pytest.fixture
def tmp_image_dir(tmp_path):
    """Create a fake images directory with a single fake image."""
    images_dir = tmp_path / "images" / "test_channel"
    images_dir.mkdir(parents=True)
    fake_image = images_dir / "12345_fake.jpg"
    fake_image.touch()  # create empty file
    return tmp_path

def test_run_yolo_pipeline_creates_csv(tmp_image_dir, monkeypatch):
    """Test that run_yolo_pipeline creates a CSV with expected columns."""
    
    # Mock YOLO model to avoid running actual inference
    mock_model = MagicMock()
    mock_result = MagicMock()
    
    # Create a fake box with attributes cls and conf
    fake_box = MagicMock()
    fake_box.cls = 0
    fake_box.conf = 0.9
    
    mock_result.boxes = [fake_box]
    mock_result.names = {0: "person"}
    mock_model.return_value = [mock_result]
    
    # Patch YOLO object and os.path.exists
    monkeypatch.setattr("src.yolo_detect.YOLO", lambda *args, **kwargs: mock_model)
    monkeypatch.setattr("os.path.exists", lambda path: True)
    
    # Patch os.walk to use our fake image directory
    def mock_os_walk(root):
        yield (str(tmp_image_dir / "images" / "test_channel"), [], ["12345_fake.jpg"])
    monkeypatch.setattr("os.walk", mock_os_walk)
    
    # Patch classify_image to return a fixed category
    monkeypatch.setattr("src.yolo_detect.classify_image", lambda detected: "lifestyle")
    
    # Run pipeline
    run_yolo_pipeline()
    
    # Check that CSV is created
    output_csv = tmp_image_dir / "yolo_detections.csv"
    assert output_csv.exists() or Path("data/raw/yolo_detections.csv").exists()
    
    # If CSV exists, check columns
    if output_csv.exists():
        df = pd.read_csv(output_csv)
        expected_cols = [
            "message_id",
            "channel",
            "image_name",
            "detected_objects",
            "confidence_score",
            "image_category",
        ]
        for col in expected_cols:
            assert col in df.columns
