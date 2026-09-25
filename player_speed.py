import pandas as pd
import math
import matplotlib.pyplot as plt

# Load tracking data
df = pd.read_csv("tracking_data.csv")

# Select only players
players = df[df["Object"] == "person"]

player_speed = {}

# Process every player
for player_id, data in players.groupby("Object_ID"):

    data = data.sort_values("Frame")

    speeds = []

    previous_x = None
    previous_y = None
    previous_frame = None

    for _, row in data.iterrows():

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

    # Average speed of player
    if speeds:
        player_speed[player_id] = sum(speeds) / len(speeds)


# Sort by speed
sorted_speed = sorted(
    player_speed.items(),
    key=lambda x: x[1],
    reverse=True
)

print("\nPLAYER SPEED ANALYSIS")
print("---------------------")

for player_id, speed in sorted_speed[:10]:

    print(
        "Player ID:",
        player_id,
        "| Average Speed:",
        round(speed, 2),
        "pixels/frame"
    )


# Most fast player
if sorted_speed:

    fastest_player = sorted_speed[0]

    print("\nFastest Tracked Player:")
    print("Player ID:", fastest_player[0])
    print(
        "Average Speed:",
        round(fastest_player[1], 2),
        "pixels/frame"
    )


# Top 10 speed chart
top_10 = sorted_speed[:10]

player_ids = [str(x[0]) for x in top_10]
speeds = [x[1] for x in top_10]

plt.figure(figsize=(10, 6))

plt.bar(player_ids, speeds)

plt.title("Top 10 Players by Average Speed")
plt.xlabel("Player ID")
plt.ylabel("Average Speed (pixels/frame)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()