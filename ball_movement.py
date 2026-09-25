import pandas as pd
import math

# Load tracking data
df = pd.read_csv("tracking_data.csv")

# Select only sports ball
ball = df[df["Object"] == "sports ball"]

# Store distance for each ball ID
ball_distance = {}

# Process each ball tracking ID
for ball_id, data in ball.groupby("Object_ID"):

    # Sort frames
    data = data.sort_values("Frame")

    total_distance = 0

    previous_x = None
    previous_y = None

    # Check ball position frame by frame
    for _, row in data.iterrows():

        current_x = row["X"]
        current_y = row["Y"]

        # Calculate movement
        if previous_x is not None:

            dx = current_x - previous_x
            dy = current_y - previous_y

            distance = math.sqrt(dx**2 + dy**2)

            total_distance += distance

        previous_x = current_x
        previous_y = current_y

    ball_distance[ball_id] = total_distance


# Display results
print("\nBALL MOVEMENT ANALYSIS")
print("----------------------")

for ball_id, distance in ball_distance.items():

    print(
        "Ball ID:",
        ball_id,
        "| Distance:",
        round(distance, 2),
        "pixels"
    )


# Find most active ball track
if ball_distance:

    most_active_ball = max(
        ball_distance,
        key=ball_distance.get
    )

    print("\nMain Ball Track:")
    print("Ball ID:", most_active_ball)
    print(
        "Distance:",
        round(ball_distance[most_active_ball], 2),
        "pixels"
    )