from ultralytics import YOLO
import csv

# Load model
model = YOLO("yolov8n.pt")

# Open CSV file
file = open("tracking_data.csv", "w", newline="")

writer = csv.writer(file)

# CSV headings
writer.writerow([
    "Frame",
    "Object_ID",
    "Object",
    "X",
    "Y"
])

# Run tracking
results = model.track(
    source="football.mp4",
    stream=True,
    persist=True,
    conf=0.25
)

# Process video
for frame_number, result in enumerate(results):

    if result.boxes.id is not None:

        boxes = result.boxes
        ids = boxes.id

        for box, track_id in zip(boxes, ids):

            object_id = int(track_id)

            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            # Bounding box coordinates
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            # Center point
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            # Save data
            writer.writerow([
                frame_number + 1,
                object_id,
                class_name,
                center_x,
                center_y
            ])

file.close()

print("Tracking data saved successfully!")