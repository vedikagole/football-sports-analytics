import pandas as pd
import math
import matplotlib.pyplot as plt

# Load tracking data
df = pd.read_csv("tracking_data.csv")

# Select ball
ball = df[df["Object"] == "sports ball"]

# Main ball ID
main_ball_id = 197

ball = ball[ball["Object_ID"] == main_ball_id]

ball = ball.sort_values("Frame")

speeds = []

previous_x = None
previous_y = None
previous_frame = None

for _, row in ball.iterrows():

    current_x = row["X"]
    current_y = row["Y"]
    current_frame = row["Frame"]

    if previous_x is not None:

        dx = current_x - previous_x
        dy = current_y - previous_y

        distance = math.sqrt(dx**2 + dy**2)

        frame_difference = current_frame - previous_frame

        if frame_difference > 0:

            speed = distance / frame_difference

            speeds.append(speed)

    previous_x = current_x
    previous_y = current_y
    previous_frame = current_frame


print("\nBALL SPEED ANALYSIS")
print("-------------------")

if speeds:

    average_speed = sum(speeds) / len(speeds)
    maximum_speed = max(speeds)

    print("Main Ball ID:", main_ball_id)
    print(
        "Average Speed:",
        round(average_speed, 2),
        "pixels/frame"
    )

    print(
        "Maximum Speed:",
        round(maximum_speed, 2),
        "pixels/frame"
    )

    # Speed graph
    plt.figure(figsize=(10, 5))

    plt.plot(speeds)

    plt.title("Football Ball Speed")
    plt.xlabel("Movement Sample")
    plt.ylabel("Speed (pixels/frame)")

    plt.tight_layout()
    plt.show()

else:

    print("No sufficient ball tracking data found.")