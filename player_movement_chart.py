import pandas as pd
import math
import matplotlib.pyplot as plt

# Load tracking data
df = pd.read_csv("tracking_data.csv")

# Select players
players = df[df["Object"] == "person"]

player_distance = {}

# Calculate distance for every player
for player_id, data in players.groupby("Object_ID"):

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

            distance = math.sqrt(dx**2 + dy**2)

            total_distance += distance

        previous_x = x
        previous_y = y

    player_distance[player_id] = total_distance


# Sort players by distance
sorted_players = sorted(
    player_distance.items(),
    key=lambda x: x[1],
    reverse=True
)

# Take top 10 players
top_players = sorted_players[:10]

player_ids = [str(x[0]) for x in top_players]
distances = [x[1] for x in top_players]


# Create bar chart
plt.figure(figsize=(10, 6))

plt.bar(player_ids, distances)

plt.title("Top 10 Players by Movement")

plt.xlabel("Player ID")
plt.ylabel("Distance (pixels)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()