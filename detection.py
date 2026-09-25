from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

print("YOLO Model Loaded Successfully!")

# Run YOLO on football video
results = model(
    source="football.mp4",
    stream=True,
   # conf=0.20
)

# Process first 10 frames
for frame_number, result in enumerate(results):

    print("\nFrame:", frame_number + 1)

    # Check detected objects
    for box in result.boxes:

        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        confidence = float(box.conf[0])

        print(
            "Object:", class_name,
            "| Confidence:", round(confidence * 100, 2), "%"
        )

    if frame_number >= 9:
        break