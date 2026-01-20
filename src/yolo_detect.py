import os
import pandas as pd
from ultralytics import YOLO

# The nano model was selected for efficient local processing
model = YOLO('yolov8n.pt')

def classify_image(detected_objects):
    # Classification logic remains as defined in the requirements
    products = {'bottle', 'cup', 'wine glass', 'vase'}
    has_person = 'person' in detected_objects
    has_product = any(obj in products for obj in detected_objects)

    if has_person and has_product:
        return 'promotional'
    elif has_product and not has_person:
        return 'product_display'
    elif has_person and not has_product:
        return 'lifestyle'
    else:
        return 'other'

def run_yolo_pipeline():
    # Paths were adjusted to navigate from src -> data -> raw -> images
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_raw_dir = os.path.abspath(os.path.join(base_dir, os.pardir, 'data', 'raw'))
    image_root = os.path.join(data_raw_dir, 'images')
    output_csv = os.path.join(data_raw_dir, 'yolo_detections.csv')
    
    results_list = []
    
    if not os.path.exists(image_root):
        print(f"Error: Image root directory not found at {image_root}")
        return

    # os.walk was implemented to scan all channel subfolders automatically
    for root, dirs, files in os.walk(image_root):
        for filename in files:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(root, filename)
                
                # Inference was performed on each image found in subdirectories
                results = model(image_path)
                
                detected_in_image = []
                max_conf = 0.0
                
                for result in results:
                    for box in result.boxes:
                        label = result.names[int(box.cls)]
                        conf = float(box.conf)
                        detected_in_image.append(label)
                        if conf > max_conf:
                            max_conf = conf
                
                category = classify_image(set(detected_in_image))
                
                # The channel name was captured from the folder structure for extra detail
                channel_name = os.path.basename(root)
                msg_id = filename.split('_')[0]
                
                results_list.append({
                    'message_id': msg_id,
                    'channel': channel_name,
                    'image_name': filename,
                    'detected_objects': ", ".join(detected_in_image),
                    'confidence_score': round(max_conf, 4),
                    'image_category': category
                })

    # The final data was saved to the raw data directory
    df = pd.DataFrame(results_list)
    df.to_csv(output_csv, index=False)
    print(f"Processing finished. Results saved to: {output_csv}")

if __name__ == "__main__":
    run_yolo_pipeline()