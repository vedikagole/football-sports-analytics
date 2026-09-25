import pandas as pd
import matplotlib.pyplot as plt

# Load tracking data
df = pd.read_csv("tracking_data.csv")

# Select ball detections
ball = df[df["Object"] == "sports ball"]

# Ball ID with maximum movement
ball_distance = {}

for ball_id, data in ball.groupby("Object_ID"):

    data = data.sort_values("Frame")

    total_distance = 0
    previous_x = None
    previous_y = None

    for _, row in data.iterrows():

        x = row["X"]
        y = row["Y"]

        if previous_x is not None:

            dx = x - previous_x
            dy = y - previous_y

            distance = (dx**2 + dy**2) ** 0.5

            total_distance += distance

        previous_x = x
        previous_y = y

    ball_distance[ball_id] = total_distance


# Find main ball track
main_ball_id = max(ball_distance, key=ball_distance.get)

print("Main Ball ID:", main_ball_id)
print("Distance:", round(ball_distance[main_ball_id], 2), "pixels")


# Get main ball data
main_ball = ball[
    ball["Object_ID"] == main_ball_id
].sort_values("Frame")


# Plot trajectory
plt.figure(figsize=(10, 6))

plt.plot(
    main_ball["X"],
    main_ball["Y"],
    marker="o",
    markersize=2
)

plt.title("Football Ball Trajectory")

plt.xlabel("X Position")
plt.ylabel("Y Position")

# Image coordinates: top is 0
plt.gca().invert_yaxis()

plt.grid()

plt.show()