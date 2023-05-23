import os
import json
from PIL import Image

yolo_labels_path = "C:/Users/mai_h/Downloads/train/train/train/labels"
yolo_images_path = "C:/Users/mai_h/Downloads/train/train/train/images"
coco_labels_path = "C:/Users/mai_h/Downloads/train/train/coco"

# Create COCO dataset dictionary
coco_dataset = {
    "info": {
        "description": "COCO format dataset",
        "version": "1.0",
        "year": 2021,
        "contributor": "Your Name",
        "date_created": "2021/10/01"
    },
    "licenses": [
        {
            "id": 1,
            "name": "License 1",
            "url": "http://licenseurl.com"
        }
    ],
    "images": [],
    "annotations": [],
    "categories": [
        {
            "id": 1,
            "name": "category1",
            "supercategory": "category"
        }
    ]
}

# Loop through YOLO labels directory
for filename in os.listdir(yolo_labels_path):
    if filename.endswith(".txt"):
        # Parse YOLO label file
        with open(os.path.join(yolo_labels_path, filename), "r") as f:
            for line in f:
                line = line.strip().split("\t")
                class_id = int(float(line[0]))
                x_center = float(line[1])
                y_center = float(line[2])
                width = float(line[3])
                height = float(line[4])

                # Convert YOLO label to COCO label
                image_id = len(coco_dataset["images"])
                bbox = [x_center, y_center, width, height]
                area = width * height
                annotation_id = len(coco_dataset["annotations"])
                coco_dataset["annotations"].append({
                    "id": annotation_id,
                    "image_id": image_id,
                    "category_id": 1,
                    "bbox": bbox,
                    "area": area,
                    "iscrowd": 0
                })

        # Add image to COCO dataset
        image_path = os.path.join(yolo_images_path, os.path.splitext(filename)[0] + ".png")
        image = Image.open(image_path)
        image_width, image_height = image.size
        image_id = len(coco_dataset["images"])
        coco_dataset["images"].append({
            "id": image_id,
            "file_name": os.path.basename(image_path),
            "width": image_width,
            "height": image_height
        })

# Save COCO dataset to file
with open(os.path.join(coco_labels_path, "coco_dataset.json"), "w") as f:
    json.dump(coco_dataset, f)