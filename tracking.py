from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolov8n.pt")

print("YOLO Tracking Started!")

# Run tracking on video
results = model.track(
    source="football.mp4",
    stream=True,
    persist=True,
    show=True,
    conf=0.50
)

# Process video frames
for frame_number, result in enumerate(results):

    print("\nFrame:", frame_number + 1)

    # Check whether tracking IDs are available
    if result.boxes.id is not None:

        track_ids = result.boxes.id.int().cpu().tolist()

        for track_id in track_ids:
            print("Tracked Object ID:", track_id)